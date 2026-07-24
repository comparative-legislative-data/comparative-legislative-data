# Scottish Parliament (Holyrood / GB-SCT) Data Workspace

**Jurisdiction Code:** `GB-SCT`  
**Legislative Assembly:** The Scottish Parliament (Pàrlamaid na h-Alba)  
**Historical Coverage:** Sessions 1–6 (May 1999 – Present)  
**Audit Baseline:** Pass 1 Complete (72 Empirical Ground-Truth Variables) | Pass 2 Candidate Assessment (47 Specifications)

---

## Data Ecosystem Overview

The Scottish Parliament operates one of the most transparent, open API-first data infrastructures among OECD devolved and national assemblies (`data.parliament.scot/api`). 

### Core Native API Endpoints
- **Bills & Legislation:** `/api/bills`, `/api/billtypes`, `/api/BillStages`, `/api/BillStageTypes`
- **Members & Governance:** `/api/members`, `/api/memberparties`, `/api/parties`, `/api/PersonCommitteeRoles`, `/api/committees`, `/api/MemberGovernmentRoles`, `/api/GovernmentRoles`
- **Sessions & Events:** `/api/sessions`, `/api/events`
- **Official Report Debate Proceedings:** `/api/orsplenarymeeting`, `/api/orscommitteemeeting`

---

## Workspace Files & Documentation

1. **[`AUDIT_BLUEPRINT.yaml`](file:///home/steven/Documents/github/comparativelegislativedata/institutions/GB-SCT/AUDIT_BLUEPRINT.yaml):** Machine-readable audit specification for all 119 canonical variables, documenting Pass 1 empirical tiers and Pass 2 candidate specifications.
2. **[`AUDIT_SUMMARY.md`](file:///home/steven/Documents/github/comparativelegislativedata/institutions/GB-SCT/AUDIT_SUMMARY.md):** Provenance matrix report breaking down the 51 `NATIVE_DIRECT`, 21 `DERIVED_DETERMINISTIC`, and 47 `NOT_YET_CATEGORISED` variables.

---

## Historical Temporal Coverage Matrix

| Entity / Dataset | Temporal Range | Format | Primary Host Endpoint |
| :--- | :--- | :--- | :--- |
| **Bills & Stages** | May 1999 – Present | JSON / Open API | `https://data.parliament.scot/api/bills` |
| **Member Profiles & Parties** | May 1999 – Present | JSON / Open API | `https://data.parliament.scot/api/members` |
| **Ministerial Roles & Portfolios** | May 1999 – Present | JSON / Open API | `https://data.parliament.scot/api/MemberGovernmentRoles` |
| **Committee Roles & Membership** | May 1999 – Present | JSON / Open API | `https://data.parliament.scot/api/PersonCommitteeRoles` |
| **Plenary Debate Interventions** | May 1999 – Present | Structured JSON | `https://data.parliament.scot/api/orsplenarymeeting` |
| **Committee Debate Interventions**| May 1999 – Present | Structured JSON | `https://data.parliament.scot/api/orscommitteemeeting` |
| **Official Stage Prints (PDF/HTML)**| May 1999 – Present | PDF / HTML | Parliament Publications Archive |
| **Marshalled Lists of Amendments** | May 1999 – Present | PDF Prints | Business Bulletin & Amendment Archives |
