# Implementation Plan: Phase 1 — Proxied Access & Academic Documentation

This document serves as the repository source of truth for the design and execution steps of Phase 1. It details the open CORS proxy and the interactive documentation explorer mapping the verified API catalog in `apilist.md`.

## Core Guardrails
1.  **Repository as Source of Truth:** All active plans, endpoint registries, and schemas are defined directly in the repository code and docs.
2.  **Open CORS Proxy:** The API server proxy will be un-gated (no authentication check required) to serve as a clean, public passthrough relay.
3.  **No Guesswork (Payload Introspection):** The SvelteKit explorer modal will dynamically introspect raw JSON responses fetched in real-time, building the schema documentation directly from the API output.

---

## 1. API Catalog to Map (Source: `apilist.md`)

Based on the verified endpoints in `apilist.md`, the explorer will map the following resources:

### Category A: Bills & Lifecycles
*   `bills` — `https://data.parliament.scot/api/bills` (Collection of Bill Titles)
*   `billstages` — `https://data.parliament.scot/api/billstages` (Bill Stage chronology)
*   `billtypes` — `https://data.parliament.scot/api/billtypes` (Bill categories)
*   `billstagetypes` — `https://data.parliament.scot/api/billstagetypes` (Stage Type definitions)

### Category B: Actors & Affiliations
*   `members` — `https://data.parliament.scot/api/members` (MSP registry)
*   `memberparties` — `https://data.parliament.scot/api/memberparties` (Member party mappings)
*   `parties` — `https://data.parliament.scot/api/parties` (Registered political parties)
*   `partyroles` — `https://data.parliament.scot/api/partyroles` (Party role definitions)
*   `committees` — `https://data.parliament.scot/api/committees` (Committee registry)
*   `personcommitteeroles` — `https://data.parliament.scot/api/personcommitteeroles` (Committee memberships)
*   `committeeroles` — `https://data.parliament.scot/api/committeeroles` (Committee role definitions)
*   `committeetypes` — `https://data.parliament.scot/api/committeetypes` (Committee category definitions)

### Category C: Debates, Motions & Votes
*   `motionsquestionsanswersmotions` — `https://data.parliament.scot/api/motionsquestionsanswersmotions` (Plenary motions)
*   `votesmotion` — `https://data.parliament.scot/api/votesmotion` (Division votes on motions, supporting query parameters like `?year=2011` through `?year=2025` as documented in `apilist.md`)
*   `orsplenarymeeting` — `https://data.parliament.scot/api/orsplenarymeeting` (Plenary official reports, supporting `?year=1999` through `?year=2025`)
*   `orscommitteemeeting` — `https://data.parliament.scot/api/orscommitteemeeting` (Committee official reports, supporting `?year=1999` through `?year=2024`)

---

## 2. Technical Implementation Steps

### Step 1: Create the Open CORS Proxy Endpoint
- File: `frontend/src/routes/api/v2/proxy/gb-sct/[...endpoint]/+server.ts`
- Behavior: Accepts any endpoint string, appends search query parameters, requests the host target from `https://data.parliament.scot/api/`, and returns the exact JSON body with `Access-Control-Allow-Origin: *` headers.
- Security: No session validation or tokens required. Open CORS.

### Step 2: Create the Explorer Page
- File: `frontend/src/routes/pilot/gb-sct/+page.svelte`
- Interface: Group endpoints by category. Clicking an endpoint opens the inspection modal.
- Document known API constraints (such as required `year` query parameters for votes and official reports).

### Step 3: Create the Introspection Modal
- File: `frontend/src/lib/components/NativeEndpointModal.svelte`
- Features:
  - **Live Dynamic Introspector:** Queries the proxy with `$top=1`, reads the keys of the JSON payload returned, evaluates Javascript type via `typeof`, and outputs a schema table in the UI.
  - **Live Response Previewer:** Renders the first 5 records in pretty-printed JSON format.
  - **Replication Code Generator:** Copyable snippets for **cURL**, **Python (requests)**, and **R (httr/jsonlite)**.

### Step 4: Re-enable layout link
- Update `+layout.svelte` to link to `/pilot/gb-sct` for header navigation.

---

## 3. Verification & Auditing

1.  **Code Compilation:** Execute `npm run check` locally to ensure there are no compilation issues.
2.  **Connectivity & Casing Audits:** Confirm that the proxy works and that endpoints return expected results for all three categories.
3.  **No Uncommitted Local Layout Drift:** Ensure that the local git branch is clean before requesting final approval.
