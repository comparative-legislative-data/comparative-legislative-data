# QA, Verification, & Technical Debt Playbook (General)

This document outlines the core testing strategies, independent verification protocols, and technical debt registers for the comparative legislative data platform.

---

## 1. Daily Sync Scraper Testing under Recess (The Mocking Protocol)

### The Problem
During parliamentary recesses, upstream official OData or REST feeds do not receive new updates. This makes it impossible to verify that incremental sync scrapers, WAL write buffers, and notification systems are functioning correctly in production.

### The QA Solution: OData Upstream Simulation
To test the pipeline under recess, the platform uses a **Local Mock Ingest Loop**:
1.  **Mock Endpoint Integration:** Configure a test-only route `/api/v2/mock/odata/[endpoint]` in the web application.
2.  **Payload Ingestion:** The mock endpoint reads from static JSON mock data files representing official upstream OData payloads.
3.  **Scrape Simulation Run:** Trigger a test sync run by pointing the scraper's base API environment variable to the local mock route:
    ```bash
    API_BASE_URL="http://localhost:3100/api/v2/mock/odata" \
    [ingest_script] --test
    ```
4.  **Incremental Drift Testing:** Modify the static JSON payload (e.g. adding a mock record with an incremented ID and current timestamp) and verify that:
    *   The incremental sync parser correctly scrapes only the new record.
    *   The record is upserted into the PostgreSQL staging tables.
    *   The mirror database compiles, export scripts trigger, and downstream downloads are updated.

---

## 2. Periodic Independent Data Auditing

To demonstrate data completeness and trustworthiness to academic researchers, the repository implements a weekly independent audit run that operates separately from the ingestion pipelines.

```
                  +---------------------------+
                  | PostgreSQL Staging Tables |
                  +---------------------------+
                               |
         +---------------------+---------------------+
         |                     |                     |
         v                     v                     v
   1. Completeness       2. Coherence          3. Freshness
  (Sequential ID        (Referential           (Heartbeat
     Gap Check)        Integrity Check)        Timestamp)
         |                     |                     |
         +---------------------+---------------------+
                               |
                               v
                     [ Public QA Badges ]
```

### 2.1 Completeness (Sequential ID Gap Checks)
Scraper sync interruptions or remote API timeouts can result in missing records. SQL checks are run on sequential database keys to identify gaps:
```sql
SELECT id + 1 AS missing_id
FROM raw_table AS t1
WHERE NOT EXISTS (
    SELECT 1 FROM raw_table AS t2 WHERE t2.id = t1.id + 1
) AND id < (SELECT MAX(id) FROM raw_table);
```
If gaps are detected, the auditor flags the specific ranges to trigger targeted scraping of those missing IDs.

### 2.2 Coherence (Referential Integrity Check)
Because raw staging tables do not enforce foreign key constraints (to prevent remote API errors from blocking ingestion runs), we must verify referential consistency after loading:
```sql
SELECT DISTINCT reference_id 
FROM raw_table_A 
WHERE reference_id NOT IN (SELECT id FROM raw_table_B);
```
If referential mismatches occur, it alerts us that an upstream entity was deleted or modified in a way that requires schema normalization updates.

### 2.3 Freshness & Verification Reports
*   **Heartbeat Timestamp:** Check the maximum `updated` date across all tables to confirm the sync cron is actively writing.
*   **Public Integrity Badges:** Generate a public static file `parity_audit_report.json` containing the database table counts and parity comparison matches. The frontend reads this file to display dynamic parity indicators.

---

## 3. Technical Debt Register Blueprint

Below is the active tracker structure of structural, performance, and API debt items to address in future sprint iterations:

*   **TD-01: Unconstrained Staging Tables** (enforcing database constraints in mirror layers vs. raw performance).
*   **TD-02: Historical Cold Ingestion limits** (handling cold starts without exceeding VPS RAM capacity).
*   **TD-03: hardcoded Lookups** (keeping OData dictionary variables synchronized between db tables and frontend Svelte templates).
*   **TD-04: Upstream Schema Drift** (detecting upstream casing or parameter modifications before they break ingestion pipelines).
