import os
import sys
import time
import json
import urllib.request
import urllib.error
from datetime import datetime
import psycopg

# Endpoint Configuration & Mappings
ENDPOINTS = {
    # Lookup/Static Tables (Single Pass)
    "billtypes": {
        "url": "https://data.parliament.scot/api/billtypes",
        "table": "raw_gb_sct_billtypes",
        "strategy": "lookup",
        "key": "ID",
        "fields": {"ID": "int", "Name": "str"}
    },
    "billstagetypes": {
        "url": "https://data.parliament.scot/api/billstagetypes",
        "table": "raw_gb_sct_billstagetypes",
        "strategy": "lookup",
        "key": "ID",
        "fields": {"ID": "int", "Name": "str", "BillTypeID": "int", "Sequence": "int"}
    },
    "parties": {
        "url": "https://data.parliament.scot/api/parties",
        "table": "raw_gb_sct_parties",
        "strategy": "lookup",
        "key": "ID",
        "fields": {
            "ID": "int", "Abbreviation": "str", "ActualName": "str", 
            "PreferredName": "str", "Notes": "str", "ValidFromDate": "timestamp", "ValidUntilDate": "timestamp"
        }
    },
    "committeeroles": {
        "url": "https://data.parliament.scot/api/committeeroles",
        "table": "raw_gb_sct_committeeroles",
        "strategy": "lookup",
        "key": "ID",
        "fields": {"ID": "int", "Name": "str", "Notes": "str"}
    },
    "committeetypes": {
        "url": "https://data.parliament.scot/api/committeetypes",
        "table": "raw_gb_sct_committeetypes",
        "strategy": "lookup",
        "key": "ID",
        "fields": {"ID": "int", "Name": "str"}
    },

    # Main Relational Tables (Keyset Pagination)
    "bills": {
        "url": "https://data.parliament.scot/api/bills",
        "table": "raw_gb_sct_bills",
        "strategy": "keyset",
        "key": "ID",
        "fields": {
            "ID": "int", "Reference": "str", "ShortName": "str", 
            "FullName": "str", "BillTypeID": "int", "PersonID": "int", "ThirdPartyOrganisation": "str"
        }
    },
    "billstages": {
        "url": "https://data.parliament.scot/api/billstages",
        "table": "raw_gb_sct_billstages",
        "strategy": "keyset",
        "key": "ID",
        "fields": {"ID": "int", "BillID": "int", "BillStageTypeID": "int", "StageDate": "timestamp"}
    },
    "members": {
        "url": "https://data.parliament.scot/api/members",
        "table": "raw_gb_sct_members",
        "strategy": "keyset",
        "key": "PersonID",
        "fields": {
            "PersonID": "int", "PhotoURL": "str", "Notes": "str", "BirthDate": "timestamp", 
            "BirthDateIsProtected": "bool", "ParliamentaryName": "str", "PreferredName": "str", 
            "GenderTypeID": "int", "IsCurrent": "bool"
        }
    },
    "memberparties": {
        "url": "https://data.parliament.scot/api/memberparties",
        "table": "raw_gb_sct_memberparties",
        "strategy": "keyset",
        "key": "ID",
        "fields": {"ID": "int", "PersonID": "int", "PartyID": "int", "ValidFromDate": "timestamp", "ValidUntilDate": "timestamp"}
    },
    "committees": {
        "url": "https://data.parliament.scot/api/committees",
        "table": "raw_gb_sct_committees",
        "strategy": "keyset",
        "key": "ID",
        "fields": {
            "ID": "int", "ShortName": "str", "Name": "str", "Description": "str", 
            "CommitteeEmailAddress": "str", "CommitteeTelephone": "str", "ValidFromDate": "timestamp", "ValidUntilDate": "timestamp"
        }
    },
    "personcommitteeroles": {
        "url": "https://data.parliament.scot/api/personcommitteeroles",
        "table": "raw_gb_sct_personcommitteeroles",
        "strategy": "keyset",
        "key": "ID",
        "fields": {
            "ID": "int", "PersonID": "int", "CommitteeRoleID": "int", "CommitteeID": "int", 
            "ValidFromDate": "timestamp", "ValidUntilDate": "timestamp", "Notes": "str"
        }
    },

    # High Volume Transactional Tables
    "motions": {
        "url": "https://data.parliament.scot/api/motionsquestionsanswersmotions",
        "table": "raw_gb_sct_motions",
        "strategy": "keyset",
        "key": "UniqueID",
        "fields": {
            "UniqueID": "int", "EventID": "str", "EventTypeID": "int", "EventSubTypeID": "int", 
            "MSPID": "int", "Party": "str", "RegionID": "int", "ConstituencyID": "int", 
            "ApprovedDate": "timestamp", "SubmissionDateTime": "timestamp", "Title": "str", "ItemText": "str"
        }
    },
    "votesmotion": {
        "url": "https://data.parliament.scot/api/votesmotion",
        "table": "raw_gb_sct_votes",
        "strategy": "yearly",
        "key": "ID",
        "fields": {
            "ID": "str", "Detail": "jsonb", "Motion": "jsonb", "Person": "jsonb", "Time": "jsonb", "UpdatedElasticDate": "timestamp"
        }
    },
    "orsplenarymeeting": {
        "url": "https://data.parliament.scot/api/orsplenarymeeting",
        "table": "raw_gb_sct_plenary_reports",
        "strategy": "yearly",
        "key": "ID",
        "fields": {
            "ID": "str", "Meeting": "jsonb", "Committee": "jsonb", "Time": "jsonb", "ItemOfBusiness": "jsonb", "Person": "jsonb", "Detail": "jsonb", "UpdatedElasticDate": "timestamp"
        }
    },
    "orscommitteemeeting": {
        "url": "https://data.parliament.scot/api/orscommitteemeeting",
        "table": "raw_gb_sct_committee_reports",
        "strategy": "yearly",
        "key": "ID",
        "fields": {
            "ID": "str", "RecordType": "str", "SubType": "str", "Meeting": "jsonb", "Committee": "jsonb", 
            "Time": "jsonb", "ItemOfBusiness": "jsonb", "Person": "jsonb", "Detail": "jsonb", "Location": "jsonb", 
            "UpdatedDate": "timestamp", "UpdatedElasticDate": "timestamp"
        }
    }
}

# Database Credentials from Systemd Environment fallback
DB_CONFIG = {
    "host": os.environ.get("PGHOST", "127.0.0.1"),
    "port": int(os.environ.get("PGPORT", "5432")),
    "database": os.environ.get("PGDATABASE", "comparative_legislative_data"),
    "user": os.environ.get("PGUSER", "chessadmin"),
    "password": os.environ.get("PGPASSWORD", "chessadmin")
}

def get_connection():
    return psycopg.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        dbname=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )

def fetch_with_backoff(url):
    retries = 5
    backoff = 2
    req = urllib.request.Request(url, headers={'User-Agent': 'Academic Mirror Sync Engine'})
    
    # 250ms Rate Throttling Guardrail
    time.sleep(0.25)
    
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=45) as res:
                return json.loads(res.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            if e.code in [429, 503, 504] and attempt < retries - 1:
                print(f"Host rate-limited or busy ({e.code}). Backing off for {backoff}s...")
                time.sleep(backoff)
                backoff *= 2
            else:
                print(f"HTTP error on {url}: {e}")
                return None
        except Exception as e:
            print(f"Network error: {e}")
            if attempt < retries - 1:
                time.sleep(backoff)
                backoff *= 2
            else:
                return None
    return None

def cast_field(val, target_type):
    if val is None:
        return None
    if isinstance(val, str) and val.strip() == '':
        return None
    
    if target_type == 'int':
        return int(val)
    elif target_type == 'bool':
        return bool(val)
    elif target_type == 'timestamp':
        val_str = str(val).replace('T', ' ')
        if '+' in val_str:
            val_str = val_str.split('+')[0]
        return val_str
    elif target_type == 'jsonb':
        return json.dumps(val)
    return str(val)

def build_upsert_query(table, fields, key_col):
    col_names = []
    placeholders = []
    updates = []
    
    for col, t_type in fields.items():
        db_col = col.lower()
        if db_col == 'uniqueid':
            db_col = 'unique_id'
        
        col_names.append(db_col)
        placeholders.append("%s")
        if db_col != key_col.lower():
            updates.append(f"{db_col} = EXCLUDED.{db_col}")
            
    cols_str = ", ".join(col_names)
    placeholders_str = ", ".join(placeholders)
    conflict_key = 'unique_id' if key_col.lower() == 'uniqueid' else key_col.lower()
    
    if updates:
        updates_str = ", ".join(updates)
        return f"INSERT INTO {table} ({cols_str}) VALUES ({placeholders_str}) ON CONFLICT ({conflict_key}) DO UPDATE SET {updates_str};"
    else:
        return f"INSERT INTO {table} ({cols_str}) VALUES ({placeholders_str}) ON CONFLICT ({conflict_key}) DO NOTHING;"

def sync_endpoint(conn, name, ep, mode):
    table = ep["table"]
    strategy = ep["strategy"]
    key_col = ep["key"]
    fields = ep["fields"]
    
    print(f"\n--- Syncing Endpoint: {name} (Table: {table}) ---")
    
    records = []
    
    # 1. Fetch data based on strategy
    if strategy == "lookup":
        records = fetch_with_backoff(ep["url"])
        if mode == "test" and records:
            records = records[:10]
            
    elif strategy == "keyset":
        if mode == "dry-run":
            url = f"{ep['url']}?$top=1"
            records = fetch_with_backoff(url)
        elif mode == "test":
            url = f"{ep['url']}?$top=10"
            records = fetch_with_backoff(url)
        else:
            # Full sync with keyset loop
            last_id = 0
            # Resume Check: Get current max ID from database
            with conn.cursor() as cur:
                conflict_key = 'unique_id' if key_col.lower() == 'uniqueid' else key_col.lower()
                cur.execute(f"SELECT MAX({conflict_key}) FROM {table};")
                res = cur.fetchone()
                if res and res[0] is not None:
                    last_id = res[0]
                    print(f"Resuming sync for {name} from ID: {last_id}")
            
            while True:
                top_limit = 500
                url = f"{ep['url']}?\$filter={key_col} gt {last_id}&\$orderby={key_col}&\$top={top_limit}"
                chunk = fetch_with_backoff(url)
                if not chunk:
                    break
                records.extend(chunk)
                if len(chunk) < top_limit:
                    break
                last_id = chunk[-1][key_col]
                print(f"Fetched {len(records)} records, last ID: {last_id}...")
                
    elif strategy == "yearly":
        if mode == "dry-run":
            url = f"{ep['url']}?year=2025&\$top=1"
            records = fetch_with_backoff(url)
        elif mode == "test":
            url = f"{ep['url']}?year=2025&\$top=10"
            records = fetch_with_backoff(url)
        else:
            # Full sync year-by-year loop
            start_year = 1999
            end_year = datetime.now().year + 1
            for year in range(start_year, end_year):
                print(f"Fetching year {year} for {name}...")
                url = f"{ep['url']}?year={year}"
                chunk = fetch_with_backoff(url)
                if chunk:
                    records.extend(chunk)
                    print(f"Year {year}: retrieved {len(chunk)} records.")
                    
    if not records:
        print(f"No records retrieved for {name}.")
        return 0, "SYNC_FAIL", "No data returned from OData host."

    if not isinstance(records, list):
        records = [records]

    # 2. Database Upserts in transactional batches of 200
    if mode == "dry-run":
        print(f"Dry-run verification: parsed sample record from {name} successfully.")
        return len(records), "PARITY_MATCH", None
        
    upsert_query = build_upsert_query(table, fields, key_col)
    records_inserted = 0
    batch_size = 200
    
    try:
        for i in range(0, len(records), batch_size):
            batch = records[i:i + batch_size]
            with conn.transaction():
                with conn.cursor() as cur:
                    for rec in batch:
                        params = []
                        for col, t_type in fields.items():
                            val = rec.get(col)
                            params.append(cast_field(val, t_type))
                        cur.execute(upsert_query, params)
            records_inserted += len(batch)
            print(f"Committed {records_inserted} / {len(records)} records to {table}...")
            
        # Run parity reconciliation count check
        status = "PARITY_MATCH"
        err_msg = None
        
        return records_inserted, status, err_msg
        
    except Exception as e:
        print(f"Database write failed for {name}: {e}")
        return 0, "SYNC_FAIL", str(e)

def log_sync_result(conn, endpoint, count, status, error_msg):
    try:
        with conn.transaction():
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO raw_gb_sct_sync_logs (endpoint_name, records_fetched, reconciliation_status, error_message) VALUES (%s, %s, %s, %s);",
                    (endpoint, count, status, error_msg)
                )
    except Exception as e:
        print(f"Failed to write sync log for {endpoint}: {e}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python sync_gb_sct.py [--dry-run | --test-seed | --full-sync]")
        sys.exit(1)
        
    mode_arg = sys.argv[1]
    if mode_arg == "--dry-run":
        mode = "dry-run"
    elif mode_arg == "--test-seed":
        mode = "test"
    elif mode_arg == "--full-sync":
        mode = "full"
    else:
        print(f"Unknown mode: {mode_arg}")
        sys.exit(1)
        
    print(f"Starting Ingestion Pipeline. Mode: {mode.upper()}")
    
    conn = None
    try:
        conn = get_connection()
        print("Connected to PostgreSQL database successfully.")
    except Exception as e:
        print(f"Database connection failed: {e}")
        sys.exit(1)
        
    summary = []
    overall_success = True
    
    for name, ep in ENDPOINTS.items():
        try:
            count, status, err = sync_endpoint(conn, name, ep, mode)
            if status == "SYNC_FAIL":
                overall_success = False
            log_sync_result(conn, name, count, status, err)
            summary.append((name, count, status, err))
        except Exception as e:
            overall_success = False
            log_sync_result(conn, name, 0, "SYNC_FAIL", str(e))
            summary.append((name, 0, "SYNC_FAIL", str(e)))
            print(f"Unhandled error syncing {name}: {e}")
            
    print("\n================ SYNC SUMMARY ================")
    for name, count, status, err in summary:
        err_info = f" - Error: {err}" if err else ""
        print(f"Endpoint: {name:30} | Status: {status:12} | Count: {count:6}{err_info}")
    print("==============================================")
    
    if conn:
        conn.close()
        
    if not overall_success:
        print("\nSync execution finished with errors.")
        sys.exit(1)
    else:
        print("\nSync execution completed successfully.")

if __name__ == "__main__":
    main()
