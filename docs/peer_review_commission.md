# Peer Review Commission Brief & Evaluation Guidelines

**Comparative Legislative Data Platform**  
**Version:** 2.4.0  
**Status:** Academic Consultation Brief

---

## 1. Executive Summary & Purpose

The **Comparative Legislative Data Platform** (`https://legislativedata.org`) is an open-access academic research infrastructure designed to standardize, mirror, and audit quantitative legislative data across international parliamentary and presidential assemblies.

We commission expert reviewers to evaluate our proposed **Dual-Layer Architecture**, **Master Canonical Variable Catalog**, and **6-Tier Data Availability & Provenance Framework**, and to submit a written **Peer Review Report** addressing the core evaluation questions in Section 4.

---

## 2. Dual-Layer Architecture & 6-Tier Provenance Framework

The platform operates on a dual-layer data model:
1. **Layer A (Native Institutional Layer):** Preserves 100% of raw assembly-specific fields, Hansard timestamps, document word counts, motion texts, and individual roll-call vote choices (`payload.native`).
2. **Layer B (Canonical Comparative Layer):** Harmonises target quantitative variables (`payload.canonical`) across 8 research domains, evaluating each variable against the 6-tier provenance spectrum:

* **Tier 1: `NATIVE_DIRECT`** — Served out-of-the-box in host assembly API/feed.
* **Tier 2: `DERIVED_DETERMINISTIC`** — Generated via rule-based joins or date arithmetic.
* **Tier 3: `DERIVED_HUMAN_CODED`** — Expert hand-coded ground truth from PhD dissertations or academic datasets.
* **Tier 4: `DERIVED_SYNTHETIC_AI`** — NLP/LLM text extractions carrying AI Validation Lifecycle (`Draft` $\rightarrow$ `Sample` $\rightarrow$ `Gold`).
* **Tier 5: `LINKED_EXTERNAL_AUTHORITY`** — Linked from benchmark datasets (ParlGov, CAP, Wikidata, MARPOR).
* **Tier 6: `UNAVAILABLE_HARD_GAP`** — Documented institutional omissions carrying sub-reason codes.

---

## 3. Core Research Domains & Master Wishlist Summary

1. **Domain 1: Assembly, Electoral & Executive Context:** Jurisdiction, chamber structure, government formation typology (`COOPERATION_AGREEMENT`), ParlGov cabinet link.
2. **Domain 2: Bill Identification, Sponsorship & Temporal Origin:** Local bill ID, title, neutral sponsor type, sponsor party role on introduction date.
3. **Domain 3: Progression, Timelines & Stage Milestones:** Introduction/outcome dates, calendar/sitting durations, stage-by-stage progression milestones (`stage_milestones`), programme/guillotine/emergency/consent flags.
4. **Domain 4: Final Disposition & Inter-Chamber Mechanisms:** Final status, termination mechanism, promulgation date, chamber ping-pong count.
5. **Domain 5: Bill Documentation & Text Size Analytics:** Document URLs, word counts (`introduced`, `post_committee`, `enacted`), text expansion ratio, CAP topic code, fiscal impact flag.
6. **Domain 6: Committee Scrutiny & Evidence:** Lead committee name, written evidence submissions count.
7. **Domain 7: Decision-Point Amendments & Text Alteration:** Amendments tabled/agreed, non-executive amendments count, committee executive acceptance rate, text alteration score.
8. **Domain 8: Temporal Divisions, Motion Types & Voting Coalitions:** Divisions count, motion breakdown (`STAGE_1_AGREEMENT`, `FINANCIAL_RESOLUTION`, `EMERGENCY_DESIGNATION`, `STAGE_3_PASSAGE`), effective majority margin at vote date $T$, party dissent rate, coalition typology.

---

## 4. Commission Questions for Written Report

### Area 1: Dual-Layer Architecture & Variable Scope
1. Does the **Dual-Layer Architecture** (preserving 100% native institutional fields alongside canonical comparative metrics) effectively resolve the tension between single-country depth and cross-national comparability?
2. Does the **Master Canonical Variable Catalog** cover the necessary quantitative variables for researching legislative effectiveness, executive dominance, stage timelines, voting coalitions, and procedural obstruction?
3. Are there critical variables in comparative legislative studies that are missing and should be added?

### Area 2: Provenance Spectrum, Stage Milestones & Voting Analytics
4. Is the 6-tier provenance spectrum methodologically sound for academic publication?
5. Does evaluating politician affiliation, majority margins, and party dissent rates at **every decision point date $T$** resolve temporal changes in parliamentary majority status?
6. How effectively does tracking document word counts across stages (`introduced` vs `enacted`) measure legislative text expansion?

### Area 3: Academic Utility & Data Gap Transparency
7. Does explicitly documenting host API omissions as `UNAVAILABLE_HARD_GAP` with sub-reason codes provide sufficient transparency for comparative political scientists?
8. What metadata or export format would make this platform most useful for your own quantitative research or teaching?

---

## 5. Report Submission Guidelines

Submit written peer review reports (PDF/Word format) to:
* **Primary Email:** `comparativelegislativedata@gmail.com`
* **GitHub Discussions:** `https://github.com/comparative-legislative-data/comparative-legislative-data/discussions`
* **Portal:** `https://legislativedata.org/peer-review`
