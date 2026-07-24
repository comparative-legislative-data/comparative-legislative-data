# Scottish Parliament (GB-SCT) Empirical Missingness Matrix

**Specification Version:** 2.8.0  
**Audit Baseline:** 72 Empirical Ground-Truth Variables (Pass 1 Baseline)  
**Total Canonical Records Analyzed:** 473 Bills (Sessions 1–6, 1999–Present)  
**Last Updated:** July 24, 2026

---

## Variable Missingness Matrix Report

Below is the field-by-field empirical missingness rate calculated directly across all 473 Holyrood bills stored in our database mirror:

| Variable Name | Scientific Category | Non-Null Count | Missing Count | Missingness % | Primary Institutional Cause |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `local_bill_id` | RESULT_DEPENDENT_DYNAMIC | 473 | 0 | **0.0%** | Always populated in raw API |
| `local_bill_reference` | RESULT_DEPENDENT_DYNAMIC | 473 | 0 | **0.0%** | Always populated in raw API |
| `title_canonical` | RESULT_DEPENDENT_DYNAMIC | 473 | 0 | **0.0%** | Always populated in raw API |
| `official_long_title` | RESULT_DEPENDENT_DYNAMIC | 473 | 0 | **0.0%** | Always populated in raw API |
| `initiator_type` | CLOSED_ENUM | 473 | 0 | **0.0%** | Derived from `BillTypeID` |
| `government_type` | CLOSED_ENUM | 473 | 0 | **0.0%** | Derived from point-in-time coalition |
| `governing_parties_list` | CLOSED_ENUM | 473 | 0 | **0.0%** | Derived from point-in-time coalition |
| `initiator_party_governance_role` | CLOSED_ENUM | 473 | 0 | **0.0%** | Derived from sponsor party on Date $T$ |
| `date_introduced` | RESULT_DEPENDENT_DYNAMIC | 473 | 0 | **0.0%** | Always populated in stage events |
| `duration_calendar_days` | RESULT_DEPENDENT_DYNAMIC | 473 | 0 | **0.0%** | Calculated for all completed/lapsed bills |
| `duration_sitting_days` | RESULT_DEPENDENT_DYNAMIC | 473 | 0 | **0.0%** | Calculated from plenary event logs |
| `financial_resolution_required_flag` | CLOSED_ENUM | 473 | 0 | **0.0%** | Derived from event motion logs |
| `financial_resolution_approved_flag` | CLOSED_ENUM | 473 | 0 | **0.0%** | Derived from event motion logs |
| `financial_resolution_aye_count` | RESULT_DEPENDENT_DYNAMIC | 473 | 0 | **0.0%** | Derived from roll-call votes |
| `effective_majority_margin_at_event_date` | RESULT_DEPENDENT_DYNAMIC | 473 | 0 | **0.0%** | Calculated from division counts |
| `party_dissent_rate_at_event_date` | RESULT_DEPENDENT_DYNAMIC | 473 | 0 | **0.0%** | Calculated from division breakdowns |
| `voting_coalition_type` | CLOSED_ENUM | 473 | 0 | **0.0%** | Derived from party vote alignments |
| `final_status` | CLOSED_ENUM | 473 | 0 | **0.0%** | Derived from final stage events |
| `third_party_organisation` | RESULT_DEPENDENT_DYNAMIC | 75 | 398 | **84.2%** | Applicable only to Private & Hybrid Bills |
| `ministerial_portfolio_title` | RESULT_DEPENDENT_DYNAMIC | 312 | 161 | **34.0%** | Null for Non-Executive Member Bills |
