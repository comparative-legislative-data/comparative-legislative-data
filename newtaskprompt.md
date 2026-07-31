# System Guidelines for Operator Ingestion & Refactoring Tasks

This prompt defines the absolute operational rules and guardrails for all code modifications, database compiles, and refactoring runs in this repository.

---

## 1. Strict Analysis-First Loop (No Preemptive Changes)
*   **Step 1: Diagnosis & Analysis Only:** Execute file reads or database checks to diagnose a request. Under no circumstances should you edit files, compile database views, or trigger sync scripts during the diagnosis phase.
*   **Step 2: Present Findings:** Present a list of files to modify, proposed SQL queries/view changes, and structural impacts in chat.
*   **Step 3: Wait for Approval:** Stop and wait. You must receive the explicit user confirmation **"proceed"** in chat before executing any code changes.

---

## 2. Consequential Drift Prevention
Whenever a database column, view formula, variable definition, or sessional classification is updated, you **MUST** audit and align all three layers of the platform:

```
    [ Database B Schema ] <---> [ Documentation ] <---> [ Frontend Registry ]
  compile_canonical_layer.sql       /docs/              +page.svelte +server.ts
```

*   **Database Compiler:** Ensure the target SQL views and inserts in `scripts/compile_canonical_layer.sql` are correct.
*   **System Documentation:** Update variables in `docs/variables.md` (General) and `docs/gb-sct/variables.md` (Assembly-specific) to mirror the exact SQL formulas and descriptions.
*   **Frontend Registry & API Router:**
    *   Verify that SvelteKit API endpoints (`[endpoint]/+server.ts`) expose correct field casings and types.
    *   Verify that `frontend/src/routes/pilot/[assembly]/+page.svelte` variables metadata objects are updated with the matching description and `sqlFormula` strings.

---

## 3. Strict Boundary Containment
*   **Workspace restriction:** Confined strictly to the repository folder `/home/steven/Documents/github/comparativelegislativedata`. Do not access adjacent directories.
*   **Repository is the Sole Source of Truth:** All design plans, implementation specifications, technical logs, walkthroughs, and checklists must be written directly into the repository folder structure (e.g., under `docs/`) and synced to the server. Do not store these documents exclusively in agent-private directories (like `.gemini/` app data folders). The codebase must remain the complete, self-contained, and version-controlled record of all project plans and actions.
*   **Stop Command Protocol:** If the user enters a "stop" command, immediately cease all background tasks, terminal executions, and file operations.

---

## 4. Temporal, Sessional, & Type Integrity
*   **Validate against System Time:** Always check the current system metadata timestamp (e.g. July 2026) and verify if subsequent elections, dissolutions, or sessional updates have occurred. Do not rely on assumptions from prior conversation turns.
*   **Database Range Diagnostics:** Query Database A and B for active table ranges (`SELECT MAX(stagedate)`, `MAX(introduction_date)`) before constructing time-bound dashboards.
*   **Data Provenance Gate (Strict T1/T2 Only):** All data variables utilized in frontend charts must be queried directly from Database B (isolated research layer) and strictly fit within Tier 1 (Native Direct) or Tier 2 (Derived Deterministic) provenance definitions. Under no circumstances should frontend views or database views use hardcoded UI constants or Tier 4 (Human-Coded) values until such structures are explicitly approved and imported.
*   **Ambiguity Gate:** If there is any ambiguity over date ranges, coalitions, sessional boundaries, or database data types, you **MUST** stop immediately, present the ambiguity, and request clarification from the user in chat before proceeding.

---

## 5. Mathematical & Statistical Transparency
*   **Dependency Mandate:** All client-side regressions (Logistic, OLS, Multivariate) must be computed using standard, open-source, peer-reviewed mathematical libraries (e.g., the `mljs` ecosystem: `ml-regression-multivariate-linear`, `ml-logistic-regression`, `ml-matrix`). 
*   **No Hand-Rolled Algorithms:** Under no circumstances should complex algorithms (such as Newton-Raphson or Iteratively Reweighted Least Squares) be hand-written in vanilla JavaScript. This guarantees numerical stability against edge cases and ensures methodology remains perfectly auditable for researchers.

---

## 6. UI & Styling Guardrails
*   **Vanilla CSS Mandate:** All frontend styling must use standard Vanilla CSS classes defined explicitly in `<style>` blocks. 
*   **No Tailwind CSS Hallucination:** Absolutely **NO** Tailwind CSS utility classes (e.g., `flex-col`, `mb-8`, `bg-indigo-500`, `text-slate-400`) are permitted unless explicitly authorized by the user. The project does not have Tailwind configured, and using its classes will result in completely broken, unstyled HTML rendering (i.e. vertical block stacking). Always verify semantic class definitions exist before applying them.
