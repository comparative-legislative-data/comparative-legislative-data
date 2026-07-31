# Repository System Architecture Specification (General)

This document provides a comprehensive, complete, and accurate description of the **Global Comparative Legislative Data Platform** core system architecture. These specifications apply universally to all integrated legislative nodes.

---

## 1. System Architecture Overview

To ensure raw data integrity and prevent custom derived calculations from contaminating the upstream replica data, the system separates all operations into two logically and physically isolated database layers.

```
                   [ Upstream Assembly APIs ]
                               |
                               v
               +-------------------------------+
               |  Database A: Raw Mirror DB    |
               |  (Pristine Raw Data Mirrors)  |
               +-------------------------------+
                               |
               (Read-Only PostgreSQL FDW Link)
                               |
                               v
               +-------------------------------+
               |   Database B: Canonical DB    |
               | (Calculated Tiers & codebook) |
               +-------------------------------+
                               |
                  (SvelteKit API Route Pools)
                               |
                               v
                 [ Frontend Research Hub ]
```

---

## 2. PostgreSQL Dual-Database Isolation

PostgreSQL hosts two distinct databases running on the same cluster instance (Port `5432`):

### 2.1 Database A: Raw Mirror Database (`comparative_legislative_data`)
*   **Role:** Holds pristine 1:1 replicas of the upstream legislative feeds.
*   **Data Constraints:** Contains **0% derived fields, custom columns, or computed views**. The database remains clean of any custom analysis logic.
*   **Write Operations:** Permitted only via automated, raw data synchronization/ingestion scripts.

### 2.2 Database B: Canonical Research Database (`comparative_legislative_data_canonical`)
*   **Role:** Houses the physical research datasets and performs all analytical calculations.
*   **Foreign Data Wrapper Link:** Mounts Database A's raw tables as read-only virtual tables inside Database B under a **`raw_mirror`** schema using PostgreSQL's native `postgres_fdw` extension.
*   **Isolation Benefits:** Completely separates derived research calculations from the raw database. Even a catastrophic schema failure or SQL compilation issue on Database B can never corrupt the raw Database A mirrors.

---

## 3. The 500-Row Plain CSV Compression Rule

To optimize server bandwidth and client-side usability, the bulk exports pipeline implements a strict file compression threshold:
*   **Threshold:** If a compiled canonical research table contains **500 rows or fewer** (e.g. general bills indexes), it is exported as a **plain, uncompressed CSV**. This ensures immediate accessibility in standard spreadsheet software (Excel, Numbers) on macOS and Windows without archive extraction utility bugs.
*   **Compression:** If a research table exceeds **500 rows** (e.g. member party histories, individual vote records), it is compressed and exported as a **Gzipped CSV** (`.csv.gz`) to conserve VPS storage and network bandwidth.
*   **Standard Formats:** SQLite databases are gzipped, and parquet files are stored natively as binary parquets.

---

## 4. SvelteKit Web Stack & Database Pool Isolation

The SvelteKit server separates database connections at the Node.js pool level:
*   **`Pool A` (`db.ts`):** Connects exclusively to Database A, serving OData raw requests from mirror tables.
*   **`Pool B` (`canonicalDb.ts`):** Connects exclusively to Database B, serving canonical OData previews and research charts.

This database pool separation ensures that the frontend API endpoints can never mix mirror replica data and canonical variables.

---

## 5. Daily Sync and Compile Automation

Every night, the VPS crontab runs a daily sync shell script that executes the following coordinate sequence:
1.  **Ingestion Pass:** Runs the raw ingest python script to fetch any upstream API updates into Database A.
2.  **Raw Export Pass:** Rebuilds the raw mirror SQLite databases, Parquet, and CSV archives from Database A.
3.  **Compilation Pass:** Executes Database B's SQL view compiler, updating the FDW views and inserting normalized rows into Database B's physical tables.
4.  **Canonical Export Pass:** Rebuilds the canonical SQLite databases, Parquet, and CSV archives from Database B.

This sequence guarantees that Database A mirrors are fully up to date before any Database B canonical views compile their derived parameters.
