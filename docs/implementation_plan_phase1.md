# Implementation Plan: Phase 1 — Proxied Access & Academic Documentation

This document serves as the repository source of truth for the design and execution steps of Phase 1 of the Scottish Parliament (`GB-SCT`) pilot.

## Core Guardrails & Findings
1.  **Repository as Source of Truth:** All active plans, mappings, and schemas are defined directly in the repository code and docs.
2.  **Un-Gated CORS Proxy:** The API server proxy will be un-gated (no authentication required) to act as a public CORS-bypass passthrough.
3.  **Dynamic Schema Introspection:** The explorer UI will dynamically query the proxy, inspect the live JSON response keys, and generate schema tables on-the-fly to ensure complete parity with the host without hardcoded guesswork.
4.  **OData Limitations Documented:**
    *   **Pagination:** All audited endpoints ignore the OData `$skip` parameter. We will document in the UI that pagination queries must use year or id filters where available.
    *   **Count:** `$count` query parameters are unsupported.
    *   **Nested Payloads:** Transcripts and votes return nested dictionaries rather than flat records.

---

## 1. Relational Entity Hubs Design

The explorer UI (`/pilot/gb-sct`) will group endpoints into logical hubs to reflect relational database joins:

### 🏛️ Bills Hub
*   `bills` (`https://data.parliament.scot/api/bills`): Main Bill Titles catalog.
*   `billstages` (`https://data.parliament.scot/api/billstages`): Progress milestones logs.
*   `billtypes` (`https://data.parliament.scot/api/billtypes`): Bill categories (Executive, Member's, Private).
*   `billstagetypes` (`https://data.parliament.scot/api/billstagetypes`): Stage ID mappings.

### 👥 Committees Hub
*   `committees` (`https://data.parliament.scot/api/committees`): Active parliamentary committees.
*   `personcommitteeroles` (`https://data.parliament.scot/api/personcommitteeroles`): Member committee assignments.
*   `committeeroles` (`https://data.parliament.scot/api/committeeroles`): Committee roles (Convener, etc.).
*   `committeetypes` (`https://data.parliament.scot/api/committeetypes`): Committee category types.

### 🗳️ Motions & Transcripts Hub
*   `motionsquestionsanswersmotions` (`https://data.parliament.scot/api/motionsquestionsanswersmotions`): Plenary motions.
*   `votesmotion` (`https://data.parliament.scot/api/votesmotion`): Plenary division votes (requires `?year=YYYY`).
*   `orsplenarymeeting` (`https://data.parliament.scot/api/orsplenarymeeting`): Plenary speeches/transcripts (requires `?year=YYYY`).
*   `orscommitteemeeting` (`https://data.parliament.scot/api/orscommitteemeeting`): Committee speeches/transcripts (requires `?year=YYYY`).

---

## 2. Technical Implementation Steps

### Step 1: Open Server Proxy
- **File:** `frontend/src/routes/api/v2/proxy/gb-sct/[...endpoint]/+server.ts`
- **Logic:**
  ```ts
  import { json } from '@sveltejs/kit';
  import type { RequestHandler } from './$types';
  
  const SP_API_BASE = 'https://data.parliament.scot/api';
  
  export const GET: RequestHandler = async ({ params, url, fetch }) => {
    const { endpoint } = params;
    if (!endpoint) return json({ error: 'Endpoint is required' }, { status: 400 });
    
    try {
      const targetUrl = `${SP_API_BASE}/${endpoint}${url.search}`;
      const response = await fetch(targetUrl, {
        headers: { 'Accept': 'application/json' }
      });
      
      if (!response.ok) {
        return json({ error: `Host error: ${response.status}`, details: await response.text() }, { status: response.status });
      }
      
      const data = await response.json();
      return json(data, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Cache-Control': 'public, max-age=3600'
        }
      });
    } catch (e: any) {
      return json({ error: 'Fetch failed', details: e.message }, { status: 500 });
    }
  };
  ```

### Step 2: Modal Component with Dynamic Introspector
- **File:** `frontend/src/lib/components/NativeEndpointModal.svelte`
- **Features:**
  - Performs dynamic introspection on the first record of the payload.
  - Recursively maps nested dictionary structures (e.g. `Detail.SpeakerName (string)`).
  - Displays the first 5 records as pretty JSON.
  - Offers replication snippets (cURL, Python, R).

### Step 3: Relational Explorer Interface
- **File:** `frontend/src/routes/pilot/gb-sct/+page.svelte`
- **Design:** Modern CSS grid displaying the three Entity Hubs.
- **Details:** Each card displays the endpoint OData path, required query parameters (like `?year=2024` for votes/transcripts), and a direct button to audit the endpoint's live schema.

---

## 3. Verification & Compliance
1.  `npm run check`: Ensure 0 compilation errors are present.
2.  `npm run build`: Confirm Vite successfully bundles the frontend.
3.  `git status`: Ensure working directory is clean.
