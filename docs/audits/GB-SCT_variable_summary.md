# Scottish Parliament (GB-SCT) Audit Variable Summary

**Specification Version:** 2.8.0  
**Audit Stage:** Pass 1 Audit Complete (Structured Native API Feeds & Relational Joins)  
**Last Updated:** July 23, 2026

---

## Pass 1 Audit Provenance Breakdown

All **114 institutional research variables** across 4 core entities (`CanonicalBill`, `CanonicalAmendment`, `CommitteeContext`, `ParsedProceedings`) and procedural hard gaps were evaluated against the 12 official Scottish Parliament Open Data API endpoints (`data.parliament.scot/api`) and Official Report Chamber Voting Logs.

```
┌───────────────────────────────────────────────────────────────────────────┐
│                    PASS 1 AUDIT DISTRIBUTION SUMMARY                       │
├───────────────────────────┬───────────────┬───────────────────────────────┤
│ PROVENANCE TIER           │ COUNT         │ PERCENTAGE                    │
├───────────────────────────┼───────────────┼───────────────────────────────┤
│ NATIVE_DIRECT             │ 46 Variables  │ 40.4%                         │
│ DERIVED_DETERMINISTIC     │ 21 Variables  │ 18.4%                         │
│ NOT_YET_CATEGORISED       │ 47 Variables  │ 41.2% (Pending Pass 2 Audit)  │
├───────────────────────────┼───────────────┼───────────────────────────────┤
│ TOTAL AUDITED             │ 114 Variables │ 100.0%                        │
└───────────────────────────┴───────────────┴───────────────────────────────┘
```

---

## 1. `NATIVE_DIRECT` (46 Variables — 40.4%)
Variables served directly raw out-of-the-box in the official API feeds:
- **Assembly & Executive Context:** `jurisdiction_code`, `name`, `chamber_type`, `statutory_seats_total`, `presiding_officer_neutral_count`, `parliament_term`, `term_start_date`, `term_end_date`, `devolved_executive_name`
- **Bill Sponsorship & Origin:** `local_bill_id`, `title_canonical`, `third_party_organisation`, `initiator_organisation_name`
- **Progression & Timelines:** `date_introduced`, `date_final_outcome`, `royal_assent_date`, `stage_1_lead_committee_report_date`, `stage_1_debate_start_date`, `stage_1_debate_end_date`, `stage_2_committee_start_date`, `stage_2_committee_end_date`, `stage_3_plenary_debate_start_date`, `stage_3_plenary_debate_end_date`
- **Financial Resolutions & Voting:** `financial_resolution_vote_date`, `financial_resolution_aye_count`, `financial_resolution_no_count`, `financial_resolution_abstain_count`
- **Document Stage Prints:** `doc_as_introduced_url`, `doc_as_amended_stage_2_url`, `doc_as_amended_stage_3_url`, `doc_as_passed_url`, `policy_memorandum_url`, `financial_memorandum_url`, `revised_financial_memorandum_url`, `explanatory_notes_url`, `combined_financial_explanatory_notes_url`, `delegated_powers_memorandum_url`, `stage_1_lead_committee_report_url`, `marshalled_list_url`
- **Committee Context:** `committee_id`, `committee_name`, `committee_membership_roster`
- **Debate Proceedings API:** `official_report_plenary_api_url`, `official_report_committee_api_url`, `official_report_publication_url`

---

## 2. `DERIVED_DETERMINISTIC` (21 Variables — 18.4%)
Variables created 100% deterministically via relational joins, temporal date arithmetic, or roster lookups directly from structured native API JSON feeds (0% parsing risk):
- **Executive Arrangement:** `government_type`, `governing_parties_list` (evaluated on decision date $T$)
- **Sponsorship & Portfolio:** `initiator_type` (relational join on `/api/billtypes`), `initiator_party_governance_role` (relational lookup on `/api/memberparties`), `ministerial_portfolio_title` (relational lookup on `/api/MemberGovernmentRoles`)
- **Stage Timelines:** `duration_calendar_days`, `duration_sitting_days`, `stage_1_debate_days_count`, `stage_3_debate_days_count`
- **Voting Coalitions:** `financial_resolution_required_flag`, `financial_resolution_approved_flag`, `decision_point_motion_type`, `effective_majority_margin_at_event_date`, `party_dissent_rate_at_event_date`, `voting_coalition_type`
- **Committee Structure:** `committee_type`, `committee_convener_member_id`, `committee_deputy_convener_member_id`
- **Macro Disposition:** `final_status`, `termination_mechanism`

---

## 3. `NOT_YET_CATEGORISED` (47 Variables — 41.2%)
Variables requiring non-API sources (PDF document extractions, Marshalled List regex parsing, Hansard transcript word counts, human coding, AI extractions, or hard gap verifications), left uncategorised at Pass 1 to avoid premature guessing.

*Note:* Pass 2 Audit will systematically evaluate these 47 variables to identify which ones can be classified as **`DERIVED_EXTRACTED`** via programmatic document parsing.
