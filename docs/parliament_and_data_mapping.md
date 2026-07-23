# Master System Architecture: Parliament Data Evaluation & Ingestion Pipeline

**Comparative Legislative Data Platform**  
*System Architecture & Data Provenance Specification*  
*Version 2.2.0 (7-Tier Spectrum, Temporal Decision-Point Engine & Schema Revision Protocol)*

---

## 1. Executive System Architecture

The **Comparative Legislative Data Platform** (`https://legislativedata.org`) is an open-access quantitative research engine designed to ingest, standardize, mirror, and audit legislative data across international parliamentary and presidential assemblies.

The architecture is built around a **7-Tier Data Availability & Provenance Model** and a **Temporal Decision-Point Engine**. Every variable in our Master Canonical Catalog is evaluated per assembly, per session, and **at every decision point** (bill introduction, committee stage amendment tabling, roll-call division, final passage) to guarantee point-in-time quantitative accuracy.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ (1) MASTER CANONICAL VARIABLE WISHLIST (The Ideal Quantitative Research Schema)             │
└───────────────────────────────┬─────────────────────────────────────────────────────────────┘
                                │
                      EVALUATED AT SPECIFIC DECISION-POINT DATES (T)
                                │
    ┌────────────────┬──────────┼──────────┬──────────────────┬──────────────────┐
    ▼                ▼          ▼          ▼                  ▼                  ▼
┌──────────────┐┌──────────┐┌──────────┐┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ (2) NATIVE   ││ (3) DERIV││ (4) DERIV││ (5) DERIVED  │   │ (6) LINKED   │   │ (7) HARD GAP │
│     DIRECT   ││ DETERMIN ││  HUMAN   ││ SYNTHETIC-AI │   │ EXTERNAL     │   │ UNAVAILABLE  │
├──────────────┤├──────────┤├──────────┤├──────────────┤   ├──────────────┤   ├──────────────┤
│ Host API or  ││ Rule-    ││ Expert   ││ NLP/LLM text │   │ Benchmark    │   │ Missing,     │
│ raw feed     ││ based    ││ hand-    ││ extractions  │   │ datasets     │   │ unrecorded,  │
│ (JSON/XML).  ││ joins &  ││ coding & ││ with AI      │   │ (ParlGov,    │   │ or non-      │
│              ││ date     ││ PhD data ││ Validation   │   │ Wikidata,    │   │ digitized    │
│              ││ math.    ││ (Gold).  ││ Lifecycle.   │   │ CAP, MARPOR).│   │ (with reason)│
└──────────────┘└──────────┘└──────────┘└──────────────┘   └──────────────┘   └──────────────┘
```

---

## 2. The 7-Tier Legislative Availability & Provenance Model

1. **`CANONICAL_WISHLIST_TARGET`:** Universal target definition in the Master Catalog.
2. **`NATIVE_DIRECT`:** Served out-of-the-box in host APIs or raw bulk data feeds.
3. **`DERIVED_DETERMINISTIC`:** Generated deterministically via pipeline joins or date arithmetic.
4. **`DERIVED_HUMAN_CODED`:** Manually hand-coded by human researchers, subject experts, or PhD coders (serving as ground truth).
5. **`DERIVED_SYNTHETIC_AI`:** Synthesized via NLP/LLM models, carrying an explicit **AI Validation Lifecycle Status**:
   - `UNVERIFIED_DRAFT`: Published immediately post-extraction for open crowdsourced peer audit.
   - `SAMPLE_VALIDATED`: Audited against a randomized human sample (reporting precision/recall).
   - `GOLD_BENCHMARKED`: Benchmarked against Tier 4 (`DERIVED_HUMAN_CODED`) ground truth.
6. **`LINKED_EXTERNAL_AUTHORITY`:** Deterministically linked from established, peer-reviewed external benchmark datasets:
   - **ParlGov:** Cabinet IDs, Government Types (`SINGLE_PARTY_MAJORITY`, `COOPERATION_AGREEMENT`).
   - **Wikidata / EveryPolitician:** Persistent member QIDs and biographical timelines.
   - **Comparative Agendas Project (CAP):** Standardized policy topic codes.
   - **Manifesto Project (MARPOR):** Party ideology scores.
7. **`UNAVAILABLE_HARD_GAP`:** Documented institutional omissions carrying sub-reason codes (`NOT_RECORDED_BY_ASSEMBLY`, `RECORDED_BUT_UNDIGITIZED`, `RESTRICTED_ACCESS`, `COST_PROHIBITIVE`).

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

As the platform ingests real-world data from diverse assemblies, procedural edge cases will inevitably emerge (e.g. unique committee structures, multi-party cooperation pacts, or non-standard voting rules).

To handle edge cases systematically without compromising core schema stability, we establish a formal 4-step protocol:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. EDGE CASE DETECTION & ISOLATION                                                          │
│    - When ingestion hits an unmapped procedural event, store payload in raw JSONB.           │
│    - Flag record with `SCHEMA_REVIEW_REQUIRED: true` and assign temporary fallback enum.    │
└───────────────────────────────┬─────────────────────────────────────────────────────────────┘
                                │
┌───────────────────────────────┴─────────────────────────────────────────────────────────────┐
│ 2. IMPACT ASSESSMENT & TAXONOMY EVALUATION                                                  │
│    - Evaluate whether edge case represents a jurisdiction-specific value or a universal     │
│      comparative phenomenon.                                                                │
│    - Check alignment against external authority taxonomies (ParlGov, CAP, Wikidata).       │
└───────────────────────────────┬─────────────────────────────────────────────────────────────┘
                                │
┌───────────────────────────────┴─────────────────────────────────────────────────────────────┐
│ 3. CONTROLLED SCHEMA EXTENSION                                                              │
│    - Propose enum addition or field adjustment in `docs/canonical_variable_catalog.md`.      │
│    - Update Pydantic v2 model definitions in `docs/schema.md`.                              │
│    - Maintain backwards compatibility via non-breaking enum additions.                      │
└───────────────────────────────┬─────────────────────────────────────────────────────────────┘
                                │
┌───────────────────────────────┴─────────────────────────────────────────────────────────────┐
│ 4. PIPELINE RETRO-FIT & PUBLICATION                                                         │
│    - Re-run ETL transformation for affected jurisdiction sessions.                         │
│    - Publish updated schema release with changelog entry.                                   │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```
