# Global Comparative Legislative Data Platform

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Specification: v2.8.0](https://img.shields.io/badge/Specification-v2.8.0-blue.svg)](docs/METHODOLOGY.md)
[![Pilot Assembly: Holyrood GB-SCT](https://img.shields.io/badge/Pilot-Scottish_Parliament_(GB--SCT)-emerald.svg)](institutions/GB-SCT/)
[![Parity Verification: 100%](https://img.shields.io/badge/Host_Parity-100.0%25_Verified-emerald.svg)](institutions/GB-SCT/PARITY_REPORT.md)

An open-science research platform, 1:1 database mirror, and standardized data architecture for comparative legislative science. The platform provides a dual-layer data model (preserving native assembly payload fidelity while harmonizing a 119-variable canonical comparative schema), automated 1:1 host parity reconciliation, and versioned REST/JSON APIs.

---

## Key Academic Innovations

1. **Dual-Layer Architecture ("Riding Two Horses"):**
   * **Layer A (Native Assembly Layer):** 100% raw payload fidelity, native API endpoints, local terminology, and full debate text (102,317 raw records mirrored).
   * **Layer B (Canonical Comparative Layer):** 119 harmonized institutional research variables evaluated at specific decision-point dates ($T$).
2. **Automated 1:1 Host Parity Reconciliation Engine:**
   * Continuous record count, key-value, and SHA-256 checksum matching comparing live host API endpoints vs. platform database mirrors. Verified **100.0% Exact Match (0 Discrepancies)**.
3. **Strict Epistemological Provenance (7-Tier Spectrum):**
   * Clear separation between `NATIVE_DIRECT` host API keys, `DERIVED_DETERMINISTIC` rule-based joins, `DERIVED_EXTRACTED` document parsings, `DERIVED_SYNTHETIC_AI` probabilistic extractions, `LINKED_EXTERNAL_AUTHORITY` benchmarks (ParlGov, CAP, Wikidata), and `UNAVAILABLE_HARD_GAP` institutional omissions.
4. **Multi-Format Data Delivery & Versioned REST APIs:**
   * High-speed REST APIs (`/api/v1/GB-SCT/canonical/bills`) and bulk research downloads in **CSV**, **JSON**, **Apache Parquet**, and **R Data Frame (`.rds`)** formats.
   * 4-Language ready-to-run code generators for **cURL**, **R**, **Python**, and **Stata**.

---

## Single-Assembly Pilot Workspace

The project is currently running its production pipeline on an early pilot assembly:

* 🏛️ **[Scottish Parliament (Holyrood / `GB-SCT`) Workspace](institutions/GB-SCT/)**
  * **Historical Range:** Sessions 1–6 (May 1999 – Present)
  * **Ingested Raw Records:** 102,317 Records across 13 Open Data Endpoints
  * **Pass 1 Empirical Baseline:** 72 Ground-Truth Variables (51 `NATIVE_DIRECT` + 21 `DERIVED_DETERMINISTIC`) across 473 Bills
  * **Host Parity Status:** `100.0% EXACT MATCH VERIFIED` ([Audit Report](institutions/GB-SCT/PARITY_REPORT.md))

---

## Production REST APIs

| Endpoint | Method | Description | Sample Output |
| :--- | :--- | :--- | :--- |
| `/api/v1/GB-SCT/health` | GET | Real-time health status, sync timestamp, & parity audit | `{"parity_verification": "100.0% EXACT MATCH"}` |
| `/api/v1/GB-SCT/canonical/bills` | GET | 72 Pass 1 canonical variables for 473 bills | `{"total_records": 473, "data": [...]}` |
| `/static/data/GB-SCT_canonical_bills.csv` | DOWNLOAD | Complete CSV dataset package | Standardized CSV Data Table |
| `/static/data/GB-SCT_canonical_bills.parquet` | DOWNLOAD | Compressed Parquet columnar dataset | Binary Parquet File |

---

## Directory Structure

```
comparativelegislativedata/
├── README.md                      # Academic Project Overview & Baseline
├── CITATION.cff                   # Standard Academic Citation Metadata (BibTeX/Zotero)
├── LICENSE                        # Open Science License (CC-BY-4.0 / MIT)
│
├── docs/                          # Core Scientific Specifications & Working Papers
│   ├── METHODOLOGY.md             # Dual-Layer Architecture & 7-Tier Spectrum
│   ├── ARCHITECTURE.md            # System Architecture & Database Mirroring Spec
│   ├── CANONICAL_CATALOG.md       # Master 119-Variable Institutional Catalog
│   ├── TECHNICAL_DEBT.md          # Technical Debt Log & Infrastructure Backlog
│   └── PAPER_SERIES/              # Working Papers in Computational Legislative Science
│       └── WP01_interactive_data_playground_concept.md
│
├── institutions/                  # Institution-Specific Workspaces
│   └── GB-SCT/                    # Scottish Parliament Workspace
│       ├── README.md              # Holyrood Data Ecosystem & 27-Year Coverage
│       ├── API_CATALOG.md         # Endpoint Codebook (13 Native Endpoints)
│       ├── TRANSFORMATION_RULES.md# Derivation Rules for 21 Derived Variables
│       ├── MISSINGNESS_MATRIX.md  # Empirical Missingness Percentages
│       ├── PARITY_REPORT.md       # Live 100% Host Parity Audit Report
│       ├── AUDIT_BLUEPRINT.yaml   # Canonical Audit Blueprint
│       └── AUDIT_SUMMARY.md       # Empirical Provenance Matrix Report
│
├── etl/                           # Production Database Ingestion & Mirroring Pipeline
│   ├── mirrors/                   # Daily Mirror Scripts (Holyrood API -> Postgres/SQLite)
│   │   ├── fetch_holyrood_raw.py  # Ingestion Engine (102,317 Raw Records)
│   │   ├── compute_deterministic.py # Deterministic Transformer Engine
│   │   └── export_formats.py      # Multi-Format Exporter (CSV, JSON, Parquet, RDS)
│   └── validation/                # 1:1 Parity Reconciliation Engine
│       └── reconcile_parity.py    # 1:1 Host Parity Reconciler
│
├── backend/                       # Independent Test Suite
│   └── tests/                     # Academic Reproducibility Test Suite
│       └── test_parity_reproducibility.py
│
└── frontend/                      # Web Portal Source Code (SvelteKit)
```

---

## Technical Debt & Infrastructure Backlog

Tracked in **[`docs/TECHNICAL_DEBT.md`](docs/TECHNICAL_DEBT.md)**:
1. *Global CDN Edge Delivery Proxying (Cloudflare / Fastly)*
2. *Automated Zenodo Archival DOI Publishing*
3. *Shinylive / WebR Wasm Package Bundling*

---

## Academic Citation

If you use this data architecture, database mirror, or software in academic research, please cite:

```bibtex
@software{comparative_legislative_data_2026,
  author = {Comparative Legislative Data Project},
  title = {Global Parliamentary Data Platform & Dual-Layer Legislative Architecture},
  version = {2.8.0},
  year = {2026},
  url = {https://legislativedata.org},
  publisher = {Comparative Legislative Data Project}
}
```

For full citation guidelines, see **[`CITATION.cff`](CITATION.cff)**.
