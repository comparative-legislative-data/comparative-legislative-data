# Legislative Assembly Data Architecture & Provenance Framework

**Specification Version:** 2.8.0  
**Purpose:** Formal specification of the Dual-Layer Data Architecture and 7-Tier Data Availability & Provenance Spectrum.

---

## 1. Dual-Layer Data Architecture ("Riding Two Horses")

Legislative scholars require two distinct layers of data to conduct rigorous research:

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
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
            EVALUATED AT SPECIFIC DECISION-POINT DATES (T)
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│   LAYER B: CANONICAL COMPARATIVE LAYER (Harmonised Research Wishlist)   │
│   └─ Evaluated against the 7-Tier Data Availability & Provenance Matrix │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. The 7-Tier Provenance Spectrum

Every canonical variable in an assembly audit blueprint is assigned a precise provenance tier:

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

### Tier Definitions

1. **`NATIVE_DIRECT` (Tier 1):** Native key served directly in official host assembly API or raw structured JSON data feed.
2. **`DERIVED_DETERMINISTIC` (Tier 2):** Pure rule-based relational joins, temporal interval calculations, or date lookups performed on structured native API JSON feeds (0% parsing risk).
3. **`DERIVED_EXTRACTED` (Tier 3):** Programmatic text extractions, regex parsing, or HTML/PDF document scraping from unstructured papers, Hansard debate transcripts, or Marshalled Amendment Lists.
4. **`DERIVED_HUMAN_CODED` (Tier 4):** Expert hand-coded ground truth from PhD dissertations or published academic datasets.
5. **`DERIVED_SYNTHETIC_AI` (Tier 5):** NLP/LLM text extractions carrying the AI Validation Lifecycle (`UNVERIFIED_DRAFT`, `SAMPLE_VALIDATED`, `GOLD_BENCHMARKED`).
6. **`LINKED_EXTERNAL_AUTHORITY` (Tier 6):** Linked from benchmark peer-reviewed datasets (ParlGov, CAP, Wikidata QIDs, MARPOR).
7. **`UNAVAILABLE_HARD_GAP` (Tier 7):** Documented institutional data omissions carrying sub-reason codes (`NOT_RECORDED_BY_ASSEMBLY`, `RECORDED_BUT_UNDIGITIZED`, `RESTRICTED_ACCESS`, `COST_PROHIBITIVE`, `NOT_APPLICABLE_TO_ASSEMBLY`).

*Note:* Variables awaiting formal empirical audit verification are assigned **`NOT_YET_CATEGORISED`**.
