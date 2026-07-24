# Scottish Parliament (GB-SCT) Audit Variable Summary

**Specification Version:** 2.8.0  
**Audit Baseline:** Pass 1 Complete (Empirical API Ground Truth) | Pass 2 Candidate Assessment  
**Last Updated:** July 24, 2026

---

## 2-Pass Audit Framework & Provenance Methodology

Our dataset provenance auditing follows a strict 2-pass scientific methodology to prevent premature labeling or data hallucination:

1. **Pass 1 — Empirical Ground Truth (Binary Baseline):**
   * **`NATIVE_DIRECT` (51 Variables — 42.9%):** Raw fields served directly out-of-the-box in official host API JSON payloads (`data.parliament.scot/api`).
   * **`DERIVED_DETERMINISTIC` (21 Variables — 17.6%):** Variables calculated with 100% mathematical certainty and 0% parsing ambiguity using relational joins or date arithmetic directly on raw host API keys.

2. **Pass 2 — Candidate Assessment (Provisional Hypotheses):**
   * **`NOT_YET_CATEGORISED` (47 Variables — 39.5%):** Variables requiring document text parsing, PDF extraction, Hansard speech analytics, external crosswalks, or procedural hard gap verification.
   * Rather than making unverified claims, all 47 variables carry a **Candidate Method Specification** (`validation_status: PROVISIONAL_HYPOTHESIS`) defining target source files, proposed extraction algorithms, and technical risk factors.
   * A variable is **only promoted** to its final tier after an extraction script is built, executed, and benchmarked against historical records with verified 100% repeatability.

```
┌───────────────────────────────────────────────────────────────────────────┐
│                    GB-SCT AUDIT PROVENANCE SUMMARY                        │
├───────────────────────────┬───────────────┬───────────────────────────────┤
│ PROVENANCE TIER           │ COUNT         │ PERCENTAGE                    │
├───────────────────────────┼───────────────┼───────────────────────────────┤
│ NATIVE_DIRECT             │ 51 Variables  │ 42.9% (Empirical Baseline)    │
│ DERIVED_DETERMINISTIC     │ 21 Variables  │ 17.6% (Empirical Baseline)    │
│ NOT_YET_CATEGORISED       │ 47 Variables  │ 39.5% (Provisional Candidate) │
├───────────────────────────┼───────────────┼───────────────────────────────┤
│ TOTAL AUDITED             │ 119 Variables │ 100.0%                        │
└───────────────────────────┴───────────────┴───────────────────────────────┘
```

---

## Pass 2 Candidate Breakdown (47 Provisional Hypotheses)

### A. Document Text & Word Count Analytics (8 Candidate Variables)
- `bill_as_introduced_word_count` (`CANDIDATE_DERIVED_EXTRACTED`) — Target: Stage 1 Bill HTML/PDF print. Method: Plain text tokenization stripping headers/footers.
- `bill_as_amended_stage_2_word_count` (`CANDIDATE_DERIVED_EXTRACTED`) — Target: Stage 2 As Amended HTML/PDF print.
- `bill_as_amended_stage_3_word_count` (`CANDIDATE_DERIVED_EXTRACTED`) — Target: Stage 3 As Amended HTML/PDF print.
- `bill_as_enacted_word_count` (`CANDIDATE_DERIVED_EXTRACTED`) — Target: Legislation.gov.uk Act text print.
- `text_expansion_ratio` (`CANDIDATE_DERIVED_EXTRACTED`) — Target: Derived math ratio of enacted vs introduced word counts.
- `fiscal_impact_flag` (`CANDIDATE_DERIVED_EXTRACTED` / `HUMAN_CODED`) — Target: Financial Memorandum print. Method: Heading regex vs qualitative summary evaluation.
- `emergency_procedure_flag` (`CANDIDATE_DERIVED_EXTRACTED`) — Target: Business Motion API. Method: Regex match on "Emergency Bill" motions.
- `section_35_order_triggered_flag` (`CANDIDATE_DERIVED_EXTRACTED`) — Target: UK Cabinet Office Section 35 Order Register.

### B. Macro & Micro Amendment Extractions (27 Candidate Variables)
- `amendments_tabled_count`, `amendments_agreed_count`, `amendments_non_executive_count`, `committee_amendments_executive_acceptance_rate`, `bill_text_alteration_score` (`CANDIDATE_DERIVED_EXTRACTED`). Target: PDF Marshalled Lists & Official Report Voting Supplements.
- **22 Micro Amendment Fields:** `canonical_amendment_id`, `local_amendment_number`, `bill_id`, `stage_canonical`, `stage_raw`, `date_tabled`, `date_decided`, `sponsor_name`, `sponsor_party_on_tabling_date`, `sponsor_party_leadership_role`, `sponsor_governance_role`, `co_sponsors_count`, `target_clause_or_schedule`, `amendment_action_type`, `government_position`, `disposition_canonical`, `decision_mechanism`, `division_id`, `aye_count`, `no_count`, `abstain_count`, `party_dissent_rate_on_amendment` (`CANDIDATE_DERIVED_EXTRACTED`). Target: PDF Marshalled Amendment Lists & Roll-Call Voting Logs.

### C. Hansard Debate & Speech Analytics (5 Candidate Variables)
- `proceedings_total_word_count`, `proceedings_interventions_count`, `proceedings_msps_speaking_count`, `executive_ministers_word_count_share`, `backbench_msps_word_count_share` (`CANDIDATE_DERIVED_EXTRACTED`). Target: Official Report HTML `Text` tags in `/api/orsplenarymeeting` and `/api/orscommitteemeeting`.

### D. Linked External Authorities & Hard Gaps (7 Candidate Variables)
- `parlgov_cabinet_id` (`CANDIDATE_LINKED_EXTERNAL`) — Target: ParlGov Cabinet Dataset crosswalk.
- `initiator_member_id`, `initiator_convener_member_id`, `sponsor_member_id` (`CANDIDATE_LINKED_EXTERNAL`) — Target: Wikidata QID entity matching.
- `cap_topic_code` (`CANDIDATE_LINKED_EXTERNAL` / `HUMAN_CODED`) — Target: Comparative Agendas Project policy classification.
- `programme_motion_flag`, `guillotine_invoked_flag` (`CANDIDATE_UNAVAILABLE_HARD_GAP`) — Target: Holyrood Standing Orders (procedural non-equivalence).
