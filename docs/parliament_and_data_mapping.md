# Master System Architecture: Parliament Data Evaluation & Ingestion Pipeline

**Comparative Legislative Data Platform**  
*System Architecture & Data Provenance Specification*  
*Version 2.3.0 (Master Wishlist & 6-Tier Data Provenance Spectrum)*

---

## 1. Executive System Architecture

The **Comparative Legislative Data Platform** (`https://legislativedata.org`) is an open-access quantitative research engine designed to ingest, standardize, mirror, and audit legislative data across international parliamentary and presidential assemblies.

The system architecture separates the **Master Canonical Variable Wishlist** (the target research schema) from the **6-Tier Data Availability & Provenance Spectrum** (how each variable is instantiated per parliament and decision point).

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

---

## 2. The 6-Tier Data Availability & Provenance Spectrum

Every variable in our Master Canonical Catalog is evaluated per assembly, per session, and at every decision point against the 6-tier spectrum:

1. **`NATIVE_DIRECT`:** Served out-of-the-box in host assembly API/feed (JSON/XML).
2. **`DERIVED_DETERMINISTIC`:** Generated deterministically via simple pipeline joins, lookup tables, or date arithmetic.
3. **`DERIVED_HUMAN_CODED`:** Manually hand-coded by human researchers, domain experts, or PhD coders (serving as ground truth).
4. **`DERIVED_SYNTHETIC_AI`:** Synthesized via NLP/LLM models, carrying an explicit **AI Validation Lifecycle Status**:
   - `UNVERIFIED_DRAFT`: Published immediately post-extraction for open crowdsourced peer audit.
   - `SAMPLE_VALIDATED`: Audited against a randomized human sample (reporting precision/recall).
   - `GOLD_BENCHMARKED`: Benchmarked against Tier 3 (`DERIVED_HUMAN_CODED`) ground truth.
5. **`LINKED_EXTERNAL_AUTHORITY`:** Deterministically linked from established, peer-reviewed external benchmark datasets:
   - **ParlGov:** Cabinet IDs, Government Types (`SINGLE_PARTY_MAJORITY`, `COOPERATION_AGREEMENT`).
   - **Wikidata / EveryPolitician:** Persistent member QIDs and biographical timelines.
   - **Comparative Agendas Project (CAP):** Standardized policy topic codes.
   - **Manifesto Project (MARPOR):** Party ideology scores.
6. **`UNAVAILABLE_HARD_GAP`:** Documented institutional omissions carrying sub-reason codes (`NOT_RECORDED_BY_ASSEMBLY`, `RECORDED_BUT_UNDIGITIZED`, `RESTRICTED_ACCESS`, `COST_PROHIBITIVE`).

---

## 3. Temporal Decision-Point Member Affiliation Engine

Parliamentary arithmetic and party affiliations vary continuously across a legislative session due to by-elections, defections, whip suspensions (members becoming Independent), or election of the Speaker/Presiding Officer.

To prevent misclassifying voting behavior or sponsor alignments:
1. The platform maintains a **Date-Bounded Member Affiliation Table** (`member_party_affiliations` with `valid_from` and `valid_to` timestamps).
2. **Decision-Point Evaluation Protocol:** Whenever an event occurs at date $T$ (e.g. an amendment is tabled, a division vote is called, or a bill is introduced):
   - The engine evaluates member party affiliation on date $T$.
   - The engine computes the **exact floor seat shares and government majority margin on date $T$**:
     $$\text{Effective Majority Margin}_T = \text{Governing Voting Seats}_T - \text{Opposition Voting Seats}_T$$
   - Party rebellions ($\ge 5\%$ party defiance) and sponsor governance roles are calculated against member party status on date $T$.

---

## 4. Schema Review & Revision Protocol for Real-World Edge Cases

To handle edge cases systematically without compromising core schema stability, we establish a formal 4-step protocol:
1. **Edge Case Detection & Isolation:** Store raw payload in JSONB, tag record `schema_review_required: true`.
2. **Impact Assessment & Taxonomy Evaluation:** Check alignment against external authority taxonomies (ParlGov, CAP, Wikidata).
3. **Controlled Schema Extension:** Update catalog and Pydantic models with non-breaking enum additions.
4. **Pipeline Retro-Fit & Publication:** Re-run ETL for affected sessions and publish release notes.
