# Project Overview & Platform Vision (General)

This document outlines the core ambition, vision, scientific guidelines, and general integration roadmap of the **Global Comparative Legislative Data Platform**.

---

## 1. Ambition & Vision

The ambition of the platform is to create a high-integrity, academic-standard data portal mapping Bills and legislative processes across various national and regional assemblies.

Comparative legislative analysis has historically been obstructed by fragmented formats, changing terminology, and network limits of individual parliamentary OData or REST endpoints. By providing standardized, clean research databases alongside pristine raw mirrors, this platform enables researchers to query, analyze, and replicate legislative models across multiple parliaments.

---

## 2. Core Guardrails & Scientific Principles

To ensure the platform meets the strict replication standards of academic publications, all development complies with three absolute rules:

### A. Academic Integrity & Transparency Over Feature Speed
Empirical researchers require absolute repeatability and proof of data provenance. If documentation is lacking, or if variables contain undocumented heuristic cleaning, the data becomes scientifically useless. We prioritize detailed documentation, visual provenance badges, and clean database calculations above rapid feature deployment.

### B. The Repository as the Source of Truth
No architectural decisions, database schemas, or ETL mappings may reside solely in chat conversations or AI context. All active plans, schemas, and data normalizations must be committed as files in the repository.

### C. Scope Restriction (Tier 1 & Tier 2 Variables Only)
To eliminate data hallucination and ensure a deterministic baseline, the active database schemas and visual dashboards only expose:
1.  **`NATIVE_DIRECT` (Tier 1):** Unmodified data points served directly from the official assembly endpoints.
2.  **`DERIVED_DETERMINISTIC` (Tier 2):** Relational joins, temporal lookups, or date arithmetic computed via 100% rule-based database SQL views, with zero parsing ambiguity.

For variables requiring document extraction (Tier 3) or external linking (Tier 6), they remain officially marked as candidates until extraction code has been verified and benchmarked against ground truth.

---

## 3. General Assembly Integration Roadmap

Every assembly integrated into the platform follows a structured, staged roadmap:
*   **Stage 1 (Raw Proxy):** Connecting to upstream OData/REST endpoints and establishing a CORS-unlocked passthrough server proxy.
*   **Stage 2 (Database Mirror):** Building a local relational database replica on the server, running daily syncs, and verifying data parity with the upstream API.
*   **Stage 3 (Canonical Compilation):** Mounting raw replicas via PostgreSQL Foreign Data Wrappers (FDW), compiling derived research tables via SQL view scripts, and exporting portable datasets (Parquet, SQLite, CSV).
*   **Stage 4 (Visual Dashboard):** Constructing interactive charts, KPI counters, and sessional volume summaries.
*   **Stage 5 (Regression Playground):** Deploying statistical modeling tools (OLS and Logistic regressions) to analyze sessional speed-up hypotheses.

For individual assembly schemas, custom dates, and checklists, refer to the assembly-specific overview directories:
*   [Scottish Parliament (GB-SCT) Project Overview](file:///home/steven/Documents/github/comparativelegislativedata/docs/gb-sct/PROJECT_OVERVIEW.md)
