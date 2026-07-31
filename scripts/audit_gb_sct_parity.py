import os
import sys
import json
import random
import urllib.request
import urllib.error
from datetime import datetime
import psycopg

# Endpoint Configuration & Mappings
ENDPOINTS = {
    "billtypes": {
        "url": "https://data.parliament.scot/api/billtypes",
        "table": "raw_gb_sct_billtypes",
        "key": "ID",
        "strategy": "lookup",
        "fields": {"ID": "int", "Name": "str"}
    },
    "billstagetypes": {
        "url": "https://data.parliament.scot/api/billstagetypes",
        "table": "raw_gb_sct_billstagetypes",
        "key": "ID",
        "strategy": "lookup",
        "fields": {"ID": "int", "Name": "str", "BillTypeID": "int", "Sequence": "int"}
    },
    "parties": {
        "url": "https://data.parliament.scot/api/parties",
        "table": "raw_gb_sct_parties",
        "key": "ID",
        "strategy": "lookup",
        "fields": {
            "ID": "int", "Abbreviation": "str", "ActualName": "str", 
            "PreferredName": "str", "Notes": "str", "ValidFromDate": "timestamp", "ValidUntilDate": "timestamp"
        }
    },
    "committeeroles": {
        "url": "https://data.parliament.scot/api/committeeroles",
        "table": "raw_gb_sct_committeeroles",
        "key": "ID",
        "strategy": "lookup",
        "fields": {"ID": "int", "Name": "str", "Notes": "str"}
    },
    "committeetypes": {
        "url": "https://data.parliament.scot/api/committeetypes",
        "table": "raw_gb_sct_committeetypes",
        "key": "ID",
        "strategy": "lookup",
        "fields": {"ID": "int", "Name": "str"}
    },
    "bills": {
        "url": "https://data.parliament.scot/api/bills",
        "table": "raw_gb_sct_bills",
        "key": "ID",
        "strategy": "lookup",
        "fields": {
            "ID": "int", "Reference": "str", "ShortName": "str", 
            "FullName": "str", "BillTypeID": "int", "PersonID": "int", "ThirdPartyOrganisation": "str"
        }
    },
    "billstages": {
        "url": "https://data.parliament.scot/api/billstages",
        "table": "raw_gb_sct_billstages",
        "key": "ID",
        "strategy": "lookup",
        "fields": {"ID": "int", "BillID": "int", "BillStageTypeID": "int", "StageDate": "timestamp"}
    },
    "members": {
        "url": "https://data.parliament.scot/api/members",
        "table": "raw_gb_sct_members",
        "key": "PersonID",
        "strategy": "lookup",
        "fields": {
            "PersonID": "int", "PhotoURL": "str", "Notes": "str", "BirthDate": "timestamp", 
            "BirthDateIsProtected": "bool", "ParliamentaryName": "str", "PreferredName": "str", 
            "GenderTypeID": "int", "IsCurrent": "bool"
        }
    },
    "memberparties": {
        "url": "https://data.parliament.scot/api/memberparties",
        "table": "raw_gb_sct_memberparties",
        "key": "ID",
        "strategy": "lookup",
        "fields": {"ID": "int", "PersonID": "int", "PartyID": "int", "ValidFromDate": "timestamp", "ValidUntilDate": "timestamp"}
    },
    "committees": {
        "url": "https://data.parliament.scot/api/committees",
        "table": "raw_gb_sct_committees",
        "key": "ID",
        "strategy": "lookup",
        "fields": {
            "ID": "int", "ShortName": "str", "Name": "str", "Description": "str", 
            "CommitteeEmailAddress": "str", "CommitteeTelephone": "str", "ValidFromDate": "timestamp", "ValidUntilDate": "timestamp"
        }
    },
    "personcommitteeroles": {
        "url": "https://data.parliament.scot/api/personcommitteeroles",
        "table": "raw_gb_sct_personcommitteeroles",
        "key": "ID",
        "strategy": "lookup",
        "fields": {
            "ID": "int", "PersonID": "int", "CommitteeRoleID": "int", "CommitteeID": "int", 
            "ValidFromDate": "timestamp", "ValidUntilDate": "timestamp", "Notes": "str"
        }
    },
    "motions": {
        "url": "https://data.parliament.scot/api/motionsquestionsanswersmotions",
        "table": "raw_gb_sct_motions",
        "key": "UniqueID",
        "strategy": "lookup",
        "fields": {
            "UniqueID": "int", "EventID": "str", "EventTypeID": "int", "EventSubTypeID": "int", 
            "MSPID": "int", "Party": "str", "RegionID": "int", "ConstituencyID": "int", 
            "ApprovedDate": "timestamp", "SubmissionDateTime": "timestamp", "Title": "str", "ItemText": "str"
        }
    },
    "votesmotion": {
        "url": "https://data.parliament.scot/api/votesmotion",
        "table": "raw_gb_sct_votes",
        "key": "ID",
        "strategy": "yearly",
        "fields": {
            "ID": "str", "Detail": "jsonb", "Motion": "jsonb", "Person": "jsonb", "Time": "jsonb", "UpdatedElasticDate": "timestamp"
        }
    },
    "orsplenarymeeting": {
        "url": "https://data.parliament.scot/api/orsplenarymeeting",
        "table": "raw_gb_sct_plenary_reports",
        "key": "ID",
        "strategy": "yearly",
        "fields": {
            "ID": "str", "Meeting": "jsonb", "Committee": "jsonb", "Time": "jsonb", "ItemOfBusiness": "jsonb", "Person": "jsonb", "Detail": "jsonb", "UpdatedElasticDate": "timestamp"
        }
    },
    "orscommitteemeeting": {
        "url": "https://data.parliament.scot/api/orscommitteemeeting",
        "table": "raw_gb_sct_committee_reports",
        "key": "ID",
        "strategy": "yearly",
        "fields": {
            "ID": "str", "RecordType": "str", "SubType": "str", "Meeting": "jsonb", "Committee": "jsonb", 
            "Time": "jsonb", "ItemOfBusiness": "jsonb", "Person": "jsonb", "Detail": "jsonb", "Location": "jsonb", 
            "UpdatedDate": "timestamp", "UpdatedElasticDate": "timestamp"
        }
    }
}

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

# Cache for yearly/lookup API downloads to prevent duplicate calls
API_CACHE = {}

def fetch_full_url(url):
    if url in API_CACHE:
        return API_CACHE[url]
        
    print(f"    - [API] Downloading from OData host: {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Academic Parity Auditor'})
    try:
        with urllib.request.urlopen(req, timeout=60) as res:
            data = json.loads(res.read().decode('utf-8'))
            if not isinstance(data, list):
                data = [data]
            API_CACHE[url] = data
            return data
    except Exception as e:
        print(f"      [!] API Fetch Error: {e}")
        return None

def normalize_db_val(val, target_type):
    if val is None:
        return None
    if target_type == 'jsonb':
        if isinstance(val, str):
            try:
                return json.loads(val)
            except:
                return val
        return val
    if target_type == 'timestamp':
        val_str = str(val).replace('T', ' ')
        if '+' in val_str:
            val_str = val_str.split('+')[0]
        if '.' in val_str:
            val_str = val_str.split('.')[0]
        return val_str
    if target_type == 'int':
        return int(val)
    if target_type == 'bool':
        return bool(val)
    return str(val)

def normalize_api_val(val, target_type):
    if val is None:
        return None
    if isinstance(val, str) and val.strip() == '':
        return None
    if target_type == 'jsonb':
        return val
    if target_type == 'timestamp':
        val_str = str(val).replace('T', ' ')
        if '+' in val_str:
            val_str = val_str.split('+')[0]
        if '.' in val_str:
            val_str = val_str.split('.')[0]
        return val_str
    if target_type == 'int':
        return int(val)
    if target_type == 'bool':
        return bool(val)
    return str(val)

def deep_compare_json(db_val, api_val):
    # Strip any formatting difference by re-serializing or direct dict comparison
    if db_val == api_val:
        return True
    # If they are both dicts or lists, do deep comparison
    if type(db_val) != type(api_val):
        return False
    if isinstance(db_val, dict):
        if len(db_val) != len(api_val):
            return False
        for k, v in db_val.items():
            if k not in api_val:
                return False
            if not deep_compare_json(v, api_val[k]):
                return False
        return True
    elif isinstance(db_val, list):
        if len(db_val) != len(api_val):
            return False
        for i in range(len(db_val)):
            if not deep_compare_json(db_val[i], api_val[i]):
                return False
        return True
    return False

def run_audit():
    print("==================================================================")
    print("      SCOTTISH PARLIAMENT DB-TO-API PARITY VALIDATION AUDIT")
    print("==================================================================")
    
    try:
        conn = get_connection()
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        sys.exit(1)
        
    all_passed = True
    
    with conn.cursor() as cur:
        for name, ep in ENDPOINTS.items():
            table = ep["table"]
            key_col = ep["key"]
            fields = ep["fields"]
            strategy = ep["strategy"]
            conflict_key = key_col.lower()
            
            print(f"\n[*] Auditing Endpoint: {name:22} (Table: {table})")
            
            # 1. Fetch total count
            cur.execute(f"SELECT COUNT(*) FROM {table};")
            db_count = cur.fetchone()[0]
            print(f"    - Database Row Count: {db_count}")
            
            if db_count == 0:
                print("    - WARNING: Table is empty! Skipping verification.")
                continue
            
            # 2. Select sample records
            # If yearly strategy, select the year as well for cache fetching
            if strategy == "yearly":
                cur.execute(f"""
                    SELECT {conflict_key}, time, {", ".join([f.lower() for f in fields.keys()])}
                    FROM {table}
                    ORDER BY RANDOM()
                    LIMIT 3;
                """)
                rows = cur.fetchall()
                sample_records = []
                for row in rows:
                    rec_id = row[0]
                    time_val = row[1]
                    db_vals = row[2:]
                    year = None
                    if time_val:
                        if isinstance(time_val, str):
                            try:
                                t_dict = json.loads(time_val)
                            except:
                                t_dict = {}
                        else:
                            t_dict = time_val
                        start_date = t_dict.get("Start")
                        if start_date and len(start_date) >= 4:
                            year = int(start_date[:4])
                    if not year:
                        year = 2025 # Fallback
                    sample_records.append((rec_id, year, db_vals))
            else:
                cur.execute(f"""
                    SELECT {conflict_key}, {", ".join([f.lower() for f in fields.keys()])}
                    FROM {table}
                    ORDER BY RANDOM()
                    LIMIT 3;
                """)
                rows = cur.fetchall()
                sample_records = []
                for row in rows:
                    rec_id = row[0]
                    db_vals = row[1:]
                    sample_records.append((rec_id, None, db_vals))
            
            print(f"    - Selected Sample IDs for Deep Comparison: {[r[0] for r in sample_records]}")
            
            # 3. Cache API source data
            api_indexed = {}
            if strategy == "lookup":
                # Fetch full lookup catalog
                api_list = fetch_full_url(ep["url"])
                if api_list:
                    for api_rec in api_list:
                        if isinstance(api_rec, dict) and key_col in api_rec:
                            api_indexed[api_rec[key_col]] = api_rec
            
            # 4. Compare each sample record
            for rec_id, year, db_vals in sample_records:
                # If yearly, fetch that year's OData slice
                if strategy == "yearly":
                    url = f"{ep['url']}?year={year}"
                    api_list = fetch_full_url(url)
                    api_indexed = {}
                    if api_list:
                        for api_rec in api_list:
                            if isinstance(api_rec, dict) and key_col in api_rec:
                                api_indexed[api_rec[key_col]] = api_rec
                
                # Fetch from local DB record dictionary
                db_record = {}
                for idx, (col_name, target_type) in enumerate(fields.items()):
                    db_record[col_name.lower()] = normalize_db_val(db_vals[idx], target_type)
                
                # Find matching record in API index
                api_raw = api_indexed.get(rec_id)
                if not api_raw:
                    # Treat string key comparison case-insensitively just in case
                    if isinstance(rec_id, str):
                        for k, v in api_indexed.items():
                            if str(k).lower() == rec_id.lower():
                                api_raw = v
                                break
                                
                if not api_raw:
                    print(f"      [!] ID {rec_id} could not be found in the live API dataset!")
                    all_passed = False
                    continue
                    
                # Normalize API fields
                api_record = {}
                for col_name, target_type in fields.items():
                    api_record[col_name.lower()] = normalize_api_val(api_raw.get(col_name), target_type)
                    
                # Field comparison
                mismatches = []
                for col, target_type in fields.items():
                    col_low = col.lower()
                    db_val = db_record.get(col_low)
                    api_val = api_record.get(col_low)
                    
                    if target_type == 'jsonb':
                        if not deep_compare_json(db_val, api_val):
                            mismatches.append((col, db_val, api_val))
                    else:
                        if db_val != api_val:
                            mismatches.append((col, db_val, api_val))
                            
                if len(mismatches) == 0:
                    print(f"      [+] ID {str(rec_id):22} -> MATCH")
                else:
                    print(f"      [X] ID {str(rec_id):22} -> MISMATCH DETECTED!")
                    all_passed = False
                    for col, db_val, api_val in mismatches:
                        print(f"          Column '{col}': DB='{db_val}' vs API='{api_val}'")
                        
    conn.close()
    
    print("\n==================================================================")
    if all_passed:
        print("  PARITY VERIFICATION RESULT: PASSED (ALL FIELDS ALIGNED!)")
    else:
        print("  PARITY VERIFICATION RESULT: FAILED (MISMATCHES FOUND!)")
    print("==================================================================")
    sys.exit(0 if all_passed else 1)

if __name__ == "__main__":
    run_audit()
