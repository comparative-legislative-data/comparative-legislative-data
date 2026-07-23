# Master Canonical Variable Catalog

**Comparative Legislative Data Platform**  
**Version:** 2.4.0  
**Specification:** Dual-Layer Architecture & Master Variable Dictionary

---

## 1. Dual-Layer Architecture & Methodology

The platform operates on a **Dual-Layer Data Architecture** designed to serve both single-country legislative specialists and cross-national quantitative political scientists:

```
                  ┌─────────────────────────────────────────────────────────┐
                  │   HIGH-RESOLUTION NATIVE INSTITUTIONAL LAYER (Layer A) │
                  │  └─ 100% granular assembly data, raw Hansard feeds,      │
                  │     native stage codes, motion texts, word counts,      │
                  │     and individual roll-call vote choice records.       │
                  └────────────────────────────┬────────────────────────────┘
                                               │
                                MAPPED & EVALUATED PER DECISION POINT (T)
                                               │
                                               ▼
                  ┌─────────────────────────────────────────────────────────┐
                  │    HARMONISED CANONICAL COMPARATIVE LAYER (Layer B)    │
                  │  └─ Abstract quantitative research metrics mapped       │
                  │     against the 6-Tier Data Availability Spectrum.      │
                  └─────────────────────────────────────────────────────────┘
```

* **Layer A (Native Institutional Layer):** Preserves 100% of the raw, assembly-specific data served by host APIs, parliamentary feeds, and academic PhD datasets (`payload.native`). No native detail is ever stripped or distorted.
* **Layer B (Canonical Comparative Layer):** Standardises quantitative variables across legislatures (`payload.canonical`) into 8 core research domains, evaluating each variable value against the **6-Tier Data Availability & Provenance Spectrum** (`NATIVE_DIRECT`, `DERIVED_DETERMINISTIC`, `DERIVED_HUMAN_CODED`, `DERIVED_SYNTHETIC_AI`, `LINKED_EXTERNAL_AUTHORITY`, `UNAVAILABLE_HARD_GAP`).

---

## 2. Master Wishlist Variable Catalog by Domain

### Domain 1: Assembly, Electoral & Executive Context
* **`jurisdiction_code`** (String, ISO 3166-2): Unique assembly identifier (e.g. `GB-UKP`, `GB-SCT`, `DE-BT`, `US-HR`).
* **`parliament_term`** (String): Macro electoral legislative period (e.g. `Session 6`, `58th Parliament`).
* **`chamber_type`** (Enum): Constitutional chamber structure (`SOVEREIGN_BICAMERAL`, `DEVOLVED_UNICAMERAL`, `FEDERAL_UPPER`, etc.).
* **`government_type`** (Enum): Executive arrangement typology (`SINGLE_PARTY_MAJORITY`, `SINGLE_PARTY_MINORITY`, `FORMAL_COALITION_MAJORITY`, `FORMAL_COALITION_MINORITY`, `CONFIDENCE_AND_SUPPLY`, `COOPERATION_AGREEMENT`, `CARETAKER_TECHNOCRATIC`).
* **`parlgov_cabinet_id`** (String): Canonical cabinet identifier linked from ParlGov authority dataset.

### Domain 2: Bill Identification, Sponsorship & Temporal Origin
* **`local_bill_id`** (String): Native reference code assigned by host legislature (e.g. `SP Bill 13`, `H.R. 815`).
* **`title_canonical`** (String): Standardized English short title.
* **`initiator_type`** (Enum): Globally neutral sponsor type (`EXECUTIVE`, `INDIVIDUAL_MEMBER`, `GROUP_MEMBERS`, `COMMITTEE`).
* **`initiator_party_governance_role`** (Enum): Primary sponsor alignment (`GOVERNING_PARTY`, `OPPOSITION_PARTY`, `CROSS_PARTY`) evaluated dynamically on introduction date $T_{\text{Intro}}$.
* **`initiator_member_id`** (String, Wikidata QID): Disambiguated persistent identifier for primary sponsor MP/MSP.

### Domain 3: Progression, Timelines & Stage Milestones
* **`date_introduced`** (Date, ISO 8601): Formal introduction date of the bill.
* **`date_final_outcome`** (Date, ISO 8601): Date of final passage, defeat, or withdrawal.
* **`duration_calendar_days`** (Integer): Calendar days elapsed from introduction to final outcome.
* **`duration_sitting_days`** (Integer): Formal parliamentary sitting days elapsed.
* **`stage_milestones`** (Array of Objects): Stage-by-stage progression interval breakdown:
  ```json
  [
    {
      "stage_sequence": 1,
      "stage_canonical": "FIRST_READING",
      "stage_raw": "Stage 1 (General Principles & Lead Committee Report)",
      "date_start": "2022-03-03",
      "date_end": "2022-10-06",
      "duration_sitting_days": 24
    },
    {
      "stage_sequence": 2,
      "stage_canonical": "COMMITTEE_STAGE",
      "stage_raw": "Stage 2 (Committee Amendments)",
      "date_start": "2022-10-07",
      "date_end": "2022-11-15",
      "duration_sitting_days": 18
    },
    {
      "stage_sequence": 3,
      "stage_canonical": "FINAL_PASSAGE",
      "stage_raw": "Stage 3 (Plenary Consideration & Final Vote)",
      "date_start": "2022-12-20",
      "date_end": "2022-12-22",
      "duration_sitting_days": 3
    }
  ]
  ```
* **`programme_motion_flag`** (Boolean): Indicates whether a formal timetabling or programme motion was imposed.
* **`guillotine_invoked_flag`** (Boolean): Indicates whether a debate closure or guillotine motion was invoked.
* **`emergency_procedure_flag`** (Boolean): Indicates whether the bill passed under fast-track or urgency procedures.
* **`prior_executive_consent_required_flag`** (Boolean): Indicates whether prior executive or Crown consent was required.

### Domain 4: Final Disposition & Inter-Chamber Mechanisms
* **`final_status`** (Enum): Terminal procedural status (`ENACTED`, `DEFEATED`, `WITHDRAWN`, `LAPSED`, `PENDING`, `VETOED`).
* **`termination_mechanism`** (Enum): Specific procedural event terminating consideration (`ENACTMENT`, `VOTE_DEFEAT`, `EXECUTIVE_WITHDRAWAL`).
* **`head_of_state_promulgation_date`** (Date, ISO 8601): Date of Royal Assent, Presidential Signature, or Promulgation. (Alias: `royal_assent_date`).
* **`chamber_ping_pong_count`** (Integer): For bicameral systems: number of amendment exchanges between chambers.

### Domain 5: Bill Documentation & Text Size Analytics
* **`doc_as_introduced_url`** (URL): Official text of the Bill as introduced.
* **`doc_as_passed_url`** (URL): Official text of the Bill as enacted or passed.
* **`word_count_introduced`** (Integer): Word count of official bill text at introduction.
* **`word_count_post_committee`** (Integer): Word count of bill text following committee stage amendments.
* **`word_count_enacted`** (Integer): Word count of final enacted statute.
* **`text_expansion_ratio`** (Float): Ratio of enacted text size vs introduced text size ($\frac{\text{word\_count\_enacted}}{\text{word\_count\_introduced}}$).
* **`cap_topic_code`** (String): Policy topic code mapped to Comparative Agendas Project taxonomy.
* **`fiscal_impact_flag`** (Boolean): Flag indicating binding fiscal expenditure or taxation impact.

### Domain 6: Committee Scrutiny & Evidence
* **`lead_committee_name`** (String): Name of the primary scrutinising committee assigned.
* **`committee_evidence_submissions_count`** (Integer): Total published written evidence submissions received.

### Domain 7: Decision-Point Amendments & Text Alteration
* **`amendments_tabled_count`** (Integer): Total count of formal amendments tabled across all stages.
* **`amendments_agreed_count`** (Integer): Total count of amendments formally adopted into the bill text.
* **`amendments_non_executive_count`** (Integer): Count of amendments tabled by non-executive members evaluated on tabling date.
* **`committee_amendments_executive_acceptance_rate`** (Float 0-1): Proportion of non-executive committee amendments supported by government.
* **`bill_text_alteration_score`** (Float 0-1): Similarity metric comparing introduced vs enacted text.

### Domain 8: Temporal Divisions, Motion Types & Voting Coalitions
* **`divisions_count`** (Integer): Total recorded roll-call division votes held on the bill.
* **`division_motions`** (Array of Objects): Detailed breakdown of key stage motion votes:
  * `motion_type`: `STAGE_1_AGREEMENT`, `FINANCIAL_RESOLUTION`, `EMERGENCY_BILL_DESIGNATION`, `STAGE_2_AMENDMENT`, `STAGE_3_PASSAGE`
  * `date`: $T_{\text{Division}}$
  * `aye_votes`, `no_votes`, `abstain_votes`
* **`effective_majority_margin_at_event_date`** (Integer): Floor majority margin ($\text{Governing Seats}_T - \text{Opposition Seats}_T$) evaluated on division date $T$.
* **`party_dissent_rate_at_event_date`** (Float 0-1): Proportion of party members voting against their party majority on division date $T$.
* **`voting_coalition_type`** (Enum): Voting alignment classification (`UNANIMOUS`, `GOVERNMENT_PARTY_LINE`, `CROSS_PARTY_MAJORITY`) evaluated on vote date.
