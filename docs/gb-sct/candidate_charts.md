# Pilot Charts Implementation Plan: Scottish Parliament (GB-SCT)

This document maps out the specific implementation checkpoints and execution steps for the Holyrood Research Charts & Analytics Dashboard (`/pilot/gb-sct/charts`). For core visual promotion rules and safety gates, see the [Interactive Dashboard Staging & Promotion Standard](file:///home/steven/Documents/github/comparativelegislativedata/docs/candidate_charts.md).

---

## Stage 1: Database B Schema Extension (Introduction Date)
*   **Objectives:** Add `introduction_date` as a physical column in Database B (`canonical_gb_sct_bills`) to enable chronological plotting.
*   **Verification Checklist:**
    1.  Add `introduction_date DATE` column to `schema_canonical.sql`.
    2.  Update `compile_canonical_layer.sql` view definitions to map `sd.intro_date`.
    3.  Run compile script on the VPS PostgreSQL server.
    4.  Verify that `SELECT COUNT(*) FROM canonical_gb_sct_bills WHERE introduction_date IS NULL` returns `0`.
*   **STOP Protocol:** Do NOT modify Svelte routes or API code. Present psql counts to the user for review.

---

## Stage 2: SvelteKit Endpoint Updates & Registry
*   **Objectives:** Expose the `introduction_date` column in the OData API router configuration.
*   **Verification Checklist:**
    1.  Add `IntroductionDate: { dbColumn: 'introduction_date', type: 'date' }` to SvelteKit `[endpoint]/+server.ts`.
    2.  Verify router functionality using OData selection queries on the server:
        `curl -s "http://localhost:5173/api/v2/canonical/gb-sct/bills?\$select=BillID,IntroductionDate&\$top=5"`
*   **STOP Protocol:** Do NOT write front-end visual canvas code. Present API query output to the user.

---

## Stage 3: Core Dashboard Layout & KPIs
*   **Objectives:** Build the core charts dashboard page, header KPIs, sessional volume bar chart, and party success distributions.
*   **Verification Checklist:**
    1.  Create route file `frontend/src/routes/pilot/gb-sct/charts/+page.svelte`.
    2.  Implement header widgets: *Introduced (All-Time)*, *Passed Stage 3*, and *Chamber Success Rate*.
    3.  Build SVG stacked bar chart splitting sessional counts into Passed Stage 3 (Green) and Fallen/Withdrawn (Red/Orange) segments with a 1px separation gap.
    4.  Implement interactive sessional tooltip cards showing exact success/failure percentages on hover.
    5.  Build the Party Sponsorship list displaying bill counts and success rates, isolating Law Officers (ID 99) and Private Promoters (ID 98) in distinct categories.
*   **STOP Protocol:** Do NOT build heatmaps, leaderboards, or regression analytics. Present active page screenshot to the user.

---

## Stage 4: Workload Heatmap & Timescale Leaderboards
*   **Objectives:** Expose dynamic sessional boundaries via a new API endpoint, compute progress quarters on the client using these boundaries, and render sessional concentration heatmaps alongside passage speed leaderboards.
*   **Verification Checklist:**
    1.  Add `sessions` endpoint mapping to the SvelteKit API router in `[endpoint]/+server.ts` to serve dynamic records from `raw_gb_sct_sessions`.
    2.  Fetch `sessions` dynamically in `charts/+page.svelte` on mount to retrieve start and end dates.
    3.  Calculate sessional progress quarters for each bill: `Q1 (0-25%)`, `Q2 (25-50%)`, `Q3 (50-75%)`, `Q4 (75-100%)` using the retrieved session bounds. Use the dissolution date `2026-03-24` as a fallback boundary for Session 6.
    4.  Build the **Sessional Workload Concentration Heatmap** using emerald-themed glassmorphism blocks (intensity representing bill density).
    5.  Build the **Passage Speed Leaderboards** showing the Top 10 Longest (warning/red border) and Top 10 Shortest (emerald/green border) bill durations.
*   **STOP Protocol:** Do NOT write Stage 5 regression calculators. Present the dynamic sessional calculations, heatmap rendering, and leaderboards to the user.

---

## Stage 4.1: Layout Decluttering & Cumulative Spacing Rollback
*   **Objectives:** Roll back the Cumulative Spacing SVG and Gini table elements, standardize academic tooltips to use `INFO_REGISTRY`, and restructure the layout to resolve filter scrolling issues.
*   **Verification Checklist:**
    1.  Delete the Cumulative Spacing SVG Chart, Gini Inequality Table, and `activeStage4Tab` pill navigation toggles.
    2.  Ensure all chart headers use the standard `<HelpCircle size={16} />` icon to trigger `INFO_REGISTRY` modals instead of displaying verbose inline text.
    3.  Implement a `position: sticky;` CSS rule on the universal Bill Type Filter bar so it remains accessible while scrolling.
    4.  **[USER DECISION REQUIRED]** Introduce a Dashboard Navigation Tab structure to split the vertical layout into three views (Overview, Workloads, Party Analysis) to reduce vertical clutter.
*   **STOP Protocol:** Await explicit user decision on the Dashboard Navigation Tabs before modifying the Svelte components.

---

## Stage 4.2: UX Differentiation for Navigation vs. Filters
*   **Objectives:** Differentiate the visual paradigm of the Bill Type Filter from the Dashboard Navigation tabs to eliminate UX ambiguity without breaking application flow.
*   **Verification Checklist:**
    1.  **[USER DECISION REQUIRED]** Choose a visual differentiation path:
        *   **Option 1 (Classic "Underline" Navigation Tabs):** Redesign the Dashboard Navigation tabs to feature a transparent background with a bright cyan bottom border (`border-bottom: 2px solid #38bdf8`) when active. Leave the Bill Type filters as individual solid green pills.
        *   **Option 2 (Dropdown Filter):** Redesign the Bill Type Filter into a stylized `<select>` dropdown menu. Leave the Dashboard Navigation as a horizontal row of unified dark blue pills.
    2.  Implement the chosen UX path in `charts/+page.svelte` using standard scoped CSS.
*   **STOP Protocol:** Await explicit user decision on the chosen Option before touching any source code.

---

## Stage 4.3: Main Page Charts Banner Layout
*   **Objectives:** Improve the layout of the "Holyrood Research Charts & Analytics Dashboard" banner on the main pilot page so it doesn't look like a disconnected, floating element.
*   **Verification Checklist:**
    1.  **[USER DECISION REQUIRED]** Choose a layout path:
        *   **Option 1 (Full-Width Expansion):** Remove the `max-width: 800px` constraint on the banner so it matches the full width of the "Canonical Research Datasets" block above it. This makes it a solid, structural row at the bottom of the page.
        *   **Option 2 (Embed Inside Canonical Hub):** Delete the standalone banner container and embed the "Open Analytics Dashboard" button and text directly *inside* the bottom of the Canonical Research Datasets card. This explicitly links the visual dashboard to the academic variables that power it.
    2.  Implement the chosen layout path in `+page.svelte`.
*   **STOP Protocol:** Await explicit user decision on the chosen Option before modifying the source code.

---

## Stage 5: Regression Analysis Panels
*   **Objectives:** Implement client-side calculators for OLS and Logistic regressions using canonical variables to display dynamic models on the dashboard.
*   **Technical Design:**
    *   **New Tab:** Add a `Regressions` tab to the Analytics Dashboard alongside `Overview`, `Workloads`, and `Party Success`.
    *   **Logistic Regression (Passage Model):** Predicts binary `passed_stage_3` using `sponsor_type` (Government=1, Non-Government=0), `sponsor_is_first_time` (True=1, False=0), and `sessional_bill_load` (int). 
    *   **OLS Regression (Speed Model):** Predicts `t1_duration_calendar` using `Days from Session Start` to evaluate whether bills speed up toward the end of the session.
*   **Open Question for User:**
    *   > [!IMPORTANT]
        > **Dependency Question:** Logistic regression (which requires Iteratively Reweighted Least Squares and matrix inversion) is complex and prone to numerical instability if written from scratch in vanilla JS. Do you approve installing the standard Javascript math libraries `ml-regression-multivariate-linear`, `ml-logistic-regression`, and `ml-matrix` to the frontend `package.json`, or would you strictly prefer a lightweight (but less robust) zero-dependency vanilla JS implementation?
*   **Verification Checklist:**
    1.  Await user decision on npm dependencies.
    2.  Build data mappers (converting dates to `Days from Session Start` and booleans/enums to `1/0`).
    3.  Implement the regression calculators (via library or custom).
    4.  Build regression UI cards showing coefficients, p-values (or t-stats), significance stars, and R² / Pseudo-R² values.
*   **STOP Protocol:** Await explicit user decision on the chosen Option before modifying the source code.

---

## Stage 5.1: Regression Transparency Fixes (INFO_REGISTRY)
*   **Objectives:** Provide academic transparency to the Regression panels using the standard `INFO_REGISTRY` process (question mark icon).
*   **Technical Design:**
    *   **Logistic Regression (`logistic`):**
        *   Variables: `passed_stage_3` (T2), `sponsor_type` (T2), `sponsor_is_first_time` (T2), `sessional_bill_load` (T2).
        *   Formula: `Logit(P(passed_stage_3)) = β0 + β1(sponsor_type) + β2(sponsor_is_first_time) + β3(sessional_bill_load)`
        *   Logic: Uses Newton-Raphson gradient descent (via `ml-logistic-regression`) to predict likelihood of passing Stage 3. Output coefficients are raw log-odds.
    *   **OLS Regression (`ols`):**
        *   Variables: `t1_duration_calendar` (T2), `introduction_date` (T2), `session_start_date` (T1).
        *   Formula: `t1_duration_calendar = β0 + β1(Days_from_Session_Start)`
        *   Logic: Tests the hypothesis that scrutiny speeds up towards the end of a session. Calculated using `ml-regression-multivariate-linear`.
*   **Verification Checklist:**
    1.  Add `logistic` and `ols` entries to `INFO_REGISTRY` in `charts/+page.svelte`.
    2.  Add `btn-info-trigger` icons to the Logistic and OLS regression cards.
    3.  Sync to VPS, build, and verify the popups render correctly.

---

## Stage 6: Regression Rollback Plan (Zero Blast Radius)
*   **Objectives:** Completely remove the Regression models (Stage 5 and 5.1) from the frontend application and dependencies, reverting the dashboard to simple descriptive insights. Ensure zero blast radius on the rest of the application.
*   **Technical Design:**
    *   **Frontend UI (`charts/+page.svelte`):**
        1.  Remove `Regressions` from the `activeDashboardTab` state and delete its toggle button.
        2.  Delete the `{#if activeDashboardTab === 'regressions'}` UI block containing the OLS and Logistic cards.
        3.  Remove the ML derivations (`const logreg`, `const mlr`) from the `$derived.by` block to stop the client-side math calculations.
        4.  Remove the `logistic` and `ols` metadata entries from `INFO_REGISTRY`.
    *   **Dependencies (`package.json`):**
        1.  Run `npm uninstall ml-logistic-regression ml-matrix ml-regression-multivariate-linear` in the frontend directory.
    *   **Database Elements:**
        1.  *NO ACTION REQUIRED.* The regression models used standard canonical variables (`passed_stage_3`, `sponsor_type`, etc.) from Database B which are shared by the other functional charts (e.g., Party Sponsorship Share, Leaderboards). Removing columns from the DB would violate the "zero blast radius" constraint by breaking other tabs.
*   **Verification Checklist:**
    1.  [x] Clean up `package.json` dependencies.
    2.  [x] Delete regression UI and logic from `charts/+page.svelte`.
    3.  [x] Sync to VPS, run `npm install` (to prune modules) and `npm run build`.
    4.  [x] Verify the "Regressions" tab is gone and other charts still function perfectly.
*   **STOP Protocol:** Await explicit user decision before modifying the source code.

---

## Stage 7: Sessional Stage Duration Stacked Bar Chart
*   **Objectives:** Introduce an attractive, descriptive, horizontal stacked bar chart that shows the average duration (in days) a bill spends in each legislative stage (Introduction to Stage 1, Stage 1 to Stage 2, Stage 2 to Stage 3), grouped by session. The chart should reside at the top of the "Workloads & Timelines" tab and dynamically respond to the global Bill Type filter (e.g., Government Bills).
*   **Variable Availability & Provenance:**
    *   **Data Audit:** The canonical API already exposes `T1DurationCalendar`, `T2DurationCalendar`, and `T3DurationCalendar` for every bill.
    *   **Provenance:** These are Tier 2 (DERIVED_DETERMINISTIC) variables pre-calculated during the pipeline transfer from Database A to Database B. No new database variables or backend derivations need to be created.
*   **Technical Design:**
    *   **Frontend Data Logic (`charts/+page.svelte`):**
        1.  Create a `$derived.by` block named `stageDurationsBySession`.
        2.  Filter `filteredBills` to include only bills that have `PassedStage3 === true` and valid `T1`, `T2`, and `T3` durations.
        3.  Group the bills by `SessionID` (1 through 6).
        4.  Calculate the mean for each stage: `avgT1`, `avgT2`, and `avgT3`, as well as the `totalAvg = avgT1 + avgT2 + avgT3` for each session.
        5.  Calculate `maxTotalDuration` across all sessions to scale the stacked bars appropriately.
    *   **Frontend UI (`charts/+page.svelte`):**
        1.  Insert the chart at the top of the `{#if activeDashboardTab === 'workloads'}` section.
        2.  Render a card with standard header styling.
        3.  Implement the chart using HTML/CSS `flex-direction: row` bars. Each bar will have three colored segments (e.g., `#6366f1` for T1, `#10b981` for T2, `#f59e0b` for T3) sized proportionally based on `(avgT_n / maxTotalDuration) * 100%`.
        4.  Add numeric labels inside each segment (average days for that stage) and an overall total average at the end of the bar.
    *   **Transparency & UI Consistency:**
        1.  Add a standard `btn-info-trigger` question mark icon to the header.
        2.  Register the chart in `INFO_REGISTRY` (Key: `stage_durations`) detailing the SQL-like formula (`AVG(t1_duration_calendar) GROUP BY SessionID`) and logical compilation.
*   **User Action Required:** Please review this Stage 7 implementation plan. Once approved, I will implement this purely on the Svelte frontend.
