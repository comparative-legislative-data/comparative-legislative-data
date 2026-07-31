# Implementation Plan: Premium Visual Refinement (Stage 4)

This plan outlines the specific CSS and HTML structural changes required to achieve pixel-perfect visual parity with the provided target design mockups (`image1.png` and `image2.png`). 

## Proposed Changes

### [Component: Dashboard UI]
#### [MODIFY] `frontend/src/routes/pilot/gb-sct/charts/+page.svelte`

1.  **Unified "Sessional Workload Spacing Audit" Card (`image1.png`)**
    *   **Structure:** Wrap both the "Workload Half-Life" table and the "Sessional Workload Concentration Heatmap" inside a single, large, full-width `chart-card` container with a dark background (`rgba(9, 13, 22, 0.6)`) and a subtle slate border.
    *   **Header & Pseudo-Tabs:** The header of this unified card will contain the title with a small yellow trend icon (`<Activity size={16} />`). The top right will feature the pill navigation: `Cumulative Spacing (Sag)`, `Cumulative Scrutiny (Scissors)`, `Timing vs. Transit`, and `Introductions Heatmap`. The first three will be styled as inactive (grey), while `Introductions Heatmap` will be highlighted in a golden/yellow hue to match the mockup.
    *   **Two-Column Grid:** Beneath the header, the layout will transition into a two-column CSS grid (`grid-template-columns: 1fr 1fr; gap: 2rem;`) for the table and heatmaps, matching the side-by-side presentation.
    *   **Table Styling:** The table headers will be recolored to match the mockup (yellow text, all-caps, no borders). The `SESSION` column text (`S1`, `S2`) will be bolded white, while the `50% MARK TIMELINE ELAPSED` values will use a golden monospaced font. The diagnosis badges will be refined with thin borders and softer background opacities.
    *   **Segmented Heatmaps:** 
        *   Labels will be added *above* each stacked bar to read: `S1        51 caucused introductions`.
        *   The Q1-Q4 percentage labels will be moved inside the respective colored bar segments (e.g., `22%`, `25%`, `31%`, `22%`).
    *   **Methodology Footer:** The methodology footnotes ("Timeline Normalization", "Gini Spacing", "Session 7 Status") will be integrated directly at the bottom interior of this unified card as a subtle, dark-grey text footer.

2.  **Timescale Leaderboards Refinement (`image2.png`)**
    *   **Header Icons:** The "Top 10 Longest" header will receive an amber `<Clock size={16} />` icon. The "Top 10 Shortest" header will receive a green `<Info size={16} />` icon. Both header texts will be colored with a golden tint.
    *   **Bill Card Typographic Hierarchy:** 
        *   Top Row: A small, grey, uppercase tracking number and bill type (`SP BILL {ID} • {TYPE} BILL`).
        *   Top Right: The total days prominently displayed in large bold font (`1135 days` in amber; `0 days` in emerald).
        *   Middle Row: The bill's short title in bold white text.
        *   Bottom Row: The Sponsor Name and Session ID (`Sponsor: David Stewart • S4`).
    *   **Introduction & Passage Dates:** A new bottom row will be appended to display `Intro: {Date} Passed: {Date}`. The introduction date is already available (`IntroductionDate`). The passage date will be dynamically calculated in JavaScript by taking the introduction date and adding the `TotalDurationCalendar` days to it to ensure robust presentation without requiring new API field mappings.

## Verification Plan

### Manual Verification
- Await user approval on this layout plan before touching any source code.
- Once approved, execute the Svelte refactor, run Vite compilation (`npm run build`), deploy to VPS, and ask the user to verify visual parity on the live URL.

---

> [!IMPORTANT]
> **User Review Required:** The mockup for `image1.png` includes "Cumulative Spacing (Sag)" tabs. Since we deleted the Sag logic in the previous rollback, this plan proposes rendering those tabs as static, inactive placeholders to perfectly mimic the visual density of your reference design. If you prefer these dummy tabs to be omitted entirely, please advise.
