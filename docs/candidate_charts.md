# Interactive Dashboard Staging & Promotion Standard (General)

This document establishes the platform-wide engineering standard for developing and promoting interactive research dashboards. All visualization modules must be built, audited, and deployed using this staged methodology to guarantee database consistency and eliminate front-end calculation errors.

---

## 1. The 5-Stage Promotion Pipeline

To prevent silent failures in the data pipeline, visual dashboards are promoted across a strict 5-stage lifecycle. Each stage acts as a gate:

```
[ Stage 1: DB Extension ] --> [ Stage 2: Endpoint Sync ] --> [ Stage 3: Core Layout & KPIs ]
                                                                             |
                                                                             v
[ Stage 5: Regression Panels ] <---------------------------- [ Stage 4: Advanced Visuals ]
```

### Stage 1: Database B Schema Extension
*   **Focus:** Physical table schemas in Database B.
*   **Goal:** Add any new canonical variables to the target tables or compilation views on the PostgreSQL server. No frontend changes are permitted.

### Stage 2: SvelteKit Endpoint Updates & Registry
*   **Focus:** Server-side API endpoints (`/api/v2/canonical/...`).
*   **Goal:** Register the new variables in the OData routing configurations and verify that OData filters and projections work correctly via command-line API queries.

### Stage 3: Core Dashboard Layout & KPIs
*   **Focus:** Primary visual canvas, KPI cards, and baseline charts.
*   **Goal:** Create the route page, lay out the SVG canvas, construct KPI counters, and implement the initial sessional aggregates and party distributions.

### Stage 4: Advanced Visuals & Spatial Aggregates
*   **Focus:** Heatmaps, timescale leaderboards, and complex visual grids.
*   **Goal:** Build advanced analytical visual blocks (such as workload distribution heatmaps, duration metrics, and sorting rankings).

### Stage 5: client-Side Analytical Regression Panels
*   **Focus:** Statistical modeling and regressions.
*   **Goal:** Implement client-side calculators for linear (OLS) and logistic regressions to provide real-time coefficient, significance, and diagnostics indicators.

---

## 2. The STOP Protocol

To enforce database-first safety, the promotion sequence is gated by a strict **STOP protocol**:
1.  **Stage Verification:** After completing a stage, the developer must stop and run approved diagnostic checks (e.g. SQL count queries, curl API queries, or Svelte build audits).
2.  **No Preemption:** Under no circumstances may any database, endpoint, or page code for *subsequent* stages be written until the active stage has been fully reviewed.
3.  **User Review:** The developer must present the completed verification output or screenshots in the communication channel and wait for explicit user sign-off before unlocking the next stage.
