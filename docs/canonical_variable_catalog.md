# Master Canonical Variable Catalog

**Comparative Legislative Data Platform**  
*Canonical Target Wishlist & Research Variable Standard*  
*Version 2.1.0 (6-Tier Provenance & System-Neutral Revision)*

---

## 1. Overview & Conceptual Scope

The **Master Canonical Variable Catalog** defines the target wishlist of quantitative variables sought by legislative scholars, political scientists, and policy analysts studying bills, legislative productivity, executive dominance, procedural control, voting coalitions, and legislative alteration across global parliamentary and presidential assemblies.

Every variable in this catalog is evaluated per parliament and per session against our **6-Tier Legislative Availability & Provenance Spectrum**:
1. **`CANONICAL_WISHLIST_TARGET`:** Universal variable definition in this catalog.
2. **`NATIVE_DIRECT`:** Served out-of-the-box in host assembly API/feed (JSON/XML).
3. **`DERIVED_DETERMINISTIC`:** Generated deterministically via simple pipeline joins, lookup tables, or date arithmetic.
4. **`DERIVED_HUMAN_CODED`:** Manually hand-coded by human researchers, domain experts, or PhD coders (serving as ground truth).
5. **`DERIVED_SYNTHETIC_AI`:** Synthesized using NLP/LLM text processing, topic modeling, or structural parsing, tagged with an explicit **AI Validation Lifecycle Status** (`UNVERIFIED_DRAFT`, `SAMPLE_VALIDATED`, `GOLD_BENCHMARKED`).
6. **`UNAVAILABLE_HARD_GAP`:** Missing or unrecorded data, categorized by sub-reason (`NOT_RECORDED_BY_ASSEMBLY`, `RECORDED_BUT_UNDIGITIZED`, `RESTRICTED_ACCESS`, `COST_PROHIBITIVE`).

---

## 2. Research Domain Catalogs

### Domain 1: Assembly & Electoral Context
*Macro constitutional, electoral, and chamber-level structural metrics.*

| Variable Name | Type / Enum Values | Provenance Tier | Description |
| :--- | :--- | :--- | :--- |
| `jurisdiction_code` | `String` (ISO 3166-2 style) | `NATIVE_DIRECT` | Unique assembly identifier (e.g. `GB-UKP`, `GB-SCT`, `DE-BT`, `US-HR`). |
| `parliament_term` | `String` | `NATIVE_DIRECT` | Electoral legislative period (e.g. `Session 6`, `58th Parliament`). |
| `session_start_date` | `Date` (ISO 8601) | `NATIVE_DIRECT` | Official opening date of the legislative session/term. |
| `session_end_date` | `Date` (ISO 8601) | `NATIVE_DIRECT` | Official closing or dissolution date of the session/term. |
| `chamber_type` | `Enum` (`SOVEREIGN_BICAMERAL`, `DEVOLVED_UNICAMERAL`, `FEDERAL_UPPER`, `FEDERAL_LOWER`, `CONCURRENT_ELECTED`) | `DERIVED_DETERMINISTIC` | Classification of the assembly's constitutional chamber structure. |
| `total_seats` | `Integer` | `DERIVED_DETERMINISTIC` | Total voting seats configured for the assembly session. |

---

### Domain 2: Bill Identification, Sponsorship & Origin
*Core bill metadata, sponsor identification, and executive governance alignment.*

| Variable Name | Type / Enum Values | Provenance Tier | Description |
| :--- | :--- | :--- | :--- |
| `local_bill_id` | `String` | `NATIVE_DIRECT` | Host legislature's native reference code (e.g. `SP Bill 13`, `H.R. 815`). |
| `title_canonical` | `String` | `NATIVE_DIRECT` | Standardized English short title of the bill. |
| `title_native` | `String` | `NATIVE_DIRECT` | Official title in the native language of the host jurisdiction. |
| `initiator_type` | `Enum` (`EXECUTIVE`, `INDIVIDUAL_MEMBER`, `GROUP_MEMBERS`, `COMMITTEE`, `PRIVATE_HYBRID`) | `DERIVED_DETERMINISTIC` | Globally neutral classification of the bill's initiating entity. |
| `initiator_party_governance_role` | `Enum` (`GOVERNING_PARTY`, `OPPOSITION_PARTY`, `CROSS_PARTY`, `NON_PARTISAN`) | `DERIVED_DETERMINISTIC` | Primary sponsor's alignment relative to executive cabinet control. |
| `initiator_member_id` | `String` (Wikidata QID / Native ID) | `DERIVED_DETERMINISTIC` | Disambiguated persistent identifier for the primary sponsor MP/MSP. |
| `co_sponsorship_count` | `Integer` | `NATIVE_DIRECT` | Total count of formal co-sponsors attached to the bill. |
| `cross_party_sponsorship_count` | `Integer` | `DERIVED_DETERMINISTIC` | Count of co-sponsors belonging to opposition parties. |

---

### Domain 3: Procedural Progression, Timelines & Procedural Control
*Stage-by-stage progression dates, fast-tracking flags, closure/guillotine motions, and prior consent.*

| Variable Name | Type / Enum Values | Provenance Tier | Description |
| :--- | :--- | :--- | :--- |
| `date_introduced` | `Date` (ISO 8601) | `NATIVE_DIRECT` | Formal introduction date of the bill in the chamber. |
| `date_final_outcome` | `Date` (ISO 8601) | `NATIVE_DIRECT` | Date of final passage, defeat, or withdrawal. |
| `duration_calendar_days` | `Integer` | `DERIVED_DETERMINISTIC` | Calendar days elapsed from introduction to final outcome. |
| `duration_sitting_days` | `Integer` | `DERIVED_DETERMINISTIC` | Formal parliamentary sitting days elapsed during consideration. |
| `term_interruption_flag` | `Boolean` | `DERIVED_DETERMINISTIC` | Indicates whether consideration spanned a recess, prorogation, or election. |
| `programme_motion_flag` | `Boolean` | `DERIVED_DETERMINISTIC` | Indicates whether a formal timetable/programme motion was imposed. |
| `guillotine_invoked_flag` | `Boolean` | `DERIVED_DETERMINISTIC` | Indicates whether a closure or guillotine motion was invoked to truncate debate. |
| `debate_time_allocated_minutes` | `Integer` | `DERIVED_HUMAN_CODED` / `DERIVED_SYNTHETIC_AI` | Total minutes allocated for plenary debate under timetable rules. |
| `emergency_procedure_flag` | `Boolean` | `NATIVE_DIRECT` / `DERIVED_DETERMINISTIC` | Indicates whether the bill passed under fast-track or urgency procedures. |
| `stages_compressed_count` | `Integer` | `DERIVED_DETERMINISTIC` | Number of standard procedural stages skipped or combined due to fast-tracking. |
| `prior_executive_consent_required_flag` | `Boolean` | `DERIVED_DETERMINISTIC` / `DERIVED_HUMAN_CODED` | Indicates whether prior executive/Crown consent was required before progression. |
| `prior_executive_consent_granted_date` | `Date` (ISO 8601) | `DERIVED_DETERMINISTIC` / `DERIVED_HUMAN_CODED` | Date prior executive/Crown consent was formally signified. |
| `stage_milestones` | `Array[Object]` | `NATIVE_DIRECT` | Chronological array of stage events (`stage_canonical`, `date_stage`, `url`). |

---

### Domain 4: Final Disposition & Inter-Chamber Mechanisms
*Terminal disposition outcomes, head of state promulgation, and bicameral ping-pong metrics.*

| Variable Name | Type / Enum Values | Provenance Tier | Description |
| :--- | :--- | :--- | :--- |
| `final_status` | `Enum` (`ENACTED`, `DEFEATED`, `WITHDRAWN`, `LAPSED`, `PENDING`, `VETOED`) | `NATIVE_DIRECT` | Terminal procedural status of the bill. |
| `termination_mechanism` | `Enum` (`ENACTMENT`, `VOTE_DEFEAT`, `EXECUTIVE_WITHDRAWAL`, `SESSION_EXPIRY`, `EXECUTIVE_VETO`, `CONSTITUTIONAL_CHALLENGE`) | `DERIVED_DETERMINISTIC` | Specific procedural event that terminated consideration. |
| `head_of_state_promulgation_date` | `Date` (ISO 8601) | `NATIVE_DIRECT` | Date of formal Royal Assent, Presidential Signature, or Promulgation. *(Alias: `royal_assent_date`)*. |
| `chamber_ping_pong_count` | `Integer` | `DERIVED_DETERMINISTIC` | For bicameral systems: number of exchanges of amendments between chambers. |
| `chamber_disagreement_flag` | `Boolean` | `DERIVED_DETERMINISTIC` | Indicates whether final passage required resolving formal inter-chamber disagreement. |

---

### Domain 5: Bill Documentation & Parliamentary Papers Chain
*Full chain of official parliamentary publications and impact assessments.*

| Variable Name | Type / Enum Values | Provenance Tier | Description |
| :--- | :--- | :--- | :--- |
| `doc_as_introduced_url` | `String` (URL) | `NATIVE_DIRECT` | Official text of the Bill as introduced. |
| `doc_as_passed_url` | `String` (URL) | `NATIVE_DIRECT` | Official text of the Bill as enacted or passed. |
| `doc_policy_memorandum_url` | `String` (URL) | `NATIVE_DIRECT` | Official policy memorandum explaining the bill's intent. |
| `doc_financial_memorandum_url` | `String` (URL) | `NATIVE_DIRECT` | Financial memorandum or budget impact assessment paper. |
| `doc_explanatory_notes_url` | `String` (URL) | `NATIVE_DIRECT` | Official explanatory notes accompanying the bill text. |
| `fiscal_impact_flag` | `Boolean` | `DERIVED_HUMAN_CODED` / `DERIVED_SYNTHETIC_AI` | Flag indicating binding fiscal expenditure or taxation impact. |
| `regulatory_impact_flag` | `Boolean` | `DERIVED_HUMAN_CODED` / `DERIVED_SYNTHETIC_AI` | Flag indicating binding regulatory compliance burdens. |

---

### Domain 6: Committee Proceedings & Evidence
*Committee scrutiny, evidence submissions, and hearing transparency.*

| Variable Name | Type / Enum Values | Provenance Tier | Description |
| :--- | :--- | :--- | :--- |
| `lead_committee_name` | `String` | `NATIVE_DIRECT` | Name of the primary scrutinising committee assigned to the bill. |
| `committee_referral_date` | `Date` (ISO 8601) | `NATIVE_DIRECT` | Formal date the bill was referred to committee. |
| `committee_report_date` | `Date` (ISO 8601) | `NATIVE_DIRECT` | Date committee reported its findings back to the plenary chamber. |
| `committee_evidence_submissions_count` | `Integer` | `NATIVE_DIRECT` / `DERIVED_DETERMINISTIC` | Total published written evidence submissions received by committee. |
| `committee_public_hearings_count` | `Integer` | `DERIVED_HUMAN_CODED` / `DERIVED_SYNTHETIC_AI` | Number of oral evidence hearing sessions held on the bill. |

---

### Domain 7: Amendments & Legislative Alteration
*Amendment activity, committee vs floor disposition, executive acceptance rates, and text alteration scores.*

| Variable Name | Type / Enum Values | Provenance Tier | Description |
| :--- | :--- | :--- | :--- |
| `amendments_tabled_count` | `Integer` | `NATIVE_DIRECT` | Total count of formal amendments tabled across all stages. |
| `amendments_agreed_count` | `Integer` | `NATIVE_DIRECT` | Total count of amendments formally adopted into the bill text. |
| `amendments_rejected_count` | `Integer` | `NATIVE_DIRECT` | Total count of tabled amendments defeated on a vote. |
| `amendments_withdrawn_count` | `Integer` | `NATIVE_DIRECT` | Total count of amendments withdrawn prior to a vote. |
| `amendments_executive_count` | `Integer` | `DERIVED_DETERMINISTIC` | Count of amendments tabled by government ministers/executive. |
| `amendments_non_executive_count` | `Integer` | `DERIVED_DETERMINISTIC` | Count of amendments tabled by backbenchers/opposition members. *(Formerly: `amendments_backbench_count`)*. |
| `committee_amendments_tabled_count` | `Integer` | `NATIVE_DIRECT` / `DERIVED_DETERMINISTIC` | Count of amendments tabled specifically at committee stage. |
| `committee_amendments_executive_acceptance_rate` | `Float` (0.0 to 1.0) | `DERIVED_HUMAN_CODED` / `DERIVED_DETERMINISTIC` | Proportion of non-executive committee amendments supported by government. |
| `bill_text_alteration_score` | `Float` (0.0 to 1.0) | `DERIVED_DETERMINISTIC` / `DERIVED_SYNTHETIC_AI` | Textual similarity metric (Cosine/Levenshtein) comparing introduced text vs enacted text. |

---

### Domain 8: Divisions, Voting Coalitions & Plenary Debate
*Roll-call voting, party rebellion flags, voting coalition typologies, and debate records.*

| Variable Name | Type / Enum Values | Provenance Tier | Description |
| :--- | :--- | :--- | :--- |
| `divisions_count` | `Integer` | `NATIVE_DIRECT` | Total recorded roll-call division votes held on the bill. |
| `rebellions_flag` | `Boolean` | `DERIVED_DETERMINISTIC` | Presence of governing or opposition party revolts ($\ge 5\%$ party defiance). |
| `voting_coalition_type` | `Enum` (`UNANIMOUS`, `GOVERNMENT_PARTY_LINE`, `CROSS_PARTY_MAJORITY`, `MINORITY_PASSED`, `OPPOSITION_DEFEAT`) | `DERIVED_DETERMINISTIC` / `DERIVED_HUMAN_CODED` | Classification of voting alignment on major bill divisions. |
| `plenary_record_urls` | `Array[String]` (URLs) | `NATIVE_DIRECT` | Direct links to official plenary debate transcripts/Hansard. *(Alias: `hansard_debate_urls`)*. |
