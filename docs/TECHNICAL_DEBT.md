# Comparative Legislative Data Platform — Technical Debt Log

**Specification Version:** 2.8.0  
**Purpose:** Formal log of deferred architectural optimizations, infrastructure scaling tasks, and technical debt.  
**Last Updated:** July 24, 2026

---

## Technical Debt Backlog & Deferred Optimizations

### 1. Global CDN Edge Delivery & Proxying
* **Status:** `DEFERRED_TECHNICAL_DEBT` (Logged for Phase 2 infrastructure sweep)
* **Description:** Platform dynamic APIs and static datasets are currently served directly from our primary European VPS instance (`45.152.161.153`). While latency in the UK and Europe is sub-20ms, queries from North America, Asia, and Oceania experience 120ms–280ms round-trip latency.
* **Proposed Remediation:**
  * Route domain DNS through Cloudflare Free Academic Proxy (Orange Cloud).
  * Configure Nginx static cache-control headers (`Cache-Control: public, max-age=86400, s-maxage=604800`) for all static datasets (`.parquet`, `.csv`, `.json`, `.rds`).
  * Attach static dataset releases to public GitHub Releases via Fastly global CDN.

---

### 2. Automated Archival DOI Publishing (Zenodo / Dataverse Integration)
* **Status:** `DEFERRED_TECHNICAL_DEBT`
* **Description:** Quantitative legislative research published in top-tier journals (*APSR*, *AJPS*) requires permanent, immutable digital object identifiers (DOIs) for replication.
* **Proposed Remediation:**
  * Add Python script `etl/publish_zenodo.py` using Zenodo's REST API.
  * When a new parliamentary session completes or a major audit baseline is released, automatically push a zip archive to Zenodo to obtain an official DOI (e.g. `10.5281/zenodo.123456`).

---

### 3. In-Browser WASM Package Bundling (Shinylive / WebR)
* **Status:** `DEFERRED_TECHNICAL_DEBT` (Phase 3 Interactive Playground Roadmap)
* **Description:** R-Studio Lite Wasm environment requires pre-compiling R binary packages (`dplyr`, `ggplot2`) into a local `.tgz` bundle to prevent network latency when researchers execute R code inside the browser.
* **Proposed Remediation:**
  * Pre-bundle WebR `.tgz` packages into `frontend/static/wasm/webr/`.
