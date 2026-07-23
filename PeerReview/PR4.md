# Written Peer Review Report

**Platform under review:** Comparative Legislative Data Platform (legislativedata.org)
**Documents reviewed:** Peer Review Commission Brief & Evaluation Guidelines, v2.0.0
**Report structure:** Organized per Section 4 of the brief (Areas 1–3)

---

## Area 1: Variable Completeness & Conceptual Scope

### 1. Overall coverage assessment

The Master Canonical Variable Catalog is a strong first draft. It correctly identifies the core units comparative legislative scholars actually regress on: timing (Domain 3), disposition (Domain 4), amendment activity (Domain 7), and roll-call behavior (Domain 8). The inclusion of `initiator_party_governance_role` and `voting_coalition_type` as neutral, cross-system enums is a genuine strength — most existing datasets (e.g. national parliamentary APIs) leave this inference to the researcher, which produces inconsistent coding across studies. Anchoring sponsorship and coalition variables to a controlled vocabulary at the point of data generation, rather than leaving it to downstream users, is exactly the kind of standardization that makes cross-national comparison tractable.

That said, the catalog currently over-indexes on **outcome and process variables** and under-indexes on **procedural control mechanisms** — the tools an executive or majority uses to accelerate, block, or reshape a bill's path. These are precisely the variables used in "executive dominance" and "procedural obstruction" research (which the brief names as target use cases), so their absence is a real gap rather than a minor omission.

### 2. Missing variables

I'd prioritize adding the following, roughly in order of importance to the stated research use cases:

- **Closure/guillotine and programme motions** (`programme_motion_flag`, `guillotine_invoked_flag`, `debate_time_allocated_minutes`) — essential for "procedural obstruction" and executive-dominance research; without these, duration variables (Domain 3) conflate genuine deliberation time with time-limited debate imposed by the majority.
- **Urgency/fast-track procedures** (`emergency_procedure_flag`, `stages_compressed_count`) — bills passed under emergency procedure behave very differently statistically (fewer amendments, compressed committee stages) and should be flagged rather than silently averaged into normal-track statistics.
- **Royal/presidential consent distinct from assent** — the catalog has `royal_assent_date` but not the separate (and Westminster-specific but analytically important) concept of prior consent required before a bill can even proceed when it touches the prerogative or reserved matters. This is a distinct veto point from final assent and shouldn't be collapsed into it.
- **Committee amendment disposition rate** — the catalog has raw amendment counts (Domain 7) but not the committee-stage acceptance rate specifically (as opposed to floor-stage), which is the more theoretically meaningful variable in the "minority influence" literature.
- **Second/revising chamber interaction** (`chamber_ping_pong_count`, `chamber_disagreement_flag`) — for bicameral systems, the back-and-forth between chambers is itself a data-rich process that the current single-chamber-oriented `stage_milestones` array does not naturally capture.
- **Cost/regulatory impact flags** — a boolean or categorical for whether a bill carries binding fiscal or regulatory impact, useful as a control variable in duration and passage-rate models.

### 3. Neutrality across system types

The enums are reasonably neutral, with one caveat: `termination_mechanism`'s inclusion of `SECTION_35_VETO` is a UK-devolution-specific value sitting inside an otherwise generic enum. This is fine as a *value*, but the catalog should make explicit that jurisdiction-specific termination mechanisms are expected to proliferate as new legislatures are onboarded, and should specify a governance process for approving new enum values (see Area 3, point 7) so the enum doesn't become an unbounded, uncurated list over time. The same applies to `chamber_type` — presidential systems often have chambers that are neither clearly "sovereign" nor "devolved" in the Westminster sense (e.g. a directly elected chamber with concurrent, non-hierarchical legislative competence with a second chamber), and the current three example values won't cleanly cover this. I'd recommend defining `chamber_type` as an open, versioned enum with documented decision rules rather than a small fixed set of examples.

---

## Area 2: 5-Tier Provenance & Methodological Rigor

### 4. Soundness of the 5-tier framework

The tier structure (`NATIVE_DIRECT` / `DERIVED_DETERMINISTIC` / `DERIVED_SYNTHETIC_AI` / `UNAVAILABLE_HARD_GAP`) is methodologically sound as a *reporting* framework, and is a meaningful improvement over the binary "available / not available" provenance disclosure common in existing legislative datasets. Two structural issues should be addressed before publication, though:

- **Granularity mismatch.** The framework is described as evaluated "per parliament," but provenance in practice varies *per variable per parliament per time period* — a host API frequently adds or drops fields across sessions, and manual Hansard digitization quality changes over time. If the tier is recorded once per parliament, users will over-trust variables that were only reliably `NATIVE_DIRECT` in later sessions. I'd recommend the tier be a versioned, time-stamped attribute at the cell level (or at minimum, per-session), not a static per-parliament label.
- **Tier 3 confidence ratings need a defined methodology, not just a label.** The brief states `DERIVED_DETERMINISTIC` variables carry `HIGH`/`MEDIUM`/`LOW` confidence, but doesn't specify what generates the rating. For academic publication, this needs to be an auditable function of something concrete — e.g. join-key match rate, proportion of records requiring manual disambiguation, or agreement with a held-out gold-standard sample — rather than an analyst's qualitative judgment call. Otherwise the confidence rating itself becomes a source of unreplicable variation across the datasets published from this platform.

### 5. Benchmarks for accepting `DERIVED_SYNTHETIC_AI` variables

Before an AI-synthesized variable is fit for quantitative publication, I'd want to see, at minimum:

- **A held-out, human-coded gold-standard sample** (stratified across jurisdictions and time periods, not just one parliament) against which precision, recall, and — for continuous variables like `bill_text_alteration_score` — correlation or mean absolute error are reported.
- **Inter-annotator agreement on the gold standard itself** before it's used to score the model, since a noisy gold standard makes any accuracy figure meaningless.
- **A published, versioned prompt/pipeline specification** so the variable's derivation is reproducible and auditable by third parties, not just described in prose.
- **A minimum accuracy threshold tied to the variable's use** — a variable used descriptively (e.g. in summary tables) can tolerate lower precision than one intended as a regression covariate or dependent variable. The platform should state which threshold applies to which use case rather than adopting a single blanket cutoff.
- **Ongoing drift monitoring** — since underlying LLMs and NLP pipelines change over time, re-scoring against the gold-standard sample should be scheduled (e.g. annually or on any pipeline version change) and the results published alongside a changelog.

Without these, `DERIVED_SYNTHETIC_AI` variables risk being used in published regressions with unknown, unstated error rates — a serious concern for a platform positioning itself as academic infrastructure.

---

## Area 3: Data Gap Transparency & Academic Utility

### 6. Transparency of `UNAVAILABLE_HARD_GAP`

Explicitly labeling gaps is valuable and better than silent nulls, but transparency for comparative work also requires knowing *why* a variable is a hard gap — whether it doesn't exist in the underlying parliamentary record at all, versus exists on paper but isn't digitized or published in structured form. These have very different implications: the former is a genuine cross-national difference worth studying in its own right (e.g. some assemblies simply don't record division lists), while the latter is a data-engineering limitation that may be resolved later and shouldn't be mistaken for a substantive finding. I'd recommend splitting `UNAVAILABLE_HARD_GAP` into at least two sub-reasons (e.g. `NOT_RECORDED_BY_ASSEMBLY` vs `RECORDED_BUT_UNDIGITIZED`) so downstream researchers don't accidentally treat a data-engineering backlog as a cross-national institutional difference.

### 7. Documentation format most useful for research and teaching

For my own use, the most valuable additions would be:

- A **machine-readable, versioned codebook** (e.g. a single JSON Schema or data dictionary file per catalog version) with the enum value lists, tier-per-variable-per-session provenance, and confidence methodology all in one place — separate from this narrative brief.
- A **changelog** documenting when variables, enum values, or jurisdiction coverage change, since longitudinal comparative work depends on knowing whether an apparent trend is real or an artifact of a schema change.
- **Worked example rows** for two or three contrasting jurisdictions (e.g. one Westminster system, one presidential system) showing the full variable set populated, including tier labels — this would let reviewers and prospective users sanity-check the schema against real cases rather than the abstract definitions alone.
- For teaching use specifically, a **stripped-down "teaching subset"** of the catalog (perhaps 15–20 of the most robustly `NATIVE_DIRECT` variables across the widest set of jurisdictions) would be more usable in an undergraduate methods course than the full catalog, where variable availability differs enough across countries to complicate classroom exercises.

---

## Summary Recommendation

The catalog and provenance framework are a credible foundation for academic-grade comparative legislative data infrastructure. Before publication I would prioritize: (a) adding procedural-control variables (closure motions, urgency procedures, prior consent) given the platform's stated research use cases; (b) moving provenance tracking to a versioned, cell-level granularity rather than static per-parliament labels; (c) specifying a concrete, auditable methodology behind confidence ratings and AI-derived variable accuracy; and (d) splitting the hard-gap category to distinguish genuine institutional absence from data-engineering backlog. None of these require rethinking the overall architecture — they are refinements to an already sound design.