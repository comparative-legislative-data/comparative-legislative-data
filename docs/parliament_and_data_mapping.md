# Parliament & Data Mapping Specification

**Comparative Legislative Data Platform**  
**Version:** 2.4.0  
**Specification:** Master Architecture, Dual-Layer Data Engine & 6-Tier Provenance Mapping

---

## 1. System Architecture: Dual-Layer Data Engine

The **Comparative Legislative Data Platform** (`https://legislativedata.org`) is an open-access quantitative research engine designed to ingest, standardize, mirror, and audit legislative data across international parliamentary and presidential assemblies.

The system architecture cleanly separates the **Native Institutional Layer** (Layer A: high-resolution raw assembly data) from the **Canonical Comparative Layer** (Layer B: harmonised target research metrics evaluated against the 6-Tier Data Availability Spectrum):

```
  LAYER A: NATIVE INSTITUTIONAL DATA (Preserving 100% Raw Granularity)
  ├─ Raw Hansard API feeds, native stage codes, motion texts, word counts,
  └─ member rosters, and individual roll-call votes (stored in payload.native).
                                     │
                  EVALUATED AT SPECIFIC DECISION-POINT DATES (T)
                                     │
                                     ▼
  LAYER B: CANONICAL COMPARATIVE LAYER (Harmonised Research Wishlist)
  └─ Evaluated against the 6-Tier Data Availability & Provenance Spectrum:

    ┌────────────────┬──────────────┬──────────────┬──────────────────┬──────────────────┐
    ▼                ▼              ▼              ▼                  ▼                  ▼
┌──────────────┐┌──────────────┐┌──────────────┐┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ 1. NATIVE    ││ 2. DERIVED   ││ 3. DERIVED   ││ 4. DERIVED   │   │ 5. LINKED    │   │ 6. HARD GAP  │
│    DIRECT    ││ DETERMINISTIC││  HUMAN-CODED ││ SYNTHETIC-AI │   │ EXTERNAL     │   │ UNAVAILABLE  │
├──────────────┤├──────────────┤├──────────────┤├──────────────┤   ├──────────────┤   ├──────────────┤
│ Served out-  ││ Rule-based   ││ Expert hand- ││ NLP/LLM text │   │ Peer-        ││ Missing,     │
│ of-the-box   ││ joins, date  ││ coding & PhD ││ extractions  │   │ reviewed     ││ unrecorded,  │
│ in host API. ││ lookups.     ││ datasets.    ││ + Lifecycle. │   │ datasets.    ││ undigitized. │
└──────────────┘└──────────────┘└──────────────┘└──────────────┘   └──────────────┘   └──────────────┘
```

---

## 2. The 3-Step Iterative Pilot Audit Workflow

To ensure our Master Wishlist Target is methodologically sound and grounded in empirical legislative reality, the platform uses a 3-step inductive-deductive scientific loop:

1. **Step 1 (Starting Wishlist Catalog):** Establish the initial target quantitative variables (~40 variables across 8 research domains).
2. **Step 2 (Empirical Assembly Audit - Scottish Parliament `GB-SCT` Pilot):**
   - Conduct an exhaustive audit of Holyrood's native APIs, Hansard feeds, and PhD dissertation hand-coded datasets.
   - Categorize every native variable on the 6-tier provenance spectrum.
   - Identify unmapped native variables (e.g. Stage 1 Lead Committee Report date, Section 35 Orders, Financial Resolutions).
3. **Step 3 (Wishlist Refinement):** Re-evaluate findings against the Master Wishlist Catalog, incorporating new metrics, adjusting definitions, and deleting unworkable variables.

---

## 3. The 6-Tier Provenance Spectrum Definitions

1. **`NATIVE_DIRECT` (Tier 1):** Native key served directly in official host assembly API or raw data feed.
2. **`DERIVED_DETERMINISTIC` (Tier 2):** Variable calculated via rule-based joins, date arithmetic, or roster lookups.
3. **`DERIVED_HUMAN_CODED` (Tier 3):** Expert hand-coded ground truth from PhD dissertations or published academic datasets.
4. **`DERIVED_SYNTHETIC_AI` (Tier 4):** NLP/LLM text extractions carrying the AI Validation Lifecycle (`UNVERIFIED_DRAFT`, `SAMPLE_VALIDATED`, `GOLD_BENCHMARKED`).
5. **`LINKED_EXTERNAL_AUTHORITY` (Tier 5):** Linked from benchmark peer-reviewed datasets (ParlGov, CAP, Wikidata, MARPOR).
6. **`UNAVAILABLE_HARD_GAP` (Tier 6):** Documented institutional data omissions carrying sub-reason codes (`NOT_RECORDED_BY_ASSEMBLY`, `RECORDED_BUT_UNDIGITIZED`, `RESTRICTED_ACCESS`, `COST_PROHIBITIVE`).

---

## 4. Temporal Decision-Point Engine

Politician party affiliations, presiding officer neutrality, and floor majority margins change over time. Every decision point (bill introduction date, Stage 1 report date, committee amendment tabling date, division vote date) evaluates:
$$\text{Effective Majority Margin}_T = \text{Governing Seats}_T - \text{Opposition Seats}_T$$
$$\text{Party Dissent Rate}_T = \frac{\text{Members of Party } P \text{ voting against party majority at } T}{\text{Total Members of Party } P \text{ voting at } T}$$
