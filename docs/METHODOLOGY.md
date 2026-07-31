# Methodological Foundation & Provenance Framework (General)

**Specification Version:** 2.8.0  
**Purpose:** Formal scientific specification of the Dual-Layer Architecture, 7-Tier Provenance Spectrum, Two-Pass Audit Protocol, and DA*RT Compliance.

---

## 1. The Dual-Layer Architecture ("Riding Two Horses")

Comparative legislative research requires balancing host assembly specificities with comparative cross-national standardization:
*   **Layer A (Native Assembly Layer):** Preserves 100% of raw host API keys, Hansard debate text, and local parliamentary terminology. Endpoints are served as transparent raw mirrors without derived pollution.
*   **Layer B (Canonical Comparative Layer):** Standardized research wishlist of variables, evaluated against strict provenance tiers at specific decision-point dates ($T$).

---

## 2. The 7-Tier Provenance Spectrum

Every canonical variable is assigned a precise provenance tier:
1.  **`NATIVE_DIRECT` (Tier 1):** Served directly in official host assembly API feeds.
2.  **`DERIVED_DETERMINISTIC` (Tier 2):** Calculated via 100% rule-based relational joins or date arithmetic on native API keys with 0% parsing ambiguity.
3.  **`DERIVED_EXTRACTED` (Tier 3):** Programmatic PDF/HTML document extractions, regex parsing, or Hansard text scraping.
4.  **`DERIVED_HUMAN_CODED` (Tier 4):** Hand-coded ground truth from peer-reviewed academic datasets or manual coding audits.
5.  **`DERIVED_SYNTHETIC_AI` (Tier 5):** NLP/LLM probabilistic text extractions carrying AI validation badges (`UNVERIFIED_DRAFT`, `SAMPLE_VALIDATED`, `GOLD_BENCHMARKED`).
6.  **`LINKED_EXTERNAL_AUTHORITY` (Tier 6):** Crosswalk identifiers linked from peer-reviewed datasets (ParlGov, CAP, Wikidata QIDs, MARPOR).
7.  **`UNAVAILABLE_HARD_GAP` (Tier 7):** Documented institutional omissions carrying sub-reason codes (`NOT_RECORDED_BY_ASSEMBLY`, `NOT_APPLICABLE_TO_ASSEMBLY`).

---

## 3. Two-Pass Empirical Audit Methodology

To prevent data hallucination, assembly audits follow a strict 2-pass protocol:

### Pass 1: Empirical API Ground Truth (Binary Baseline)
Only `NATIVE_DIRECT` (keys literally present in host API feeds) and `DERIVED_DETERMINISTIC` (100% rule-based joins on host keys) are assigned. This establishes a zero-hallucination empirical baseline.

### Pass 2: Candidate Assessment & Specification (Non-Binary Hypotheses)
Variables requiring document parsing, Hansard text scraping, external crosswalks, or hard gap verification remain officially **`NOT_YET_CATEGORISED`** in their primary tier, carrying a **Candidate Specification**:
*   `candidate_tier`: (e.g. `CANDIDATE_DERIVED_EXTRACTED`)
*   `target_document_source`: Exact document print or API text stream
*   `proposed_extraction_method`: Proposed parsing algorithm
*   `validation_status`: `PROVISIONAL_HYPOTHESIS`
*   `risk_factors`: Technical risks (PDF layout shifts, OCR errors)

---

## 4. Promotion Criteria

A candidate variable is **only promoted** to its final tier after an extraction script is written, executed, and benchmarked against historical records with verified **100% repeatability**.

---

## 5. DA*RT Compliance & Replication Code Generation

All interactive visualizations and statistical models generated on the platform automatically produce copyable SQL, R (`ggplot2`, `dplyr`), and Python (`pandas`) replication scripts. This guarantees compliance with Data Access and Research Transparency (DA*RT) mandates enforced by leading journals (*APSR*, *AJPS*).

---

## 6. Database-First Visualization Principle (No Client-Side "Magic")

To ensure strict scientific reproducibility and data auditability, the frontend is forbidden from performing any data transformations, categorization overrides, or client-side filtering logic. The Svelte visualization layer acts strictly as a passive presentation layer. 
*   **Replication Parity:** Every plotted metric, filter group, or count corresponds exactly to a physical table column or SQL compiler view in Database B. 
*   **Download Integrity:** A researcher downloading the canonical CSV, Parquet, or SQLite databases will get the exact same counts, success rates, and category shapes as those visualized on the dashboard.

---

## 7. Comparative Legislative Normalization (General Rules)

Assembly terminology changes over time and across countries, requiring systematic standardization to enable comparative long-term analysis:
*   **Sessional Terminology Aggregation:** Raw designations representing executive bills must be aggregated into a unified comparative `Government` category to prevent false comparative gaps caused by sessional nomenclature shifts.
*   **Non-Partisan Delineation:** 
    *   *Non-Elected Officers:* Appointed, non-elected government legal advisers introducing legislation on behalf of the cabinet must be assigned a unique synthetic party ID to reflect their non-partisan status.
    *   *Private Promoters:* External non-assembly corporate or municipal bodies promoting private legislation must be assigned a separate synthetic party ID.
    *   *Elected Independents:* Elected politicians sitting as independents maintain standard political party codes, ensuring no blending occurs between these distinct categories.

---

## 8. Temporal Resolution of Session Boundaries and Outcomes (General Rules)

*   **Governing Cabinet Status (Deferred to future Human-Coded Phase):** Since cabinet coalitions and portfolio assignments do not exist in raw assembly OData feeds (and are classified as Tier 4 Human-Coded data), this variable is deferred and excluded from the initial Tier 1 / Tier 2 build phase.
*   **Binary Outcome Baselines:** All parliamentary outcomes are simplified into a binary indicator (`PASSED` vs. `FALLEN`). All bills that do not pass Stage 3 (withdrawn by sponsor, voted down, or lapsed at sessional dissolution) are grouped under the category `FALLEN` to establish a standard success-rate benchmark.
*   **Sessional Date Partitions:** Sessional cohorts are partitioned strictly using calendar date boundaries corresponding to the opening day of each parliament.
