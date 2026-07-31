# scripts/export_canonical.py
import os
import sqlite3
import psycopg
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import json
import gzip
import shutil
import time
import sys
import subprocess

DB_CONN_STR = "host=127.0.0.1 dbname=comparative_legislative_data_canonical user=chessadmin password=chessadmin"
OUTPUT_DIR = "/home/chessadmin/comparativelegislativedata/downloads/gb-sct"

ENDPOINTS = {
    "canonical_bills": {
        "table": "canonical_gb_sct_bills",
        "fields": {
            "bill_id": ("BillID", "INTEGER PRIMARY KEY"),
            "short_name": ("ShortName", "TEXT"),
            "session_id": ("SessionID", "INTEGER"),
            "sponsor_type": ("SponsorType", "TEXT"),
            "sponsor_name": ("SponsorName", "TEXT"),
            "sponsor_gender_id": ("SponsorGenderID", "INTEGER"),
            "sponsor_party_id": ("SponsorPartyID", "INTEGER"),
            "sponsor_is_first_time": ("SponsorIsFirstTime", "INTEGER"),
            "sessional_bill_load": ("SessionalBillLoad", "INTEGER"),
            "passed_stage_3": ("PassedStage3", "INTEGER"),
            "went_to_reconsideration": ("WentToReconsideration", "INTEGER"),
            "bill_outcome": ("BillOutcome", "TEXT"),
            "t1_duration_calendar": ("T1DurationCalendar", "INTEGER"),
            "t2_duration_calendar": ("T2DurationCalendar", "INTEGER"),
            "t3_duration_calendar": ("T3DurationCalendar", "INTEGER"),
            "viscosity_outlier": ("ViscosityOutlier", "INTEGER")
        }
    },
    "canonical_memberpartyhistory": {
        "table": "canonical_gb_sct_member_party_history",
        "fields": {
            "snapshot_date": ("SnapshotDate", "TEXT"),
            "party_id": ("PartyID", "INTEGER"),
            "party_name": ("PartyName", "TEXT"),
            "member_count": ("MemberCount", "INTEGER")
        }
    }
}

def export_parquet():
    print("\n------------------------------------------------------------------")
    print("      EXPORTING CANONICAL TABLES TO PARQUET")
    print("------------------------------------------------------------------")
    sys.stdout.flush()
    
    pg_conn = psycopg.connect(DB_CONN_STR)
    
    for name, ep in ENDPOINTS.items():
        t0 = time.time()
        table = ep["table"]
        out_file = os.path.join(OUTPUT_DIR, f"{name}.parquet")
        
        print(f"[*] Exporting {table} -> {out_file}...", end="", flush=True)
        
        # Build SQL SELECT statement mapping keys to CamelCase
        select_cols = []
        for low_key, (camel_key, _) in ep["fields"].items():
            select_cols.append(f'{low_key} as "{camel_key}"')
        
        query = f"SELECT {', '.join(select_cols)} FROM {table}"
        
        # Build Arrow schema
        schema_fields = []
        for low_key, (camel_key, sql_type) in ep["fields"].items():
            if "INTEGER" in sql_type:
                schema_fields.append((camel_key, pa.int64()))
            else:
                schema_fields.append((camel_key, pa.string()))
        pa_schema = pa.schema(schema_fields)
        
        df = pd.read_sql_query(query, pg_conn)
        
        # Format columns
        for low_key, (camel_key, sql_type) in ep["fields"].items():
            if len(df) > 0:
                if "INTEGER" in sql_type:
                    df[camel_key] = pd.to_numeric(df[camel_key], errors='coerce').astype('Int64')
                else:
                    df[camel_key] = df[camel_key].astype(str).where(df[camel_key].notnull(), None)
        
        table_pa = pa.Table.from_pandas(df, schema=pa_schema, preserve_index=False)
        pq.write_table(table_pa, out_file, compression="snappy")
        
        size_mb = os.path.getsize(out_file) / (1024 * 1024)
        print(f" Done. {len(df)} rows, {size_mb:.3f} MB in {time.time() - t0:.2f}s", flush=True)
        
    pg_conn.close()

def export_sqlite():
    print("\n------------------------------------------------------------------")
    print("      EXPORTING CANONICAL TO PORTABLE SQLITE DATABASE")
    print("------------------------------------------------------------------")
    sys.stdout.flush()
    
    sqlite_file = os.path.join(OUTPUT_DIR, "gb_sct_canonical.sqlite")
    if os.path.exists(sqlite_file):
        os.remove(sqlite_file)
        
    sqlite_conn = sqlite3.connect(sqlite_file)
    sqlite_conn.execute("PRAGMA journal_mode=WAL;")
    sqlite_conn.execute("PRAGMA synchronous=normal;")
    
    pg_conn = psycopg.connect(DB_CONN_STR)
    
    for name, ep in ENDPOINTS.items():
        t0 = time.time()
        table = ep["table"]
        
        # Create Table in SQLite
        fields_def = []
        insert_cols = []
        select_cols = []
        for low_key, (camel_key, sql_type) in ep["fields"].items():
            fields_def.append(f'"{camel_key}" {sql_type}')
            insert_cols.append(f'"{camel_key}"')
            select_cols.append(f'{low_key} as "{camel_key}"')
            
        create_sql = f"CREATE TABLE {name} ({', '.join(fields_def)});"
        sqlite_conn.execute(create_sql)
        
        # Insert Data
        select_clause = ", ".join(select_cols)
        query = f"SELECT {select_clause} FROM {table}"
        placeholders = ", ".join(["?" for _ in insert_cols])
        insert_sql = f"INSERT INTO {name} ({', '.join(insert_cols)}) VALUES ({placeholders})"
        
        print(f"[*] Exporting {table} -> SQLite '{name}'...", end="", flush=True)
        
        with pg_conn.cursor() as pg_cursor:
            pg_cursor.execute(query)
            rows = pg_cursor.fetchall()
            
            formatted_rows = []
            for row in rows:
                formatted_row = []
                for val in row:
                    if hasattr(val, 'isoformat'):
                        formatted_row.append(val.isoformat())
                    elif isinstance(val, bool):
                        formatted_row.append(1 if val else 0)
                    else:
                        formatted_row.append(val)
                formatted_rows.append(formatted_row)
                
            if formatted_rows:
                sqlite_conn.executemany(insert_sql, formatted_rows)
                sqlite_conn.commit()
                
        print(f" Done. {len(formatted_rows)} rows in {time.time() - t0:.2f}s", flush=True)
        
    pg_conn.close()
    sqlite_conn.close()
    
    # Gzip the SQLite file
    gzip_file = sqlite_file + ".gz"
    if os.path.exists(gzip_file):
        os.remove(gzip_file)
        
    print(f"[*] Gzipping SQLite database to {gzip_file}...", end="", flush=True)
    t0 = time.time()
    with open(sqlite_file, 'rb') as f_in:
        with gzip.open(gzip_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(sqlite_file)
    print(f" Done. {os.path.getsize(gzip_file) / (1024*1024):.3f} MB in {time.time() - t0:.2f}s", flush=True)

def export_csv():
    print("\n------------------------------------------------------------------")
    print("      EXPORTING CANONICAL TO BULK CSV FILES")
    print("------------------------------------------------------------------")
    sys.stdout.flush()
    
    # Check bounds: canonical_bills (473 rows, uncompressed), canonical_memberpartyhistory (2378 rows, compressed)
    # Task 5 enforces the 500-record compression threshold
    UNCOMPRESSED_ENDPOINTS = {"canonical_bills"}
    
    for name, ep in ENDPOINTS.items():
        t0 = time.time()
        table = ep["table"]
        
        is_uncompressed = name in UNCOMPRESSED_ENDPOINTS
        ext = "csv" if is_uncompressed else "csv.gz"
        output_file = os.path.join(OUTPUT_DIR, f"{name}.{ext}")
        
        print(f"[*] Exporting {name:32} (Table: {table}, Format: {ext})")
        
        # Build SQL SELECT statement
        select_cols = []
        for low_key, (camel_key, _) in ep["fields"].items():
            select_cols.append(f'{low_key} as "{camel_key}"')
        sql_query = f"SELECT {', '.join(select_cols)} FROM {table}"
        
        if is_uncompressed:
            cmd = (
                f"PGPASSWORD=chessadmin psql -h 127.0.0.1 -U chessadmin -d comparative_legislative_data_canonical "
                f"-c \"\\copy ({sql_query}) TO stdout WITH CSV HEADER\" > {output_file}"
            )
        else:
            cmd = (
                f"PGPASSWORD=chessadmin psql -h 127.0.0.1 -U chessadmin -d comparative_legislative_data_canonical "
                f"-c \"\\copy ({sql_query}) TO stdout WITH CSV HEADER\" | gzip > {output_file}"
            )
        
        try:
            subprocess.run(cmd, shell=True, check=True)
            size_bytes = os.path.getsize(output_file)
            size_mb = size_bytes / (1024 * 1024)
            print(f"    [+] Saved: {output_file} ({size_mb:.4f} MB) in {time.time() - t0:.2f}s")
        except Exception as e:
            print(f"    [!] Export Failed: {e}")

if __name__ == "__main__":
    export_parquet()
    export_sqlite()
    export_csv()
