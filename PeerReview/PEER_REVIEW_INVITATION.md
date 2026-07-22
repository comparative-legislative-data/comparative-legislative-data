# Project Briefing & External Peer Review Synthesis

**Project Title:** Comparative Legislative Data Platform  
**Document Purpose:** Self-Contained Project Briefing, Technical Specification, & External Peer Review Synthesis Report  
**Author:** Comparative Legislative Data Team  

---

## 1. Project Background, Context & Academic Motivation

### 1.1 Origin & Research Context
This project originates from empirical academic research into legislative delivery and executive dominance (building upon doctoral research *"Does Government dominate the legislative process"*, 2022, grounded in 25 years of practitioner experience in parliamentary delivery).

The central academic problem is that **comparative research into legislative scrutiny, amendment success, executive dominance, and procedural velocity across international parliaments is severely bottlenecked by data fragmentation.**

### 1.2 The Analytical Gap Addressed
Quantitative political scientists, legislative scholars, and policy research institutes face four major barriers:
1. **Missing Analytical Data in Native Feeds:** Official parliamentary APIs and open data feeds export raw procedural logs, but rarely provide explicit Bill outcome classifications (`ENACTED`, `DEFEATED`, `WITHDRAWN`, `LAPSED`), stage-by-stage amendment outcomes, sponsor executive alignment (minister vs backbench/opposition), or stage duration metrics.
2. **Format Fragmentation & Incompatibility:** Every legislature uses incompatible data models (REST APIs, bulk XML dumps, HTML web portals, PDF papers). Existing academic software relies on ad-hoc, single-country scrapers that break frequently.
3. **Westminster & US Bias in Existing Schemas:** Comparative tools often force non-Westminster assemblies into US or UK procedural categories, obscuring consensus parliaments, micro-legislatures, and civil law decree mechanisms.
4. **Lack of Linked Proceedings & Citation Longevity:** Verbatim speech transcripts (Hansard / Official Reports) are rarely linked directly to specific Bills or Amendments, and upstream website redesigns frequently break academic citation URLs.

### 1.3 Core Philosophy: Atomic Data Generation over Imposed Indices
Following external peer review, the platform enforces a core infrastructure philosophy: **The platform does NOT impose pre-calculated scalar indices (e.g. Executive Dominance Scores).** Instead, it executes **algorithmic data derivation** (`ENRICHED_BY_PIPELINE`) to generate clean, high-fidelity atomic variables (`author_type`, `author_party_role`, `disposal_outcome`, `rebellions_flag`, `cross_party_sponsorship_count`, `duration_sitting_days`, `termination_mechanism`, `derivation_confidence`) so researchers can construct their own custom indices for their specific research designs.

---

## 2. Peer Review Synthesis & Actionable Resolutions

Following review by external academic and technical reviewers, the project team accepted and implemented six major structural enhancements:

```
===================================================================================================
PEER REVIEW FINDING                                IMPLEMENTED PIPELINE SOLUTION
===================================================================================================
1. Drop Pre-Calculated EDS Index                --> Removed pre-calculated EDS scalar. Expose atomic
                                                    building-block variables for custom researcher metrics.
2. Persistent Member ID Disambiguation          --> Replaced raw string name matching with stable
                                                    persistent identifiers (Wikidata QIDs / native IDs).
3. Sitting Days vs Calendar Duration            --> Added `duration_sitting_days` and a boolean
                                                    `suspension_interrupted` flag.
4. Outcome Mechanism & Confidence               --> Added `termination_mechanism` and explicit
                                                    `derivation_confidence` tags (HIGH / MEDIUM / LOW).
5. Academic Citation Longevity (Zenodo/OSF)     --> Added automated mirroring of raw archives and
                                                    Parquet releases to Zenodo/OSF for permanent DOIs.
6. Non-Partisan Consensus Support (BICD)         --> Added `NON_PARTISAN` and `COMMITTEE_PROPOSED` roles
                                                    for consensus assemblies (Jersey, Guernsey, Tynwald).
===================================================================================================
```

---

## 3. Project Architecture & 4-Phase Lifecycle

```
===================================================================================
PHASE 0: GLOBAL DATA AUDIT & MAPPING ATLAS
===================================================================================
• Audits data availability, APIs, formats, Hansard links, and open gaps across 30+ GLOBAL PARLIAMENTS.
• Establishes 3-Tier Data Provenance, persistent member ID joins, and Zenodo DOI archiving.
• Includes a dedicated, detailed audit subset for the 8 BICD assemblies.
                                       │
                                       ▼
===================================================================================
PHASE 1: BICD PILOT INGESTION (2019–2024)
===================================================================================
• Ingests raw data and generates derived metrics ONLY for the 8 BICD assemblies for 2019–2024.
• BICD Cohort: UK Parliament, Scottish Parliament, Senedd Cymru, NI Assembly, Isle of Man Tynwald,
  States of Jersey, States of Guernsey, Gibraltar Parliament.
• Validates schema resilience, proceedings links, and data derivation algorithms on a clean 5-year cohort.
                                       │
                                       ▼
===================================================================================
PHASE 2: BICD FULL HISTORICAL BACKFILL & LIVE CRON MAINTENANCE
===================================================================================
• Backfills FULL digital history ONLY for the BICD group (1997+ UK, 1999+ Scotland, 1999+ Wales, etc.).
• Deploys automated daily ingestion crons + weekly programmatic & AI health monitoring for BICD feeds.
• Proves the entire end-to-end data mirror, derivation algorithms, API, and maintenance flow.
                                       │
                                       ▼
===================================================================================
PHASE 3: GLOBAL EXPANSION (PARLIAMENT BY PARLIAMENT)
===================================================================================
• Add major global parliaments ONE BY ONE (US Congress, German Bundestag, Canada, Australia, France,
  European Parliament, Japan, India, Brazil, etc.) drawing directly from Phase 0 mapping blueprints.
```

---

## 4. Data Specification & Dual-Layer JSON Payload Model

### Canonical JSON Payload Specification Example

```json
{
  "canonical_id": "GB-SCT-S6-SPB13",
  "jurisdiction_code": "GB-SCT",
  
  "normalized": {
    "title": "Gender Recognition Reform (Scotland) Bill",
    "parliament_term": "Session 6",
    "session_subperiod": "Session 6",
    "session_start_date": "2021-05-13",
    "session_end_date": "2026-05-07",
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
    "derivation_confidence": "HIGH",
    "stage_milestones": [
      {
        "stage_canonical": "FIRST_READING",
        "stage_raw": "Introduced",
        "chamber": "DEVOLVED_UNICAMERAL",
        "date_stage": "2022-03-03",
        "proceedings_url": "https://www.parliament.scot/bills/5"
      },
      {
        "stage_canonical": "COMMITTEE_STAGE",
        "stage_raw": "Stage 1 (Committee Consideration)",
        "chamber": "DEVOLVED_UNICAMERAL",
        "date_stage": "2022-10-06",
        "proceedings_url": "https://www.parliament.scot/bills/5#stage1"
      },
      {
        "stage_canonical": "FINAL_PASSAGE",
        "stage_raw": "Stage 3 (Passed)",
        "chamber": "DEVOLVED_UNICAMERAL",
        "date_stage": "2022-12-22",
        "proceedings_url": "https://www.parliament.scot/bills/5#stage3"
      }
    ]
  },
  
  "native": {
    "local_bill_id": "SP Bill 13",
    "title_native": "Gender Recognition Reform (Scotland) Bill",
    "initiator_raw": "Cabinet Secretary for Social Justice, Housing and Local Government",
    "initiator_name": "Shona Robison MSP",
    "initiator_member_id": "Q59385108",
    "initiator_party": "Scottish National Party",
    "raw_status": "Passed (Subject to Section 35 Order)",
    "parliament_term_raw": "Session 6 (2021-2026)",
    "official_proceedings_url": "https://www.parliament.scot/bills-and-laws/bills/gender-recognition-reform-scotland-bill",
    "official_publication_ref": "SP Bill 13 Session 6 (2022)"
  },
  
  "provenance": {
    "source_url": "https://www.parliament.scot/api/bills/5",
    "retrieved_at": "2026-07-22T08:30:00Z",
    "raw_payload_hash": "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "scraper_version": "0.1.0-gb-sct",
    "zenodo_doi": "10.5281/zenodo.1234567",
    "license": "Open Government Licence v3.0"
  }
}
```

---

## 5. Technical Infrastructure, Access Tiers & Commercial Framework

- **Backend & Ingestion Engine:** Python 3.11+ (FastAPI + Pydantic v2 + Rust-backed validation).
- **Databases:** PostgreSQL 16 (Primary Relational Store) + DuckDB (In-Process OLAP & Parquet Generation).
- **Host Infrastructure:** Dedicated VPS host (`45.152.161.153`, 6 AMD EPYC cores, 11 GiB free RAM, 257 GiB free SSD) running Native Systemd User Isolation with Caddy reverse proxy.
- **Academic & Commercial Access Model:**
  - **Academic & Student Tier:** **£0 / Free** unlimited bulk `.parquet` / `.csv` downloads + 50,000 daily REST API requests for verified PhD students, researchers, and university faculty.
  - **Commercial Pro / Enterprise Tier:** Paid subscription (£49 – £499/month) for commercial public affairs firms and law firms needing high-throughput API keys, SLAs, and webhooks.
  - **Legal Compliance:** Fully authorized under Open Parliament Licence v3.0, Open Government Licence (OGL) v3.0, US 17 U.S.C. § 105, and dl-de/by-2-0.
