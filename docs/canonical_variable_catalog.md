# Master Canonical Variable Catalog

**Comparative Legislative Data Platform**  
**Version:** 2.5.0  
**Specification:** Dual-Layer & Dual-Entity (Bill + Amendment) Master Variable Dictionary

---

## 1. Dual-Layer & Dual-Entity Architecture

The platform operates on a **Dual-Layer & Dual-Entity Data Architecture** designed to serve both single-country legislative specialists and cross-national quantitative political scientists:

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
                  │  ├─ Entity 1: CanonicalBill (Macro legislative journey) │
                  │  └─ Entity 2: CanonicalAmendment (Micro amendment text) │
                  └─────────────────────────────────────────────────────────┘
```

---

## 2. Scientific Variable Taxonomy Categories

Every variable in the platform is explicitly classified under a 5-part scientific value profile:
1. **`DEFINITIVE_CONSTANT`:** Invariable institutional properties (e.g. Assembly Name, Chamber Structure, Seat Totals).
2. **`CLOSED_ENUM`:** Categorical variables with a strictly declared, exhaustive set of allowed choices (`allowed_values`).
3. **`RESULT_DEPENDENT_DYNAMIC`:** Continuous or discrete empirical measures determined per bill, document, or vote event.
4. **`BINARY_FLAG`:** Boolean indicators (`True` / `False`) for specific procedural triggers.
5. **`PERSISTENT_IDENTIFIER`:** Unique disambiguated pointers linking external authority datasets (Wikidata QIDs, ParlGov Cabinet IDs).

---

## 3. Entity 1: Master Bill-Level Variable Catalog

### Domain 1: Assembly, Electoral & Executive Context
* **`jurisdiction_code`** (`DEFINITIVE_CONSTANT`, String ISO 3166-2): Unique assembly identifier (e.g. `GB-UKP`, `GB-SCT`, `DE-BT`).
* **`parliament_term`** (`RESULT_DEPENDENT_DYNAMIC`, String): Macro electoral legislative period (e.g. `Session 6`, `58th Parliament`).
* **`chamber_type`** (`DEFINITIVE_CONSTANT`, Enum): `[SOVEREIGN_BICAMERAL, DEVOLVED_UNICAMERAL, FEDERAL_UPPER, CONSENSUS_UNICAMERAL]`.
* **`government_type`** (`CLOSED_ENUM`, Enum): Executive arrangement typology:
  * `allowed_values`: `[SINGLE_PARTY_MAJORITY, SINGLE_PARTY_MINORITY, FORMAL_COALITION_MAJORITY, FORMAL_COALITION_MINORITY, CONFIDENCE_AND_SUPPLY, COOPERATION_AGREEMENT, CARETAKER_TECHNOCRATIC]`
* **`parlgov_cabinet_id`** (`PERSISTENT_IDENTIFIER`, String): Canonical cabinet identifier linked from ParlGov authority dataset.

### Domain 2: Bill Identification, Sponsorship & Temporal Origin
* **`local_bill_id`** (`PERSISTENT_IDENTIFIER`, String): Native reference code assigned by host legislature (e.g. `SP Bill 13`, `H.R. 815`).
* **`title_canonical`** (`RESULT_DEPENDENT_DYNAMIC`, String): Standardized English short title.
* **`initiator_type`** (`CLOSED_ENUM`, Enum): Sponsor typology:
  * `allowed_values`: `[EXECUTIVE, INDIVIDUAL_MEMBER, GROUP_MEMBERS, COMMITTEE, PRIVATE_ORGANISATION]`
* **`initiator_party_governance_role`** (`CLOSED_ENUM`, Enum): Sponsor alignment on introduction date $T_{\text{Intro}}$:
  * `allowed_values`: `[GOVERNING_PARTY, OPPOSITION_PARTY, CROSS_PARTY]`
* **`initiator_member_id`** (`PERSISTENT_IDENTIFIER`, String): Wikidata QID for primary sponsor MP/MSP.

### Domain 3: Progression, Timelines & Stage Milestones
* **`date_introduced`** (`RESULT_DEPENDENT_DYNAMIC`, Date ISO 8601): Formal introduction date.
* **`date_final_outcome`** (`RESULT_DEPENDENT_DYNAMIC`, Date ISO 8601): Date of final passage, defeat, or withdrawal.
* **`duration_calendar_days`** (`RESULT_DEPENDENT_DYNAMIC`, Integer): Calendar days elapsed from introduction to outcome.
* **`duration_sitting_days`** (`RESULT_DEPENDENT_DYNAMIC`, Integer): Formal parliamentary sitting days elapsed.
* **`stage_milestones`** (`RESULT_DEPENDENT_DYNAMIC`, Array of Objects): Stage-by-stage progression interval breakdown (`stage_sequence`, `stage_canonical`, `date_start`, `date_end`, `duration_sitting_days`).
* **`programme_motion_flag`** (`BINARY_FLAG`, Boolean): Timetabling or programme motion imposed.
* **`guillotine_invoked_flag`** (`BINARY_FLAG`, Boolean): Debate closure or guillotine motion invoked.
* **`emergency_procedure_flag`** (`BINARY_FLAG`, Boolean): Fast-track or urgency procedure invoked.
* **`prior_executive_consent_required_flag`** (`BINARY_FLAG`, Boolean): Prior executive or Crown consent required.

### Domain 4: Final Disposition & Inter-Chamber Mechanisms
* **`final_status`** (`CLOSED_ENUM`, Enum): Terminal procedural status:
  * `allowed_values`: `[ENACTED, DEFEATED, WITHDRAWN, LAPSED, PENDING, VETOED]`
* **`termination_mechanism`** (`CLOSED_ENUM`, Enum): Procedural termination event:
  * `allowed_values`: `[ENACTMENT, VOTE_DEFEAT, EXECUTIVE_WITHDRAWAL, DISSOLUTION_LAPSE]`
* **`head_of_state_promulgation_date`** (`RESULT_DEPENDENT_DYNAMIC`, Date ISO 8601): Date of Royal Assent, Presidential Signature, or Promulgation.
* **`chamber_ping_pong_count`** (`RESULT_DEPENDENT_DYNAMIC`, Integer): Number of amendment exchanges between chambers.

### Domain 5: Bill Documentation & Text Size Analytics
* **`doc_as_introduced_url`** (`PERSISTENT_IDENTIFIER`, URL): Official text of the Bill as introduced.
* **`doc_as_passed_url`** (`PERSISTENT_IDENTIFIER`, URL): Official text of the Bill as enacted or passed.
* **`word_count_introduced`** (`RESULT_DEPENDENT_DYNAMIC`, Integer): Word count of bill text as introduced.
* **`word_count_post_committee`** (`RESULT_DEPENDENT_DYNAMIC`, Integer): Word count of bill text post-committee stage.
* **`word_count_enacted`** (`RESULT_DEPENDENT_DYNAMIC`, Integer): Word count of final enacted Act.
* **`text_expansion_ratio`** (`RESULT_DEPENDENT_DYNAMIC`, Float): Ratio of enacted text vs introduced text ($\frac{\text{word\_count\_enacted}}{\text{word\_count\_introduced}}$).
* **`cap_topic_code`** (`PERSISTENT_IDENTIFIER`, String): Policy topic code mapped to Comparative Agendas Project taxonomy.
* **`fiscal_impact_flag`** (`BINARY_FLAG`, Boolean): Flag indicating binding fiscal expenditure or taxation impact.

### Domain 6: Committee Scrutiny & Evidence
* **`lead_committee_name`** (`RESULT_DEPENDENT_DYNAMIC`, String): Name of primary scrutinising committee.
* **`committee_evidence_submissions_count`** (`RESULT_DEPENDENT_DYNAMIC`, Integer): Published written evidence submissions received.

### Domain 7: Macro Bill Amendment Aggregates
* **`amendments_tabled_count`** (`RESULT_DEPENDENT_DYNAMIC`, Integer): Total amendments lodged across all stages.
* **`amendments_agreed_count`** (`RESULT_DEPENDENT_DYNAMIC`, Integer): Total amendments formally adopted.
* **`amendments_non_executive_count`** (`RESULT_DEPENDENT_DYNAMIC`, Integer): Total non-executive amendments tabled.
* **`committee_amendments_executive_acceptance_rate`** (`RESULT_DEPENDENT_DYNAMIC`, Float 0-1): Proportion of non-executive committee amendments supported by government.
* **`bill_text_alteration_score`** (`RESULT_DEPENDENT_DYNAMIC`, Float 0-1): Text similarity score comparing introduced vs enacted text.

### Domain 8: Temporal Divisions, Motion Types & Voting Coalitions
* **`divisions_count`** (`RESULT_DEPENDENT_DYNAMIC`, Integer): Total roll-call division votes held on the bill.
* **`motion_type`** (`CLOSED_ENUM`, Enum): Stage division motion classification:
  * `allowed_values`: `[STAGE_1_AGREEMENT, FINANCIAL_RESOLUTION, EMERGENCY_BILL_DESIGNATION, STAGE_2_AMENDMENT, STAGE_3_PASSAGE]`
* **`effective_majority_margin_at_event_date`** (`RESULT_DEPENDENT_DYNAMIC`, Integer): Floor majority margin ($\text{Governing Seats}_T - \text{Opposition Seats}_T$) evaluated on division date $T$.
* **`party_dissent_rate_at_event_date`** (`RESULT_DEPENDENT_DYNAMIC`, Float 0-1): Proportion of party members voting against frontbench line on division date $T$.
* **`voting_coalition_type`** (`CLOSED_ENUM`, Enum): Voting alignment:
  * `allowed_values`: `[UNANIMOUS, GOVERNMENT_PARTY_LINE, CROSS_PARTY_MAJORITY]`

---

## 4. Entity 2: Master Amendment-Level Variable Catalog (Domain 9)

### Domain 9: Granular Amendment Entity Variables (`CanonicalAmendment`)

* **`canonical_amendment_id`** (`PERSISTENT_IDENTIFIER`, String): Unique persistent amendment identifier (e.g. `GB-SCT-S6-SPB13-AMD-042`).
* **`local_amendment_number`** (`RESULT_DEPENDENT_DYNAMIC`, String): Native marshaled amendment number (e.g. `Amd 42`, `LOD 104`).
* **`bill_id`** (`PERSISTENT_IDENTIFIER`, String): Parent bill identifier link (`local_bill_id`).
* **`stage_canonical`** (`CLOSED_ENUM`, Enum): Stage of consideration:
  * `allowed_values`: `[COMMITTEE_STAGE, REPORT_STAGE, FINAL_PASSAGE]`
* **`stage_raw`** (`RESULT_DEPENDENT_DYNAMIC`, String): Raw native stage description (e.g. "Stage 2 Equalities Committee Day 3").
* **`committee_name`** (`RESULT_DEPENDENT_DYNAMIC`, String): Name of scrutinising committee (e.g. "Equalities, Human Rights and Civil Justice Committee").
* **`date_tabled`** (`RESULT_DEPENDENT_DYNAMIC`, Date ISO 8601): Date amendment formally lodged.
* **`date_decided`** (`RESULT_DEPENDENT_DYNAMIC`, Date ISO 8601): Date amendment voted on or disposed.

* **`sponsor_member_id`** (`PERSISTENT_IDENTIFIER`, String): Wikidata QID for lead MSP sponsor.
* **`sponsor_name`** (`RESULT_DEPENDENT_DYNAMIC`, String): Full name of lead sponsor.
* **`sponsor_party_on_tabling_date`** (`RESULT_DEPENDENT_DYNAMIC`, String): Party affiliation of sponsor evaluated on date Tabled.
* **`sponsor_governance_role`** (`CLOSED_ENUM`, Enum): Sponsor's institutional alignment:
  * `allowed_values`: `[EXECUTIVE_MINISTER, GOVERNING_BACKBENCH, OPPOSITION_MEMBER, CROSS_PARTY]`
* **`co_sponsors_count`** (`RESULT_DEPENDENT_DYNAMIC`, Integer): Count of supporting co-signatory members.

* **`target_clause_or_schedule`** (`RESULT_DEPENDENT_DYNAMIC`, String): Target structural location in Bill (e.g. "Section 4, Page 3, Line 12").
* **`amendment_action_type`** (`CLOSED_ENUM`, Enum): Proposed text action:
  * `allowed_values`: `[INSERTION, DELETION, SUBSTITUTION, PROBING]`
* **`full_text_proposed`** (`RESULT_DEPENDENT_DYNAMIC`, String): Full text of proposed amendment.

* **`government_position`** (`CLOSED_ENUM`, Enum): Executive stance during debate:
  * `allowed_values`: `[SUPPORTED, OPPOSED, NEUTRAL_NO_STANCE, MINISTERIAL_OWN_AMENDMENT]`

* **`disposition_canonical`** (`CLOSED_ENUM`, Enum): Final amendment disposition outcome:
  * `allowed_values`: `[AGREED_TO, DEFEATED, WITHDRAWN, NOT_MOVED, FALLEN]`
* **`decision_mechanism`** (`CLOSED_ENUM`, Enum): Procedural decision mechanism:
  * `allowed_values`: `[VOICE_VOTE_UNANIMOUS, DIVISION_ROLL_CALL, WITHDRAWN_WITHOUT_VOTE]`

* **`division_id`** (`PERSISTENT_IDENTIFIER`, String): Linked roll-call division record ID (if division held).
* **`aye_count` / `no_count` / `abstain_count`** (`RESULT_DEPENDENT_DYNAMIC`, Integers): Vote tallies.
* **`party_dissent_rate_on_amendment`** (`RESULT_DEPENDENT_DYNAMIC`, Float 0-1): Proportion of governing party members rebelling against frontbench whip on this amendment division.
