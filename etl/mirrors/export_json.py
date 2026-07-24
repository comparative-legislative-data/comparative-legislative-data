#!/usr/bin/env python3
"""
Export Canonical Bills to JSON & Parquet
========================================
Exports canonical_gbsct_bills table to frontend/static/data/GB-SCT_canonical_bills.json
for zero-dependency SvelteKit API serving.
"""

import json
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), 'holyrood_mirror.db')
OUT_JSON = os.path.join(os.path.dirname(__file__), '../../frontend/static/data/GB-SCT_canonical_bills.json')

def main():
    os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM canonical_gbsct_bills")
    rows = [dict(r) for r in cur.fetchall()]
    
    with open(OUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(rows, f, indent=2)
        
    print(f"✅ Exported {len(rows)} canonical bill records to: {OUT_JSON}")

if __name__ == '__main__':
    main()
