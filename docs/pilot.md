# Phase 1 Pilot Strategy: "BICD Pilot Ingestion (2019–2024)"

This document outlines the execution plan, temporal scope, inclusion rules, and sequential step-by-step roadmap for the **Phase 1 Pilot Ingestion**, focused exclusively on the **British Isles & Crown Dependencies (BICD) Group**.

Full mapping blueprints, 3-tier data provenance rules, and the 4-phase project lifecycle are specified in [`docs/parliament_and_data_mapping.md`](file:///home/steven/Documents/github/comparativelegislativedata/docs/parliament_and_data_mapping.md).

---

## 1. Pilot Cohort Scope: The 8 BICD Assemblies

For the Phase 1 Pilot, ingestion and database mirroring are restricted strictly to the 8 assemblies of the **BICD Group**:

1. **UK Parliament (`GB-UKP`)** — Westminster Sovereign Bicameral.
2. **Scottish Parliament (`GB-SCT`)** — Devolved Unicameral.
3. **Senedd Cymru / Welsh Parliament (`GB-WLS`)** — Devolved Unicameral.
4. **Northern Ireland Assembly (`GB-NIR`)** — Devolved Assembly.
5. **Isle of Man Tynwald (`IM-TYN`)** — Crown Dependency Bicameral/Tricameral.
6. **States of Jersey (`JE-STJ`)** — Crown Dependency Non-Partisan Consensus.
7. **States of Guernsey (`GG-STG`)** — Crown Dependency Non-Partisan Consensus.
8. **Gibraltar Parliament (`GI-GIB`)** — Overseas Territory Parliament.

---

## 2. Standardised Temporal Scope: 2019-01-01 to 2024-12-31

To test the mirror pipeline on a clean, bounded 5-year cohort before post-pilot full historical backfilling, we enforce a **single, uniform calendar window across all 8 BICD assemblies**:

> **Pilot Window:** **2019-01-01 to 2024-12-31** (5 Full Calendar Years)

### Inclusion Criteria: Clean Complete Cohort
- **Included:** Bills both **INTRODUCED ($\ge \text{2019-01-01}$)** AND reached a **CONCLUSION ($\le \text{2024-12-31}$)**.
- **Definition of "Conclusion":** Reaching ANY terminal disposition (`ENACTED`, `DEFEATED`, `WITHDRAWN`, `LAPSED`).
- **Post-Pilot Note:** After the Phase 1 Pilot is completed and verified, **Phase 2 will backfill full historical digital archives** (e.g. 1997+ UK, 1999+ Scotland, etc.) and set up automated daily cron updates for the BICD group.

---

## 3. Dual-Layer Data Structure (`normalized.*` vs `native.*`)

Every record stored in our PostgreSQL database and served by our API is structured into three explicit blocks:

1. **`normalized.*` Block:** Standardised comparative fields (`title`, `initiator_type`, `final_status`, `duration_calendar_days`, `stage_milestones`) for cross-assembly queries.
2. **`native.*` Block:** Original assembly-specific fields (`local_bill_id`, `title_native`, `initiator_raw`, `raw_status`, `official_proceedings_url`, `official_publication_ref`).
3. **`provenance.*` Block:** Source URL, timestamp, raw payload hash, scraper version, and open data license.

---

## 4. Sequential Step-by-Step BICD Pilot Ingestion Roadmap

We will complete these steps sequentially, writing transparent documentation for each:

- `[x]` **Step 1: Core Engine & Canonical Model Setup**
  - Setup Python project structure (`backend/app/`).
  - Implement Pydantic v2 `Bill` canonical model matching [`docs/schema.md`](file:///home/steven/Documents/github/comparativelegislativedata/docs/schema.md).
  - Implement provenance hashing & audit logging engine.

- `[ ]` **Step 2: UK Parliament (`GB-UKP`) Ingestion & Mirroring**
  - Implement `bills-api.parliament.uk` client.
  - Ingest 2019–2024 introduced & concluded UK Bills; verify canonical output.

- `[ ]` **Step 3: Scottish Parliament (`GB-SCT`) Ingestion & Mirroring**
  - Implement Scottish Parliament open data client.
  - Ingest 2019–2024 introduced & concluded Scottish Bills; verify canonical output.

- `[ ]` **Step 4: Senedd Cymru (`GB-WLS`) Ingestion & Mirroring**
  - Implement Welsh Parliament data client; ingest 2019–2024 Bills.

- `[ ]` **Step 5: Northern Ireland Assembly (`GB-NIR`) Ingestion & Mirroring**
  - Implement NI Assembly data client; ingest 2019–2024 Bills.

- `[ ]` **Step 6: Crown Dependencies Ingestion & Mirroring (`IM-TYN`, `JE-STJ`, `GG-STG`, `GI-GIB`)**
  - Implement data clients for Isle of Man, Jersey, Guernsey, and Gibraltar.

- `[ ]` **Step 7: BICD Pilot Audit & Comparative Synthesis Report**
  - Stress-test schema resilience across all 8 BICD assemblies.
  - Publish initial comparative quantitative summary table (total volumes, passage rates, duration averages).

---

## Document Revision History

- **2026-07-22 (v1.1):** Refocused pilot scope exclusively on the 8 assemblies of the BICD Group for 2019–2024. Referenced `docs/parliament_and_data_mapping.md` for Phase 0 Global Audit.
- **2026-07-21 (v0.1):** Initial draft of pilot strategy.
