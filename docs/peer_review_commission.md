# Peer Review Commission Brief & Evaluation Guidelines

**Comparative Legislative Data Platform**  
*Academic Consultation & External Expert Commission*  
*Version 2.0.0 (Self-Contained Report Commission)*

---

## 1. Executive Summary & Purpose

The **Comparative Legislative Data Platform** (`https://legislativedata.org`) is an open-access academic research infrastructure designed to standardize, mirror, and audit quantitative legislative data across international parliamentary assemblies.

This **Peer Review Commission Brief** is a self-contained briefing document intended for external academic reviewers, legislative scholars, political scientists, and data engineering experts. **No GitHub repository access or technical setup is required to complete this review.**

We commission expert reviewers to evaluate our proposed **Master Canonical Variable Catalog** (Section 3) and **5-Tier Data Availability & Provenance Framework** (Section 2), and to submit a written **Peer Review Report** addressing the core evaluation questions in Section 4.

---

## 2. The 5-Tier Data Availability & Provenance Framework

To ensure maximum academic transparency, every variable in our canonical schema is evaluated per parliament against a 5-tier availability and provenance spectrum:

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│ (1) MASTER CANONICAL VARIABLE WISHLIST (The Ideal Quantitative Research Schema)         │
│     The universal set of variables legislative scholars want (Titles, Sponsors, Party   │
│     Roles, Stage Dates, Amendment Text & Outcomes, Division Votes, Rebellions,          │
│     Committee Evidence, Bill Text, Explanatory Notes, Policy Intent).                  │
└───────────────────────────────────────────┬─────────────────────────────────────────────┘
                                            │
                                  EVALUATED PER PARLIAMENT
                                            │
         ┌──────────────────┬───────────────┴───────────────┬──────────────────┐
         ▼                  ▼                               ▼                  ▼
┌──────────────────┐┌──────────────────┐           ┌──────────────────┐┌──────────────────┐
│ (2) NATIVE       ││ (3) DERIVED      │           │ (4) DERIVED      ││ (5) HARD GAP     │
│     DIRECT       ││     DETERMINISTIC│           │     AI / SYNTHETIC ││     UNAVAILABLE  │
├──────────────────┤├──────────────────┤           ├──────────────────┤├──────────────────┤
│ Served out-of-   ││ Created by       │           │ Created via      ││ Does not exist,  │
│ the-box in API/  ││ simple pipeline  │           │ elaborate NLP/   ││ unrecorded, or   │
│ feeds (JSON/XML).││ joins/transforms │           │ LLM text         ││ resource-        │
│                  ││ (e.g. sponsor +  │           │ analysis (e.g.   ││ prohibitive to   │
│                  ││ Roster = Party   │           │ topic intent,    ││ generate for this│
│                  ││ Governance Role).│           │ amendment impact)││ parliament.      │
└──────────────────┘└──────────────────┘           └──────────────────┘└──────────────────┘
```

1. **`CANONICAL_WISHLIST_TARGET`:** Universal variable definition in our Master Catalog.
2. **`NATIVE_DIRECT`:** Available directly in the host assembly's official API or raw feed (JSON/XML).
3. **`DERIVED_DETERMINISTIC`:** Generated deterministically via simple pipeline transformations, date arithmetic, or joins against persistent datasets (e.g. Executive Rosters). Includes explicit confidence ratings (`HIGH`, `MEDIUM`, `LOW`).
4. **`DERIVED_SYNTHETIC_AI`:** Synthesized using advanced NLP/LLM text processing, topic modeling, or structural parsing of unstructured Hansard/PDF text.
5. **`UNAVAILABLE_HARD_GAP`:** Missing natively from the host assembly, unrecorded, or resource-prohibitive to generate (Documented Open Data Gap).

---

## 3. Master Canonical Variable Catalog (The Evaluation Target)

Below is the proposed wishlist of quantitative legislative variables grouped across 8 research domains:

### Domain 1: Assembly & Electoral Context
- `jurisdiction_code`: ISO-style unique country/sub-national code (e.g. `GB-UKP`, `GB-SCT`, `DE-BT`).
- `parliament_term`: Macro electoral period spanning general elections (e.g. `Session 6`, `58th Parliament`).
- `session_start_date` / `session_end_date`: Official term boundaries.
- `chamber_type`: Chamber classification (`SOVEREIGN_BICAMERAL`, `DEVOLVED_UNICAMERAL`, `FEDERAL_UPPER`).

### Domain 2: Bill Identification, Sponsorship & Origin
- `local_bill_id`: Official reference assigned by host legislature (e.g. `SP Bill 13`, `H.R. 815`).
- `title_canonical` / `title_native`: Normalized English title vs official native language title.
- `initiator_type`: Globally neutral sponsor type (`EXECUTIVE`, `INDIVIDUAL_MEMBER`, `GROUP_MEMBERS`, `COMMITTEE`, `PRIVATE_HYBRID`).
- `initiator_party_governance_role`: Alignment of primary sponsor relative to executive power (`GOVERNING_PARTY`, `OPPOSITION_PARTY`, `CROSS_PARTY`, `NON_PARTISAN`).
- `initiator_member_id`: Persistent disambiguated member ID (Wikidata QID / native ID).
- `co_sponsorship_count` & `cross_party_sponsorship_count`: Total co-sponsors vs opposition co-sponsors.

### Domain 3: Procedural Progression & Timelines
- `date_introduced` / `date_final_outcome`: Formal introduction and terminal disposition dates.
- `duration_calendar_days` / `duration_sitting_days`: Calendar days vs actual parliamentary sitting days elapsed.
- `suspension_interrupted_flag`: Boolean flagging whether bill passage spanned a recess, prorogation, or election.
- `stage_milestones`: Sequential array of stage events (`stage_canonical`, `stage_raw`, `date_stage`, `proceedings_url`).

### Domain 4: Final Disposition & Termination Mechanisms
- `final_status`: Terminal status (`ENACTED`, `DEFEATED`, `WITHDRAWN`, `LAPSED`, `PENDING`).
- `termination_mechanism`: Procedural mechanism (`ENACTMENT`, `VOTE_DEFEAT`, `EXECUTIVE_WITHDRAWAL`, `SESSION_EXPIRY`, `SECTION_35_VETO`).
- `royal_assent_date`: Date of formal Royal Assent or Presidential Promulgation.

### Domain 5: Bill Documentation & Parliamentary Papers Chain
- `doc_as_introduced_url` / `doc_as_passed_url`: Text of Bill at introduction vs final passage.
- `doc_policy_memorandum_url` / `doc_financial_memorandum_url`: Policy rationale and costing papers.
- `doc_explanatory_notes_url`: Official legal explanatory notes.
- `doc_marshalled_amendments_urls`: Array of links to official Marshalled Lists of Amendments.

### Domain 6: Committee Proceedings & Evidence
- `lead_committee_name`: Name of primary scrutinising committee assigned to the bill.
- `committee_referral_date` / `committee_report_date`: Dates of committee remit and Stage 1/scrutiny report.
- `committee_evidence_submissions_count`: Total published written evidence submissions received.

### Domain 7: Amendments & Legislative Alteration
- `amendments_tabled_count` / `amendments_agreed_count` / `amendments_rejected_count` / `amendments_withdrawn_count`.
- `amendments_executive_count` vs `amendments_backbench_count`: Government minister vs backbench amendments.
- `bill_text_alteration_score`: Derived similarity metric of text change from introduction to passage (Levenshtein/Cosine similarity).

### Domain 8: Divisions, Voting Coalitions & Hansard Debates
- `divisions_count` & `division_records`: Roll-call votes held, Yeas, Nays, Abstentions, and motion outcome.
- `rebellions_flag`: Presence of governing or opposition party revolts (>=5% party defiance).
- `voting_coalition_type`: Voting alignment classification (`UNANIMOUS`, `GOVERNMENT_PARTY_LINE`, `CROSS_PARTY_MAJORITY`, `MINORITY_PASSED`).
- `hansard_debate_urls`: Array of direct links to speech-level Hansard debate transcripts.

---

## 4. Commission Questions for the Written Peer Review Report

Reviewers are requested to submit a structured **Written Peer Review Report** addressing the following evaluation areas:

### Area 1: Variable Completeness & Conceptual Scope
1. Does the **Master Canonical Variable Catalog** (Section 3) cover the necessary quantitative variables for researching legislative effectiveness, executive dominance, sessional timelines, voting coalitions, and procedural obstruction?
2. Are there critical variables in comparative legislative studies (e.g., guillotine/closure motions, royal consent, committee amendment disposition rates, urgency procedures) that are missing and should be added?
3. Are the variable definitions and enums sufficiently neutral to span both parliamentary (Westminster, devolved, consensus) and presidential/semi-presidential systems?

### Area 2: 5-Tier Provenance & Methodological Rigor
4. Is the 5-tier distinction (`NATIVE_DIRECT` vs `DERIVED_DETERMINISTIC` vs `DERIVED_SYNTHETIC_AI` vs `UNAVAILABLE_HARD_GAP`) methodologically sound for academic publication?
5. What criteria or benchmarks should be required before an AI-synthesized variable (`DERIVED_SYNTHETIC_AI`) is considered reliable enough for quantitative dataset publication?

### Area 3: Data Gap Transparency & Academic Utility
6. Does explicitly documenting host API omissions as **`UNAVAILABLE_HARD_GAP`** provide sufficient transparency for comparative political scientists?
7. What metadata or documentation format would make this platform most useful for your own quantitative research or teaching?

---

## 5. Report Submission Guidelines

Expert reviewers are requested to compile their findings into a **Written Peer Review Report** (PDF or Word document format) and submit it directly to the project team:

- **Primary Submission Email:** `peer-review@legislativedata.org`
- **Project Portal:** `https://legislativedata.org`

*Thank you for contributing your expertise to advancing open, transparent comparative legislative science.*
