# Methodological Foundation: Scottish Parliament (GB-SCT)

This document provides assembly-specific methodological details and normalization rules for the Scottish Parliament (`gb-sct`) implementation. For core methodology standards and the 7-Tier Provenance Spectrum, see the [Core Repository Methodology Specification](file:///home/steven/Documents/github/comparativelegislativedata/docs/METHODOLOGY.md).

---

## 1. Sessional Terminology Aggregation

To trace sessional government volumes across a 25-year timeline (Sessions 1-6) without comparative gaps, we normalize raw legislative classifications at the database view level into a unified `'Government'` comparative type:
*   **Executive Bills (Raw ID 1):** Introduced by the Scottish Executive (primarily Sessions 1-2).
*   **Government Bills (Raw ID 7):** Introduced by the Scottish Government (primarily Sessions 3-6).
*   **Budget Bills (Raw ID 3):** Procedural financial legislation introduced by the government.
*   **Normalized Value:** `'Government'` (in the canonical `bill_type` variable).

---

## 2. Non-Partisan Delineation (Zero Blending)

We enforce a strict separation between elected backbench Independent MSPs, appointed non-elected Law Officers, and external private bill promoters by assigning unique synthetic party IDs:

| Normalized Category | Synthetic ID | Target database Field Value | Description |
| :--- | :--- | :--- | :--- |
| **Private Promoter** | `98` | `'External Private Promoter'` | External corporate or municipal bodies promoting private legislation. |
| **Law Officer** | `99` | `'Lord Advocate (Law Officer)'` | Non-elected Crown Officers (e.g. Lord Advocate) introducing consolidation bills. |
| **Elected Independent** | `1` or `2` | Member Name | Elected MSP constituency/regional representatives sitting without party whip. |

## 3. Sessional Date Cohorts

Bills are partitioned into sessional cohorts dynamically based on the official start and end dates returned from the parliament's OData `/sessions` API endpoint:
*   **Session 1:** `1999-05-12` to `2003-03-31`
*   **Session 2:** `2003-05-07` to `2007-04-02`
*   **Session 3:** `2007-05-09` to `2011-03-22`
*   **Session 4:** `2011-05-11` to `2016-03-23`
*   **Session 5:** `2016-05-12` to `2021-05-04`
*   **Session 6:** `2021-05-13` to `2026-03-24` (Dissolution)
