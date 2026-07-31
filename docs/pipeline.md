# Data Ingestion & Multi-Format Export Pipeline (General)

This document describes the core design, execution, validation, and automation architecture of the data ingestion and export pipelines implemented in this repository. These standards apply to all integrated legislative sync modules.

---

## 1. General Ingestion Architecture

Ingestion scripts synchronize live upstream APIs to local PostgreSQL databases using several optimization and security layers:

### 1.1 Upsert Strategy (`ON CONFLICT`)
To prevent duplicate records or key conflicts during repeated runs, ingestion runs execute upsert SQL patterns mapping raw data objects safely:
```sql
INSERT INTO raw_table (id, name, updated) 
VALUES (%s, %s, %s) 
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name, updated = EXCLUDED.updated;
```

### 1.2 Performance Batching
To optimize network communication with the database server, writes are executed in batches of `200` records using psycopg's bulk insertion driver:
```python
cursor.executemany(upsert_query, params_list)
```
This batching yields a significant speedup over standard single-insert loops, maximizing transaction throughput.

### 1.3 Defensive Type Normalization
*   **Empty strings:** Incoming empty strings (`""`) or unpopulated keys are normalized to database `NULL` representations.
*   **Defensive Type Checks:** Feeds containing malformed data streams are checked defensively at the ingest loop level to prevent crashes on high-volume runs.

---

## 2. Parity Validation Auditing (Concept)

To guarantee database replication integrity, the platform utilizes an automated **Parity Validation Engine**:
1.  **Random Sampling:** Selects a randomized sample of records (typically 3) from each raw mirror table.
2.  **API Verification:** Queries the upstream REST/OData API endpoint for the exact primary key of the sample.
3.  **Field-by-Field Check:** Executes a deep assertion check comparing every database column against the upstream JSON payload (verifying dates, string matches, booleans, and JSONB structures).
4.  **Enforcement Gate:** Confirms complete alignment between the Postgres mirror database and the live API before any canonical exports are compiled.

---

## 3. Multi-Format Exporters & Compression Standard

We provide bulk downloads in three formats (CSV, Parquet, and SQLite) to support diverse statistical environments.

### 3.1 The 500-Row Plain CSV Rule
To balance download performance against macOS/Windows spreadsheet compatibility:
*   **Uncompressed CSV (`.csv`):** Datasets containing **fewer than 500 records** (e.g. index tables, lookup taxonomies) are exported as raw, plain CSV files.
    *   *Rationale:* Extremely small files (under ~200 bytes) are sometimes misidentified by macOS's native Archive Utility (`libarchive`) as `mtree` files, causing extraction errors. Keeping small datasets uncompressed eliminates this issue and allows instant double-click opening in spreadsheet software (Excel, Numbers).
*   **Compressed Gzip CSV (`.csv.gz`):** Datasets containing **500 or more records** are compressed using `gzip`.
    *   *Rationale:* Conserves server storage and download bandwidth, while remaining natively readable by statistical toolchains (e.g. pandas `read_csv` or R's `readr` stream directly over HTTP).

### 3.2 Streaming PyArrow (Parquet)
*   **Method:** Streams postgres queries directly to Snappy-compressed Apache Parquet format in chunks of `50,000` rows using PyArrow.
*   **RAM Safety:** Ensures memory footprint remains extremely low (under 60 MB) even during high-volume exports of millions of records.

### 3.3 Portable SQLite Compiler
*   **Method:** Compiles a pre-indexed, standalone SQLite database.
*   **Design:** Configures WAL journaling for compilation speed, builds database indexes on primary key IDs, and compresses the final database using Gzip.
*   **Researchers Value:** Serves as a local "database-in-a-box," allowing researchers to query and join the entire dataset collection without setting up a database server.
