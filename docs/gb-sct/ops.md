# Operations Reference Manual: Scottish Parliament (GB-SCT)

This document provides assembly-specific operational pathways, database schemas, sync cron logs, and target export pathways for the Scottish Parliament (`gb-sct`) implementation. For core VPS specifications and systemd service commands, see the [Core Operations & VPS Access Guide](file:///home/steven/Documents/github/comparativelegislativedata/docs/ops.md).

---

## 1. Database Specifications

*   **Database A (Raw Mirror):** `comparative_legislative_data`
    *   Holds only raw OData staging tables. Read-only connection for all API/Research scripts.
*   **Database B (Research Layer):** `comparative_legislative_data_canonical`
    *   Holds the physical `canonical_*` tables and the `postgres_fdw` foreign tables mapping.

### psql Database Access Commands
```bash
# Connect to Database A (Raw Mirror)
ssh chessserver "sudo -u postgres psql -d comparative_legislative_data"

# Connect to Database B (Canonical Layer)
ssh chessserver "sudo -u postgres psql -d comparative_legislative_data_canonical"
```

---

## 2. Ingestion Sync & Bulk Export Automation

*   **Raw Mirror Sync Script:** `/home/chessadmin/comparativelegislativedata/scripts/sync_gb_sct.py`
*   **Raw Mirror Exporter:** `/home/chessadmin/comparativelegislativedata/scripts/export_multi_formats.py` (SQLite/Parquet) and `/home/chessadmin/comparativelegislativedata/scripts/export_gb_sct_bulk.py` (CSV).
*   **Canonical ETL Compiler SQL:** `/home/chessadmin/comparativelegislativedata/scripts/compile_canonical_layer.sql`
*   **Canonical Exporter:** `/home/chessadmin/comparativelegislativedata/scripts/export_canonical.py`
*   **Daily Cron Job Shell Wrapper:** `/home/chessadmin/comparativelegislativedata/scripts/cron_daily_sync.sh`
*   **Bulk Downloads Target Folder:** `/home/chessadmin/comparativelegislativedata/downloads/gb-sct/`

### Crontab Entry (Runs daily at 3:00 AM)
```cron
0 3 * * * /home/chessadmin/comparativelegislativedata/scripts/cron_daily_sync.sh >> /home/chessadmin/comparativelegislativedata/cron_sync.log 2>&1
```

---

## 3. Operational Terminal Commands

Use these exact commands on `chessserver` to manually execute or audit the Scottish Parliament data pipeline:

### Ingest and Export Data
```bash
# Force execute a manual incremental sync and mirror export run
ssh chessserver "/home/chessadmin/comparativelegislativedata/scripts/cron_daily_sync.sh"

# Re-compile Database B canonical variables
ssh chessserver "sudo -u postgres psql -d comparative_legislative_data_canonical -f /home/chessadmin/comparativelegislativedata/scripts/compile_canonical_layer.sql"

# Re-export Database B canonical datasets (SQLite, Parquets, CSVs)
ssh chessserver "/home/chessadmin/comparativelegislativedata/.venv/bin/python3 /home/chessadmin/comparativelegislativedata/scripts/export_canonical.py"
```

### Auditing & Logging
```bash
# Inspect the tail of the daily cron execution logs
ssh chessserver "tail -n 100 /home/chessadmin/comparativelegislativedata/cron_sync.log"

# Check sizes of compiled downloads on disk
ssh chessserver "du -sh /home/chessadmin/comparativelegislativedata/downloads/gb-sct/*"
```
