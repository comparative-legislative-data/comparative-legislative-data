# Peer Review Commission Brief & Evaluation Guidelines

**Comparative Legislative Data Platform**  
*Academic Consultation & External Expert Commission*  
*Version 2.3.0 (Self-Contained 6-Tier Provenance Commission Brief)*

---

## 1. Executive Summary & Purpose

The **Comparative Legislative Data Platform** (`https://legislativedata.org`) is an open-access academic research infrastructure designed to standardize, mirror, and audit quantitative legislative data across international parliamentary and presidential assemblies.

This **Peer Review Commission Brief** is a self-contained briefing document intended for external academic reviewers, legislative scholars, political scientists, and data engineering experts. **No GitHub repository access or technical setup is required to complete this review.**

We commission expert reviewers to evaluate our proposed **Master Canonical Variable Catalog** (Section 3) and **6-Tier Data Availability & Provenance Framework** (Section 2), and to submit a written **Peer Review Report** addressing the core evaluation questions in Section 4.

---

## 2. The 6-Tier Data Availability & Provenance Framework

The framework cleanly separates the **Master Canonical Variable Wishlist** (the target research schema) from the **6-Tier Data Availability & Provenance Spectrum** (how each variable value is obtained per parliament and decision point):

```
 MASTER CANONICAL VARIABLE WISHLIST (Target Dictionary of Quantitative Variables)
 └─ The ideal set of variables sought by comparative legislative researchers.
                                    │
                  EVALUATED AT SPECIFIC DECISION-POINT DATES (T)
                                    │
  ┌─────────────────────────────────┴─────────────────────────────────┐
  │         THE 6-TIER DATA AVAILABILITY & PROVENANCE SPECTRUM        │
  └─────────────────────────────────┬─────────────────────────────────┘
                                    │
    ┌────────────────┬──────────────┼──────────────┬──────────────────┬──────────────────┐
    ▼                ▼              ▼              ▼                  ▼                  ▼
┌──────────────┐┌──────────────┐┌──────────────┐┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ 1. NATIVE    ││ 2. DERIVED   ││ 3. DERIVED   ││ 4. DERIVED   │   │ 5. LINKED    │   │ 6. HARD GAP  │
│    DIRECT    ││ DETERMINISTIC││  HUMAN-CODED ││ SYNTHETIC-AI │   │ EXTERNAL     │   │ UNAVAILABLE  │
├──────────────┤├──────────────┤├──────────────┤├──────────────┤   ├──────────────┤   ├──────────────┤
│ Served out-  ││ Rule-based   ││ Expert hand- ││ NLP/LLM text │   │ Peer-        ││ Missing,     │
│ of-the-box   ││ joins, date  ││ coding & PhD ││ extractions  │   │ reviewed     ││ unrecorded,  │
│ in API/feed  ││ math & roster││ dataset      ││ with AI      │   │ datasets     ││ or non-      │
│ (JSON/XML).  ││ lookups.     ││ ingestion    ││ Validation   │   │ (ParlGov,    ││ digitized    │
│              ││              ││ (Gold).      ││ Lifecycle.   │   │ CAP, QID).   ││ (with reason)│
└──────────────┘└──────────────┘└──────────────┘└──────────────┘   └──────────────┘└──────────────┘
```

1. **`NATIVE_DIRECT`:** Available directly in host assembly official APIs or raw feeds (JSON/XML).
2. **`DERIVED_DETERMINISTIC`:** Generated deterministically via rule-based joins, date arithmetic, or roster lookups.
3. **`DERIVED_HUMAN_CODED`:** Manually hand-coded by human researchers, subject experts, or doctoral coders (serving as ground truth).
4. **`DERIVED_SYNTHETIC_AI`:** Synthesized using advanced NLP/LLM text processing, carrying an explicit **Validation Lifecycle Status**:
   - `UNVERIFIED_DRAFT`: Published immediately post-extraction for open crowdsourced audit.
   - `SAMPLE_VALIDATED`: Audited against a randomized human sample with recorded precision/recall metrics.
   - `GOLD_BENCHMARKED`: Extensively benchmarked against Tier 3 (`DERIVED_HUMAN_CODED`) ground truth.
5. **`LINKED_EXTERNAL_AUTHORITY`:** Deterministically linked from established, peer-reviewed external benchmark datasets (e.g. ParlGov, Wikidata, CAP, Manifesto Project).
6. **`UNAVAILABLE_HARD_GAP`:** Missing natively from the host assembly, carrying sub-reason codes:
   - `NOT_RECORDED_BY_ASSEMBLY` (institutional absence).
   - `RECORDED_BUT_UNDIGITIZED` (data-engineering backlog).
   - `RESTRICTED_ACCESS` / `COST_PROHIBITIVE`.

---

## 3. Master Canonical Variable Catalog (The Evaluation Target)

Below is the proposed wishlist of quantitative legislative variables grouped across 8 research domains:

### Domain 1: Assembly, Electoral & Executive Context
- `jurisdiction_code`: ISO-style unique country/sub-national code (e.g. `GB-UKP`, `GB-SCT`, `DE-BT`, `US-HR`).
- `parliament_term`: Macro electoral period spanning general elections (e.g. `Session 6`, `58th Parliament`).
- `session_start_date` / `session_end_date`: Official term boundaries.
- `chamber_type`: Chamber classification (`SOVEREIGN_BICAMERAL`, `DEVOLVED_UNICAMERAL`, `FEDERAL_UPPER`, `FEDERAL_LOWER`, `CONCURRENT_ELECTED`).
- `government_type`: Executive arrangement typology (`SINGLE_PARTY_MAJORITY`, `SINGLE_PARTY_MINORITY`, `FORMAL_COALITION_MAJORITY`, `COOPERATION_AGREEMENT`, `CONFIDENCE_AND_SUPPLY`).
- `parlgov_cabinet_id`: Linked cabinet identifier from the ParlGov database.

### Domain 2: Bill Identification, Sponsorship & Temporal Origin
- `local_bill_id`: Official reference assigned by host legislature (e.g. `SP Bill 13`, `H.R. 815`).
- `title_canonical` / `title_native`: Normalized English title vs official native language title.
- `initiator_type`: Globally neutral sponsor type (`EXECUTIVE`, `INDIVIDUAL_MEMBER`, `GROUP_MEMBERS`, `COMMITTEE`, `PRIVATE_HYBRID`).
- `initiator_party_governance_role`: Primary sponsor's governance alignment evaluated **on the exact date of introduction**.
- `initiator_member_id`: Persistent disambiguated member ID (Wikidata QID / native ID).
- `co_sponsorship_count` & `cross_party_sponsorship_count`: Total co-sponsors vs opposition co-sponsors on introduction date.

### Domain 3: Procedural Progression, Timelines & Procedural Control
- `date_introduced` / `date_final_outcome`: Formal introduction and terminal disposition dates.
- `duration_calendar_days` / `duration_sitting_days`: Calendar days vs actual parliamentary sitting days elapsed.
- `term_interruption_flag`: Boolean flagging whether bill passage spanned a recess, prorogation, or election.
- `programme_motion_flag` & `guillotine_invoked_flag`: Flags for formal timetabling or debate closure motions.
- `emergency_procedure_flag` & `stages_compressed_count`: Flags for fast-track or urgency procedures.
- `prior_executive_consent_required_flag` & `prior_executive_consent_granted_date`: Significance of prior executive/Crown consent.
- `stage_milestones`: Sequential array of stage events (`stage_canonical`, `date_stage`, `proceedings_url`).

### Domain 4: Final Disposition & Inter-Chamber Mechanisms
- `final_status`: Terminal status (`ENACTED`, `DEFEATED`, `WITHDRAWN`, `LAPSED`, `PENDING`, `VETOED`).
- `termination_mechanism`: Procedural mechanism (`ENACTMENT`, `VOTE_DEFEAT`, `EXECUTIVE_WITHDRAWAL`, `SESSION_EXPIRY`, `EXECUTIVE_VETO`, `CONSTITUTIONAL_CHALLENGE`).
- `head_of_state_promulgation_date`: Date of formal Royal Assent or Presidential Promulgation. *(Alias: `royal_assent_date`)*.
- `chamber_ping_pong_count` & `chamber_disagreement_flag`: Inter-chamber exchange and disagreement metrics for bicameral systems.

### Domain 5: Bill Documentation & Parliamentary Papers Chain
- `doc_as_introduced_url` / `doc_as_passed_url`: Text of Bill at introduction vs final passage.
- `doc_policy_memorandum_url` / `doc_financial_memorandum_url`: Policy rationale and costing papers.
- `doc_explanatory_notes_url`: Official legal explanatory notes.
- `cap_topic_code`: Policy topic code linked to Comparative Agendas Project taxonomy.
- `fiscal_impact_flag` & `regulatory_impact_flag`: Flags indicating binding fiscal or regulatory impact.

### Domain 6: Committee Proceedings & Evidence
- `lead_committee_name`: Name of primary scrutinising committee assigned to the bill.
- `committee_referral_date` / `committee_report_date`: Dates of committee remit and report.
- `committee_evidence_submissions_count` & `committee_public_hearings_count`: Written submissions and oral hearing counts.

### Domain 7: Decision-Point Amendments & Legislative Alteration
- `amendments_tabled_count` / `amendments_agreed_count` / `amendments_rejected_count` / `amendments_withdrawn_count`.
- `amendments_executive_count` vs `amendments_non_executive_count`: Government minister vs non-executive amendments evaluated **on date of tabling**.
- `committee_amendments_tabled_count` & `committee_amendments_executive_acceptance_rate`: Committee-stage amendment activity and executive acceptance rate.
- `bill_text_alteration_score`: Derived similarity metric of text change from introduction to passage (Levenshtein/Cosine similarity).

### Domain 8: Temporal Divisions, Floor Arithmetic & Voting Coalitions
- `divisions_count`: Total roll-call division votes held.
- `effective_majority_margin_at_event_date`: Mathematical floor majority margin ($\text{Governing Seats} - \text{Opposition Seats}$) **on the exact vote date**.
- `governing_seats_at_event_date`: Active voting seats held by executive coalition **on the exact vote date**.
- `rebellions_flag`: Presence of party revolts ($\ge 5\%$ party defiance) evaluated against member party status **on the vote date**.
- `voting_coalition_type`: Voting alignment classification evaluated against floor arithmetic **on the vote date**.
- `plenary_record_urls`: Array of direct links to plenary debate transcripts/Hansard. *(Alias: `hansard_debate_urls`)*.

---

## 4. Commission Questions for the Written Peer Review Report

Reviewers are requested to submit a structured **Written Peer Review Report** addressing the following evaluation areas:

### Area 1: Variable Completeness & Conceptual Scope
1. Does the **Master Canonical Variable Catalog** (Section 3) cover the necessary quantitative variables for researching legislative effectiveness, executive dominance, sessional timelines, voting coalitions, and procedural obstruction?
2. Are there critical variables in comparative legislative studies that are missing and should be added?
3. Are the variable definitions and enums sufficiently neutral to span both parliamentary (Westminster, devolved, consensus) and presidential/semi-presidential systems?

### Area 2: 6-Tier Provenance Spectrum, Temporal Tracking & External Linking
4. Is the 6-tier provenance spectrum (`NATIVE_DIRECT` vs `DERIVED_DETERMINISTIC` vs `DERIVED_HUMAN_CODED` vs `DERIVED_SYNTHETIC_AI` vs `LINKED_EXTERNAL_AUTHORITY` vs `UNAVAILABLE_HARD_GAP`) methodologically sound for academic publication?
5. Does evaluating politician affiliation and floor arithmetic at **every decision point** (bill introduction, amendment tabling, division vote) resolve temporal changes in parliamentary majority status?
6. How effectively does linking external authority datasets (ParlGov, CAP, Wikidata) enhance comparative analysis?

### Area 3: Data Gap Transparency & Academic Utility
7. Does explicitly documenting host API omissions as **`UNAVAILABLE_HARD_GAP`** with sub-reason codes provide sufficient transparency for comparative political scientists?
8. What metadata or documentation format would make this platform most useful for your own quantitative research or teaching?

---

## 5. Report Submission Guidelines

Expert reviewers are requested to compile their findings into a **Written Peer Review Report** (PDF or Word document format) and submit it directly to the project team:

- **Primary Submission Email:** `peer-review@legislativedata.org`
- **Project Portal:** `https://legislativedata.org`
