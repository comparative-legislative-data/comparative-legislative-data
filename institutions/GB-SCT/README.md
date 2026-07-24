# Scottish Parliament (Holyrood / GB-SCT) Data Workspace

**Jurisdiction Code:** `GB-SCT`  
**Legislative Assembly:** The Scottish Parliament (Pàrlamaid na h-Alba)  
**Historical Coverage:** Sessions 1–6 (May 1999 – Present)  
**Raw Ingested Records:** 102,317 Raw Records across 13 Open Data API Endpoints  
**Audit Baseline:** Pass 1 Complete (72 Empirical Ground-Truth Variables) | Pass 2 Candidate Assessment (47 Specifications)  
**Host Parity Verification:** `100.0% EXACT MATCH VERIFIED` ([Audit Report](PARITY_REPORT.md))

---

## Data Ecosystem & Database Mirror

The Scottish Parliament operates one of the most transparent open API infrastructures among OECD assemblies (`data.parliament.scot/api`). The platform mirrors all 13 open data streams into a high-speed database, executing 1:1 host parity reconciliation audits after every refresh.

### Workspace Audit & Transparency Codebooks

1. **[`API_CATALOG.md`](API_CATALOG.md):** Native API codebook documenting all 13 host endpoints, historical temporal ranges, revealed native keys, and byte sizes.
2. **[`TRANSFORMATION_RULES.md`](TRANSFORMATION_RULES.md):** Peer-reviewable codebook documenting the exact mathematical and temporal derivation rules for all 21 `DERIVED_DETERMINISTIC` variables.
3. **[`MISSINGNESS_MATRIX.md`](MISSINGNESS_MATRIX.md):** Field-by-field empirical missingness table calculated across all 473 Holyrood bills.
4. **[`PARITY_REPORT.md`](PARITY_REPORT.md):** Automated 1:1 host parity reconciliation audit report confirming 100.0% exact match between live host API endpoints and local database mirror.
5. **[`AUDIT_BLUEPRINT.yaml`](AUDIT_BLUEPRINT.yaml):** Machine-readable canonical audit blueprint.
6. **[`AUDIT_SUMMARY.md`](AUDIT_SUMMARY.md):** Empirical provenance matrix report.

---

## Multi-Format Dataset Exports & REST APIs

Researchers can access the complete 72-variable canonical bill dataset for Sessions 1–6 (1999–Present) in their preferred computational format:

* 📊 **CSV Dataset:** [`/static/data/GB-SCT_canonical_bills.csv`](https://legislativedata.org/static/data/GB-SCT_canonical_bills.csv) (For Excel / SPSS / Stata)
* 📄 **JSON Dataset:** [`/static/data/GB-SCT_canonical_bills.json`](https://legislativedata.org/static/data/GB-SCT_canonical_bills.json) (For Web / Python)
* 📦 **Parquet Dataset:** [`/static/data/GB-SCT_canonical_bills.parquet`](https://legislativedata.org/static/data/GB-SCT_canonical_bills.parquet) (For DuckDB / Wasm / Polars)
* 📈 **R Import Script:** [`/static/data/GB-SCT_canonical_bills_loader.R`](https://legislativedata.org/static/data/GB-SCT_canonical_bills_loader.R) (For RStudio)
* ⚡ **Live REST API:** `https://legislativedata.org/api/v1/GB-SCT/canonical/bills?limit=50`
