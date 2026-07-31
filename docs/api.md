# Core Repository API Specification (General)

This document provides peer-review-grade documentation of the general API layers and route architecture implemented in this repository. These standards apply universally to all legislatures integrated into the platform.

---

## 1. The Three-Pass Route Architecture

Every integrated legislature exposes endpoints under one of three API passes:

```
                      [ Client Requests ]
                               |
         +---------------------+---------------------+
         |                     |                     |
         v                     v                     v
   1. Proxy Layer        2. Mirror Layer       3. Canonical Layer
  (/api/v2/proxy/...)   (/api/v2/mirror/...)  (/api/v2/canonical/...)
         |                     |                     |
   (CORS Unlocked        (Postgres Replica     (Normalized Tiered
    Live Request)         Raw FDW Tables)      Variables for Models)
```

### 1. Proxy API (Live CORS-Unlocked Relay)
*   **Route:** `/api/v2/proxy/[assembly_code]/[endpoint]`
*   **Behavior:** Acts as a transparent, CORS-unlocked passthrough relay directly to the official upstream OData or REST endpoints.
*   **Use Case:** Real-time checking of upstream data shifts, though subject to remote API latency.

### 2. Database Mirror API (Optimized Local Replica)
*   **Route:** `/api/v2/mirror/[assembly_code]/[endpoint]`
*   **Behavior:** Queries a local PostgreSQL replica of the raw upstream data (populated via Foreign Data Wrappers or scheduled sync pipelines).
*   **Use Case:** High-volume data retrieval, bypassing remote network hops to deliver latency under 50ms.

### 3. Canonical API (Standardized Comparative Layer)
*   **Route:** `/api/v2/canonical/[assembly_code]/[endpoint]`
*   **Behavior:** Serves the normalized Layer B variables compiled strictly for comparative research. 
*   **Use Case:** Fetching clean, audit-ready data models for R, Python, and statistical regressions without raw nomenclature pollution.

---

## 2. Supported OData Query Parser Parameters

The local database mirror and canonical engines parse OData-style URL query queries into safe, parameterized SQL queries to prevent injection:

*   **`$select` (Column Projection):**
    *   Filters the returned columns list to reduce bandwidth.
    *   *Example:* `?$select=BillID,ShortName`
    *   *SQL Translation:* `SELECT bill_id, short_name`
*   **`$top` (Limit Pagination):**
    *   Limits the number of rows returned. Defaults to 100.
    *   *Safety Cap:* Submissions are capped at a maximum of 1000 records per request to protect server resources.
*   **`$skip` (Offset Pagination):**
    *   Skips the specified number of rows (used for client-side pagination).
    *   *Example:* `?$skip=100&$top=50`
*   **`$orderby` (Sort Order):**
    *   Sorts records by designated fields. All sorts are sanitized against database column names to block SQL injection.
    *   *Example:* `?$orderby=ShortName desc`
*   **`$filter` (Parameterized Conditions):**
    *   Applies basic logical operators (`eq` (equal), `ne` (not equal), `gt` (greater than), `ge` (greater or equal), `lt` (less than), `le` (less or equal)). All filters are parameterized via PG query placeholders.
    *   *Example:* `?$filter=SessionID eq 5`

---

## 3. Casing, Schema, and Serialization Rules

*   **CamelCase to Snake_Case Translation:** Host assemblies often return data keys in `CamelCase`. PostgreSQL tables are saved strictly in `lowercase` snake_case columns. The API engine maps incoming OData CamelCase keys to lowercase columns for database querying and maps the output back to CamelCase in the JSON response.
*   **Null Serialization:** Empty strings (`""`) or unpopulated elements returned by raw feeds are normalized to standard database `NULL` representations on output.
*   **Nested JSONB Structures:** Upstream complex objects (e.g. lists of addresses, temporal event logs) are stored directly inside PostgreSQL `JSONB` columns and returned as nested JSON objects, preserving detail without database inflation.
