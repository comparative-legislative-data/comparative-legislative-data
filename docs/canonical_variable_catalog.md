# Master Canonical Variable Catalog

**Comparative Legislative Data Platform**  
*Version 1.0.0 (Clean-Slate Reset — Draft for Peer Review)*

---

## Executive Summary & Core Philosophy

This catalog defines the **Master Canonical Variable Wishlist** for quantitative legislative analysis. It represents the comprehensive, globally neutral inventory of variables sought by political scientists, legislative scholars, and data engineers studying parliamentary lawmaking.

### The 5-Tier Data Availability & Provenance Framework

Every variable in this catalog is evaluated per legislature against a strict 5-tier spectrum:

1. **`CANONICAL_WISHLIST_TARGET`:** Universal variable definition in this catalog.
2. **`NATIVE_DIRECT`:** Available directly in the host assembly’s official API or raw feed (JSON/XML).
3. **`DERIVED_DETERMINISTIC`:** Generated deterministically via simple pipeline transformations, date math, or joins against persistent datasets (e.g. Executive Rosters). Includes an explicit confidence rating (`HIGH`, `MEDIUM`, `LOW`).
4. **`DERIVED_SYNTHETIC_AI`:** Synthesized using advanced NLP/LLM text processing, topic modeling, or structural parsing of unstructured Hansard/PDF text.
5. **`UNAVAILABLE_HARD_GAP`:** Missing natively from the host assembly, unrecorded, or resource-prohibitive to generate (Documented Open Data Gap).

---

## Domain 1: Assembly & Electoral Context

| Canonical Variable Name | Data Type | Academic Rationale & Description | Example Values |
| :--- | :--- | :--- | :--- |
| `jurisdiction_code` | String (ISO) | ISO-style unique country/sub-national code for comparative cross-national filtering. | `GB-UKP`, `GB-SCT`, `GB-WLS`, `DE-BT`, `US-FED` |
| `assembly_name` | String | Official native name of the legislative body. | `Scottish Parliament`, `House of Commons`, `Bundestag` |
| `chamber_type` | Enum | Classification of chamber structure. | `SOVEREIGN_BICAMERAL`, `DEVOLVED_UNICAMERAL`, `FEDERAL_UPPER` |
| `parliament_term` | String | Macro electoral period spanning general elections. | `58th Parliament`, `Session 6`, `118th Congress` |
| `session_subperiod` | String | Sessional sub-period within a parliament term. | `Session 2022-23`, `1st Session` |
| `session_start_date` | Date | Formal opening / swearing-in date of the parliamentary term or session. | `2021-05-13` |
| `session_end_date` | Date | Prorogation or dissolution date of the term or session. | `2026-05-07` |

---

## Domain 2: Bill Identification, Sponsorship & Origin

| Canonical Variable Name | Data Type | Academic Rationale & Description | Example Values |
| :--- | :--- | :--- | :--- |
| `local_bill_id` | String | Official reference assigned by host legislature. | `SP Bill 13`, `Bill 102`, `H.R. 815` |
| `title_canonical` | String | Primary title of the bill in English (or standardized English translation). | `Gender Recognition Reform (Scotland) Bill` |
| `title_native` | String | Title in official native language of the host jurisdiction. | `Bille Diwygio Senedd Cymru 2024` |
| `initiator_type` | Enum | Globally neutral sponsor classification. | `EXECUTIVE`, `INDIVIDUAL_MEMBER`, `GROUP_MEMBERS`, `COMMITTEE`, `PRIVATE_HYBRID` |
| `initiator_party_governance_role` | Enum | Alignment of primary sponsor relative to executive power at introduction. | `GOVERNING_PARTY`, `OPPOSITION_PARTY`, `CROSS_PARTY`, `NON_PARTISAN` |
| `initiator_member_id` | String | Persistent disambiguated member identifier (Wikidata QID / native ID). | `Q7500342` / `PersonID:1870` |
| `initiator_name` | String | Primary sponsor or minister name string. | `Shona Robison MSP` |
| `co_sponsorship_count` | Integer | Total number of formal co-sponsors attached to the bill. | `14` |
| `cross_party_sponsorship_count` | Integer | Number of co-sponsors from opposition parties relative to primary sponsor. | `3` |

---

## Domain 3: Procedural Progression & Timelines

| Canonical Variable Name | Data Type | Academic Rationale & Description | Example Values |
| :--- | :--- | :--- | :--- |
| `date_introduced` | Date | Formal submission or introduction date into the primary chamber. | `2022-03-03` |
| `date_final_outcome` | Date | Date of final disposition (Enactment, Defeat, Withdrawal) or `NULL` if pending. | `2022-12-22` |
| `duration_calendar_days` | Integer | Calculated calendar days elapsed between introduction and final outcome. | `294` |
| `duration_sitting_days` | Integer | Calculated actual parliamentary sitting days elapsed (excluding recesses). | `68` |
| `suspension_interrupted_flag` | Boolean | Flags whether bill passage spanned a formal parliamentary recess, prorogation, or election suspension. | `true` / `false` |
| `stage_milestones` | Array[Object] | Ordered array of milestone events: `stage_canonical`, `stage_raw`, `chamber`, `date_stage`, `proceedings_url`. | `[{"stage_canonical": "FIRST_READING", "date": "2022-03-03"}]` |

---

## Domain 4: Final Disposition & Termination Mechanisms

| Canonical Variable Name | Data Type | Academic Rationale & Description | Example Values |
| :--- | :--- | :--- | :--- |
| `final_status` | Enum | Standardized terminal disposition of the legislation. | `ENACTED`, `DEFEATED`, `WITHDRAWN`, `LAPSED`, `PENDING` |
| `termination_mechanism` | Enum | Procedural mechanism resulting in bill termination or enactment. | `ENACTMENT`, `VOTE_DEFEAT`, `EXECUTIVE_WITHDRAWAL`, `SESSION_EXPIRY`, `SECTION_35_VETO` |
| `royal_assent_date` | Date | Date of formal Royal Assent or Presidential Promulgation. | `2023-01-15` |

---

## Domain 5: Bill Documentation & Papers Chain

| Canonical Variable Name | Data Type | Academic Rationale & Description | Example Values |
| :--- | :--- | :--- | :--- |
| `doc_as_introduced_url` | String (URL) | Direct link to official text of the Bill as first introduced. | `https://parliament.scot/bills/.../introduced.pdf` |
| `doc_as_passed_url` | String (URL) | Direct link to final text of the Bill as passed by the legislature. | `https://parliament.scot/bills/.../passed.pdf` |
| `doc_policy_memorandum_url` | String (URL) | Direct link to official Policy Memorandum explaining bill rationale. | `https://parliament.scot/bills/.../policy_memo.pdf` |
| `doc_financial_memorandum_url` | String (URL) | Direct link to Financial Memorandum detailing public cost estimates. | `https://parliament.scot/bills/.../financial_memo.pdf` |
| `doc_explanatory_notes_url` | String (URL) | Direct link to official Explanatory Notes on bill clauses. | `https://parliament.scot/bills/.../notes.pdf` |
| `doc_marshalled_amendments_urls` | Array[String] | Array of links to official Marshalled Lists of Amendments for Stage 2/3. | `["https://.../amendments_list1.pdf"]` |

---

## Domain 6: Committee Proceedings & Evidence

| Canonical Variable Name | Data Type | Academic Rationale & Description | Example Values |
| :--- | :--- | :--- | :--- |
| `lead_committee_name` | String | Name of the primary scrutinising committee assigned to the bill. | `Equalities, Human Rights and Civil Justice Committee` |
| `committee_referral_date` | Date | Date bill was formally remitted to lead committee. | `2022-03-08` |
| `committee_report_date` | Date | Date lead committee published Stage 1 / scrutiny report. | `2022-10-06` |
| `committee_report_url` | String (URL) | Direct link to published committee scrutiny report. | `https://parliament.scot/committees/.../report.pdf` |
| `committee_evidence_submissions_count` | Integer | Total count of published written evidence submissions received by committee. | `1450` |

---

## Domain 7: Amendments & Legislative Alteration

| Canonical Variable Name | Data Type | Academic Rationale & Description | Example Values |
| :--- | :--- | :--- | :--- |
| `amendments_tabled_count` | Integer | Total number of individual amendments submitted across all stages. | `154` |
| `amendments_agreed_count` | Integer | Number of amendments formally agreed / accepted into the bill text. | `42` |
| `amendments_rejected_count` | Integer | Number of amendments formally defeated or disagreed to in division/voice vote. | `88` |
| `amendments_withdrawn_count` | Integer | Number of amendments withdrawn by sponsor without vote. | `24` |
| `amendments_executive_count` | Integer | Amendments tabled by government ministers. | `30` |
| `amendments_backbench_count` | Integer | Amendments tabled by non-executive backbench MSPs/MPs. | `124` |
| `bill_text_alteration_score` | Float | Derived metric of text change from introduction to passage (Levenshtein/Cosine similarity). | `0.18` (18% text alteration) |

---

## Domain 8: Divisions, Voting Coalitions & Hansard Debates

| Canonical Variable Name | Data Type | Academic Rationale & Description | Example Values |
| :--- | :--- | :--- | :--- |
| `divisions_count` | Integer | Total roll-call division votes held during bill passage. | `14` |
| `division_records` | Array[Object] | Array of recorded divisions: `division_id`, `stage`, `yeas`, `nays`, `abstentions`, `passed_flag`. | `[{"division_id": "S6V-120", "yeas": 86, "nays": 39}]` |
| `rebellions_flag` | Boolean | Flags whether any division experienced governing or opposition party revolts (>=5% party defiance). | `true` |
| `voting_coalition_type` | Enum | Derived classification of parliamentary voting alignment. | `UNANIMOUS`, `GOVERNMENT_PARTY_LINE`, `CROSS_PARTY_MAJORITY`, `MINORITY_PASSED` |
| `hansard_debate_urls` | Array[String] | Array of direct links to speech-level Hansard debate transcripts. | `["https://parliament.scot/hansard/..."]` |

---

## Feedback & Revision Instructions

This draft catalog is open for academic peer review and domain expert revision. Please flag any missing variables, terminology refinements, or structural adjustments.
