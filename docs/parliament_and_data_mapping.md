# Master System Architecture: Parliament Data Evaluation & Ingestion Pipeline

**Comparative Legislative Data Platform**  
*System Architecture & Data Provenance Specification*  
*Version 2.1.0 (6-Tier Data Availability & AI Validation Spectrum)*

---

## 1. Executive System Architecture

The **Comparative Legislative Data Platform** (`https://legislativedata.org`) is designed as an open-access quantitative research engine. The platform ingests, standardizes, mirrors, and audits legislative data across international parliamentary and presidential assemblies.

Rather than assuming all assemblies serve identical structured APIs, the architecture is built around a **6-Tier Data Availability & Provenance Model**. Every variable in our Master Canonical Catalog is evaluated per assembly and per session to establish explicit provenance, methodological certainty, and open data gap transparency.

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ (1) MASTER CANONICAL VARIABLE WISHLIST (The Ideal Quantitative Research Schema)             │
└───────────────────────────────┬─────────────────────────────────────────────────────────────┘
                                │
                      EVALUATED PER VARIABLE / SESSION
                                │
    ┌────────────────┬──────────┴─────────┬──────────────────┬──────────────────┐
    ▼                ▼                    ▼                  ▼                  ▼
┌──────────────┐┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│ (2) NATIVE   ││ (3) DERIVED  │   │ (4) DERIVED  │   │ (5) DERIVED  │   │ (6) HARD GAP │
│     DIRECT   ││ DETERMINISTIC│   │  HUMAN-CODED │   │ SYNTHETIC-AI │   │ UNAVAILABLE  │
├──────────────┤├──────────────┤   ├──────────────┤   ├──────────────┤   ├──────────────┤
│ Host API or  ││ Rule-based   │   │ Expert hand- │   │ NLP/LLM text │   │ Missing,     │
│ raw feed     ││ transforms & │   │ coding & PhD │   │ extraction & │   │ unrecorded,  │
│ (JSON/XML).  ││ joins        │   │ datasets     │   │ probabilistic│   │ or non-      │
│              ││ (e.g. roster │   │ (Gold        │   │ inference    │   │ digitized    │
│              ││ lookup).     │   │ Standard).   │   │ (Tier 4-     │   │ (with reason │
│              ││              │   │              │   │ benchmarked).│   │ code).       │
└──────────────┘└──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘
```

---

## 2. The 6-Tier Legislative Availability & Provenance Model

### Tier 1: `CANONICAL_WISHLIST_TARGET`
The universal definition of the variable as specified in the [Master Canonical Variable Catalog](file:///home/steven/Documents/github/comparativelegislativedata/docs/canonical_variable_catalog.md).

### Tier 2: `NATIVE_DIRECT`
Data points served directly out-of-the-box in the host assembly's official API endpoints or raw bulk data feeds (JSON/XML). No complex inference or multi-table joins are required.

### Tier 3: `DERIVED_DETERMINISTIC`
Data points constructed deterministically via pipeline logic, exact relational joins, or date arithmetic.
* *Example:* Joining `initiator_member_id` against an external Executive Roster table to derive `initiator_party_governance_role`.
* *Confidence Ratings:* Rated as `HIGH`, `MEDIUM`, or `LOW` based on join key completeness.

### Tier 4: `DERIVED_HUMAN_CODED` *(Academic Ground Truth)*
Data points manually hand-coded and verified by human researchers, political science domain experts, or doctoral dissertation coders.
* *Role:* Serves as the high-accuracy "Gold Standard" for quantitative research and provides the ground truth required to train and validate Tier 5 AI pipelines.

### Tier 5: `DERIVED_SYNTHETIC_AI` *(Probabilistic Text Intelligence)*
Data points synthesized using advanced NLP models, LLM text extractions, or topic modeling over unstructured parliamentary texts (e.g., Hansard transcripts, Explanatory Notes, Marshalled Amendment lists).

#### The AI Validation Lifecycle:
To avoid hiding valuable AI analysis in secret silos, Tier 5 data is published immediately upon extraction, carrying an explicit **Validation Lifecycle Status**:
1. **`UNVERIFIED_DRAFT` (Exploratory & Open):** Live on the platform immediately post-extraction. Flagged with a prominent visual badge for crowdsourced peer review and audit.
2. **`SAMPLE_VALIDATED` (Community Audited):** Audited against a randomized human sample (50–100 records), reporting precision, recall, and F1 scores.
3. **`GOLD_BENCHMARKED` (Publication Ready):** Extensively benchmarked against a Tier 4 (`DERIVED_HUMAN_CODED`) dataset, achieving high agreement metrics ($\ge 0.85$ F1 score).

### Tier 6: `UNAVAILABLE_HARD_GAP` *(Documented Institutional Omissions)*
Variables that cannot be served or derived for a specific assembly session. To prevent "missing data bias" in quantitative regressions, hard gaps carry mandatory sub-reason codes:
* **`NOT_RECORDED_BY_ASSEMBLY`:** Institutional omission (e.g., assembly does not record division vote lists).
* **`RECORDED_BUT_UNDIGITIZED`:** Existing paper records or unparsed PDFs not yet digitized (data engineering backlog).
* **`RESTRICTED_ACCESS`:** Data restricted by parliamentary copyright or paywalls.
* **`COST_PROHIBITIVE`:** Resource-prohibitive processing cost.

---

## 3. Data Processing & Provenance Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. HOST ASSEMBLY API / FEED INGESTION                                                       │
│    Fetch raw host payloads -> Store in Host Raw Storage (PostgreSQL JSONB / S3)             │
└───────────────────────────────┬─────────────────────────────────────────────────────────────┘
                                │
┌───────────────────────────────┴─────────────────────────────────────────────────────────────┐
│ 2. CANONICAL ETL & PROVENANCE EVALUATION                                                    │
│    - Map Native Direct Fields       (Tier 2: NATIVE_DIRECT)                                  │
│    - Compute Deterministic Joins   (Tier 3: DERIVED_DETERMINISTIC)                          │
│    - Ingest Academic Datasets       (Tier 4: DERIVED_HUMAN_CODED)                            │
│    - Run NLP/LLM Synthesizer       (Tier 5: DERIVED_SYNTHETIC_AI + Validation Status)        │
│    - Flag Hard Gaps + Reason Codes  (Tier 6: UNAVAILABLE_HARD_GAP)                         │
└───────────────────────────────┬─────────────────────────────────────────────────────────────┘
                                │
┌───────────────────────────────┴─────────────────────────────────────────────────────────────┐
│ 3. PERSISTENCE & ATLAS SERVING                                                              │
│    - PostgreSQL Canonical Models (`canonical_bills`, `bill_provenance_audit`)              │
│    - Fast FastAPI Platform REST API (`/v2/atlas`, `/v2/bills`)                              │
│    - SvelteKit Atlas Web Interface with 6-Tier Badges & Payload Inspector                   │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```
