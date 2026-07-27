# Implementation Plan: Phase 2 — Database Ingestion & Mirroring (ELT)

This document establishes the architecture, database schema design, and ingestion strategies for mirroring raw Scottish Parliament (`GB-SCT`) OData feeds into our local PostgreSQL database on the VPS.

## Core Guardrails & Findings
1.  **Repository as Source of Truth:** Table schemas, foreign keys, and script designs are fully declared in this plan inside the repository.
2.  **Strict 1:1 Mirroring (Layer A):** Relational tables will map exactly to the OData fields discovered in Phase 1. No custom column cleaning or transformation is allowed in this layer.
3.  **Solving the broken `$skip` Pagination:**
    *   **Static/Lookup Tables:** Fetched completely in a single pass (total records < 100).
    *   **Yearly Split Tables:** Transcripts and votes (`votesmotion`, `orsplenarymeeting`, `orscommitteemeeting`) will be synced in loops filtering by year (`?year=YYYY`) from 1999 to the current year.
    *   **High-Volume Keyset Pagination:** High-volume endpoints like `motionsquestionsanswersmotions` will paginate using OData `$filter` on keysets (`$filter=UniqueID gt LAST_SEEN_ID&$orderby=UniqueID`) instead of `$skip` to eliminate infinite loop risk.

---

## 1. Database Schema Design (Layer A)

All tables will use the prefix `raw_gb_sct_` to separate raw data from subsequent canonical views (Layer B).

### Core Lookup Tables

```sql
CREATE TABLE raw_gb_sct_billtypes (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE raw_gb_sct_billstagetypes (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    bill_type_id INT,
    sequence INT
);

CREATE TABLE raw_gb_sct_parties (
    id INT PRIMARY KEY,
    abbreviation VARCHAR(50),
    actual_name VARCHAR(255),
    preferred_name VARCHAR(255),
    notes TEXT,
    valid_from_date TIMESTAMP,
    valid_until_date TIMESTAMP
);

CREATE TABLE raw_gb_sct_committeeroles (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    notes TEXT
);

CREATE TABLE raw_gb_sct_committeetypes (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
```

### Main Relational Tables

```sql
CREATE TABLE raw_gb_sct_bills (
    id INT PRIMARY KEY,
    reference VARCHAR(100),
    short_name VARCHAR(255),
    full_name TEXT,
    bill_type_id INT,
    person_id INT,
    third_party_organisation TEXT
);

CREATE TABLE raw_gb_sct_billstages (
    id INT PRIMARY KEY,
    bill_id INT REFERENCES raw_gb_sct_bills(id),
    bill_stage_type_id INT REFERENCES raw_gb_sct_billstagetypes(id),
    stage_date TIMESTAMP
);

CREATE TABLE raw_gb_sct_members (
    person_id INT PRIMARY KEY,
    photo_url TEXT,
    notes TEXT,
    birth_date TIMESTAMP,
    birth_date_is_protected BOOLEAN,
    parliamentary_name VARCHAR(255),
    preferred_name VARCHAR(255),
    gender_type_id INT,
    is_current BOOLEAN
);

CREATE TABLE raw_gb_sct_memberparties (
    id INT PRIMARY KEY,
    person_id INT REFERENCES raw_gb_sct_members(person_id),
    party_id INT REFERENCES raw_gb_sct_parties(id),
    valid_from_date TIMESTAMP,
    valid_until_date TIMESTAMP
);

CREATE TABLE raw_gb_sct_committees (
    id INT PRIMARY KEY,
    short_name VARCHAR(100),
    name VARCHAR(255),
    description TEXT,
    committee_email_address VARCHAR(255),
    committee_telephone VARCHAR(100),
    valid_from_date TIMESTAMP,
    valid_until_date TIMESTAMP
);

CREATE TABLE raw_gb_sct_personcommitteeroles (
    id INT PRIMARY KEY,
    person_id INT REFERENCES raw_gb_sct_members(person_id),
    committee_role_id INT REFERENCES raw_gb_sct_committeeroles(id),
    committee_id INT REFERENCES raw_gb_sct_committees(id),
    valid_from_date TIMESTAMP,
    valid_until_date TIMESTAMP,
    notes TEXT
);
```

### Complex / Document-Oriented Tables (Nested JSONB)

For Votes and Hansard Transcripts, we preserve structural fidelity by loading nested JSON dictionaries directly into PostgreSQL `JSONB` fields.

```sql
CREATE TABLE raw_gb_sct_motions (
    unique_id INT PRIMARY KEY,
    event_id VARCHAR(100),
    event_type_id INT,
    event_sub_type_id INT,
    msp_id INT,
    party VARCHAR(100),
    region_id INT,
    constituency_id INT,
    approved_date TIMESTAMP,
    submission_date_time TIMESTAMP,
    title VARCHAR(255),
    item_text TEXT
);

CREATE TABLE raw_gb_sct_votes (
    id VARCHAR(100) PRIMARY KEY,
    detail JSONB NOT NULL,
    motion JSONB NOT NULL,
    person JSONB NOT NULL,
    time JSONB NOT NULL,
    updated_elastic_date TIMESTAMP
);

CREATE TABLE raw_gb_sct_plenary_reports (
    id VARCHAR(100) PRIMARY KEY,
    meeting JSONB NOT NULL,
    committee JSONB NOT NULL,
    time JSONB NOT NULL,
    item_of_business JSONB NOT NULL,
    person JSONB NOT NULL,
    detail JSONB NOT NULL,
    updated_elastic_date TIMESTAMP
);

CREATE TABLE raw_gb_sct_committee_reports (
    id VARCHAR(100) PRIMARY KEY,
    record_type VARCHAR(100),
    sub_type VARCHAR(100),
    meeting JSONB NOT NULL,
    committee JSONB NOT NULL,
    time JSONB NOT NULL,
    item_of_business JSONB NOT NULL,
    person JSONB NOT NULL,
    detail JSONB NOT NULL,
    location JSONB,
    updated_date TIMESTAMP,
    updated_elastic_date TIMESTAMP
);
```

---

## 2. Ingestion & ELT Pipeline Engine

### Ingestion Script Design (`scripts/sync_gb_sct.py`)
A single, resilient Python script managed via systemd timer/cron.

- **Idempotency:** Uses `INSERT ... ON CONFLICT (id) DO UPDATE` to allow safe, repeated runs without duplicating records.
- **Keyset Pagination Strategy:**
  For high-volume tables:
  ```python
  # Pseudo-code logic for Keyset pagination
  last_id = get_max_id_from_local_db()
  while True:
      url = f"https://data.parliament.scot/api/motionsquestionsanswersmotions?$filter=UniqueID gt {last_id}&$orderby=UniqueID&$top=500"
      records = fetch_json(url)
      if not records:
          break
      upsert_to_db(records)
      last_id = records[-1]['UniqueID']
  ```
- **Yearly Partition loop:**
  For `votesmotion`, `orsplenarymeeting`, and `orscommitteemeeting`:
  ```python
  for year in range(1999, datetime.now().year + 1):
      url = f"https://data.parliament.scot/api/{endpoint}?year={year}"
      records = fetch_json(url)
      upsert_to_db(records)
  ```

---

## 3. Reconciliation & Parity Auditing

To guarantee 100% academic parity, every sync task executes a reconciliation audit:

1.  **Count Checks:** Query total rows in the local database vs. estimated records on the host.
2.  **Completeness Audit:** Ensure there are no numerical gaps in contiguous sequential IDs.
3.  **Synchronization Log (`raw_gb_sct_sync_logs`):**
    ```sql
    CREATE TABLE raw_gb_sct_sync_logs (
        id SERIAL PRIMARY KEY,
        sync_time TIMESTAMP DEFAULT NOW(),
        endpoint_name VARCHAR(100) NOT NULL,
        records_fetched INT,
        reconciliation_status VARCHAR(50), -- 'PARITY_MATCH', 'GAP_DETECTED', 'SYNC_FAIL'
        error_message TEXT
    );
    ```

---

## 4. Verification Plan

### Automated Database Tests
*   **Audit Script:** Write `tests/test_reconciliation.py` to compare OData endpoints against our database counts and log any mismatched IDs.
*   **Index Checks:** Verify that indices exist on all join columns (`person_id`, `bill_id`, `party_id`) to ensure fast querying.
*   **Build & Deployment checks:** Run type checking on SvelteKit components connecting to the local database.
