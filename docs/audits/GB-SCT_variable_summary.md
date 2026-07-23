# Scottish Parliament (GB-SCT) Audit Variable Summary

**Specification Version:** 2.8.0  
**Audit Stage:** 100% Fully Audited Baseline (Pass 1 & Pass 2 Complete)  
**Last Updated:** July 24, 2026

---

## 2-Pass Empirical Audit Provenance Matrix

All **119 institutional research variables** across 4 core entities (`CanonicalBill`, `CanonicalAmendment`, `CommitteeContext`, `ParsedProceedings`) and procedural hard gaps have been evaluated through our 2-pass audit methodology against the 13 official Scottish Parliament Open Data API endpoints (`data.parliament.scot/api`), Official Report Chamber Voting Logs, and PDF Marshalled Amendment Lists.

```
┌───────────────────────────────────────────────────────────────────────────┐
│                 GB-SCT 2-PASS EMPIRICAL AUDIT DISTRIBUTION                 │
├───────────────────────────┬───────────────┬───────────────────────────────┤
│ PROVENANCE TIER           │ COUNT         │ PERCENTAGE                    │
├───────────────────────────┼───────────────┼───────────────────────────────┤
│ NATIVE_DIRECT             │ 51 Variables  │ 42.9%                         │
│ DERIVED_DETERMINISTIC     │ 21 Variables  │ 17.6%                         │
│ DERIVED_EXTRACTED         │ 40 Variables  │ 33.6%                         │
│ LINKED_EXTERNAL_AUTHORITY │ 5 Variables   │ 4.2%                          │
│ UNAVAILABLE_HARD_GAP      │ 2 Variables   │ 1.7%                          │
├───────────────────────────┼───────────────┼───────────────────────────────┤
│ TOTAL AUDITED             │ 119 Variables │ 100.0% (0 Uncategorised)      │
└───────────────────────────┴───────────────┴───────────────────────────────┘
```

---

## 1. `NATIVE_DIRECT` (51 Variables — 42.9%)
Raw host variables served directly out-of-the-box in the official API feeds:
- **Assembly & Executive Context:** `jurisdiction_code`, `name`, `chamber_type`, `statutory_seats_total`, `presiding_officer_neutral_count`, `parliament_term`, `term_start_date`, `term_end_date`, `devolved_executive_name`
- **Bill Sponsorship & Member Attributes:** `local_bill_id`, `title_canonical`, `official_long_title`, `third_party_organisation`, `initiator_organisation_name`, `msp_birth_date`, `msp_gender`, `msp_photo_url`, `party_abbreviation`
- **Progression & Stage Dates:** `date_introduced`, `date_final_outcome`, `royal_assent_date`, `stage_1_lead_committee_report_date`, `stage_1_debate_start_date`, `stage_1_debate_end_date`, `stage_2_committee_start_date`, `stage_2_committee_end_date`, `stage_3_plenary_debate_start_date`, `stage_3_plenary_debate_end_date`
- **Financial Resolutions & Roll-Call Voting:** `financial_resolution_vote_date`, `financial_resolution_aye_count`, `financial_resolution_no_count`, `financial_resolution_abstain_count`
- **Document Stage Prints:** `doc_as_introduced_url`, `doc_as_amended_stage_2_url`, `doc_as_amended_stage_3_url`, `doc_as_passed_url`, `policy_memorandum_url`, `financial_memorandum_url`, `revised_financial_memorandum_url`, `explanatory_notes_url`, `combined_financial_explanatory_notes_url`, `delegated_powers_memorandum_url`, `stage_1_lead_committee_report_url`, `marshalled_list_url`
- **Committee Context:** `committee_id`, `committee_name`, `committee_membership_roster`
- **Official Report Debate Endpoints:** `official_report_plenary_api_url`, `official_report_committee_api_url`, `official_report_publication_url`

---

## 2. `DERIVED_DETERMINISTIC` (21 Variables — 17.6%)
Variables created 100% deterministically via relational joins, temporal date arithmetic, or roster lookups directly from structured native API JSON feeds (0% parsing risk):
- **Executive Arrangement:** `government_type`, `governing_parties_list` (evaluated on decision date $T$)
- **Sponsorship & Portfolio:** `initiator_type` (relational join on `/api/billtypes`), `initiator_party_governance_role` (relational lookup on `/api/memberparties`), `ministerial_portfolio_title` (relational lookup on `/api/MemberGovernmentRoles`)
- **Stage Timelines:** `duration_calendar_days`, `duration_sitting_days`, `stage_1_debate_days_count`, `stage_3_debate_days_count`
- **Voting Coalitions:** `financial_resolution_required_flag`, `financial_resolution_approved_flag`, `decision_point_motion_type`, `effective_majority_margin_at_event_date`, `party_dissent_rate_at_event_date`, `voting_coalition_type`
- **Committee Structure:** `committee_type`, `committee_convener_member_id`, `committee_deputy_convener_member_id`
- **Macro Disposition:** `final_status`, `termination_mechanism`

---

## 3. `DERIVED_EXTRACTED` (40 Variables — 33.6%)
Variables programmatically parsed or extracted from PDF Marshalled Amendment Lists, HTML Hansard transcripts, or raw bill text files:
- **Document Text Analytics:** `bill_as_introduced_word_count`, `bill_as_amended_stage_2_word_count`, `bill_as_amended_stage_3_word_count`, `bill_as_enacted_word_count`, `text_expansion_ratio`, `fiscal_impact_flag`, `emergency_procedure_flag`, `section_35_order_triggered_flag`
- **Macro & Micro Amendment Data:** `amendments_tabled_count`, `amendments_agreed_count`, `amendments_non_executive_count`, `committee_amendments_executive_acceptance_rate`, `bill_text_alteration_score`, `canonical_amendment_id`, `local_amendment_number`, `bill_id`, `stage_canonical`, `stage_raw`, `date_tabled`, `date_decided`, `sponsor_name`, `sponsor_party_on_tabling_date`, `sponsor_party_leadership_role`, `sponsor_governance_role`, `co_sponsors_count`, `target_clause_or_schedule`, `amendment_action_type`, `government_position`, `disposition_canonical`, `decision_mechanism`, `division_id`, `aye_count`, `no_count`, `abstain_count`, `party_dissent_rate_on_amendment`
- **Hansard Debate Analytics:** `proceedings_total_word_count`, `proceedings_interventions_count`, `proceedings_msps_speaking_count`, `executive_ministers_word_count_share`, `backbench_msps_word_count_share`

---

## 4. `LINKED_EXTERNAL_AUTHORITY` (5 Variables — 4.2%)
Cross-reference identifiers deterministically linked from peer-reviewed external datasets:
- `parlgov_cabinet_id` (ParlGov dataset cross-reference ID)
- `initiator_member_id`, `initiator_convener_member_id`, `sponsor_member_id` (Wikidata QIDs)
- `cap_topic_code` (Comparative Agendas Project policy classification)

---

## 5. `UNAVAILABLE_HARD_GAP` (2 Variables — 1.7%)
Procedural institutional omissions carrying sub-reason codes:
- `programme_motion_flag` (`NOT_APPLICABLE_TO_ASSEMBLY` — Westminster concept; Holyrood uses Business Motions)
- `guillotine_invoked_flag` (`NOT_APPLICABLE_TO_ASSEMBLY` — Westminster closure motion; not applicable to Holyrood procedure)
