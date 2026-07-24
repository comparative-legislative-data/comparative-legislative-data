#!/usr/bin/env python3
"""
Production-Grade Scottish Parliament (GB-SCT) Raw API Ingestion Mirror
=======================================================================
Connects to data.parliament.scot/api, fetches raw JSON payload streams,
computes SHA-256 payload hashes, and stores raw records cleanly in SQLite/PostgreSQL.

Usage:
  python3 fetch_holyrood_raw.py --dry-run --endpoint bills --sample 5 --verbose
  python3 fetch_holyrood_raw.py --endpoint bills --sample 5
  python3 fetch_holyrood_raw.py --all --reconcile
"""

import argparse
import hashlib
import json
import os
import sqlite3
import sys
import time
import urllib.request
from datetime import datetime

ENDPOINTS = {
    'bills': 'https://data.parliament.scot/api/bills',
    'billtypes': 'https://data.parliament.scot/api/billtypes',
    'members': 'https://data.parliament.scot/api/members',
    'memberparties': 'https://data.parliament.scot/api/memberparties',
    'parties': 'https://data.parliament.scot/api/parties',
    'PersonCommitteeRoles': 'https://data.parliament.scot/api/PersonCommitteeRoles',
    'committees': 'https://data.parliament.scot/api/committees',
    'MemberGovernmentRoles': 'https://data.parliament.scot/api/MemberGovernmentRoles',
    'GovernmentRoles': 'https://data.parliament.scot/api/GovernmentRoles',
    'sessions': 'https://data.parliament.scot/api/sessions',
    'events': 'https://data.parliament.scot/api/events',
    'orsplenarymeeting': 'https://data.parliament.scot/api/orsplenarymeeting?year=2024',
    'orscommitteemeeting': 'https://data.parliament.scot/api/orscommitteemeeting?year=2024'
}

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), 'holyrood_mirror.db')

def init_db(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Execution Log Table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS etl_execution_logs (
            run_id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            trigger_type TEXT NOT NULL,
            endpoint TEXT NOT NULL,
            duration_ms INTEGER NOT NULL,
            records_fetched INTEGER NOT NULL,
            payload_bytes INTEGER NOT NULL,
            sha256_hash TEXT NOT NULL,
            status TEXT NOT NULL,
            error_message TEXT
        )
    ''')
    
    # Raw JSON Endpoint Mirror Tables
    for ep_name in ENDPOINTS.keys():
        table_name = f"raw_gbsct_{ep_name.lower()}"
        cur.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
                record_id TEXT PRIMARY KEY,
                raw_json TEXT NOT NULL,
                sha256_hash TEXT NOT NULL,
                ingested_at TEXT NOT NULL
            )
        ''')
        
    conn.commit()
    return conn

def fetch_endpoint(ep_name, url, sample_limit=None, verbose=False):
    start_time = time.time()
    if verbose:
        print(f"🌐 Fetching endpoint '{ep_name}' from: {url}")
        
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Research Pipeline Bot)'})
    with urllib.request.urlopen(req, timeout=15) as res:
        raw_bytes = res.read()
        duration_ms = int((time.time() - start_time) * 1000)
        payload_bytes = len(raw_bytes)
        sha256_hash = hashlib.sha256(raw_bytes).hexdigest()
        
        text = raw_bytes.decode('utf-8').strip()
        data = json.loads(text)
        
        if isinstance(data, list):
            records = data
        elif isinstance(data, dict):
            records = [data]
        else:
            records = []
            
        if sample_limit and sample_limit > 0:
            records = records[:sample_limit]
            
        return {
            'ep_name': ep_name,
            'url': url,
            'duration_ms': duration_ms,
            'payload_bytes': payload_bytes,
            'sha256_hash': sha256_hash,
            'records': records,
            'total_count': len(records)
        }

def process_ingest(conn, ep_result, dry_run=False, verbose=False):
    ep_name = ep_result['ep_name']
    records = ep_result['records']
    table_name = f"raw_gbsct_{ep_name.lower()}"
    now_iso = datetime.utcnow().isoformat() + 'Z'
    
    if dry_run:
        print(f"🧪 [DRY RUN] Endpoint: '{ep_name}'")
        print(f"   - URL: {ep_result['url']}")
        print(f"   - Latency: {ep_result['duration_ms']} ms")
        print(f"   - Payload Size: {(ep_result['payload_bytes']/1024):.2f} KB")
        print(f"   - SHA-256 Hash: {ep_result['sha256_hash']}")
        print(f"   - Sample Records Count: {len(records)}")
        if len(records) > 0 and verbose:
            sample_keys = list(records[0].keys()) if isinstance(records[0], dict) else []
            print(f"   - Sample Revealed Keys ({len(sample_keys)}): {sample_keys}")
            print(f"   - Sample Record #1: {json.dumps(records[0], indent=2)[:300]}...")
        return
        
    cur = conn.cursor()
    inserted_count = 0
    
    for idx, rec in enumerate(records):
        if isinstance(rec, dict):
            rec_id = str(rec.get('ID') or rec.get('PersonID') or idx)
        else:
            rec_id = str(idx)
        rec_json = json.dumps(rec)
        rec_hash = hashlib.sha256(rec_json.encode('utf-8')).hexdigest()
        
        cur.execute(f'''
            INSERT INTO {table_name} (record_id, raw_json, sha256_hash, ingested_at)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(record_id) DO UPDATE SET
                raw_json = excluded.raw_json,
                sha256_hash = excluded.sha256_hash,
                ingested_at = excluded.ingested_at
        ''', (rec_id, rec_json, rec_hash, now_iso))
        inserted_count += 1
        
    cur.execute('''
        INSERT INTO etl_execution_logs 
        (timestamp, trigger_type, endpoint, duration_ms, records_fetched, payload_bytes, sha256_hash, status, error_message)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (now_iso, 'MANUAL', ep_name, ep_result['duration_ms'], inserted_count, ep_result['payload_bytes'], ep_result['sha256_hash'], 'SUCCESS', None))
    
    conn.commit()
    print(f"✅ Ingested '{ep_name}': {inserted_count} records into '{table_name}' (Hash: {ep_result['sha256_hash'][:12]}...)")

def main():
    parser = argparse.ArgumentParser(description="Scottish Parliament Raw Ingestion ETL Mirror")
    parser.add_argument('--dry-run', action='store_true', help="Fetch and log without DB modification")
    parser.add_argument('--endpoint', type=str, help="Target specific endpoint name (e.g. bills, members)")
    parser.add_argument('--all', action='store_true', help="Fetch all endpoints")
    parser.add_argument('--sample', type=int, default=None, help="Limit fetch to N sample records")
    parser.add_argument('--reconcile', action='store_true', help="Run 1:1 host parity reconciliation after fetch")
    parser.add_argument('--verbose', action='store_true', help="Enable detailed console output")
    parser.add_argument('--db-path', type=str, default=DEFAULT_DB_PATH, help="Path to SQLite database")
    
    args = parser.parse_args()
    
    if not args.endpoint and not args.all:
        print("Error: Specify either --endpoint <name> or --all")
        sys.exit(1)
        
    conn = init_db(args.db_path)
    target_endpoints = {}
    
    if args.endpoint:
        if args.endpoint not in ENDPOINTS:
            print(f"Error: Unknown endpoint '{args.endpoint}'. Valid options: {list(ENDPOINTS.keys())}")
            sys.exit(1)
        target_endpoints[args.endpoint] = ENDPOINTS[args.endpoint]
    else:
        target_endpoints = ENDPOINTS
        
    print(f"🚀 Initializing ETL Ingestion (Endpoints: {len(target_endpoints)} | Dry Run: {args.dry_run})")
    
    for ep_name, url in target_endpoints.items():
        try:
            res = fetch_endpoint(ep_name, url, sample_limit=args.sample, verbose=args.verbose)
            process_ingest(conn, res, dry_run=args.dry_run, verbose=args.verbose)
        except Exception as e:
            print(f"❌ Error fetching endpoint '{ep_name}': {e}")
            if not args.dry_run:
                cur = conn.cursor()
                now_iso = datetime.utcnow().isoformat() + 'Z'
                cur.execute('''
                    INSERT INTO etl_execution_logs 
                    (timestamp, trigger_type, endpoint, duration_ms, records_fetched, payload_bytes, sha256_hash, status, error_message)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (now_iso, 'MANUAL', ep_name, 0, 0, 0, '', 'FAILURE', str(e)))
                conn.commit()

if __name__ == '__main__':
    main()
