# Global Comparative Legislative Data Platform

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Specification: v2.8.0](https://img.shields.io/badge/Specification-v2.8.0-blue.svg)](docs/METHODOLOGY.md)
[![Pilot Assembly: Holyrood GB-SCT](https://img.shields.io/badge/Pilot-Scottish_Parliament_(GB--SCT)-emerald.svg)](institutions/GB-SCT/)

An open-science research platform and standardized data architecture for comparative legislative science. The platform provides a dual-layer data model (preserving native assembly payload fidelity while harmonizing a 119-variable canonical comparative schema) and an in-browser WebAssembly research environment.

---

## Key Academic Innovations

1. **Dual-Layer Architecture ("Riding Two Horses"):**
   * **Layer A (Native Assembly Layer):** 100% raw payload fidelity, native API endpoints, local terminology, and full debate text.
   * **Layer B (Canonical Comparative Layer):** 119 harmonized institutional research variables evaluated at specific decision-point dates ($T$).
2. **Strict Epistemological Provenance (7-Tier Spectrum):**
   * Clear separation between `NATIVE_DIRECT` host API keys, `DERIVED_DETERMINISTIC` rule-based joins, `DERIVED_EXTRACTED` document parsings, `DERIVED_SYNTHETIC_AI` probabilistic extractions, `LINKED_EXTERNAL_AUTHORITY` benchmarks (ParlGov, CAP, Wikidata), and `UNAVAILABLE_HARD_GAP` institutional omissions.
3. **Two-Pass Empirical Audit Methodology:**
   * **Pass 1 Baseline:** Zero-hallucination empirical ground truth sourced directly from native APIs and 100% deterministic temporal joins.
   * **Pass 2 Candidate Assessment:** Non-API variables carry explicit candidate specifications (`PROVISIONAL_HYPOTHESIS`) defining target source files, proposed parsing algorithms, and risk factors before empirical promotion.
4. **Proposed Interactive Data Playground (Multi-Studio Wasm Lab):**
   * Concept for a zero-install, in-browser computational laboratory powered by **DuckDB-Wasm** (analytical SQL engine) and **WebR** (R in WebAssembly).
   * Generates automatic **DA*RT-compliant replication code** (SQL/R/Python) and **LaTeX Stargazer regression tables**.
   * Integrates an **ORCID-authenticated crowdsourcing loop** allowing researchers to propose custom analytical views as peer-reviewed platform presets with academic credit attribution.

---

## Single-Assembly Pilot Workspace

The project is currently testing its infrastructure on an early pilot assembly:

* 🏛️ **[Scottish Parliament (Holyrood / `GB-SCT`) Workspace](institutions/GB-SCT/)**
  * **Historical Range:** Sessions 1–6 (May 1999 – Present)
  * **Pass 1 Empirical Baseline:** 72 Ground-Truth Variables (51 `NATIVE_DIRECT` + 21 `DERIVED_DETERMINISTIC`)
  * **Pass 2 Candidate Specifications:** 47 Candidate Specifications (`PROVISIONAL_HYPOTHESIS`)

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
│   └── PAPER_SERIES/              # Working Papers in Computational Legislative Science
│       └── WP01_interactive_data_playground_concept.md
│
├── institutions/                  # Institution-Specific Workspaces
│   └── GB-SCT/                    # Scottish Parliament Workspace
│       ├── README.md              # Holyrood Data Ecosystem & 27-Year Coverage
│       ├── AUDIT_BLUEPRINT.yaml   # Canonical Audit Blueprint
│       └── AUDIT_SUMMARY.md       # Empirical Provenance Matrix Report
│
├── etl/                           # Production Database Ingestion & Mirroring Pipeline
│   ├── mirrors/                   # Daily Mirror Scripts (Holyrood API -> Postgres)
│   └── validation/                # Schema Integrity & Payload Checkers
│
└── frontend/                      # Web Portal Source Code (SvelteKit)
```

---

## Academic Citation

If you use this data architecture or software in academic research, please cite:

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
