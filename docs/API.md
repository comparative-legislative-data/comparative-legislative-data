# Comparative Legislative Data API Specification

This document defines the **REST API Architecture, Endpoint Specification, Access Tiers, Rate Limits, and Commercial Licensing Framework** for the Comparative Legislative Data platform.

---

## 1. API Principles & Architecture

- **Host Base URL:** `https://api.comparativelegislativedata.org/v1`
- **Format:** All requests and responses use standard JSON (`application/json`).
- **Data Mirror Guarantee:** Queries are served directly from our mirrored PostgreSQL/DuckDB datastore on host `45.152.161.153` with $< 15\text{ms}$ target latency.
- **Dual-Layer Payload:** Every record contains explicit `normalized.*` (comparative cross-national fields), `native.*` (country-specific raw terms), and `provenance.*` (audit trail & Zenodo DOI) blocks.
- **Infrastructure Philosophy:** The API exports **clean, high-fidelity atomic variables** (`duration_sitting_days`, `termination_mechanism`, `rebellions_flag`, `cross_party_sponsorship_count`, `derivation_confidence`) allowing researchers to construct custom indices for their specific research designs.

---

## 2. API Access Tiers & Rate Limiting

```
                       API ACCESS & RATE-LIMIT TIERS
                                    │
       ┌────────────────────────────┼────────────────────────────┐
       ▼                            ▼                            ▼
[Public / Explorer]        [Academic & Student]        [Commercial Pro / Ent.]
No API key required        Academic email (.edu/.ac.uk) Paid API Key (Stripe)
1,000 requests/day         50,000 requests/day         500,000+ requests/day
(10 req/min)               (100 req/min + Bulk)        (500 req/min + SLAs)
£0 / month                 £0 / month (Free)           £49 – £499 / month
```

### Access Tier Summary

| Tier Name | Target Audience | Pricing | Daily Quota | Rate Limit | Features & Support |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Public / Explorer** | Citizens, casual developers | **£0 / month** | 1,000 req/day | 10 req/min | Basic REST API access. |
| **Academic & Student** | PhD candidates, university faculty, think tanks | **£0 / month (Free)** | **50,000 req/day** | 100 req/min | Full REST API access + **Direct Bulk Parquet/CSV Downloads**. Verified via `.ac.uk` / `.edu` email. |
| **Commercial Pro** | Boutique public affairs firms, lobbying consultancies | **£49 – £99 / month** | **500,000 req/day** | 500 req/min | High-throughput API, commercial SLA, email support. |
| **Enterprise / Legal** | Major law firms, news organizations, risk platforms | **£299 – £499 / month** | **Custom / Unlimited** | 2,000 req/min | Dedicated infrastructure, custom data exports, live webhooks. |

---

## 3. Core API Endpoints

### 3.1 List / Search Bills (`GET /v1/bills`)

Query and filter mirrored Bills across all target parliaments.

#### Query Parameters:
- `jurisdiction` (Optional, string): ISO code filter (e.g. `GB-UKP`, `GB-SCT`, `US-FED`, `DE-BT`).
- `status` (Optional, string): Standardised status filter (`ENACTED`, `DEFEATED`, `WITHDRAWN`, `LAPSED`).
- `termination_mechanism` (Optional, string): (`ENACTMENT`, `EXECUTIVE_WITHDRAWAL`, `VOTE_DEFEAT`, `SESSION_EXPIRY`).
- `initiator_type` (Optional, string): (`EXECUTIVE`, `INDIVIDUAL_MEMBER`, `COMMITTEE`, `OTHER`).
- `governance_role` (Optional, string): (`GOVERNING_PARTY`, `OPPOSITION_PARTY`, `CROSS_PARTY`, `NON_PARTISAN`).
- `date_from` (Optional, ISO Date): Filter introduction date $\ge \text{YYYY-MM-DD}$.
- `date_to` (Optional, ISO Date): Filter outcome date $\le \text{YYYY-MM-DD}$.
- `page` (Integer, default 1), `limit` (Integer, default 50, max 100).

#### Response Payload (`200 OK`):
```json
{
  "total_records": 1420,
  "page": 1,
  "limit": 50,
  "data": [
    {
      "canonical_id": "GB-SCT-S6-SPB13",
      "jurisdiction_code": "GB-SCT",
      "normalized": {
        "title": "Gender Recognition Reform (Scotland) Bill",
        "parliament_term": "Session 6",
        "initiator_type": "EXECUTIVE",
        "initiator_party_governance_role": "GOVERNING_PARTY",
        "date_introduced": "2022-03-03",
        "date_final_outcome": "2022-12-22",
        "duration_calendar_days": 294,
        "duration_sitting_days": 82,
        "suspension_interrupted": false,
        "final_status": "ENACTED",
        "termination_mechanism": "ENACTMENT",
        "rebellions_flag": false,
        "cross_party_sponsorship_count": 0,
        "derivation_confidence": "HIGH"
      },
      "native": {
        "local_bill_id": "SP Bill 13",
        "title_native": "Gender Recognition Reform (Scotland) Bill",
        "initiator_name": "Shona Robison MSP",
        "initiator_member_id": "Q59385108",
        "initiator_party": "Scottish National Party",
        "raw_status": "Passed"
      },
      "provenance": {
        "source_url": "https://www.parliament.scot/api/bills/5",
        "retrieved_at": "2026-07-22T08:30:00Z",
        "raw_payload_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "zenodo_doi": "10.5281/zenodo.1234567"
      }
    }
  ]
}
```

---

### 3.2 Get Single Bill Detail (`GET /v1/bills/{canonical_id}`)

Retrieves the complete record including stage milestones, native Hansard proceedings links, persistent member IDs, and publication citations.

---

### 3.3 Global Legislative Data Atlas (`GET /v1/legislatures`)

Returns live status, data access tiers, mirror health, and field availability matrix across all 30+ audited parliaments.

---

### 3.4 Bulk Dataset Downloads (`GET /v1/downloads/{jurisdiction}`)

Provides direct download URLs for complete, compressed `.parquet` and `.csv` release files with permanent Zenodo DOIs.

---

## 4. Legal & Licensing Framework for Commercial Access

### 4.1 Underlying Source Licenses
Primary legislative texts and parliamentary proceedings are public domain materials or covered by non-exclusive open licenses (Open Parliament Licence v3.0, OGL v3.0, US 17 U.S.C. § 105, dl-de/by-2-0).

### 4.2 Attribution Compliance
Every API response includes source provenance metadata and Zenodo DOIs, satisfying all open license attribution and academic reproducibility standards.
