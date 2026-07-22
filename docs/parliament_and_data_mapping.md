# Comparative Legislative Data Platform — Architecture & Audit Blueprint Specification

**Master Architecture & Data Governance Document**  
*Version 2.0.0 (North Star Reset)*

---

## 1. Project Mission & Core Vision

The **Comparative Legislative Data Platform** (`https://legislativedata.org`) is an open-access academic research infrastructure designed to map, mirror, standardize, and audit legislative data across international parliamentary assemblies.

The project operates under two foundational pillars:
1. **Academic Data Auditing (Phase 0):** Field-by-field transparent auditing of host parliamentary APIs, data availability, variable coverage, and structural open data gaps.
2. **Data Mirroring & Standardization (Phase 1):** Ingesting, hashing, and storing normalized legislative records bounded to target sessional cohorts (e.g. 2019–2024 BICD Cohort 1).

---

## 2. The 5-Tier Data Availability & Provenance Framework

All data auditing and pipeline derivation operate strictly under a **5-tier provenance model**:

1. **`CANONICAL_WISHLIST_TARGET`:** Universal variable definition established in the Master Canonical Variable Catalog ([`docs/canonical_variable_catalog.md`](file:///home/steven/Documents/github/comparativelegislativedata/docs/canonical_variable_catalog.md)).
2. **`NATIVE_DIRECT`:** Available directly in the host assembly’s official API or raw feed (JSON/XML).
3. **`DERIVED_DETERMINISTIC`:** Generated deterministically via simple pipeline transformations, date math, or joins against persistent datasets (e.g. Executive Rosters). Includes explicit confidence ratings (`HIGH`, `MEDIUM`, `LOW`).
4. **`DERIVED_SYNTHETIC_AI`:** Synthesized using advanced NLP/LLM text processing, topic modeling, or structural parsing of unstructured Hansard/PDF text.
5. **`UNAVAILABLE_HARD_GAP`:** Missing natively from the host assembly, unrecorded, or resource-prohibitive to generate (Documented Open Data Gap).

---

## 3. Core Project Documentation Architecture

The project documentation is organized into three authoritative core documents:

```
docs/
├── canonical_variable_catalog.md  ◄── Master Wishlist (8 Quantitative Research Domains)
├── peer_review_commission.md      ◄── Academic Consultation & Peer Review Brief
├── parliament_and_data_mapping.md  ◄── This Master System Architecture Specification
└── ops.md                          ◄── VPS Operations, Infrastructure & SSH Guide
```

---

## 4. Master Project Lifecycle: Phase -1 through Phase 3

```
===================================================================================
PHASE -1: FRONTEND PORTAL FOUNDATION & VPS PRODUCTION DEPLOYMENT (COMPLETE)
===================================================================================
• Standalone Node.js server (@sveltejs/adapter-node) on VPS host 45.152.161.153.
• Served via Nginx reverse proxy under SSL at https://legislativedata.org.
• Full academic SEO suite: Dataset, BreadcrumbList, Organization, TechArticle JSON-LD.
                                       │
                                       ▼
===================================================================================
PHASE 0: GLOBAL DATA AUDIT & CANONICAL MAPPING ATLAS (IN PROGRESS)
===================================================================================
• Evaluates 30+ international assemblies against the Master Canonical Variable Catalog.
• Produces declarative YAML audit blueprints documenting native keys, derivations, and hard data gaps.
• Embeds live HTTP API health probes for automated endpoint drift detection.
                                       │
                                       ▼
===================================================================================
PHASE 1: QUANTITATIVE DATA MIRRORING & PIPELINE INGESTION
===================================================================================
• Automated Python ingestion pipelines reading declarative audit blueprints.
• Ingests, hashes (SHA-256), and mirrors target cohort records into PostgreSQL.
• Generates standardized bulk Parquet export archives for academic distribution.
                                       │
                                       ▼
===================================================================================
PHASE 2: TEXT & HANSARD PROCEEDINGS INTEGRATION
===================================================================================
• Ingestion of full bill text versions, explanatory notes, and Hansard debate transcripts.
• Persistent speaker disambiguation engine joining speech segments to member IDs.
                                       │
                                       ▼
===================================================================================
PHASE 3: AMENDMENTS, DIVISIONS & AI SYNTHETIC EXTRACTORS
===================================================================================
• Extraction of Marshalled Amendment lists, Stage 2/3 division roll-call votes.
• LLM/NLP synthetic extraction of policy intent and text alteration metrics.
===================================================================================
```
