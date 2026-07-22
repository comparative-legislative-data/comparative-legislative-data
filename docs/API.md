# Comparative Legislative Data Platform API Specification

**Platform API & Data Access Specification**  
*Version 2.0.0 (North Star Reset)*

---

## 1. Core Endpoints Overview

The platform exposes open JSON/REST RESTful endpoints for academic research, automated data mirroring, and audit inspection.

Base URL: `https://legislativedata.org/api/v1`

---

## 2. API Endpoints Reference

### A. Global Data Atlas Audit Blueprints
- **`GET /api/v1/audits`**
  - **Description:** Returns index of all audited parliamentary assemblies.
  - **Query Parameters:** `cohort` (e.g. `2019-2024`), `region` (e.g. `EUROPE`).
  - **Response:** JSON array of top-level assembly metadata and probe status.

- **`GET /api/v1/audits/{jurisdiction_code}`**
  - **Description:** Returns full declarative audit blueprint for a target legislature (e.g. `GB-UKP`, `GB-SCT`, `GB-WLS`).
  - **Response Object:**
    - `assembly`: Top-level institutional metadata.
    - `endpoints`: Host API endpoints with rate limits and sample raw payloads.
    - `field_mappings`: 5-tier evaluation matrix across all 8 research domains.
    - `hansard`: Speaker disambiguation and debate resolution rules.
    - `typology_tests`: 5 representative bill empirical audit test cases.
    - `probe_status`: Live latency and drift status.

### B. Canonical Legislative Data API
- **`GET /api/v1/bills`**
  - **Description:** Queries normalized bill records across international legislatures.
  - **Query Parameters:**
    - `jurisdiction` (e.g. `GB-SCT`)
    - `term` (e.g. `Session 6`)
    - `status` (`ENACTED`, `PENDING`, `DEFEATED`)
    - `initiator_type` (`EXECUTIVE`, `INDIVIDUAL_MEMBER`)
    - `limit` (default: 50, max: 500)
    - `offset` (default: 0)
  - **Response:** Paginated JSON array of canonical `Bill` records conforming to [`docs/schema.md`](file:///home/steven/Documents/github/comparativelegislativedata/docs/schema.md).

- **`GET /api/v1/bills/{canonical_id}`**
  - **Description:** Returns single canonical bill record including normalized fields, stage timeline, document URLs, and SHA-256 provenance metadata.

- **`GET /api/v1/bills/{canonical_id}/raw`**
  - **Description:** Returns the unmodified, raw host API payload for data audit inspection.

### C. Live API Health & Drift Probes
- **`GET /api/v1/probes/health`**
  - **Description:** Returns live latency, HTTP status codes, and drift hashes for all host parliamentary API endpoints probed by the backend engine.

---

## 3. Data License & Attribution

All API data is served under the **Open Government Licence v3.0** (or host parliament's equivalent open data licence). Commercial and academic reuse is permitted with appropriate attribution to the Comparative Legislative Data Project.
