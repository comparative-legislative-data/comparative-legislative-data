# Platform API Specification

**Comparative Legislative Data Platform**  
*RESTful & Audit Inspection API Standard*  
*Version 2.3.0 (Master Wishlist & 6-Tier Provenance Specification)*

---

## 1. API Architecture Overview

The Platform API (`https://legislativedata.org/api/v2`) provides open endpoints for querying canonical legislative datasets, auditing 6-tier data availability across assemblies, querying decision-point member affiliations, and inspecting raw host JSON/XML payloads.

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
        "NATIVE_DIRECT_PCT": 42.1,
        "DERIVED_DETERMINISTIC_PCT": 26.5,
        "DERIVED_HUMAN_CODED_PCT": 12.0,
        "DERIVED_SYNTHETIC_AI_PCT": 8.0,
        "LINKED_EXTERNAL_AUTHORITY_PCT": 6.4,
        "UNAVAILABLE_HARD_GAP_PCT": 5.0
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
      "status": "HEALTHY"
    }
  ],
  "canonical_variable_matrix": [
    {
      "variable_name": "government_type",
      "domain": "Domain 1: Assembly & Executive Context",
      "tier": "LINKED_EXTERNAL_AUTHORITY",
      "confidence": "HIGH",
      "linked_authority_source": "ParlGov",
      "value": "COOPERATION_AGREEMENT",
      "notes": "Mapped to ParlGov Cabinet ID for SNP/Green Bute House Agreement (2021-2024)."
    },
    {
      "variable_name": "committee_amendments_executive_acceptance_rate",
      "domain": "Domain 7: Amendments & Legislative Alteration",
      "tier": "DERIVED_HUMAN_CODED",
      "confidence": "HIGH",
      "citation": "PhD Dissertation Dataset: Scottish Parliament Amendment Outcomes (2016-2021)."
    },
    {
      "variable_name": "effective_majority_margin_at_event_date",
      "domain": "Domain 8: Temporal Divisions",
      "tier": "DERIVED_DETERMINISTIC",
      "confidence": "HIGH",
      "methodology": "Evaluated dynamically against member_party_affiliations on vote date T."
    }
  ]
}
```

---

### 3. Decision-Point Member Affiliation Engine
`GET /api/v2/members/{member_id}/affiliation`
* **Query Parameters:**
  * `date`: Target decision-point date ISO 8601 (e.g. `2014-03-12`).

```json
{
  "member_id": "MSP_1042",
  "member_name": "Tricia Marwick",
  "jurisdiction_code": "GB-SCT",
  "evaluated_date": "2014-03-12",
  "party_id": "NEUTRAL_PRESIDING_OFFICER",
  "party_role": "SPEAKER_NEUTRAL",
  "voting_status": "NON_VOTING_CHAIR"
}
```

---

### 4. Canonical Bills Query Engine
`GET /api/v2/bills`
* **Query Parameters:**
  * `jurisdiction_code`: Filter by assembly (e.g. `GB-SCT`, `GB-UKP`).
  * `government_type`: Filter by executive type (`SINGLE_PARTY_MINORITY`, `COOPERATION_AGREEMENT`).
  * `provenance_tier`: Filter by availability tier (`DERIVED_HUMAN_CODED`, `LINKED_EXTERNAL_AUTHORITY`).
  * `ai_validation_status`: Filter AI data (`UNVERIFIED_DRAFT`, `SAMPLE_VALIDATED`, `GOLD_BENCHMARKED`).

---

### 5. Direct Bill Payload & Audit Inspector
`GET /api/v2/bills/{jurisdiction_code}/{local_bill_id}`
* **Description:** Retrieves the full canonical record for a specific bill, including raw host payload, key-by-key variable provenance map, and edge-case review status.
