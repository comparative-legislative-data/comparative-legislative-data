# Legislative Assembly Data Architecture & Provenance Framework

**Specification Version:** 2.8.0  
**Purpose:** Formal specification of the Dual-Layer Data Architecture, 7-Tier Provenance Spectrum, and Two-Pass Empirical Audit Methodology.

---

## 1. Dual-Layer Data Architecture ("Riding Two Horses")

Legislative scholars require two distinct layers of data to conduct rigorous comparative research:

```
┌─────────────────────────────────────────────────────────────────────────┐
│              HOST LEGISLATIVE ASSEMBLY (e.g. Holyrood, Westminster)    │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                                     ▼
                      INDUCTIVE PILOT AUDIT WORKFLOW
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│   LAYER A: NATIVE INSTITUTIONAL LAYER (Assembly-Specific Payload)       │
│   └─ Preserves 100% of raw fields, Hansard text, local terminology.     │
│   └─ Transparent host API endpoints (No derived pollution).             │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
            EVALUATED AT SPECIFIC DECISION-POINT DATES (T)
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│   LAYER B: CANONICAL COMPARATIVE LAYER (Harmonised Research Wishlist)   │
│   └─ Evaluated against the 7-Tier Data Availability & Provenance Matrix │
│   └─ Audited via the Two-Pass Candidate Assessment Framework           │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. The 7-Tier Provenance Spectrum

Every canonical variable in an assembly audit blueprint is assigned a precise provenance tier based on how it is sourced:

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 1. NATIVE    │ │ 2. DERIVED   │ │ 3. DERIVED   │ │ 4. DERIVED   │ │ 5. DERIVED   │ │ 6. LINKED    │ │ 7. HARD GAP  │
│    DIRECT    │ │ DETERMINISTIC│ │    EXTRACTED │ │  HUMAN-CODED │ │ SYNTHETIC-AI │ │ EXTERNAL     │ │ UNAVAILABLE  │
├──────────────┤ ├──────────────┤ ├──────────────┤ ├──────────────┤ ├──────────────┤ ├──────────────┤ ├──────────────┤
│ Served out-  │ │ Pure joins,  │ │ Programmatic │ │ Expert hand- │ │ NLP/LLM text │ │ Peer-        │ │ Missing,     │
│ of-the-box   │ │ date math on │ │ PDF/HTML text│ │ coding & PhD │ │ probabilistic│ │ reviewed     │ │ unrecorded,  │
│ in host API. │ │ native JSON. │ │ extractions. │ │ datasets.    │ │ extractions. │ │ benchmark IDs│ │ or N/A.      │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

### Provenance Tier Definitions

1. **`NATIVE_DIRECT` (Tier 1):** Native key served directly in the official host assembly API or raw structured JSON data feed.
2. **`DERIVED_DETERMINISTIC` (Tier 2):** Pure rule-based relational joins, temporal interval calculations, or date lookups performed on structured native API JSON feeds (0% parsing risk).
3. **`DERIVED_EXTRACTED` (Tier 3):** Programmatic text extractions, regex parsing, or HTML/PDF document scraping from unstructured papers, Hansard debate transcripts, or Marshalled Amendment Lists.
4. **`DERIVED_HUMAN_CODED` (Tier 4):** Expert hand-coded ground truth from PhD dissertations or published academic datasets.
5. **`DERIVED_SYNTHETIC_AI` (Tier 5):** NLP/LLM text extractions carrying the AI Validation Lifecycle (`UNVERIFIED_DRAFT`, `SAMPLE_VALIDATED`, `GOLD_BENCHMARKED`).
6. **`LINKED_EXTERNAL_AUTHORITY` (Tier 6):** Linked from benchmark peer-reviewed datasets (ParlGov, CAP, Wikidata QIDs, MARPOR).
7. **`UNAVAILABLE_HARD_GAP` (Tier 7):** Documented institutional data omissions carrying sub-reason codes (`NOT_RECORDED_BY_ASSEMBLY`, `RECORDED_BUT_UNDIGITIZED`, `RESTRICTED_ACCESS`, `COST_PROHIBITIVE`, `NOT_APPLICABLE_TO_ASSEMBLY`).

---

## 3. Two-Pass Empirical Audit Methodology

To ensure absolute scientific rigor and prevent data hallucination, we separate the audit process into two distinct phases:

### Phase 1: Empirical API Ground Truth (Strict Binary Baseline)
In Pass 1, we evaluate variables **strictly against the native open data API feeds** (`data.parliament.scot/api`):
- **`NATIVE_DIRECT`**: Binary fact. The field literally exists in the host JSON payload or it does not.
- **`DERIVED_DETERMINISTIC`**: Binary fact. A 100% deterministic rule-based join or math calculation on host JSON keys exists with 0% parsing ambiguity, or it does not.
- **Result:** Establishes a rock-solid, zero-hallucination empirical baseline.

### Phase 2: Candidate Assessment & Extraction Specification (Non-Binary Territory)
Variables requiring document parsing, PDF text extractions, Hansard debate word counts, external crosswalks, or procedural hard gap verification enter a non-binary, methodological space.

#### The Candidate Assessment Protocol:
During audit assessment, non-API variables are **not** prematurely assigned final execution tiers (e.g. claiming a PDF parser works before writing it). Instead, they remain officially **`NOT_YET_CATEGORISED`** in their primary tier while carrying a **Candidate Specification**:

```yaml
provenance_tier: NOT_YET_CATEGORISED
candidate_tier: CANDIDATE_DERIVED_EXTRACTED
target_document_source: "PDF Marshalled List of Amendments"
proposed_extraction_method: "PyMuPDF layout parsing & regex header matching"
validation_status: PROVISIONAL_HYPOTHESIS
risk_factors: "PDF table formatting shifts across Sessions 1–6"
```

---

## 4. Promotion & Validation Lifecycle

A variable is **only formally promoted** from `PROVISIONAL_HYPOTHESIS` to its final provenance tier when it passes empirical validation:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    PROVISIONAL CANDIDATE HYPOTHESIS                     │
│                    (Target Source + Proposed Method)                    │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
                          BENCHMARK & STRESS TEST
                                     │
         ┌───────────────────────────┴───────────────────────────┐
         ▼                                                       ▼
100% REPEATABLE & DETERMINISTIC                         REQUIRES NLP/LLM OR HUMAN
         │                                                       │
         ▼                                                       ▼
   PROMOTED TO:                                            PROMOTED TO:
`DERIVED_EXTRACTED`                                  `DERIVED_SYNTHETIC_AI`
                                                                OR
                                                     `DERIVED_HUMAN_CODED`
```

### Promotion Criteria:
1. **`DERIVED_EXTRACTED`**: Promoted only after an extraction parser is written, executed on historical records, and verified to achieve 100% repeatability with zero manual interventions.
2. **`DERIVED_SYNTHETIC_AI`**: Assigned if extraction requires LLM/NLP probabilistic parsing, carrying explicit validation badges (`UNVERIFIED_DRAFT`, `SAMPLE_VALIDATED`, `GOLD_BENCHMARKED`).
3. **`DERIVED_HUMAN_CODED`**: Assigned if extraction requires manual expert coding.
4. **`UNAVAILABLE_HARD_GAP`**: Promoted after procedural rules (e.g., Standing Orders) confirm institutional non-existence or non-applicability.

---

## 5. Strict Separation of API Endpoints vs Blueprint Variables

- **Native Host API Endpoints (`Section 1`):** Transparent mirrors of host assembly endpoints. They must **never** be polluted with derived comparative variables or artificial provenance badges. The payload inspector modal displays **only raw keys revealed directly by the host API response payload**.
- **Canonical Comparative Blueprint (`Section 2`):** Our standardized 119-variable institutional research catalog, cleanly reflecting Pass 1 empirical ground truth and Pass 2 candidate specifications.
