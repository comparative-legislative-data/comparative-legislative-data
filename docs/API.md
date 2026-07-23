# Platform API Specification

**Comparative Legislative Data Platform**  
*RESTful & Audit Inspection API Standard*  
*Version 2.1.0 (6-Tier Provenance & AI Validation Specification)*

---

## 1. API Architecture Overview

The Platform API (`https://legislativedata.org/api/v2`) provides open endpoints for querying canonical legislative datasets, auditing 6-tier data availability across assemblies, and inspecting raw host JSON/XML payloads.

---

## 2. API Endpoints Specification

### 1. Global Assembly Audit Summaries
`GET /api/v2/atlas`
* **Description:** Returns the list of tracked legislative assemblies and their 6-tier variable coverage matrix.

```json
{
  "assemblies": [
    {
      "jurisdiction_code": "GB-SCT",
      "assembly_name": "Scottish Parliament",
      "country": "United Kingdom",
      "chamber_type": "DEVOLVED_UNICAMERAL",
      "total_bills_indexed": 142,
      "provenance_coverage_summary": {
        "NATIVE_DIRECT_PCT": 45.2,
        "DERIVED_DETERMINISTIC_PCT": 28.1,
        "DERIVED_HUMAN_CODED_PCT": 12.5,
        "DERIVED_SYNTHETIC_AI_PCT": 8.2,
        "UNAVAILABLE_HARD_GAP_PCT": 6.0
      }
    }
  ]
}
```

---

### 2. Parliament Audit & Payload Explorer
`GET /api/v2/atlas/{jurisdiction_code}`
* **Description:** Detailed assembly audit breakdown, API endpoints list, sample payloads, and variable-session provenance matrix.

```json
{
  "jurisdiction_code": "GB-SCT",
  "assembly_name": "Scottish Parliament",
  "native_endpoints": [
    {
      "endpoint_name": "Bills Feed",
      "url": "https://data.parliament.scot/api/bills",
      "status": "HEALTHY",
      "sample_payload": {
        "BillId": 13,
        "ShortTitle": "Gender Recognition Reform (Scotland) Bill",
        "Stage": "Passed"
      }
    }
  ],
  "canonical_variable_matrix": [
    {
      "variable_name": "initiator_party_governance_role",
      "domain": "Domain 2: Bill Identification & Sponsorship",
      "tier": "DERIVED_DETERMINISTIC",
      "confidence": "HIGH",
      "methodology": "Sponsor MSP matched to Scottish Government Cabinet roster table."
    },
    {
      "variable_name": "committee_amendments_executive_acceptance_rate",
      "domain": "Domain 7: Amendments & Legislative Alteration",
      "tier": "DERIVED_HUMAN_CODED",
      "confidence": "HIGH",
      "citation": "PhD Dissertation Dataset: Scottish Parliament Amendment Outcomes (2016-2021)."
    },
    {
      "variable_name": "fiscal_impact_flag",
      "domain": "Domain 5: Documentation Chain",
      "tier": "DERIVED_SYNTHETIC_AI",
      "ai_validation_status": "UNVERIFIED_DRAFT",
      "confidence": "MEDIUM",
      "methodology": "Extracted via LLM analysis of official Financial Memorandum text."
    },
    {
      "variable_name": "guillotine_invoked_flag",
      "domain": "Domain 3: Timelines & Procedural Control",
      "tier": "UNAVAILABLE_HARD_GAP",
      "hard_gap_reason": "NOT_RECORDED_BY_ASSEMBLY",
      "notes": "Scottish Parliament standing orders do not feature formal Westminster-style guillotine motions."
    }
  ]
}
```

---

### 3. Canonical Bills Query Engine
`GET /api/v2/bills`
* **Query Parameters:**
  * `jurisdiction_code`: Filter by assembly (e.g. `GB-SCT`, `GB-UKP`).
  * `term`: Filter by session (e.g. `Session 6`).
  * `final_status`: Filter by status (`ENACTED`, `DEFEATED`).
  * `provenance_tier`: Filter by availability tier (`DERIVED_HUMAN_CODED`, `DERIVED_SYNTHETIC_AI`).
  * `ai_validation_status`: Filter AI data (`UNVERIFIED_DRAFT`, `SAMPLE_VALIDATED`, `GOLD_BENCHMARKED`).

---

### 4. Direct Bill Payload & Audit Inspector
`GET /api/v2/bills/{jurisdiction_code}/{local_bill_id}`
* **Description:** Retrieves the full canonical record for a specific bill, including raw host payload and key-by-key variable provenance map.
