# External Peer Review: Comparative Legislative Data Platform

**Reviewer role:** External academic and technical reviewer
**Scope of review:** Project background, architecture, data model, derived-metrics methodology, and phasing strategy, per the four commissioned domains
**Overall verdict:** A well-motivated project addressing a genuine and well-documented gap in comparative legislative research. The core design decisions (dual-layer payload, three-tier provenance model, BICD-first phasing) are broadly sound. However, several methodological, legal, and operational risks need to be resolved before Phase 1 ingestion begins, and a few technical/architectural choices carry more risk than the document currently acknowledges.

---

## Summary Judgment

The project correctly identifies that legislative open-data ecosystems are rich in raw procedural logs but poor in analytically usable classifications. This is a real and recurring complaint in the legislative studies literature, and building a **derivation layer** rather than a passive mirror is the right response to it. The greatest strengths of the proposal are the explicit separation of native and normalized data, and the decision to document — rather than paper over — the cases where derivation is impossible (`UNAVAILABLE_GAP`). The greatest risks are (a) the single-maintainer/single-VPS operational model set against an ambitious global-scope roadmap, (b) under-specified validation methodology for the algorithmic classifiers, and (c) some conceptual slippage in how "executive dominance" will be operationalized across systems that don't map cleanly onto a government/opposition binary.

---

## Domain 1: Data Generation, Derived Metrics & Fill-a-Gap Critique

**Does this fill a genuine gap?** Yes. The four barriers listed (missing outcome classification, format fragmentation, Westminster/US schema bias, weak proceedings-to-Hansard linkage) are all independently documented pain points for anyone who has tried to build a cross-national bill-tracking dataset (e.g., users of ParlTrack, LegiScan, or country-specific tools consistently report exactly these gaps). Treating this as a *generation* problem rather than a *retrieval* problem is the correct framing.

**Are the proposed indices the most useful?**

- **Terminal outcome classification and stage duration** are unambiguously valuable and low-risk to derive; almost every comparative legislative study needs these as baseline variables.
- **Sponsor executive alignment** is valuable but harder than it looks (see Domain 3).
- The **Executive Dominance Score (EDS)**, defined as "the ratio of executive amendment success vs opposition/backbench amendment uptake," is the most conceptually exposed metric in the whole spec:
  - It assumes every amendment has a clearly identifiable proposer type (executive/opposition/backbench), which breaks down in consensus systems, coalition governments where confidence-and-supply partners table amendments, and unicameral systems with free votes.
  - It does not yet specify a **denominator**: is EDS per-bill, per-session, per-chamber? A single scalar can't do all three without separate documented formulas.
  - It does not yet address how **government-sponsored amendments to its own bill** should be counted — these are common (and often reflect responsiveness to committee scrutiny, not "dominance") and could distort the index if lumped in with straightforward votes-down of opposition amendments.
- Missing but valuable derived fields the pipeline could reasonably add: (i) an explicit **amendment disposal type** (agreed without division, agreed on division, negatived, withdrawn, not moved, not called) — collapsing all of this into "success/failure" loses information researchers will want; (ii) **committee type** (select/standing/joint/whole-house) since procedural weight varies; (iii) a **government-defeat flag** distinct from amendment-level dominance, since whole-bill government defeats are a headline variable in the executive-dominance literature independent of amendment counts.

**Recommendation:** Publish the EDS formula, unit of analysis, and edge-case handling rules (own-amendments, free votes, coalition amendments) as a versioned methodology note before ingestion, not as an implicit pipeline behavior. Comparative researchers will need to cite the *formula*, not just the platform.

---

## Domain 2: Schema Harmonisation & Conceptual Validity

**Is the `LegislativeMeasure` definition robust?** The inclusion of primary bills, executive decrees with statutory force, and constitutional amendments, with exclusion of secondary instruments (SIs) and non-binding motions, is a reasonable and defensible cut for a first version — it mirrors distinctions already used in comparative legislative studies (e.g., primary vs. delegated legislation). Two gaps worth flagging:

- **Private member's/private bills and hybrid bills** are not mentioned. These matter for the executive-dominance research question specifically, since their success rate is a natural comparator to executive-sponsored legislation. If they are silently excluded, that should be stated explicitly rather than left ambiguous.
- **"Executive decrees with primary statutory force"** is doing a lot of work in one clause. Many civil law systems have several *tiers* of decree power (e.g., decree-laws requiring subsequent ratification vs. decrees that are immediately final), and treating them as a single canonical category risks exactly the Westminster/US schema bias the project says it wants to avoid. This needs its own sub-taxonomy before Phase 3 (global expansion), even if it can be deferred past Phase 1/2 since the BICD cohort doesn't exercise this pathway.

**Does the dual-layer model resolve the comparative/specialist tension?** Yes, in principle, and this is one of the strongest design decisions in the proposal. Keeping `native.*` fields untouched preserves citability and trust with country specialists, while `normalized.*` gives quantitative researchers a stable schema to model against. The main outstanding question is **who owns the mapping table** between native statuses and normalized enums, and whether that mapping is versioned and publicly diffable — this table is where most classification errors will live, and it should be treated as a citable artifact in its own right (e.g., a public changelog), not just internal pipeline logic.

---

## Domain 3: Data Generation Methodology & Technical Architecture

**Is the 3-tier provenance model sound?** Yes — `NATIVE_DIRECT` / `ENRICHED_BY_PIPELINE` / `UNAVAILABLE_GAP` is a clean and citation-friendly model, and explicitly marking `UNAVAILABLE_GAP` rather than silently omitting fields is good academic practice; it lets researchers distinguish "zero" from "unknown."

**Risks in the Executive Roster join (sponsor name + date → minister status):**

- **Name disambiguation** is the single largest failure risk. Members change titles (peerages, honorifics), names are transliterated differently across native feeds and Hansard, and common surnames collide within the same legislature over decades. A join keyed on raw name strings will produce silent false positives/negatives unless backed by a persistent member ID (e.g., matched to Wikidata QIDs or an internal stable ID) rather than string matching.
- **Junior ministerial and PPS boundary cases**: Parliamentary Private Secretaries are not ministers but are sometimes treated as "payroll vote" in dominance literature; the roster needs an explicit policy on where the executive/backbench line is drawn, since this materially changes EDS results.
- **Ministerial transitions mid-bill**: a bill introduced by one minister and completed by their successor (post-reshuffle) needs a rule for whether `initiator_type` reflects the introducing minister or is time-varying across stages. The current schema (`initiator_type` as a bill-level, not stage-level, field) suggests a single fixed value, which will misclassify some longer-running bills.
- **Coalition and confidence-and-supply governments**: "GOVERNING_PARTY" as a binary undercounts arrangements where a supporting party votes with government without holding ministerial posts. The roster model as described only captures *ministerial office*, not *voting alignment*, which is a narrower and safer scope — this should be stated explicitly as a limitation, not an oversight.

**Terminal outcome classification risks:** Native status strings like "Order for 2nd Reading discharged" or "Prorogation" are genuinely ambiguous — the former can mean withdrawal or effective lapse depending on context, and the latter is not itself an outcome but an event that *may* cause lapse depending on carry-over rules (which differ, e.g., UK carry-over motions vs. Scottish Parliament end-of-session rules). This classification will need a **rules table per jurisdiction**, not a single global lookup — the document doesn't yet distinguish "sameness of raw phrase" from "sameness of legal effect," which will vary by legislature even for identical-sounding phrases.

**Object storage / citation permanence:** Content-addressed storage (SHA-256 hashing, as already planned) is the right foundation. To guarantee permanent citation URLs, the missing piece is a documented external-facing **persistent identifier scheme decoupled from your own domain** (e.g., register hashes with a third-party persistent-identifier service, or mirror to an academic archive like Zenodo/Internet Archive with a DOI), since a URL under your own domain is only as permanent as your own hosting arrangement — see operational risk below.

**A data-integrity note on the example payload:** the sample `raw_payload_hash` given (`sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`) is one character too long for a valid SHA-256 digest (65 hex characters rather than 64). This is presumably a typo in the illustrative example rather than a real hash, but given that data provenance is a stated pillar of the project, it's worth running an automated format/length validator over every stored hash before this schema goes live — a single mistyped-length constant undermines the audit-layer credibility the project is built on.

**Operational architecture risk (not explicitly one of the four domains, but material to all of them):** The entire pipeline — ingestion, PostgreSQL, DuckDB, API, and archive — currently runs on a single VPS with modest resources (6 cores, 11 GiB RAM, 257 GiB SSD). This is adequate for the BICD pilot (Phase 1/2) but is a single point of failure for a project whose core value proposition is *citation permanence*. Before Phase 3 (global expansion) at the latest, the project needs an explicit backup/replication and disaster-recovery plan (off-site backups of the Postgres store and the `/data/raw/` archive at minimum), since losing this single host would not just cause downtime but would break the permanent-citation promise made in Domain 3's own review question.

---

## Domain 4: Strategic Phasing & BICD Focus

**Is BICD-first the right initial focus?** Yes, and it is well justified methodologically: the eight BICD assemblies share a family of procedural conventions (Westminster-derived, but with meaningful variation — devolved unicameral vs. Westminster bicameral vs. Crown Dependency assemblies), giving a controlled testbed that still exercises non-trivial schema variation before committing to full global rollout. Validating on a "clean" but non-trivial cohort before Phase 3 is sound engineering practice as well as sound research design.

**Specific challenges within the BICD cohort worth pre-empting:**

- **Tynwald (Isle of Man)** uses a distinctive branch structure (House of Keys / Legislative Council / Tynwald Court) and its legislative process for some instruments proceeds by resolution rather than the reading-stage model used elsewhere in the cohort — this will stress-test the `stage_canonical` enum earlier than expected, which is useful, but the schema should not assume all eight assemblies share the same stage vocabulary even within Phase 1.
- **Jersey and Guernsey** have historically weaker digitized Hansard back-coverage than Westminster/Holyrood, and Guernsey's committee-based (non-party) system of government makes "sponsor executive alignment" nearly meaningless in its Westminster-derived sense — the "GOVERNING_PARTY" concept may need a Guernsey-specific null/alternative category (e.g., "COMMITTEE_PROPOSED") rather than forcing a fit, which is precisely the Westminster-bias risk flagged in the project's own Domain 2 concern, arising within the "safe" pilot cohort itself.
- **Gibraltar** has a small legislature with correspondingly sparse Hansard digitization pre-2010s; full historical backfill to a single fixed start year across the cohort (as implied by Phase 2's per-country start dates) may not be achievable for Gibraltar at the same depth as UK/Scotland, and the plan should state a per-assembly realistic backfill floor rather than implying uniform depth.
- **Northern Ireland Assembly** has had multiple suspensions and restoration periods (most recently around 2017–2020 and again in 2022–2024); "session" and "duration" calculations need explicit handling for bills that span a suspension, since calendar-day duration calculations (as shown in the sample payload) will otherwise produce misleadingly long "duration_calendar_days" values that don't reflect actual sitting time — a `duration_sitting_days` or `duration_excluding_suspension` field is worth adding alongside the calendar figure.

**Recommendation:** Treat the BICD group not as internally homogeneous but as its own miniature version of the Phase 0 audit — i.e., run the 3-tier provenance audit *within* BICD before Phase 1 ingestion starts on all eight, rather than assuming Westminster conventions apply uniformly across the cohort.

---

## Additional Cross-Cutting Observations

1. **Legal/licensing consistency:** The document cites OGL v3.0, Open Parliament Licence, US 17 U.S.C. §105 (US federal government works have no copyright), and dl-de/by-2-0 (German open data licence) as the legal basis, but the worked example payload only shows an OGL licence tag. As the project scales to more jurisdictions, each source's licence terms (attribution requirements, share-alike conditions, commercial-use restrictions) should be captured as a first-class, machine-readable field per source rather than an assumed blanket compatibility — some jurisdictions' Hansard/proceedings transcripts carry more restrictive terms than the underlying bill-status data, and mirroring full transcripts is a materially different legal act from mirroring structured metadata.
2. **Sustainability/governance:** The academic tier is free and unlimited; the commercial tier funds the service. The document doesn't state a bus-factor or continuity plan (what happens to the free academic tier and citation permanence promise if the paid tier under-subscribes, or if the single maintainer becomes unavailable). Given that the project's academic value proposition rests partly on *citation longevity*, a stated data-escrow or archival-partner plan (e.g., committing to periodic full-dataset deposit with a long-term repository) would materially strengthen the proposal's credibility for citation by peer-reviewed research.
3. **Validation methodology not yet specified:** The document describes *what* the pipeline derives but not how derivation accuracy will be measured. A stated intent to publish inter-rater reliability or spot-check accuracy figures (e.g., a random sample of derived outcome classifications manually checked against Hansard/official record) for each jurisdiction before its data is marked `ENRICHED_BY_PIPELINE`-complete would substantially increase academic users' confidence in citing the platform.

---

## Summary of Recommendations

| Priority | Recommendation |
|---|---|
| High | Publish a versioned EDS methodology note (denominator, own-amendment handling, free-vote/coalition handling) before ingestion |
| High | Replace name-string matching in the Executive Roster join with a persistent member identifier |
| High | Add per-jurisdiction rules tables for ambiguous native status strings, rather than one global lookup |
| High | Add explicit handling for legislative sessions spanning suspensions (e.g., NI Assembly) |
| Medium | Extend the BICD "clean cohort" assumption check — run a mini Phase-0-style audit within BICD before Phase 1 |
| Medium | Define a disaster-recovery/replication plan for the single-VPS architecture before Phase 3 |
| Medium | Capture per-source licence terms as structured metadata, distinguishing structured data from full transcript mirroring |
| Low | Fix the illustrative SHA-256 length in the sample payload; add automated hash-format validation |
| Low | State explicit inclusion/exclusion policy for private member's bills and sub-decree-tier taxonomy ahead of Phase 3 |

---

*This review addresses the four commissioned domains plus cross-cutting operational and legal observations. Happy to expand on any single domain (e.g., a fuller worked EDS formula proposal, or a jurisdiction-by-jurisdiction BICD stage-vocabulary mapping) on request.*