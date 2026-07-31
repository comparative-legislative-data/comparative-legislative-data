# QA, Verification, & Technical Debt Playbook: Scottish Parliament (GB-SCT)

This document provides assembly-specific verification scripts, localized SQL integrity checks, and the active technical debt register for the Scottish Parliament (`gb-sct`) implementation. For core mocking logic and the gap-checking methodology, see the [Core QA, Verification, & Technical Debt Playbook](file:///home/steven/Documents/github/comparativelegislativedata/docs/qa.md).

---

## 1. Daily Sync Scraper Testing under Recess

Use the following localized environment variables to route the Holyrood scraper to the local mock SvelteKit endpoint during recess testing:

```bash
API_BASE_URL="http://localhost:3100/api/v2/mock/odata" \
/home/chessadmin/comparativelegislativedata/.venv/bin/python3 /home/chessadmin/comparativelegislativedata/scripts/sync_gb_sct.py --test
```

Verify that the mock ingestion sync correctly loads, updates staging records, and triggers raw mirror exports.

---

## 2. Localized Independent Data Audits

Run these exact SQL checks weekly on Database A (`comparative_legislative_data`) to audit the health of the Holyrood datasets:

### 2.1 Motion ID Completeness (Sequence Checks)
Checks for missing motion IDs in sequence, identifying network drops or API pagination timeouts:
```sql
SELECT id + 1 AS missing_id
FROM raw_mirror.raw_gb_sct_motions AS t1
WHERE NOT EXISTS (
    SELECT 1 FROM raw_mirror.raw_gb_sct_motions AS t2 WHERE t2.id = t1.id + 1
) AND id < (SELECT MAX(id) FROM raw_mirror.raw_gb_sct_motions);
```

### 2.2 Member Roles Coherence (Referential Checks)
Because raw staging tables do not enforce foreign key constraints, verify that all committee roles are associated with an active, valid elected member:
```sql
SELECT DISTINCT personid 
FROM raw_mirror.raw_gb_sct_personcommitteeroles 
WHERE personid NOT IN (SELECT personid FROM raw_mirror.raw_gb_sct_members);
```

### 2.3 Heartbeat Freshness Verification
Verify the date of the most recent sync event by checking the maximum update date:
```sql
SELECT MAX(updated) FROM raw_mirror.raw_gb_sct_motions;
```

---

## 3. Technical Debt Register: Scottish Parliament (`gb-sct`)

Below is the active tracker of structural, performance, and API debt items to address in future sprint iterations:

| ID | Component | Debt Description | Risk / Impact | Mitigation Strategy |
| :--- | :--- | :--- | :--- | :--- |
| **TD-01** | Database | Raw staging tables do not enforce strict schema constraints. | Relational integrity issues can bypass ingestion. | Run the weekly Independent coherence query checks. |
| **TD-02** | Scraper | Ingestion scans years back to 1999 during cold starts. | Scraper memory limits may overflow on full historical rebuilds. | Stream OData responses directly into files using chunked file writers instead of loading arrays into RAM. |
| **TD-03** | Frontend | Hardcoded array of lookups in Svelte layout. | If a lookup grows past 500 records, the compression threshold behaves incorrectly. | Move the compression threshold logic to the server side (let the download API report the configuration). |
| **TD-04** | API | OData upstream changes casings and parameters without notice. | Scrapers or API mirrors will break if schemas change. | Implement schema validation contracts (e.g., using Pydantic in sync scripts) to alert on schema changes before write. |
| **TD-05** | Database | Large transcript tables grow by millions of records. | SQL query latency on `$filter` and `$orderby` will slow down. | Partition the massive plenary and committee reports tables by year, and add indexes to JSONB query attributes. |
