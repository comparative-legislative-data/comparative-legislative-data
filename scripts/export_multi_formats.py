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

DB_CONN_STR = "host=127.0.0.1 dbname=comparative_legislative_data user=chessadmin password=chessadmin"
OUTPUT_DIR = "/home/chessadmin/comparativelegislativedata/downloads/gb-sct"

ENDPOINTS = {
    "billtypes": {
        "table": "raw_gb_sct_billtypes",
        "fields": {"id": ("ID", "INTEGER PRIMARY KEY"), "name": ("Name", "TEXT")}
    },
    "billstagetypes": {
        "table": "raw_gb_sct_billstagetypes",
        "fields": {"id": ("ID", "INTEGER PRIMARY KEY"), "name": ("Name", "TEXT"), "billtypeid": ("BillTypeID", "INTEGER"), "sequence": ("Sequence", "INTEGER")}
    },
    "parties": {
        "table": "raw_gb_sct_parties",
        "fields": {
            "id": ("ID", "INTEGER PRIMARY KEY"), "abbreviation": ("Abbreviation", "TEXT"), "actualname": ("ActualName", "TEXT"),
            "preferredname": ("PreferredName", "TEXT"), "notes": ("Notes", "TEXT"),
            "validfromdate": ("ValidFromDate", "TEXT"), "validuntildate": ("ValidUntilDate", "TEXT")
        }
    },
    "committeeroles": {
        "table": "raw_gb_sct_committeeroles",
        "fields": {"id": ("ID", "INTEGER PRIMARY KEY"), "name": ("Name", "TEXT"), "notes": ("Notes", "TEXT")}
    },
    "committeetypes": {
        "table": "raw_gb_sct_committeetypes",
        "fields": {"id": ("ID", "INTEGER PRIMARY KEY"), "name": ("Name", "TEXT")}
    },
    "bills": {
        "table": "raw_gb_sct_bills",
        "fields": {
            "id": ("ID", "INTEGER PRIMARY KEY"), "reference": ("Reference", "TEXT"), "shortname": ("ShortName", "TEXT"),
            "fullname": ("FullName", "TEXT"), "billtypeid": ("BillTypeID", "INTEGER"), "personid": ("PersonID", "INTEGER"),
            "thirdpartyorganisation": ("ThirdPartyOrganisation", "TEXT")
        }
    },
    "billstages": {
        "table": "raw_gb_sct_billstages",
        "fields": {"id": ("ID", "INTEGER PRIMARY KEY"), "billid": ("BillID", "INTEGER"), "billstagetypeid": ("BillStageTypeID", "INTEGER"), "stagedate": ("StageDate", "TEXT")}
    },
    "members": {
        "table": "raw_gb_sct_members",
        "fields": {
            "personid": ("PersonID", "INTEGER PRIMARY KEY"), "photourl": ("PhotoURL", "TEXT"), "notes": ("Notes", "TEXT"), "birthdate": ("BirthDate", "TEXT"),
            "birthdateisprotected": ("BirthDateIsProtected", "INTEGER"), "parliamentaryname": ("ParliamentaryName", "TEXT"),
            "preferredname": ("PreferredName", "TEXT"), "gendertypeid": ("GenderTypeID", "INTEGER"), "iscurrent": ("IsCurrent", "INTEGER")
        }
    },
    "memberparties": {
        "table": "raw_gb_sct_memberparties",
        "fields": {"id": ("ID", "INTEGER PRIMARY KEY"), "personid": ("PersonID", "INTEGER"), "partyid": ("PartyID", "INTEGER"), "validfromdate": ("ValidFromDate", "TEXT"), "validuntildate": ("ValidUntilDate", "TEXT")}
    },
    "committees": {
        "table": "raw_gb_sct_committees",
        "fields": {
            "id": ("ID", "INTEGER PRIMARY KEY"), "shortname": ("ShortName", "TEXT"), "name": ("Name", "TEXT"), "description": ("Description", "TEXT"),
            "committeeemailaddress": ("CommitteeEmailAddress", "TEXT"), "committeetelephone": ("CommitteeTelephone", "TEXT"),
            "validfromdate": ("ValidFromDate", "TEXT"), "validuntildate": ("ValidUntilDate", "TEXT")
        }
    },
    "personcommitteeroles": {
        "table": "raw_gb_sct_personcommitteeroles",
        "fields": {
            "id": ("ID", "INTEGER PRIMARY KEY"), "personid": ("PersonID", "INTEGER"), "committeeroleid": ("CommitteeRoleID", "INTEGER"), "committeeid": ("CommitteeID", "INTEGER"),
            "validfromdate": ("ValidFromDate", "TEXT"), "validuntildate": ("ValidUntilDate", "TEXT"), "notes": ("Notes", "TEXT")
        }
    },
    "motionsquestionsanswersmotions": {
        "table": "raw_gb_sct_motions",
        "fields": {
            "uniqueid": ("UniqueID", "INTEGER PRIMARY KEY"), "eventid": ("EventID", "TEXT"), "eventtypeid": ("EventTypeID", "INTEGER"), "eventsubtypeid": ("EventSubTypeID", "INTEGER"),
            "mspid": ("MSPID", "INTEGER"), "party": ("Party", "TEXT"), "regionid": ("RegionID", "INTEGER"), "constituencyid": ("ConstituencyID", "INTEGER"),
            "approveddate": ("ApprovedDate", "TEXT"), "submissiondatetime": ("SubmissionDateTime", "TEXT"), "title": ("Title", "TEXT"), "itemtext": ("ItemText", "TEXT")
        }
    },
    "votesmotion": {
        "table": "raw_gb_sct_votes",
        "fields": {
            "id": ("ID", "TEXT PRIMARY KEY"), "detail": ("Detail", "TEXT"), "motion": ("Motion", "TEXT"), "person": ("Person", "TEXT"),
            "time": ("Time", "TEXT"), "updatedelasticdate": ("UpdatedElasticDate", "TEXT")
        }
    },
    "orsplenarymeeting": {
        "table": "raw_gb_sct_plenary_reports",
        "fields": {
            "id": ("ID", "TEXT PRIMARY KEY"), "meeting": ("Meeting", "TEXT"), "committee": ("Committee", "TEXT"), "time": ("Time", "TEXT"),
            "itemofbusiness": ("ItemOfBusiness", "TEXT"), "person": ("Person", "TEXT"), "detail": ("Detail", "TEXT"), "updatedelasticdate": ("UpdatedElasticDate", "TEXT")
        }
    },
    "orscommitteemeeting": {
        "table": "raw_gb_sct_committee_reports",
        "fields": {
            "id": ("ID", "TEXT PRIMARY KEY"), "recordtype": ("RecordType", "TEXT"), "subtype": ("SubType", "TEXT"), "meeting": ("Meeting", "TEXT"),
            "committee": ("Committee", "TEXT"), "time": ("Time", "TEXT"), "itemofbusiness": ("ItemOfBusiness", "TEXT"), "person": ("Person", "TEXT"),
            "detail": ("Detail", "TEXT"), "location": ("Location", "TEXT"), "updateddate": ("UpdatedDate", "TEXT"), "updatedelasticdate": ("UpdatedElasticDate", "TEXT")
        }
    }
}

def export_parquet():
    print("\n------------------------------------------------------------------")
    print("      EXPORTING TABLES TO PARQUET (STREAMING MODE)")
    print("------------------------------------------------------------------")
    sys.stdout.flush()
    
    pg_conn = psycopg.connect(DB_CONN_STR)
    
    for name, ep in ENDPOINTS.items():
        t0 = time.time()
        table = ep["table"]
        out_file = os.path.join(OUTPUT_DIR, f"{name}.parquet")
        
        # Build SQL SELECT clause with CamelCase aliases
        select_fields = []
        for low_key, (camel_key, _) in ep["fields"].items():
            select_fields.append(f"{low_key} as \"{camel_key}\"")
        select_clause = ", ".join(select_fields)
        
        query = f"SELECT {select_clause} FROM {table}"
        print(f"[*] Exporting {name} to parquet...", end="", flush=True)
        
        # Build PyArrow schema explicitly to prevent null-type schema drift
        schema_fields = []
        for low_key, (camel_key, sql_type) in ep["fields"].items():
            if "INTEGER" in sql_type:
                schema_fields.append((camel_key, pa.int64()))
            else:
                schema_fields.append((camel_key, pa.string()))
        pa_schema = pa.schema(schema_fields)
        
        writer = None
        total_rows = 0
        
        # Streaming read in 50,000 row chunks to limit RAM usage
        for chunk in pd.read_sql_query(query, pg_conn, chunksize=50000):
            total_rows += len(chunk)
            
            # Format/cast columns in pandas chunk to match SQLite/Parquet target schema types
            for low_key, (camel_key, sql_type) in ep["fields"].items():
                if len(chunk) > 0:
                    val = chunk[camel_key]
                    
                    # If JSONB, stringify dicts/lists
                    first_val = val.iloc[0] if len(chunk) > 0 else None
                    if isinstance(first_val, (dict, list)):
                        chunk[camel_key] = chunk[camel_key].apply(lambda x: json.dumps(x) if x is not None else None)
                    elif hasattr(first_val, 'isoformat'):
                        chunk[camel_key] = chunk[camel_key].apply(lambda x: x.isoformat() if pd.notnull(x) else None)
                        
                    # Enforce strict dtype casting
                    if "INTEGER" in sql_type:
                        chunk[camel_key] = pd.to_numeric(chunk[camel_key], errors='coerce').astype('Int64')
                    else:
                        chunk[camel_key] = chunk[camel_key].astype(str).where(chunk[camel_key].notnull(), None)
            
            # Write chunk to Parquet with pre-defined schema
            table_pa = pa.Table.from_pandas(chunk, schema=pa_schema, preserve_index=False)
            if writer is None:
                writer = pq.ParquetWriter(out_file, pa_schema, compression="snappy")
            writer.write_table(table_pa)
            
        if writer:
            writer.close()
            
        # Create motions alias copy as well
        if name == "motionsquestionsanswersmotions":
            shutil.copyfile(out_file, os.path.join(OUTPUT_DIR, "motions.parquet"))
            
        size_mb = os.path.getsize(out_file) / (1024 * 1024)
        print(f" Done. {total_rows} rows, {size_mb:.2f} MB in {time.time() - t0:.2f}s", flush=True)
        
    pg_conn.close()

def export_sqlite():
    print("\n------------------------------------------------------------------")
    print("      EXPORTING TO PORTABLE SQLITE DATABASE")
    print("------------------------------------------------------------------")
    sys.stdout.flush()
    
    sqlite_file = os.path.join(OUTPUT_DIR, "gb_sct_mirror.sqlite")
    if os.path.exists(sqlite_file):
        os.remove(sqlite_file)
        
    sqlite_conn = sqlite3.connect(sqlite_file)
    sqlite_conn.execute("PRAGMA journal_mode=WAL;")
    sqlite_conn.execute("PRAGMA synchronous=normal;")
    
    pg_conn = psycopg.connect(DB_CONN_STR)
    
    for name, ep in ENDPOINTS.items():
        t0 = time.time()
        table = ep["table"]
        sqlite_table = name if name != "motionsquestionsanswersmotions" else "motions"
        
        # 1. Create Table in SQLite
        fields_def = []
        insert_cols = []
        select_cols = []
        
        for low_key, (camel_key, sql_type) in ep["fields"].items():
            fields_def.append(f'"{camel_key}" {sql_type}')
            insert_cols.append(f'"{camel_key}"')
            select_cols.append(f'{low_key} as "{camel_key}"')
            
        create_sql = f"CREATE TABLE {sqlite_table} ({', '.join(fields_def)});"
        sqlite_conn.execute(create_sql)
        
        # 2. Insert Data in Batches
        select_clause = ", ".join(select_cols)
        query = f"SELECT {select_clause} FROM {table}"
        
        placeholders = ", ".join(["?" for _ in insert_cols])
        insert_sql = f"INSERT INTO {sqlite_table} ({', '.join(insert_cols)}) VALUES ({placeholders})"
        
        print(f"[*] Exporting {table} -> SQLite '{sqlite_table}'...", end="", flush=True)
        
        with pg_conn.cursor() as pg_cursor:
            pg_cursor.execute(query)
            count = 0
            
            while True:
                rows = pg_cursor.fetchmany(50000)
                if not rows:
                    break
                
                # Format rows: Convert dict/list JSONB objects to JSON string text
                formatted_rows = []
                for row in rows:
                    formatted_row = []
                    for val in row:
                        if isinstance(val, (dict, list)):
                            formatted_row.append(json.dumps(val))
                        elif hasattr(val, 'isoformat'):
                            formatted_row.append(val.isoformat())
                        elif isinstance(val, bool):
                            formatted_row.append(1 if val else 0)
                        else:
                            formatted_row.append(val)
                    formatted_rows.append(formatted_row)
                    
                sqlite_conn.executemany(insert_sql, formatted_rows)
                count += len(rows)
                
        # 3. Create Indexes for SQLite Tables
        primary_key_col = next(camel_key for low, (camel_key, typ) in ep["fields"].items() if "PRIMARY KEY" in typ)
        index_sql = f'CREATE INDEX "idx_{sqlite_table}_{primary_key_col.lower()}" ON {sqlite_table} ("{primary_key_col}");'
        sqlite_conn.execute(index_sql)
        
        sqlite_conn.commit()
        print(f" Done. {count} rows in {time.time() - t0:.2f}s", flush=True)
        
    sqlite_conn.close()
    pg_conn.close()
    
    # Compress SQLite file to .sqlite.gz
    t0 = time.time()
    compressed_file = sqlite_file + ".gz"
    print(f"[*] Gzipping SQLite database to {compressed_file}...", end="", flush=True)
    with open(sqlite_file, 'rb') as f_in:
        with gzip.open(compressed_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            
    # Remove uncompressed sqlite file to save web space
    os.remove(sqlite_file)
    size_mb = os.path.getsize(compressed_file) / (1024 * 1024)
    print(f" Done. {size_mb:.2f} MB in {time.time() - t0:.2f}s", flush=True)

if __name__ == "__main__":
    t_start = time.time()
    export_parquet()
    export_sqlite()
    print(f"\n[+] MULTI-FORMAT BULK EXPORT COMPLETED IN {time.time() - t_start:.2f}s!", flush=True)
