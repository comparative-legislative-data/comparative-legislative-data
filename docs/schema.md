# Canonical Legislative Data Schema

This document serves as the **Single Source of Truth (SSOT)** for data models across all phases of the Comparative Legislative Data API project.

---

## Technical Stack & Architectural Context

- **Backend & Ingestion Engine:** Python 3.11+ (FastAPI + Pydantic v2).
- **Databases:** PostgreSQL 16 (Primary Relational Store) + DuckDB (In-Process OLAP & Parquet Generation).
- **Frontend & Data Graphics:** SvelteKit (Svelte 5) with D3 / LayerCake visualization engine.
- **Deployment:** Native Systemd User Isolation on Primary VPS (`45.152.161.153`) with Caddy reverse proxy.
- **Documentation SSOT Suite:**
  - [`docs/schema.md`](file:///home/steven/Documents/github/comparativelegislativedata/docs/schema.md) (Canonical Schema)
  - [`docs/parliament_and_data_mapping.md`](file:///home/steven/Documents/github/comparativelegislativedata/docs/parliament_and_data_mapping.md) (Phase 0 Global Audit & Mapping Atlas)
  - [`docs/pilot.md`](file:///home/steven/Documents/github/comparativelegislativedata/docs/pilot.md) (Phase 1 BICD Pilot Strategy)
  - [`docs/stack.md`](file:///home/steven/Documents/github/comparativelegislativedata/docs/stack.md) (Stack & Host Specifications)
  - [`docs/ARCHITECTURE.md`](file:///home/steven/Documents/github/comparativelegislativedata/docs/ARCHITECTURE.md) (Systemd Architecture & Security)
  - [`docs/MONITORING.md`](file:///home/steven/Documents/github/comparativelegislativedata/docs/MONITORING.md) (Observability, Pruning & Backups)
  - [`docs/API.md`](file:///home/steven/Documents/github/comparativelegislativedata/docs/API.md) (REST API Specification & Commercial Tiering)
  - [`PeerReview/PEER_REVIEW_INVITATION.md`](file:///home/steven/Documents/github/comparativelegislativedata/PeerReview/PEER_REVIEW_INVITATION.md) (Peer Review Commissioning Briefing)

---

## Peer Review Design Principles & Infrastructure Philosophy

Following external academic peer review, the schema enforces three core design principles:

1. **Atomic Data Generation over Imposed Indices:** The platform does **not** impose pre-calculated scalar indices (e.g., Executive Dominance Scores). Instead, it generates clean, high-fidelity atomic variables (`author_type`, `author_party_role`, `disposal_outcome`, `rebellions_flag`, `cross_party_sponsorship_count`, `duration_sitting_days`) so researchers can construct custom indices for their specific research designs.
2. **Dual-Layer Payload Model:**
   - **Normalized Comparative Layer (`normalized.*`):** Standardised, globally neutral canonical terms (`ENACTED`, `EXECUTIVE`, `GOVERNING_PARTY`, `NON_PARTISAN`, `COMMITTEE_PROPOSED`).
   - **Native Country-Specific Layer (`native.*`):** Unmodified local terms, native stage descriptions, local status phrasing, and official Hansard citations (`official_publication_ref`, `official_proceedings_url`).
3. **Transparent Data Derivation & Provenance:**
   - Every generated field carries a `derivation_confidence` level (`HIGH`, `MEDIUM`, `LOW`).
   - Member identities are resolved to persistent IDs (Wikidata QIDs / native IDs) before joining against historical Executive Rosters.
   - Raw JSON/XML payloads on disk (`/data/raw/`) are verified with SHA-256 hashes and mirrored to Zenodo/OSF for permanent DOI minting.

---

## Phase 1: Bill Quantitative Data Schema

Focuses on the macro legislative record: Bill metadata, persistent sponsor identification, sessional dates, procedural timestamps, stage milestones, proceedings citations, document length, sitting days, and final outcome mechanisms.

### Entity: `StageMilestone`

Representing key procedural progression steps in official parliamentary proceedings.

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `stage_canonical` | Enum | `FIRST_READING`, `SECOND_READING`, `COMMITTEE_STAGE`, `REPORT_STAGE`, `THIRD_READING`, `SECOND_CHAMBER_REVIEW`, `CONCILIATION`, `FINAL_PASSAGE`, `PROMULGATION` |
| `stage_raw` | String | Native stage name (e.g. "Public Bill Committee", "Stage 1 Consideration", "Ping-Pong", "Lesung"). |
| `chamber` | Enum | `PRIMARY_CHAMBER`, `SECONDARY_CHAMBER`, `JOINT_SESSION`, `DEVOLVED_UNICAMERAL` |
| `date_stage` | Date | Date of stage event/completion (`YYYY-MM-DD`). |
| `proceedings_url` | String (Optional) | Direct URL to official Hansard/Journal debate transcript for this stage. |

---

### Entity: `Bill` API Response Payload Structure

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

## Phase 2: Amendment Quantitative Data Schema

Focuses on the scrutiny engine: amendment counts, persistent author origins, stage progression, decision outcomes, voting statistics, and proceedings citations.

### Entity: `Amendment`

| Field Name | Type | Canonical Enum / Format | Description & Harmonisation Rule |
| :--- | :--- | :--- | :--- |
| `amendment_id` | String | `[CANONICAL_BILL_ID]-AMD-[NO]` | Unique identifier for the amendment. |
| `bill_canonical_id` | String | FK to `Bill` | Reference to parent Bill. |
| `author_type` | Enum | `EXECUTIVE`<br>`GOVERNING_BACKBENCH`<br>`OPPOSITION`<br>`COMMITTEE_PROPOSED`<br>`CROSS_PARTY` | Categorization of the amendment sponsor(s). |
| `author_raw` | String | Text | Native author/sponsor string. |
| `author_member_id` | String | Text (Wikidata QID / Native ID) | Persistent member ID for sponsor disambiguation. |
| `stage_canonical` | Enum | `PRE_LEGISLATIVE`<br>`INITIAL_CONSIDERATION`<br>`COMMITTEE_STAGE`<br>`REPORT_STAGE`<br>`FINAL_CONSIDERATION`<br>`SECOND_CHAMBER_REVIEW`<br>`CONCILIATION` | Neutral stage classification across single/multi-chamber systems. |
| `stage_raw` | String | Text | Native stage name (e.g., "Committee Stage", "Mark-up", "Ping-Pong"). |
| `decision_outcome` | Enum | `AGREED`<br>`REJECTED`<br>`WITHDRAWN`<br>`UNCONSIDERED`<br>`SUPERSEDED` | Standardised disposition of the amendment. |
| `decision_raw` | String | Text | Native outcome string. |
| `was_divided` | Boolean | True/False | Whether a formal recorded vote (division) was taken. |
| `votes_for` | Integer | Count | Number of votes in favour (Ayes/Yeas). |
| `votes_against` | Integer | Count | Number of votes opposed (Noes/Nays). |
| `votes_abstain` | Integer | Count | Number of abstentions/present. |
| `proceedings_paper_ref` | String | Text | Official amendment paper / marshalled list publication citation. |
| `proceedings_division_ref` | String | Text | Official Hansard division / vote reference number. |

---

## Phase 3: Qualitative Data Layer Schema

Layers semantic content, textual diffs, policy topic coding, and executive responsiveness tagging on top of the quantitative foundation.

### Entity: `AmendmentQualitative`

| Field Name | Type | Description |
| :--- | :--- | :--- |
| `amendment_id` | String | Foreign key to `Amendment`. |
| `text_diff` | Object | Full text inserted, deleted, or substituted. |
| `structural_target` | String | Target section/clause reference. |
| `substantive_classification` | Enum | `SUBSTANTIVE_POLICY`<br>`TECHNICAL_DRAFTING`<br>`PROCEDURAL`<br>`FINANCIAL` |
| `cap_topic_code` | Integer | Comparative Agendas Project 21 major topic code. |
| `cap_subtopic_code` | Integer | CAP detailed subtopic code. |
| `executive_concession_match` | String | Optional ID of an earlier withdrawn non-executive amendment that this executive amendment responds to. |
| `executive_concession_notes` | Text | Qualitative rationale and evidence for concession tagging. |

---

## Document Revision History

- **2026-07-22 (v2.0):** Incorporated Peer Review findings: removed pre-calculated $EDS$, added `duration_sitting_days`, `suspension_interrupted`, `termination_mechanism`, `rebellions_flag`, `cross_party_sponsorship_count`, `derivation_confidence`, persistent `member_id`, and Zenodo DOI archiving metadata.
- **2026-07-22 (v1.1):** Updated SSOT header referencing `docs/parliament_and_data_mapping.md`.
- **2026-07-21 (v0.1):** Initial draft of canonical schema.
