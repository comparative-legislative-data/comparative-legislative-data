# Peer Review Commission Brief & Evaluation Guidelines

**Comparative Legislative Data Platform**  
*Academic Consultation & External Expert Commission*  
*Version 2.1.0 (Self-Contained 6-Tier Commission Brief)*

---

## 1. Executive Summary & Purpose

The **Comparative Legislative Data Platform** (`https://legislativedata.org`) is an open-access academic research infrastructure designed to standardize, mirror, and audit quantitative legislative data across international parliamentary and presidential assemblies.

This **Peer Review Commission Brief** is a self-contained briefing document intended for external academic reviewers, legislative scholars, political scientists, and data engineering experts. **No GitHub repository access or technical setup is required to complete this review.**

We commission expert reviewers to evaluate our proposed **Master Canonical Variable Catalog** (Section 3) and **6-Tier Data Availability & Provenance Framework** (Section 2), and to submit a written **Peer Review Report** addressing the core evaluation questions in Section 4.

---

## 2. The 6-Tier Data Availability & Provenance Framework

To ensure maximum academic transparency, every variable in our canonical schema is evaluated per parliament and per session against a 6-tier availability and provenance spectrum:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ (1) MASTER CANONICAL VARIABLE WISHLIST (The Ideal Quantitative Research Schema)             │
└───────────────────────────────┬─────────────────────────────────────────────────────────────┘
                                │
                      EVALUATED PER VARIABLE / SESSION
                                │
    ┌────────────────┬──────────┴─────────┬──────────────────┬──────────────────┐
    ▼                ▼                    ▼                  ▼                  ▼
┌──────────────┐┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ (2) NATIVE   ││ (3) DERIVED  │   │ (4) DERIVED  │   │ (5) DERIVED  │   │ (6) HARD GAP │
│     DIRECT   ││ DETERMINISTIC│   │  HUMAN-CODED │   │ SYNTHETIC-AI │   │ UNAVAILABLE  │
├──────────────┤├──────────────┤   ├──────────────┤   ├──────────────┤   ├──────────────┤
│ Host API or  ││ Rule-based   │   │ Expert hand- │   │ NLP/LLM text │   │ Missing,     │
│ raw feed     ││ transforms & │   │ coding & PhD │   │ extraction & │   │ unrecorded,  │
│ (JSON/XML).  ││ joins        │   │ datasets     │   │ probabilistic│   │ or non-      │
│              ││ (e.g. roster │   │ (Gold        │   │ inference    │   │ digitized    │
│              ││ lookup).     │   │ Standard).   │   │ (Tier 4-     │   │ (with reason │
│              ││              │   │              │   │ benchmarked).│   │ code).       │
└──────────────┘└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
```

1. **`CANONICAL_WISHLIST_TARGET`:** Universal variable definition in our Master Catalog.
2. **`NATIVE_DIRECT`:** Available directly in the host assembly's official API or raw feed (JSON/XML).
3. **`DERIVED_DETERMINISTIC`:** Generated deterministically via simple pipeline transformations, date arithmetic, or joins against persistent datasets (e.g. Executive Rosters). Includes explicit confidence ratings (`HIGH`, `MEDIUM`, `LOW`).
4. **`DERIVED_HUMAN_CODED`:** Manually hand-coded by human researchers, subject experts, or doctoral coders. Represents ground-truth data for publication and AI benchmarking.
5. **`DERIVED_SYNTHETIC_AI`:** Synthesized using advanced NLP/LLM text processing, carrying an explicit **Validation Lifecycle Status**:
   - `UNVERIFIED_DRAFT`: Published immediately post-extraction for open crowdsourced audit.
   - `SAMPLE_VALIDATED`: Audited against a randomized human sample with recorded precision/recall metrics.
   - `GOLD_BENCHMARKED`: Extensively benchmarked against Tier 4 (`DERIVED_HUMAN_CODED`) ground truth.
6. **`UNAVAILABLE_HARD_GAP`:** Missing natively from the host assembly, carrying sub-reason codes:
   - `NOT_RECORDED_BY_ASSEMBLY` (institutional absence).
   - `RECORDED_BUT_UNDIGITIZED` (data-engineering backlog).
   - `RESTRICTED_ACCESS` / `COST_PROHIBITIVE`.

---

## 3. Master Canonical Variable Catalog (The Evaluation Target)

Below is the proposed wishlist of quantitative legislative variables grouped across 8 research domains:

### Domain 1: Assembly & Electoral Context
- `jurisdiction_code`: ISO-style unique country/sub-national code (e.g. `GB-UKP`, `GB-SCT`, `DE-BT`, `US-HR`).
- `parliament_term`: Macro electoral period spanning general elections (e.g. `Session 6`, `58th Parliament`).
- `session_start_date` / `session_end_date`: Official term boundaries.
- `chamber_type`: Chamber classification (`SOVEREIGN_BICAMERAL`, `DEVOLVED_UNICAMERAL`, `FEDERAL_UPPER`, `FEDERAL_LOWER`, `CONCURRENT_ELECTED`).

### Domain 2: Bill Identification, Sponsorship & Origin
- `local_bill_id`: Official reference assigned by host legislature (e.g. `SP Bill 13`, `H.R. 815`).
- `title_canonical` / `title_native`: Normalized English title vs official native language title.
- `initiator_type`: Globally neutral sponsor type (`EXECUTIVE`, `INDIVIDUAL_MEMBER`, `GROUP_MEMBERS`, `COMMITTEE`, `PRIVATE_HYBRID`).
- `initiator_party_governance_role`: Alignment of primary sponsor relative to executive power (`GOVERNING_PARTY`, `OPPOSITION_PARTY`, `CROSS_PARTY`, `NON_PARTISAN`).
- `initiator_member_id`: Persistent disambiguated member ID (Wikidata QID / native ID).
- `co_sponsorship_count` & `cross_party_sponsorship_count`: Total co-sponsors vs opposition co-sponsors.

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
- `fiscal_impact_flag` & `regulatory_impact_flag`: Flags indicating binding fiscal or regulatory impact.

### Domain 6: Committee Proceedings & Evidence
- `lead_committee_name`: Name of primary scrutinising committee assigned to the bill.
- `committee_referral_date` / `committee_report_date`: Dates of committee remit and report.
- `committee_evidence_submissions_count` & `committee_public_hearings_count`: Written submissions and oral hearing counts.

### Domain 7: Amendments & Legislative Alteration
- `amendments_tabled_count` / `amendments_agreed_count` / `amendments_rejected_count` / `amendments_withdrawn_count`.
- `amendments_executive_count` vs `amendments_non_executive_count`: Government minister vs non-executive amendments.
- `committee_amendments_tabled_count` & `committee_amendments_executive_acceptance_rate`: Committee-stage amendment activity and executive acceptance rate.
- `bill_text_alteration_score`: Derived similarity metric of text change from introduction to passage (Levenshtein/Cosine similarity).

### Domain 8: Divisions, Voting Coalitions & Debate Records
- `divisions_count` & `division_records`: Roll-call votes held, Yeas, Nays, Abstentions, and motion outcome.
- `rebellions_flag`: Presence of governing or opposition party revolts ($\ge 5\%$ party defiance).
- `voting_coalition_type`: Voting alignment classification (`UNANIMOUS`, `GOVERNMENT_PARTY_LINE`, `CROSS_PARTY_MAJORITY`, `MINORITY_PASSED`, `OPPOSITION_DEFEAT`).
- `plenary_record_urls`: Array of direct links to plenary debate transcripts/Hansard. *(Alias: `hansard_debate_urls`)*.

---

## 4. Commission Questions for the Written Peer Review Report

Reviewers are requested to submit a structured **Written Peer Review Report** addressing the following evaluation areas:

### Area 1: Variable Completeness & Conceptual Scope
1. Does the **Master Canonical Variable Catalog** (Section 3) cover the necessary quantitative variables for researching legislative effectiveness, executive dominance, sessional timelines, voting coalitions, and procedural obstruction?
2. Are there critical variables in comparative legislative studies that are missing and should be added?
3. Are the variable definitions and enums sufficiently neutral to span both parliamentary (Westminster, devolved, consensus) and presidential/semi-presidential systems?

### Area 2: 6-Tier Provenance, Human Data & AI Validation
4. Is the 6-tier distinction (`NATIVE_DIRECT` vs `DERIVED_DETERMINISTIC` vs `DERIVED_HUMAN_CODED` vs `DERIVED_SYNTHETIC_AI` vs `UNAVAILABLE_HARD_GAP`) methodologically sound for academic publication?
5. Does the **AI Validation Lifecycle** (`UNVERIFIED_DRAFT` $\rightarrow$ `SAMPLE_VALIDATED` $\rightarrow$ `GOLD_BENCHMARKED`) strike an appropriate balance between open exploratory data access and academic rigor?
6. How can human-coded datasets (`DERIVED_HUMAN_CODED`) from doctoral research or academic repositories best be integrated and benchmarked on the platform?

### Area 3: Data Gap Transparency & Academic Utility
7. Does explicitly documenting host API omissions as **`UNAVAILABLE_HARD_GAP`** with sub-reason codes provide sufficient transparency for comparative political scientists?
8. What metadata or documentation format would make this platform most useful for your own quantitative research or teaching?

---

## 5. Report Submission Guidelines

Expert reviewers are requested to compile their findings into a **Written Peer Review Report** (PDF or Word document format) and submit it directly to the project team:

- **Primary Submission Email:** `peer-review@legislativedata.org`
- **Project Portal:** `https://legislativedata.org`
