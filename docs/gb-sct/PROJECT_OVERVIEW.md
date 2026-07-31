# Project Overview & Case Study: Scottish Parliament (GB-SCT)

This document provides assembly-specific roadmap phases and case-study context for the Scottish Parliament (`gb-sct`) implementation. For core project guidelines and variables scope restrictions, see the [Core Project Overview & Platform Vision](file:///home/steven/Documents/github/comparativelegislativedata/docs/PROJECT_OVERVIEW.md).

---

## 1. Why the Scottish Parliament (`GB-SCT`)?

The Scottish Parliament (Holyrood) serves as our primary case study and pilot assembly because:
1.  **OData Maturity:** Holyrood publishes an extensive, open, and well-structured OData v4 API (`data.parliament.scot/api`).
2.  **Dataset Complexity:** The database tracks bills, events, members, and voting records across six distinct legislative terms (1999–present), capturing a wide variety of bill types (Government, Member's, Private, Committee, Hybrid).
3.  **Governance Variations:** Over its 25-year history, Scotland has transitioned through diverse coalition formats (Labour-LibDem coalitions, SNP majorities, SNP minorities, and the SNP-Green agreement), providing a rich testing ground for temporal governing status checks.

---

## 2. Five-Phase Implementation Roadmap

The Scottish Parliament pilot is executed across five structured phases:

### Phase 1: Proxied Access & Academic Documentation (Completed)
*   **Objectives:** Connect to upstream APIs and build a SvelteKit explorer UI.
*   **Components:**
    *   CORS-bypass server proxy.
    *   Raw OData explorer displaying records and upstream schemas in Svelte.
    *   Clickable variables codebook linking schemas to academic definitions.

### Phase 2: In-Memory / Database Mirroring (Completed)
*   **Objectives:** Replicate raw OData tables to a local PostgreSQL Database A mirror on `chessserver`.
*   **Components:**
    *   Idempotent sync script `sync_gb_sct.py` with performance batching (200 rows).
    *   Parity validation auditing script `audit_gb_sct_parity.py` using random key sampling.

### Phase 3: Derived & Canonical Variables (Completed)
*   **Objectives:** Compile derived research variables (durations, outcomes, coalitions) in Database B and provide multi-format downloads.
*   **Components:**
    *   Database B (`comparative_legislative_data_canonical`) with read-only FDW links to Database A.
    *   SQL view script `compile_canonical_layer.sql` executing duration and temporal coalition arithmetic.
    *   Bulk exporter `export_canonical.py` generating SQLite, Parquet, and CSV files (complying with the 500-row plain CSV compression rule).

### Phase 4: Example Visualizations (Active Phase)
*   **Objectives:** Create static, polished visual charts of the sessional bill volume, success rates, and party shares at `/pilot/gb-sct/charts`.
*   **Components:**
    *   Visual SVG stacked bar chart splitting sessional volumes into Passed vs. Fallen/Withdrawn with 1px gaps.
    *   Interactive hover overlays showing exact counts.
    *   Party success progress bars isolating Law Officers (ID 99) and Private Promoters (ID 98) from Independent MSPs.

### Phase 5: Client-Side Regression Playground (Next Phase)
*   **Objectives:** Embed a client-side visualization sandbox and regression analytics panels.
*   **Components:**
    *   Dynamic filtering tool allowing custom subsets.
    *   Linear (OLS) and Logistic regression calculator modules predicting passage speeds and success rates.
