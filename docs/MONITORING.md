# Operational Monitoring, Pruning & Backup Architecture

This document defines the **Senior-Engineer Observability, Log Pruning, and Backup Specification** for the Comparative Legislative Data infrastructure.

---

## 1. Operational Observability Domains

The monitoring system is divided into two distinct domains:
1. **Application & Infrastructure Operational Metrics** (How our VPS, scrapers, databases, and processes are running).
2. **Public API & Data Usage Metrics** (How our public endpoints, bulk exports, and query latencies are performing).

```
 ┌────────────────────────────────────────────────────────────────────────────────────────┐
 │                        DOMAIN 1: APPLICATION & INFRASTRUCTURE HEALTH                   │
 ├─────────────────────────┬───────────────────────────────┬──────────────────────────────┤
 │ Host & System Resources │ Pipeline & Scraper ETL Health │ Database & Storage Integrity │
 ├─────────────────────────┼───────────────────────────────┼──────────────────────────────┤
 │ • CPU / RAM Utilization │ • Scraper Ingestion Status    │ • PostgreSQL Connection Pool │
 │ • Disk Space & I/O      │ • External Host Status Codes  │ • Query Latency & Slow Logs  │
 │ • Systemd Process Uptime│ • Schema Validation Errors    │ • Raw Payload Archive Size   │
 │ • OOM / Crash Counts    │ • Upstream Schema Drift Warnings • Parquet Generation Time  │
 └─────────────────────────┴───────────────────────────────┴──────────────────────────────┘
```

---

## 2. Log & System File Pruning Strategy

To prevent system logs and temporary scraping artifacts from consuming VPS disk space over time, we enforce automated log rotation and file pruning policies.

### 2.1 Systemd Journal Logs (`journalctl`)
Configured via `/etc/systemd/journald.conf` on the host:
- `SystemMaxUse=2G`: Caps total system log storage at 2 GB.
- `MaxRetentionSec=30day`: Automatically purges logs older than 30 days.

### 2.2 Application & Audit Logs (`data/logs/`)
Managed via Linux `logrotate` (`/etc/logrotate.d/compdata`):
- **Frequency:** Daily log rotation with gzip compression (`compress`).
- **Retention:** 30 rotated log archives retained (30-day rolling audit trail).
- **Threshold:** Immediate rotation if `audit.jsonl` or `app.log` exceeds 100 MB.

### 2.3 Temporary Scraping Artifacts (`data/tmp/`)
Managed via an automated daily cleanup cron:
```bash
# Purge temporary scrape downloads older than 7 days
find /opt/comparativelegislativedata/data/tmp/ -type f -mtime +7 -delete
```

---

## 3. Automated Backup & Recovery Architecture

Academic datasets and raw source payloads must be safely backed up off-site to protect against hardware failures or data corruption.

```
 ┌─────────────────────────────────────────────────────────────────────────────────────────┐
 │                                   NIGHTLY BACKUP PIPELINE                               │
 │                                                                                         │
 │  ┌─────────────────────────────┐        ┌────────────────────────────────────────────┐  │
 │  │ PostgreSQL Database Dump    │        │ Raw Payload Incremental Sync               │  │
 │  │ (pg_dump -Fc -> db.sql.gz)  │        │ (rclone sync /data/raw/ -> off-site)       │  │
 │  └──────────────┬──────────────┘        └─────────────────────┬──────────────────────┘  │
 │                 │                                             │                         │
 │                 ▼                                             ▼                         │
 │  ┌─────────────────────────────┐        ┌────────────────────────────────────────────┐  │
 │  │ Local Backup Retention      │        │ Off-Site Secondary VPS / S3 Storage        │  │
 │  │ (Retain 14 daily dumps)     │        │ (e.g. HostbrrThreadripper / Backblaze)    │  │
 │  └─────────────────────────────┘        └────────────────────────────────────────────┘  │
 └─────────────────────────────────────────────────────────────────────────────────────────┘
```

### 3.1 Backup Classification & Frequency

| Component | Target Path | Backup Frequency | Strategy & Retention |
| :--- | :--- | :--- | :--- |
| **PostgreSQL Database** | `db_compdata` | Daily (03:00 UTC) | `pg_dump -Fc` compressed dump. Retain 14 daily, 4 weekly, 12 monthly local snapshots. |
| **Raw Payload Archive** | `/data/raw/` | Daily (03:30 UTC) | `rclone` / `rsync` incremental sync to secondary storage (`HostbrrThreadripper` or S3/B2). |
| **Environment & Secrets** | `.env`, systemd units | On modification | Encrypted backup stored off-site. |
| **Parquet Datasets** | `/data/parquet/` | Re-generable | Re-compiled automatically from Postgres + Raw Payloads if lost. |

### 3.2 Automated Backup Service (`compdata-backup.service`)
A dedicated nightly systemd service executes the backup script:

```bash
#!/usr/bin/env bash
set -euo pipefail

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/data/backups"
mkdir -p "$BACKUP_DIR"

# 1. Dump PostgreSQL database
pg_dump -U compdata -d compdata -Fc | gzip > "$BACKUP_DIR/db_$TIMESTAMP.sql.gz"

# 2. Prune local database backups older than 14 days
find "$BACKUP_DIR" -name "db_*.sql.gz" -mtime +14 -delete

# 3. Incremental sync of raw payload archives off-site
rclone sync /opt/comparativelegislativedata/data/raw/ remote_secondary:compdata-raw-backups/
```

---

## 4. Alerting Threshold Matrix

| Alert Name | Severity | Condition | Action / Notification |
| :--- | :--- | :--- | :--- |
| `DiskSpaceLow` | 🔴 **Critical** | Available disk space $< 15\text{ GB}$ | Email / Notification to SysAdmin to clean or expand storage. |
| `BackupFailed` | 🔴 **Critical** | `compdata-backup.service` exits with error | Immediate notification; inspect backup log. |
| `APIHighErrorRate` | 🔴 **Critical** | 5xx error rate $> 0.5\%$ over 5 min | Immediate alert; inspect `journalctl -u compdata-api`. |
| `ScraperDriftDetected` | 🟡 **Warning** | Validation error rate $> 2\%$ on ETL run | Flag scraper for HTML/API schema review in `docs/mappings/`. |
| `UpstreamRateLimited` | 🟡 **Warning** | Source API returns HTTP 429 | Automatic backoff delay; notify ETL log. |
| `APISlowResponse` | 🟡 **Warning** | $p_{95}$ latency $> 250\text{ms}$ over 10 min | Inspect slow SQL / DuckDB query log. |

---

## Document Revision History

- **2026-07-21 (v1.1):** Added Section 2 (System File & Log Pruning Strategy) and Section 3 (Automated Backup & Off-Site Recovery Architecture).
- **2026-07-21 (v1.0):** Initial operational monitoring and observability specification.
