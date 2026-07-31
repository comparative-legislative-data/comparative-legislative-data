# API Reference Manual: Scottish Parliament (GB-SCT)

This document provides assembly-specific endpoint directories and parameters for the Scottish Parliament (`gb-sct`) implementation. For the core architectural spec and query parameters, see the [Core Repository API Specification](file:///home/steven/Documents/github/comparativelegislativedata/docs/api.md).

---

## 1. Upstream Data Source
*   **Official Endpoint:** `https://data.parliament.scot/api/`
*   **Format:** OData v4 (served via proxy in CamelCase format)

---

## 2. API Endpoint Directories

### Raw Mirror Endpoints (Layer A Replica)
Exposed at `/api/v2/mirror/gb-sct/[endpoint]` (and `/api/v2/proxy/gb-sct/[endpoint]`):

| API Endpoint | Target Postgres Mirror Table | Description |
| :--- | :--- | :--- |
| `bills` | `raw_mirror.raw_gb_sct_bills` | Upstream bill listings and meta-attributes. |
| `billstages` | `raw_mirror.raw_gb_sct_billstages` | Stage completion events, event dates, and progress logs. |
| `billstagetypes`| `raw_mirror.raw_gb_sct_billstagetypes`| Reference dictionary for sessional legislative stage codes. |
| `billtypes` | `raw_mirror.raw_gb_sct_billtypes` | Sessional bill classification codes (Executive, Private, etc.). |
| `members` | `raw_mirror.raw_gb_sct_members` | Elected Members of the Scottish Parliament (MSPs). |
| `memberparties` | `raw_mirror.raw_gb_sct_memberparties` | Sessional political party affiliations of MSPs with validity dates. |
| `parties` | `raw_mirror.raw_gb_sct_parties` | Official political party reference dictionary. |

### Canonical Endpoints (Layer B Normalized Research Tables)
Exposed at `/api/v2/canonical/gb-sct/[endpoint]`:

| API Endpoint | Target Database B Table | Description |
| :--- | :--- | :--- |
| `bills` | `canonical_gb_sct_bills` | Clean, normalized sessional bills dataset containing all 20+ Tier 1 and Tier 2 variables. |
| `memberpartyhistory` | `canonical_gb_sct_member_party_history` | Historical sessional political party snapshot datasets. |

---

## 3. Custom Sessional Filters

To safely handle high-volume transactional OData feeds without overloading memory or database connections, the mirror endpoints for certain tables support a custom helper filter:

### `year` (Year-Slicing Query Helper)
*   **Applicable Endpoints:** `votesmotion`, `orsplenarymeeting`, `orscommitteemeeting`
*   **Behavior:** Slices records by calendar year based on timestamp values located in nested JSONB objects.
*   **Example Query:** `/api/v2/mirror/gb-sct/votesmotion?year=2024&$top=5`
*   **SQL Translation:** 
    ```sql
    WHERE (time->>'Start')::timestamp >= '2024-01-01' 
      AND (time->>'Start')::timestamp < '2025-01-01'
    ```
