# Scottish Parliament (GB-SCT) Empirical API Endpoint Discovery Sweep

**Date:** July 23, 2026  
**Target Host Base:** `https://data.parliament.scot/api/`  
**Specification:** Version 2.7.0 (Verified Open Data API Audit & Expert Review Corrections)

---

## 1. Discovered Active API Endpoints (200 OK Native Feeds)

| Endpoint Path | Total Records | Key Fields Discovered | Scientific & Analytical Value |
| :--- | :--- | :--- | :--- |
| **`/api/bills`** | 473 Bills | `ID`, `Reference`, `ShortName`, `FullName`, `BillTypeID`, `PersonID`, `ThirdPartyOrganisation` | Native bill metadata, lead MSP sponsor (`PersonID`), and external promoter (`ThirdPartyOrganisation`). |
| **`/api/billtypes`** | 7 Types | `ID`, `Name` (`Executive`, `Member's`, `Committee`, `Private`, etc.) | Closed-enum classification of bill origin. |
| **`/api/billstages`** | 1,754 Stage Events | `ID`, `BillID`, `BillStageTypeID`, `StageDate` | Historical stage event timestamps for every bill. |
| **`/api/billstagetypes`** | 34 Stage Types | `ID`, `Name`, `BillTypeID`, `Sequence` | Stage taxonomy with explicit ordering sequence (`Sequence: 0, 1, 2...`). |
| **`/api/sessions`** | 6 Sessions | `ID`, `ShortName`, `Name`, `StartDate`, `EndDate` | Official term registry (`Session 1` through `Session 6`) with exact statutory start/end dates. |
| **`/api/PersonCommitteeRoles`**| **3,699 Records** | `ID`, `PersonID`, `CommitteeID`, `CommitteeRoleID`, `ValidFromDate`, `ValidUntilDate` | **Complete Committee Membership & Convener Engine.** Serves exact start/end dates for every MSP's committee membership and Convener/Deputy Convener roles. |
| **`/api/CommitteeRoles`** | 8 Roles | `ID`, `Name` (`Convener`, `Deputy Convener`, `Member`, etc.) | Taxonomy of committee positions. |
| **`/api/committees`** | 169 Committees| `ID`, `ShortName`, `Name`, `Description`, `ValidFromDate`, `ValidUntilDate` | Historical committee registry with active date ranges. |
| **`/api/committeetypes`**| 3 Types | `ID`, `Name` (`Mandatory`, `Subject`, `Ad Hoc`) | Committee classification. |
| **`/api/MemberGovernmentRoles`**| **381 Records** | `ID`, `PersonID`, `GovernmentRoleID`, `ValidFromDate`, `ValidUntilDate` | **Temporal Executive Portfolio Engine.** Serves exact start/end appointment dates for Ministers. |
| **`/api/GovernmentRoles`** | 251 Roles | `ID`, `Name`, `Notes` | Portfolio title registry (e.g. *Cabinet Secretary for Health and Social Care*). |
| **`/api/members`** | 416 MSPs | `PersonID`, `ParliamentaryName`, `PreferredName`, `GenderTypeID`, `IsCurrent`, `PhotoURL` | Full historical roster of Members of the Scottish Parliament. |
| **`/api/memberparties`** | 975 Records | `ID`, `PersonID`, `PartyID`, `ValidFromDate`, `ValidUntilDate` | **Temporal Party Affiliation Engine.** Exact start/end dates for every MSP's party status (enabling point-in-time vote evaluation on date $T$). |
| **`/api/parties`** | 14 Parties | `ID`, `Abbreviation`, `ActualName`, `PreferredName`, `ValidFromDate`, `ValidUntilDate` | Party lookup table (SNP, Scottish Labour, Scottish Conservatives, Scottish Greens, Lib Dems, Independent). |
| **`/api/memberpartyroles`**| 1,508 Records | `ID`, `MemberPartyID`, `PartyRoleTypeID`, `ValidFromDate`, `ValidUntilDate` | Internal party leadership roles (Leader, Business Manager, Chief Whip). |

---

## 2. Plenary Motion Votes & Paper Dispositions

1. **Plenary Motion Division Votes (Stage 1, Stage 3, Financial Resolution, Emergency Motions):**
   * *Status:* Available from Holyrood Chamber Voting logs and Official Report feeds.
   * *Provenance Tier:* **`NATIVE_DIRECT`** / **`DERIVED_DETERMINISTIC`**.
2. **Committee Amendments & Marshalled Lists:**
   * *Status:* Marshalled Lists and amendment outcomes are published as standalone PDF/HTML papers and Official Report committee proceedings.
   * *Provenance Tier:* **`DERIVED_DETERMINISTIC`** / **`DERIVED_HUMAN_CODED`** (Requires Marshalled List parsing + PhD dataset ingestion).
3. **Petitions Note:** Citizen petitions endpoint (`/api/petitions`) dropped from scope per expert review.

---

## 3. Discovered Native Variables Integrated into Blueprint

1. **`person_committee_roles` (`/api/PersonCommitteeRoles`):**
   * Captures committee memberships, Convener MSP IDs, and Deputy Convener MSP IDs with exact active date ranges.
2. **`third_party_organisation` (`/api/bills`):**
   * Captures external non-governmental promoters for Private Bills (*National Galleries of Scotland*, *Edinburgh Tram Project*).
3. **`ministerial_portfolio_title` (`/api/MemberGovernmentRoles` + `/api/GovernmentRoles`):**
   * Serves exact historical ministerial portfolio names for lead sponsors.
4. **`session_dates` (`/api/sessions`):**
   * Serves exact statutory start/end dates for Sessions 1 through 6.
