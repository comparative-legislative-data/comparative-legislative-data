# Methodological Foundation & Provenance Framework

**Specification Version:** 2.8.0  
**Purpose:** Formal scientific specification of the Dual-Layer Architecture, 7-Tier Provenance Spectrum, Two-Pass Audit Protocol, and DA*RT Compliance.

---

## 1. The Dual-Layer Architecture ("Riding Two Horses")

Comparative legislative research requires balancing host assembly specificities with comparative cross-national standardization:

* **Layer A (Native Assembly Layer):** Preserves 100% of raw host API keys, Hansard debate text, and local parliamentary terminology (e.g. Scottish Parliament `/api/bills`, `/api/members`). Endpoints are served as transparent raw mirrors without derived pollution.
* **Layer B (Canonical Comparative Layer):** Standardized 119-variable research wishlist, evaluated against strict provenance tiers at specific decision-point dates ($T$).

---

## 2. The 7-Tier Provenance Spectrum

Every canonical variable is assigned a precise provenance tier:

1. **`NATIVE_DIRECT` (Tier 1):** Served directly in official host assembly API feeds (`data.parliament.scot/api`).
2. **`DERIVED_DETERMINISTIC` (Tier 2):** Calculated via 100% rule-based relational joins or date arithmetic on native API keys with 0% parsing ambiguity.
3. **`DERIVED_EXTRACTED` (Tier 3):** Programmatic PDF/HTML document extractions, regex parsing, or Hansard text scraping.
4. **`DERIVED_HUMAN_CODED` (Tier 4):** Hand-coded ground truth from PhD dissertations or published academic datasets.
5. **`DERIVED_SYNTHETIC_AI` (Tier 5):** NLP/LLM probabilistic text extractions carrying AI validation badges (`UNVERIFIED_DRAFT`, `SAMPLE_VALIDATED`, `GOLD_BENCHMARKED`).
6. **`LINKED_EXTERNAL_AUTHORITY` (Tier 6):** Crosswalk identifiers linked from peer-reviewed datasets (ParlGov, CAP, Wikidata QIDs, MARPOR).
7. **`UNAVAILABLE_HARD_GAP` (Tier 7):** Documented institutional omissions carrying sub-reason codes (`NOT_RECORDED_BY_ASSEMBLY`, `NOT_APPLICABLE_TO_ASSEMBLY`).

---

## 3. Two-Pass Empirical Audit Methodology

To prevent data hallucination, assembly audits follow a strict 2-pass protocol:

### Pass 1: Empirical API Ground Truth (Binary Baseline)
Only `NATIVE_DIRECT` (keys literally present in host API feeds) and `DERIVED_DETERMINISTIC` (100% rule-based joins on host keys) are assigned. This establishes a zero-hallucination empirical baseline.

### Pass 2: Candidate Assessment & Specification (Non-Binary Hypotheses)
Variables requiring document parsing, Hansard text scraping, external crosswalks, or hard gap verification remain officially **`NOT_YET_CATEGORISED`** in their primary tier, carrying a **Candidate Specification**:
- `candidate_tier`: (e.g. `CANDIDATE_DERIVED_EXTRACTED`)
- `target_document_source`: Exact document print or API text stream
- `proposed_extraction_method`: Proposed parsing algorithm
- `validation_status`: `PROVISIONAL_HYPOTHESIS`
- `risk_factors`: Technical risks (PDF layout shifts, OCR errors)

---

## 4. Promotion Criteria

A candidate variable is **only promoted** to its final tier after an extraction script is written, executed, and benchmarked against historical records with verified **100% repeatability**.

---

## 5. DA*RT Compliance & Replication Code Generation

All interactive visualizations and statistical models generated on the platform automatically produce copyable SQL, R (`ggplot2`, `dplyr`), and Python (`pandas`) replication scripts. This guarantees compliance with Data Access and Research Transparency (DA*RT) mandates enforced by leading journals (*APSR*, *AJPS*).
