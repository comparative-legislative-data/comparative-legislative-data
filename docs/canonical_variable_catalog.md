# Master Canonical Variable Catalog

**Comparative Legislative Data Platform**  
**Version:** 2.6.0  
**Specification:** Dual-Layer & Triple-Entity (Bill + Amendment + Proceedings) Master Variable Dictionary

---

## 1. Multi-Entity Architecture

The platform operates on a **Multi-Entity Architecture**:
1. **`CanonicalBill` (Macro Level):** Tracks the complete legislative journey, multi-day stage intervals, accompanying documents, and floor vote outcomes.
2. **`CanonicalAmendment` (Micro Level):** Tracks individual amendment lodgings, Marshalled List numbers, target clauses, text alterations, government positions, and division votes.
3. **`ParsedProceedings` (Hansard Text Level):** Tracks official report debate transcripts, speech interventions, word count shares, and speaker roles.

---

## 2. Scientific Variable Taxonomy Categories

Every variable is classified under a 5-part scientific value profile:
1. **`DEFINITIVE_CONSTANT`:** Invariable institutional properties (e.g. Assembly Name, Seat Totals).
2. **`CLOSED_ENUM`:** Categorical variables with an explicit list of allowed choices (`allowed_values`).
3. **`RESULT_DEPENDENT_DYNAMIC`:** Continuous or discrete empirical measures determined per bill, document, or vote event.
4. **`BINARY_FLAG`:** Boolean indicators (`True` / `False`) for specific procedural triggers.
5. **`PERSISTENT_IDENTIFIER`:** Unique disambiguated pointers linking external authority datasets.

---

## 3. Entity 1: Master Bill-Level Variable Catalog (`CanonicalBill`)

### Domain 1: Assembly, Electoral & Executive Context
* **`jurisdiction_code`** (`DEFINITIVE_CONSTANT`, String ISO 3166-2): Assembly code (`GB-SCT`, `GB-UKP`, `DE-BT`).
* **`parliament_term`** (`RESULT_DEPENDENT_DYNAMIC`, String): Electoral period identifier (e.g. `Session 6`).
* **`term_start_date`** (`RESULT_DEPENDENT_DYNAMIC`, Date ISO 8601): Term start date.
* **`term_end_date`** (`RESULT_DEPENDENT_DYNAMIC`, Date ISO 8601): Term end date.
* **`chamber_type`** (`DEFINITIVE_CONSTANT`, Enum): `[SOVEREIGN_BICAMERAL, DEVOLVED_UNICAMERAL, FEDERAL_UPPER, CONSENSUS_UNICAMERAL]`.
* **`devolved_executive_name`** (`RESULT_DEPENDENT_DYNAMIC`, String): Historical executive entity name (`"Scottish Executive"` 1999–2007; `"Scottish Government"` 2007–Present).
* **`government_type`** (`CLOSED_ENUM`, Enum): Executive arrangement typology (`SINGLE_PARTY_MAJORITY`, `SINGLE_PARTY_MINORITY`, `FORMAL_COALITION_MAJORITY`, `FORMAL_COALITION_MINORITY`, `CONFIDENCE_AND_SUPPLY`, `COOPERATION_AGREEMENT`, `CARETAKER_TECHNOCRATIC`).
* **`governing_parties_list`** (`RESULT_DEPENDENT_DYNAMIC`, Array of Strings): Array of governing coalition parties.
* **`parlgov_cabinet_id`** (`PERSISTENT_IDENTIFIER`, String): ParlGov cabinet identifier.

### Domain 2: Bill Identification, Sponsorship & Temporal Origin
* **`local_bill_id`** (`PERSISTENT_IDENTIFIER`, String): Native reference code (e.g. `SP Bill 13`).
* **`title_canonical`** (`RESULT_DEPENDENT_DYNAMIC`, String): Standardized short title.
* **`initiator_type`** (`CLOSED_ENUM`, Enum): Sponsor typology (`EXECUTIVE`, `INDIVIDUAL_MEMBER`, `COMMITTEE`, `PRIVATE_ORGANISATION`).
* **`initiator_party_governance_role`** (`CLOSED_ENUM`, Enum): Sponsor party alignment on introduction date ($T_{\text{Intro}}$).
* **`initiator_member_id`** (`PERSISTENT_IDENTIFIER`, String): Lead MSP sponsor Wikidata QID.
* **`initiator_convener_member_id`** (`PERSISTENT_IDENTIFIER`, String): Lead Committee Convener MSP Wikidata QID (for Committee Bills).
* **`initiator_organisation_name`** (`RESULT_DEPENDENT_DYNAMIC`, String): Name of Initiating Committee or External Promoter.

### Domain 3: Progression, Stage Timelines & Multi-Day Debates
* **`date_introduced`** (`RESULT_DEPENDENT_DYNAMIC`, Date ISO 8601): Introduction date.
* **`date_final_outcome`** (`RESULT_DEPENDENT_DYNAMIC`, Date ISO 8601): Final outcome date.
* **`duration_calendar_days`** (`RESULT_DEPENDENT_DYNAMIC`, Integer): Calendar days elapsed.
* **`duration_sitting_days`** (`RESULT_DEPENDENT_DYNAMIC`, Integer): Parliamentary sitting days elapsed.
* **`stage_1_lead_committee_report_date`** (`RESULT_DEPENDENT_DYNAMIC`, Date ISO 8601): Stage 1 report publication date.
* **`stage_1_debate_start_date` / `stage_1_debate_end_date`** (`RESULT_DEPENDENT_DYNAMIC`, Dates): Stage 1 debate start and end dates.
* **`stage_1_debate_days_count`** (`RESULT_DEPENDENT_DYNAMIC`, Integer): Number of sitting days Stage 1 debate straddled.
* **`stage_2_committee_start_date` / `stage_2_committee_end_date`** (`RESULT_DEPENDENT_DYNAMIC`, Dates): Stage 2 committee start and end dates.
* **`stage_3_plenary_debate_start_date` / `stage_3_plenary_debate_end_date`** (`RESULT_DEPENDENT_DYNAMIC`, Dates): Stage 3 debate start and end dates.
* **`stage_3_debate_days_count`** (`RESULT_DEPENDENT_DYNAMIC`, Integer): Number of sitting days Stage 3 debate straddled.
* **`royal_assent_date`** (`RESULT_DEPENDENT_DYNAMIC`, Date ISO 8601): Royal Assent date.
* **`emergency_procedure_flag`** (`BINARY_FLAG`, Boolean): Emergency Bill designation under Rule 9.21.
* **`section_35_order_triggered_flag`** (`BINARY_FLAG`, Boolean): Section 35 Scotland Act Order issued blocking Royal Assent.
* **`programme_motion_flag` / `guillotine_invoked_flag`** (`INSTITUTIONAL_HARD_GAP` for Holyrood): Assembly procedural omissions.

### Domain 4: Financial Resolutions (Rule 9.12)
* **`financial_resolution_required_flag`** (`BINARY_FLAG`, Boolean): Financial Resolution motion required.
* **`financial_resolution_approved_flag`** (`BINARY_FLAG`, Boolean): Financial Resolution approved.
* **`financial_resolution_vote_date`** (`RESULT_DEPENDENT_DYNAMIC`, Date ISO 8601): Vote date.
* **`financial_resolution_aye_count` / `no_count` / `abstain_count`** (`RESULT_DEPENDENT_DYNAMIC`, Integers): Vote tallies.

### Domain 5: Standardised Decision-Point Roll-Call Votes
* **`decision_point_motion_type`** (`CLOSED_ENUM`, Enum): `[STAGE_1_AGREEMENT, FINANCIAL_RESOLUTION, EMERGENCY_BILL_DESIGNATION, STAGE_3_PASSAGE]`.
* **`decision_point_vote_date`** (`RESULT_DEPENDENT_DYNAMIC`, Date ISO 8601): Vote date $T$.
* **`decision_point_result`** (`CLOSED_ENUM`, Enum): `[PASSED, DEFEATED]`.
* **`decision_point_party_cohesion_rate`** (`RESULT_DEPENDENT_DYNAMIC`, Float 0-1): Party unity rate.
* **`decision_point_voting_coalition_type`** (`CLOSED_ENUM`, Enum): `[UNANIMOUS, GOVERNMENT_PARTY_LINE, CROSS_PARTY_MAJORITY]`.
* **`individual_msp_votes_array`** (`RESULT_DEPENDENT_DYNAMIC`, Array of Objects): Member vote choices paired with party status evaluated on date $T$.

### Domain 6: Accompanying Bill Documents & Size Analytics
* **`doc_as_introduced_url` / `doc_as_passed_url`** (`PERSISTENT_IDENTIFIER`, URLs): Primary Bill text URLs.
* **`policy_memorandum_url`** (`PERSISTENT_IDENTIFIER`, URL): Policy Memorandum document URL & word count.
* **`financial_memorandum_url`** (`PERSISTENT_IDENTIFIER`, URL): Standalone Financial Memorandum URL & word count.
* **`explanatory_notes_url`** (`PERSISTENT_IDENTIFIER`, URL): Standalone Explanatory Notes URL & word count.
* **`combined_financial_explanatory_notes_url`** (`PERSISTENT_IDENTIFIER`, URL): Historical legacy combined notes URL.
* **`delegated_powers_memorandum_url`** (`PERSISTENT_IDENTIFIER`, URL): Delegated Powers Memorandum URL & word count.
* **`stage_1_lead_committee_report_url`** (`PERSISTENT_IDENTIFIER`, URL): Lead Committee Stage 1 Report URL & word count.
* **`bill_as_introduced_word_count` / `bill_as_amended_stage_2_word_count` / `bill_as_enacted_word_count`** (`RESULT_DEPENDENT_DYNAMIC`, Integers): Text word counts across stages.
* **`text_expansion_ratio`** (`RESULT_DEPENDENT_DYNAMIC`, Float): Text growth ratio.
* **`cap_topic_code`** (`PERSISTENT_IDENTIFIER`, String): CAP policy topic code.
* **`fiscal_impact_flag`** (`BINARY_FLAG`, Boolean): Binding fiscal impact flag.

### Domain 7: Final Disposition
* **`final_status`** (`CLOSED_ENUM`, Enum): `[ENACTED, DEFEATED, WITHDRAWN, LAPSED, PENDING, VETOED]`.
* **`termination_mechanism`** (`CLOSED_ENUM`, Enum): `[ENACTMENT, VOTE_DEFEAT, EXECUTIVE_WITHDRAWAL, DISSOLUTION_LAPSE]`.

### Domain 8: Macro Amendment Aggregates
* **`amendments_tabled_count` / `amendments_agreed_count` / `amendments_non_executive_count`** (`RESULT_DEPENDENT_DYNAMIC`, Integers): Macro amendment tallies.
* **`committee_amendments_executive_acceptance_rate`** (`RESULT_DEPENDENT_DYNAMIC`, Float 0-1): Non-executive committee amendment government acceptance rate.
* **`bill_text_alteration_score`** (`RESULT_DEPENDENT_DYNAMIC`, Float 0-1): Text alteration similarity score.

---

## 4. Entity 2: Master Amendment-Level Variable Catalog (`CanonicalAmendment`)

### Domain 9: Micro Amendment Entity Records
* **`canonical_amendment_id`** (`PERSISTENT_IDENTIFIER`, String): Persistent amendment ID.
* **`local_amendment_number`** (`RESULT_DEPENDENT_DYNAMIC`, String): Holyrood Marshalled List amendment number.
* **`bill_id`** (`PERSISTENT_IDENTIFIER`, String): Parent bill link.
* **`marshalled_list_url`** (`PERSISTENT_IDENTIFIER`, URL): Source Marshalled List document URL.
* **`stage_canonical`** (`CLOSED_ENUM`, Enum): `[COMMITTEE_STAGE, REPORT_STAGE, FINAL_PASSAGE]`.
* **`stage_raw`** (`RESULT_DEPENDENT_DYNAMIC`, String): Native stage text.
* **`committee_name`** (`RESULT_DEPENDENT_DYNAMIC`, String): Scrutinising committee name.
* **`date_tabled` / `date_decided`** (`RESULT_DEPENDENT_DYNAMIC`, Dates): Lodging and decision dates.
* **`sponsor_member_id`** (`PERSISTENT_IDENTIFIER`, String): Lead MSP sponsor Wikidata QID.
* **`sponsor_name`** (`RESULT_DEPENDENT_DYNAMIC`, String): Lead sponsor full name.
* **`sponsor_party_on_tabling_date`** (`RESULT_DEPENDENT_DYNAMIC`, String): Party status on tabling date.
* **`sponsor_governance_role`** (`CLOSED_ENUM`, Enum): `[EXECUTIVE_MINISTER, GOVERNING_BACKBENCH, OPPOSITION_MEMBER, CROSS_PARTY]`.
* **`co_sponsors_count`** (`RESULT_DEPENDENT_DYNAMIC`, Integer): Count of co-signing MSPs.
* **`target_clause_or_schedule`** (`RESULT_DEPENDENT_DYNAMIC`, String): Target structural location in Bill.
* **`amendment_action_type`** (`CLOSED_ENUM`, Enum): `[INSERTION, DELETION, SUBSTITUTION]`.
* **`government_position`** (`CLOSED_ENUM`, Enum): `[SUPPORTED, OPPOSED, NEUTRAL_NO_STANCE, MINISTERIAL_OWN_AMENDMENT]`.
* **`disposition_canonical`** (`CLOSED_ENUM`, Enum): `[AGREED_TO, DEFEATED, WITHDRAWN, NOT_MOVED, FALLEN]`.
* **`decision_mechanism`** (`CLOSED_ENUM`, Enum): `[VOICE_VOTE_UNANIMOUS, DIVISION_ROLL_CALL, WITHDRAWN_WITHOUT_VOTE]`.
* **`division_id`** (`PERSISTENT_IDENTIFIER`, String): Linked roll-call division record ID.
* **`aye_count` / `no_count` / `abstain_count`** (`RESULT_DEPENDENT_DYNAMIC`, Integers): Vote tallies.
* **`party_dissent_rate_on_amendment`** (`RESULT_DEPENDENT_DYNAMIC`, Float 0-1): Governing party rebellion rate on this amendment.

---

## 5. Domain 10: Parsed Proceedings & Official Report Analytics (`ParsedProceedings`)

* **`official_report_proceedings_url`** (`PERSISTENT_IDENTIFIER`, URL): Official Report Hansard transcript URL.
* **`proceedings_total_word_count`** (`RESULT_DEPENDENT_DYNAMIC`, Integer): Debate proceedings total word count.
* **`proceedings_interventions_count`** (`RESULT_DEPENDENT_DYNAMIC`, Integer): Recorded speech interventions count.
* **`proceedings_msps_speaking_count`** (`RESULT_DEPENDENT_DYNAMIC`, Integer): Unique participating MSPs count.
* **`executive_ministers_word_count_share`** (`RESULT_DEPENDENT_DYNAMIC`, Float 0-1): Proportion of debate word count spoken by Executive Ministers.
* **`backbench_msps_word_count_share`** (`RESULT_DEPENDENT_DYNAMIC`, Float 0-1): Proportion of debate word count spoken by backbench/opposition MSPs.
