# Ingestion & Export Pipelines: Scottish Parliament (GB-SCT)

This document provides assembly-specific script paths, validation rules, and crontab operations for the Scottish Parliament (`gb-sct`) data pipelines. For core architectures and the 500-row CSV rule, see the [Core Ingestion & Export Pipeline Specification](file:///home/steven/Documents/github/comparativelegislativedata/docs/pipeline.md).

---

## 1. Data Ingestion (`sync_gb_sct.py`)

*   **Script Location:** `/home/chessadmin/comparativelegislativedata/scripts/sync_gb_sct.py`
*   **Target Tables:** Writes OData records directly to 15 raw staging tables in Database A (e.g., `raw_mirror.raw_gb_sct_bills`).
*   **Recent-Only Scrapes:** In daily execution, the script is run with `RECENT_ONLY=true` to restrict API scraping to the most recent records, completing incremental updates in under 20 seconds.

---

## 2. Parity Validation Auditing (`audit_gb_sct_parity.py`)

*   **Script Location:** `/home/chessadmin/comparativelegislativedata/scripts/audit_gb_sct_parity.py`
*   **Auditing Target:** Runs field-by-field verification audits between local PostgreSQL Database A mirror tables and the live remote `https://data.parliament.scot/api/` endpoints.
*   **Verification Count:** Samples 3 random rows from each of the 15 staging tables on every sync run.

---

## 3. Multi-Format Exporters & Files

We compile mirror exports using two python scripts:
1.  **`export_multi_formats.py`:** Exports mirror tables from Database A to Parquet and SQLite format.
2.  **`export_gb_sct_bulk.py`:** Exports mirror tables from Database A to plain and compressed CSV formats.

### Target Downloads Directory
*   `/home/chessadmin/comparativelegislativedata/downloads/gb-sct/`

### Mirror Files Generated
*   `gb_sct_mirror.sqlite.gz` (Gzipped raw SQLite replica database)
*   Table-level raw Parquet files (e.g. `raw_bills.parquet`)
*   Table-level raw CSV files (e.g. lookups as uncompressed `.csv`, transaction logs as `.csv.gz`)

### Research/Canonical Files Generated (`export_canonical.py`)
Exclusively queries Database B and runs in under 0.3s:
*   `gb_sct_canonical.sqlite.gz` (Gzipped research SQLite database)
*   `canonical_bills.csv` (Uncompressed plain CSV, containing 473 rows)
*   `canonical_memberpartyhistory.csv.gz` (Gzipped CSV, containing 2,378 rows)

---

## 4. Daily Cron Automation (`cron_daily_sync.sh`)

The daily cron wrapper integrates the entire pipeline sequence in a single bash file:
*   **Wrapper Script:** `/home/chessadmin/comparativelegislativedata/scripts/cron_daily_sync.sh`
*   **Crontab execution:**
    ```cron
    0 3 * * * /home/chessadmin/comparativelegislativedata/scripts/cron_daily_sync.sh >> /home/chessadmin/comparativelegislativedata/cron_sync.log 2>&1
    ```
