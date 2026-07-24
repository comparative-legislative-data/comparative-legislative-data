# Master Canonical Variable Catalog

**Specification Version:** 2.8.0  
**Purpose:** Master Target Wishlist of quantitative research variables across 11 Legislative Research Domains.

---

## Provenance Evaluation Matrix

Every assembly audit blueprint evaluates variables against the **7-Tier Provenance Spectrum**:

1. **`NATIVE_DIRECT`**: Served directly out-of-the-box in host API feeds.
2. **`DERIVED_DETERMINISTIC`**: Pure rule-based relational joins or date arithmetic on structured JSON feeds.
3. **`DERIVED_EXTRACTED`**: Programmatic PDF/HTML document text extractions & regex parsing.
4. **`DERIVED_HUMAN_CODED`**: Expert hand-coding & academic datasets.
5. **`DERIVED_SYNTHETIC_AI`**: NLP/LLM probabilistic extractions.
6. **`LINKED_EXTERNAL_AUTHORITY`**: External benchmark identifiers (Wikidata QIDs, ParlGov, CAP).
7. **`UNAVAILABLE_HARD_GAP`**: Procedural hard gaps (`NOT_APPLICABLE_TO_ASSEMBLY`).

Variables pending formal audit verification are tagged **`NOT_YET_CATEGORISED`**.

---

## 11 Legislative Research Domains

* **Domain 1:** Assembly, Electoral & Executive Context
* **Domain 2:** Bill Identification, Sponsorship & Temporal Origin
* **Domain 3:** Progression, Stage Timelines & Multi-Day Debates
* **Domain 4:** Financial Resolutions & Procedural Motions
* **Domain 5:** Plenary Roll-Call Motions & Voting Coalitions
* **Domain 6:** Accompanying Bill Documents & Text Size Analytics
* **Domain 7:** Final Disposition & Inter-Chamber Mechanisms
* **Domain 8:** Macro Amendment Aggregates & Text Alteration
* **Domain 9:** Micro Amendment Entity Records (`CanonicalAmendment`)
* **Domain 10:** Committee Context & Roster Engine (`CommitteeContext`)
* **Domain 11:** Parsed Proceedings & Official Report Analytics (`ParsedProceedings`)
