# Peer Review Commission Brief & Evaluation Guidelines

**Comparative Legislative Data Platform**  
**Version:** 2.8.0  
**Status:** Academic Consultation Brief

---

## 1. Executive Summary & Purpose

The **Comparative Legislative Data Platform** (`https://legislativedata.org`) is an open-access academic research infrastructure designed to standardize, mirror, and audit quantitative legislative data across international parliamentary and presidential assemblies.

We commission expert reviewers to evaluate our proposed **Dual-Layer Architecture**, **Master Canonical Variable Catalog**, and **7-Tier Data Availability & Provenance Framework**, and to submit a written **Peer Review Report** addressing the core evaluation questions in Section 4.

---

## 2. Dual-Layer Architecture & 7-Tier Provenance Framework

The platform operates on a dual-layer data model ("Riding Two Horses"):
1. **Layer A (Native Institutional Layer):** Preserves 100% of raw assembly-specific fields, Hansard timestamps, document word counts, motion texts, committee rosters, and individual roll-call vote choices (`payload.native`).
2. **Layer B (Canonical Comparative Layer):** Harmonises target quantitative variables (`payload.canonical`) across 11 research domains, evaluating each variable against the 7-tier provenance spectrum:

* **Tier 1: `NATIVE_DIRECT`** — Served out-of-the-box in host assembly API/feed.
* **Tier 2: `DERIVED_DETERMINISTIC`** — Generated via rule-based joins, temporal roster lookups, or date math on structured API JSON feeds.
* **Tier 3: `DERIVED_EXTRACTED`** — Programmatically parsed/extracted from unstructured PDF documents, HTML scraping, or Hansard regex parsing.
* **Tier 4: `DERIVED_HUMAN_CODED`** — Expert hand-coded ground truth from PhD dissertations or published academic datasets.
* **Tier 5: `DERIVED_SYNTHETIC_AI`** — NLP/LLM text extractions carrying AI Validation Lifecycle (`Draft` $\rightarrow$ `Sample` $\rightarrow$ `Gold`).
* **Tier 6: `LINKED_EXTERNAL_AUTHORITY`** — Linked from benchmark datasets (ParlGov, CAP, Wikidata QIDs, MARPOR).
* **Tier 7: `UNAVAILABLE_HARD_GAP`** — Documented institutional omissions carrying sub-reason codes.

*Note:* Variables pending formal audit verification are marked **`NOT_YET_CATEGORISED`**.

---

## 3. Core Research Domains (11 Domains)

1. **Domain 1: Assembly, Electoral & Executive Context:** Jurisdiction, chamber structure, government formation typology (`COOPERATION_AGREEMENT`), ParlGov cabinet link.
2. **Domain 2: Bill Identification, Sponsorship & Temporal Origin:** Local bill ID, title, neutral sponsor type, sponsor party role on introduction date, ministerial portfolio title, third-party promoter.
3. **Domain 3: Progression, Timelines & Stage Milestones:** Introduction/outcome dates, calendar/sitting durations, multi-day stage debate counts, Section 35 orders, emergency flags.
4. **Domain 4: Financial Resolutions & Procedural Motions:** Rule 9.12 Financial Resolution required/approved flags, vote dates, and tallies.
5. **Domain 5: Plenary Roll-Call Motions & Voting Coalitions:** Plenary decision-point votes (Stage 1, Financial Resolution, Emergency, Stage 3 Passage), voting coalition typologies, party cohesion rates.
6. **Domain 6: Accompanying Bill Documents & Text Size Analytics:** Document URLs (Policy Memo, Financial Memo, Explanatory Notes, Lead Committee Report), word counts (`introduced`, `post_committee`, `enacted`), text expansion ratio, CAP topic code, fiscal impact flag.
7. **Domain 7: Final Disposition & Inter-Chamber Mechanisms:** Final status, termination mechanism, promulgation date.
8. **Domain 8: Macro Amendment Aggregates & Text Alteration:** Amendments tabled/agreed, non-executive amendments count, committee executive acceptance rate, text alteration score.
9. **Domain 9: Micro Amendment Entity Records (`CanonicalAmendment`):** Granular amendment-level lodgings, Marshalled List numbers, target clauses, text alterations, government positions, division votes.
10. **Domain 10: Committee Context & Roster Engine (`CommitteeContext`):** Committee classification, Convener/Deputy Convener MSP IDs, membership rosters with active date bounds.
11. **Domain 11: Parsed Proceedings & Official Report Analytics (`ParsedProceedings`):** Official Report debate transcripts, total word counts, speech interventions, participating MSPs count, word count shares (Ministers vs Backbenchers).
