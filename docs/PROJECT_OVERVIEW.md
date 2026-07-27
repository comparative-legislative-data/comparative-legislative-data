# Project Overview: Comparative Legislative Data Platform

## 1. Ambition & Vision

The ambition of the **Global Comparative Legislative Data Platform** is to create a high-integrity, academic-standard data portal mapping Bills and legislative processes across various national and regional assemblies.

Our primary pilot case-study is the **Scottish Parliament (Holyrood / `GB-SCT`)**, leveraging deep doctoral and professional-level understanding of its legislative systems. The Scottish Parliament pilot will establish a clean, reusable blueprint/template that can be adapted for other parliaments, accounting for structural variations in datasets, political procedures, and OData endpoints.

---

## 2. Core Guardrails & Scientific Principles

To prevent data dilution, duplication, and AI hallucinations, we operate under three absolute rules:

### A. Academic Integrity & Transparency Over Speed
Academics require absolute repeatability and empirical proof. If documentation is lacking, or if variables contain probabilistic guesses, researchers will abandon the platform. We value precision and clear documentation of limitations above fast feature delivery.

### B. The Repository as the Source of Truth
No planning, database schema architecture, or data mappings will live solely in conversational memory or AI context. All active plans, system specifications, database schemas, and transformation rulebooks must be fully documented as files in this repository (e.g., in `/docs` and specific pilot subfolders).

### C. Scope Restriction: Tier 1 & Tier 2 Data Only
During this initial build phase, the database, API, and frontend will **only** surface:
1.  **`NATIVE_DIRECT` (Tier 1):** Unmodified data points served directly from the official assembly endpoints.
2.  **`DERIVED_DETERMINISTIC` (Tier 2):** Relational joins or arithmetic calculations computed via 100% rule-based database queries/views, with zero parsing ambiguity.

All probabilistic, document-scraped, or external authority data classes (Tiers 3 to 7) are deferred to future stages.

---

## 3. Phased Roadmap (Scottish Parliament Pilot)

The pilot will be executed in five distinct, serial phases. Each phase requires a dedicated, repository-controlled implementation plan before code execution begins:

### Phase 1: Proxied Access & Academic Documentation
- **Objective:** Map and connect to every relevant Scottish Parliament API containing data useful for analyzing the Bill lifecycle.
- **Components:**
  - Build a clean CORS-bypass passthrough server proxy.
  - Implement a SvelteKit explorer UI that displays raw API payloads.
  - Render actual, deterministically-extracted schemas (rather than hardcoded assumptions) alongside academic codebooks describing each endpoint's parameters, anomalies, and performance constraints.

### Phase 2: In-Memory / Database Mirroring (ELT)
- **Objective:** Build a resilient, high-performance local database mirror on the VPS to backfill raw data.
- **Components:**
  - Setup raw relational tables mapped exactly to the verified schemas from Phase 1.
  - Write idempotent ingestion scripts with exponential backoff and loop-detection to resolve OData pagination quirks.
  - Run automated count-based and hash-based reconciliation audits to guarantee 100% data parity between the VPS database and the live host.

### Phase 3: Derived & Canonical Variables (Standardization & Export)
- **Objective:** Synthesize variables of academic interest (e.g., sponsor party alignment, bill durations, outcomes) and provide multi-format downloads.
- **Components:**
  - Write deterministic SQL views to compute Tier 2 comparative variables.
  - Implement export pipelines for standard research formats: **CSV**, **JSON**, **Apache Parquet**, and **R Data Frame (`.rds`)**.
  - Embed copy-pasteable direct download code generators for **cURL**, **R**, **Python**, and **Stata**.

### Phase 4: Example Visualizations
- **Objective:** Design static, highly polished visual representations of the processed dataset.
- **Components:**
  - Render custom visual charts (e.g., timeline progressions, density curves of passage durations, and sponsor-party mappings) to showcase the analytical power of the clean baseline data.

### Phase 5: The Interactive Data Playground
- **Objective:** Embed a client-side visualization sandbox.
- **Components:**
  - Build UI tools allowing researchers to dynamically group, filter, and cross-tabulate variables to generate custom charts and download customized subsets without leaving the application.
