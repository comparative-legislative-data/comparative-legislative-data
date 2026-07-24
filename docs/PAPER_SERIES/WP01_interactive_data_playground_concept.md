# Working Paper 01: The Interactive Legislative Data Playground & Multi-Studio Architecture

**Author:** Comparative Legislative Data Project  
**Series:** Working Papers in Computational Legislative Science (WP01-2026)  
**Date:** July 2026  
**URL:** `https://legislativedata.org/docs/PAPER_SERIES/WP01_interactive_data_playground_concept.md`

---

## Abstract

Traditional comparative political science data platforms (e.g., V-Dem, ParlGov, Comparative Agendas Project) follow a static **"Download and Leave"** paradigm, forcing researchers to download flat files and configure local software environments offline. This paper introduces the **Interactive Legislative Data Playground**, a zero-compute, in-browser data laboratory powered by WebAssembly (DuckDB-Wasm, PGlite, and WebR). 

Operating on our single-assembly pilot baseline (The Scottish Parliament / `GB-SCT`, 1999–Present, 72 empirical ground-truth variables), the Playground introduces a 4-Studio Multi-Interface Suite (Visual Builder, Grid Studio, Econometrics/Stata Studio, and R-Studio Lite). To satisfy stringent Data Access and Research Transparency (DA*RT) mandates, the platform generates copyable SQL, R, and Python replication scripts in real time alongside publication-ready LaTeX Stargazer regression tables. Finally, an ORCID-authenticated crowdsourcing loop allows researchers to propose custom visualizations as peer-reviewed platform presets, transforming the infrastructure from a static repository into a living scientific laboratory.

---

## 1. Introduction & Theoretical Motivation

Quantitative legislative research suffers from significant friction regarding software setup, environment configuration, and replication compliance. Before a researcher can evaluate whether a legislative dataset contains relevant signals for their research design, they must download, clean, and merge secondary files locally.

Furthermore, traditional visualization tools on academic websites operate as "read-only" presentation layers. Researchers cannot write custom queries, execute regressions, or export replication code without leaving the site.

The **Interactive Legislative Data Playground** addresses this friction by embedding a full computational laboratory directly into the browser.

---

## 2. Epistemological Foundation: Two-Pass Empirical Baseline

To maintain absolute academic credibility, the Playground operates strictly on our **Pass 1 Empirical Ground-Truth Baseline**:
* **51 Native Direct Variables:** Sourced raw from official host assembly APIs (`data.parliament.scot/api`).
* **21 Derived Deterministic Variables:** Calculated via 100% deterministic relational and temporal joins with 0% parsing ambiguity (evaluated on Date $T$).

Unvalidated non-API variables (e.g., OCR text extractions, sentiment scores) are kept under **Pass 2 Candidate Specifications** (`PROVISIONAL_HYPOTHESIS`) and visually quarantined from primary regression tools to prevent statistical misinterpretation or p-hacking.

---

## 3. The 4-Studio Architecture

The Playground provides 4 distinct modes suited to every type of researcher:

```
┌──────────────────────────────────────────────────────────────────────────┐
│                   THE GLOBAL LEGISLATIVE DATA PLAYGROUND                 │
├──────────────┬─────────────────┬──────────────────┬──────────────────────┤
│ 1. VISUAL    │ 2. EXCEL / GRID │ 3. ECONOMETRICS  │ 4. R-STUDIO LITE     │
│    BUILDER   │    STUDIO       │    & STATA STUDIO│    (WebR)            │
├──────────────┼─────────────────┼──────────────────┼──────────────────────┤
│ Drag-&-drop  │ In-browser live │ One-click cross- │ Write actual R code  │
│ X/Y axes,    │ spreadsheet grid│ tabs (χ²), OLS   │ (`ggplot2`, `dplyr`) │
│ chart types, │ with pivot      │ regressions, &   │ inside the browser   │
│ & filters.   │ tables.         │ LaTeX stargazer  │ with zero setup!     │
│              │                 │ output tables.   │                      │
└──────────────┴─────────────────┴──────────────────┴──────────────────────┘
```

1. **Visual Drag-&-Drop Builder:** Tableau-style UI generating automatic SQL/R/Python replication code.
2. **Excel / Grid Studio:** In-browser live spreadsheet with pivot tables and instant CSV exports.
3. **Econometrics & Stata Studio:** One-click OLS regressions and cross-tabulations exporting publication-ready **LaTeX Stargazer tables**.
4. **R-Studio Lite (WebR):** Embedded R console executing native R code inside WebAssembly with zero setup.

---

## 4. Technical Architecture: Zero-Compute Edge Infrastructure

By shipping data as compressed Parquet files and executing queries via **DuckDB-Wasm** and **PGlite**, the platform shifts 100% of computational work to the client's browser memory:
* **Query Latency:** < 10ms for aggregations on 1,000,000+ rows.
* **Server Cost:** $0 compute cost (static CDN host model).
* **Local Persistence:** PGlite (Postgres Wasm) saves user presets in browser IndexedDB/OPFS.

---

## 5. Peer-Reviewed Crowdsourced Presets & ORCID Integration

Researchers can click **"Propose as Platform Preset"** to submit a custom visual or econometric view. Submissions are peer-reviewed by the editorial board and, upon approval, pushed directly to the author's **ORCID profile** as a recognized digital research output, fostering an active global research community.
