# Global Research Variables Codebook Index & Taxonomy (General)

This document defines the platform-wide research variables taxonomy. It outlines the standardized comparative baseline variables guaranteed to exist across all legislatures, and indexes the individual assembly codebooks.

---

## 1. Comparative Core Variables Baseline

To enable cross-national comparative queries, every integrated assembly is required to compile a canonical table of bills (`canonical_[assembly_code]_bills`) that maps to the following standardized research variables:

| Standard Variable Name | Core Data Type | Target Provenance Tier | General Rationale |
| :--- | :--- | :--- | :--- |
| **`bill_id`** | `INTEGER` | Tier 1 (`NATIVE_DIRECT`) | Unique primary identifier mapped from the raw assembly record. |
| **`short_name`** | `VARCHAR(250)`| Tier 2 (`DERIVED_DETERMINISTIC`) | Unified title of the bill (cleaned of procedural codes). |
| **`session_id`** | `INTEGER` | Tier 2 (`DERIVED_DETERMINISTIC`) | Numeric sessional term identifier (e.g. 1, 2, 3...) based on introduction date. |
| **`sponsor_type`** | `VARCHAR(20)` | Tier 2 (`DERIVED_DETERMINISTIC`) | Normalized sponsor group: `GOVERNMENT` or `NON_GOVERNMENT`. |
| **`sponsor_name`** | `VARCHAR(150)`| Tier 2 (`DERIVED_DETERMINISTIC`) | Sponsoring member's parliamentary name or institutional role. |
| **`sponsor_party_id`** | `INTEGER` | Tier 2 (`DERIVED_DETERMINISTIC`) | Political party ID of sponsor at the date of introduction. |
| **`passed_stage_3`** | `BOOLEAN` | Tier 2 (`DERIVED_DETERMINISTIC`) | `TRUE` if the bill completed its final legislative vote in the chamber. |
| **`bill_outcome`** | `VARCHAR(20)`| Tier 2 (`DERIVED_DETERMINISTIC`) | Standardized ultimate outcome: `PASSED` or `FALLEN`. |
| **`introduction_date`**| `DATE` | Tier 1 (`NATIVE_DIRECT`) | The official calendar date of the bill's introduction. |

---

## 2. Assembly-Specific Variable Codebooks

For the detailed SQL formulas, sessional date ranges, synthetic non-partisan IDs, and endpoint configurations for individual legislatures, refer to their specific manuals:

*   [Scottish Parliament (GB-SCT) Research Variables Manual](file:///home/steven/Documents/github/comparativelegislativedata/docs/gb-sct/variables.md)
