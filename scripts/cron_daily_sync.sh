#!/bin/bash
set -e

# Load PostgreSQL configuration environment variables
export PGHOST=127.0.0.1
export PGPORT=5432
export PGDATABASE=comparative_legislative_data
export PGUSER=chessadmin
export PGPASSWORD=chessadmin

# Enable incremental sync mode (only fetch recent years for transcripts and votes)
export RECENT_ONLY=true

echo "=================================================================="
echo "Starting Daily Mirror Sync: $(date)"
echo "=================================================================="

# 1. Run database sync
/home/chessadmin/comparativelegislativedata/.venv/bin/python3 /home/chessadmin/comparativelegislativedata/scripts/sync_gb_sct.py

# 2. Run multi-format exporter to regenerate Parquet and SQLite db
/home/chessadmin/comparativelegislativedata/.venv/bin/python3 /home/chessadmin/comparativelegislativedata/scripts/export_multi_formats.py

# 3. Run CSV exporter to regenerate gzipped CSV bulk files
/home/chessadmin/comparativelegislativedata/.venv/bin/python3 /home/chessadmin/comparativelegislativedata/scripts/export_gb_sct_bulk.py

# 4. Compile Database B canonical research layer
sudo -u postgres psql -d comparative_legislative_data_canonical -f /home/chessadmin/comparativelegislativedata/scripts/compile_canonical_layer.sql

# 5. Export canonical research variables files (SQLite, Parquets, CSVs)
/home/chessadmin/comparativelegislativedata/.venv/bin/python3 /home/chessadmin/comparativelegislativedata/scripts/export_canonical.py

echo "Daily Sync completed successfully: $(date)"
