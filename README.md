# Global Comparative Legislative Data Platform

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Specification: v2.8.0](https://img.shields.io/badge/Specification-v2.8.0-blue.svg)](docs/METHODOLOGY.md)
[![Pilot Assembly: Holyrood GB-SCT](https://img.shields.io/badge/Pilot-Scottish_Parliament_(GB--SCT)-emerald.svg)](frontend/src/routes/pilot/gb-sct/)

An open-science research platform, 1:1 database mirror, and standardized data architecture for comparative legislative science. The platform provides a dual-layer data model (preserving native assembly payload fidelity while harmonizing a 119-variable canonical comparative schema), automated 1:1 host parity reconciliation, and versioned REST/JSON APIs.

---

## Key Academic Innovations

1. **Dual-Layer Architecture ("Riding Two Horses"):**
   * **Layer A (Native Assembly Layer):** 100% raw payload fidelity, native API endpoints, local terminology, and full debate text (2,678,613 raw records mirrored).
   * **Layer B (Canonical Comparative Layer):** 119 harmonized institutional research variables evaluated at specific decision-point dates ($T$).
2. **Automated 1:1 Host Parity Reconciliation Engine:**
   * Continuous record count, key-value, and SHA-256 checksum matching comparing live host API endpoints vs. platform database mirrors. Verified **100.0% Exact Match (0 Discrepancies)**.
3. **Multi-Format Data Delivery & Pre-Indexed Relational SQLite DB:**
   * High-speed REST APIs (`/api/v2/mirror/gb-sct/...`) and bulk downloads in **CSV.GZ**, **Apache Parquet**, and a **Portable SQLite database-in-a-box** containing all tables and indexes precompiled for local joining.
   * Ready-to-run code generators for **cURL**, **R**, and **Python** inside the web inspector.

---

## Institutional Explorer Workspaces

The project is currently running its production pipeline on the pilot assembly:

* 🏛️ **[Scottish Parliament (Holyrood / `GB-SCT`) Explorer](frontend/src/routes/pilot/gb-sct/)**
  * **Historical Range:** Sessions 1–6 (May 1999 – Present)
  * **Ingested Raw Records:** 2,678,613 Records across 15 Open Data Endpoints
  * **Host Parity Status:** `100.0% EXACT MATCH VERIFIED` ([Parity Audit Code](scripts/audit_gb_sct_parity.py))

---

## Directory Structure

```
comparativelegislativedata/
├── README.md                      # Academic Project Overview & Baseline
├── CITATION.cff                   # Standard Academic Citation Metadata
├── LICENSE                        # Open Science License (CC-BY-4.0 / MIT)
│
├── docs/                          # Core Scientific Specifications & Manuals
│   ├── METHODOLOGY.md             # Dual-Layer Architecture & 7-Tier Spectrum
│   ├── PROJECT_OVERVIEW.md        # Institutional Mapping Overview
│   ├── api.md                     # [NEW] REST API Endpoints & Query Specs
│   ├── pipeline.md                # [NEW] Ingest Pipeline, Normalization, & Formats
│   ├── ops.md                     # VPS Operations, Systemd Services, & Cron Jobs
│   └── AUTH_SCHEMA.md             # Platform Authentication Model
│
├── scripts/                       # Database Sync, Audits, & Multi-Format Exporters
│   ├── sync_gb_sct.py             # Keyset-Resuming DB Scraper & Upsert Engine
│   ├── audit_gb_sct_parity.py     # Random Sample Parity Auditor
│   ├── export_multi_formats.py    # PyArrow Streaming Parquet & SQLite Compiler
│   ├── cron_daily_sync.sh         # Bash Cron Sync Wrapper (daily at 3:00 AM)
│   └── schema_phase2.sql          # PostgreSQL DDL Schemas
│
├── backend/                       # Independent Test Suite
│   └── tests/                     # Academic Reproducibility Test Suite
│
└── frontend/                      # Web Portal Source Code (SvelteKit)
    ├── src/
    │   ├── routes/
    │   │   ├── api/v2/mirror/     # Optimized DB-backed OData Mirror Endpoints
    │   │   ├── api/v2/proxy/      # Live Upstream OData Relay Proxies
    │   │   ├── downloads/         # Raw Binary File Streaming Endpoints
    │   │   └── pilot/gb-sct/      # Interactive Explorer Dashboard
    │   └── lib/components/        # Inspector Modals & Code Generators
    └── static/                    # Frontend Web Assets
```

---

## Documentation Quick Links

*   **API Reference Manual:** [`docs/api.md`](docs/api.md) — Reference for Proxy/Mirror endpoints and OData query syntax.
*   **Ingest Pipeline Manual:** [`docs/pipeline.md`](docs/pipeline.md) — Technical details on PostgreSQL upserts, type-safe casting normalizations, Parquet writers, and SQLite compilers.
*   **VPS Operations Manual:** [`docs/ops.md`](docs/ops.md) — Reference for systemd services, postgres database operations, and daily cron schedules.
