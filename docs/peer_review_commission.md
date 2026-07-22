# Peer Review Commission Brief

**Comparative Legislative Data Platform**  
*Academic Consultation & Peer Review Directive*

---

## 1. Context & Purpose

The **Comparative Legislative Data Platform** (`https://legislativedata.org`) is an open-access, academic data architecture designed to standardize, mirror, and audit quantitative legislative data across international parliamentary assemblies.

To ensure our schema, variable classifications, and data availability assessments meet the rigorous standards of political science, quantitative legislative studies, and public data engineering, we are opening a formal **Peer Review Commission**.

We invite external experts—including legislative studies scholars, political scientists, parliamentary open data practitioners, and data engineers—to evaluate our **Master Canonical Variable Catalog** ([`docs/canonical_variable_catalog.md`](file:///home/steven/Documents/github/comparativelegislativedata/docs/canonical_variable_catalog.md)) and **5-Tier Data Availability & Provenance Framework**.

---

## 2. The 5-Tier Data Availability & Provenance Framework

We request peer review feedback on our proposed 5-tier classification model, which evaluates every canonical variable per legislature:

1. **`CANONICAL_WISHLIST_TARGET`:** The universal variable definition in our Master Catalog.
2. **`NATIVE_DIRECT`:** Available directly in the host assembly's official API or raw feed (JSON/XML).
3. **`DERIVED_DETERMINISTIC`:** Generated deterministically via pipeline transformations, date math, or joins against persistent datasets (e.g. Executive Rosters). Includes an explicit confidence rating (`HIGH`, `MEDIUM`, `LOW`).
4. **`DERIVED_SYNTHETIC_AI`:** Synthesized using advanced NLP/LLM text processing, topic modeling, or structural parsing of unstructured Hansard/PDF text.
5. **`UNAVAILABLE_HARD_GAP`:** Missing natively from the host assembly, unrecorded, or resource-prohibitive to generate (Documented Open Data Gap).

---

## 3. Commission Review Questions for Academic Peers

We request expert feedback on the following specific questions:

### Question A: Variable Completeness & Taxonomy
1. Does the **Master Canonical Variable Catalog** ([`docs/canonical_variable_catalog.md`](file:///home/steven/Documents/github/comparativelegislativedata/docs/canonical_variable_catalog.md)) cover the necessary quantitative variables for researching legislative effectiveness, executive dominance, sessional timelines, voting coalitions, and procedural obstruction?
2. Are there critical variables in comparative legislative studies (e.g., guillotine/closure motions, royal consent, committee amendment disposition rates) that should be added to the catalog?

### Question B: 5-Tier Provenance & Feasibility Model
3. Is the distinction between **`DERIVED_DETERMINISTIC`** (simple joins/date math) and **`DERIVED_SYNTHETIC_AI`** (NLP/LLM text extraction) clear, robust, and methodologically sound for academic publication?
4. How should the platform handle confidence scoring when pipeline-derived fields rely on external datasets (e.g., historical party rosters)?

### Question C: Open Data Gap Transparency
5. Does documenting host API omissions as explicit **`UNAVAILABLE_HARD_GAP`** entries provide sufficient transparency for researchers conducting comparative quantitative studies?

---

## 4. Submission & Consultation Process

Peer reviewers and domain experts can submit feedback by:
- Submitting issue reviews or pull requests to the remote GitHub repository: `https://github.com/explainmecrypto/comparativelegislativedata`.
- Contacting the project team via `peer-review@legislativedata.org`.
