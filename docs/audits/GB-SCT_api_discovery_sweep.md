# Scottish Parliament (GB-SCT) Empirical API Endpoint Discovery Sweep

**Date:** July 23, 2026  
**Target Host Base:** `https://data.parliament.scot/api/`  
**Purpose:** An isolated empirical discovery probe of all live open data endpoints served by Holyrood *before* mapping data availability against our institutional variables.

---

## 1. Discovered Active API Endpoints (200 OK Native Feeds)

| Endpoint Path | Total Records | Key Fields Discovered | Scientific & Analytical Value |
| :--- | :--- | :--- | :--- |
| **`/api/bills`** | 473 Bills | `ID`, `Reference`, `ShortName`, `FullName`, `BillTypeID`, `PersonID`, `ThirdPartyOrganisation` | Native bill metadata, primary MSP sponsor ID (`PersonID`), and external promoter (`ThirdPartyOrganisation`). |
| **`/api/billtypes`** | 7 Types | `ID`, `Name` (`Executive`, `Member's`, `Committee`, `Private`, etc.) | Closed-enum classification of bill origin. |
| **`/api/billstages`** | 1,754 Stage Events | `ID`, `BillID`, `BillStageTypeID`, `StageDate` | Historical stage event timestamps for every bill. |
| **`/api/billstagetypes`** | 34 Stage Types | `ID`, `Name`, `BillTypeID`, `Sequence` | Stage taxonomy with explicit ordering sequence (`Sequence: 0, 1, 2...`). |
| **`/api/sessions`** | 6 Sessions | `ID`, `ShortName`, `Name`, `StartDate`, `EndDate` | Official parliamentary term registry (`Session 1` through `Session 6`) with exact statutory start/end dates. |
| **`/api/governmentroles`**| 251 Roles | `ID`, `Name`, `Notes` | Exact ministerial portfolio registry (e.g. *Cabinet Secretary for Health and Social Care*). |
| **`/api/members`** | 416 MSPs | `PersonID`, `ParliamentaryName`, `PreferredName`, `GenderTypeID`, `IsCurrent`, `PhotoURL` | Full historical roster of Members of the Scottish Parliament. |
| **`/api/memberparties`** | 975 Records | `ID`, `PersonID`, `PartyID`, `ValidFromDate`, `ValidUntilDate` | **Temporal party affiliation engine.** Exact start/end dates for every MSP's party status (enabling point-in-time vote evaluation on date $T$). |
| **`/api/parties`** | 14 Parties | `ID`, `Abbreviation`, `ActualName`, `PreferredName`, `ValidFromDate`, `ValidUntilDate` | Party lookup table (SNP, Scottish Labour, Scottish Conservatives, Scottish Greens, Lib Dems, Independent). |
| **`/api/memberpartyroles`**| 1,508 Records | `ID`, `MemberPartyID`, `PartyRoleTypeID`, `ValidFromDate`, `ValidUntilDate` | Internal party leadership roles (Leader, Business Manager, Chief Whip). |
| **`/api/partyroles`** | 547 Roles | `ID`, `Name`, `PartyID` | Full historical party position titles. |
| **`/api/committees`** | 169 Committees| `ID`, `ShortName`, `Name`, `Description`, `ValidFromDate`, `ValidUntilDate` | Historical committee registry with exact active date ranges. |
| **`/api/committeetypes`**| 3 Types | `ID`, `Name` (`Mandatory`, `Subject`, `Ad Hoc`) | Committee classification. |
| **`/api/petitions`** | 2,250 Records | `ID`, `PetitionNumber`, `FirstName`, `LastName`, `PetitionTitle`, `PetitionSummary`, `SignaturesCollected`, `DateSubmitted`, `CommitteeID` | Citizen petitions linked to parliamentary committees. |
| **`/api/events`** | 2,710 Events | `ID`, `Date`, `Title`, `Sponsor` | Parliamentary events and member sponsorships. |
| **`/api/websites`** | 209 Links | `ID`, `PersonID`, `WebURL` | MSP official Twitter/X and website links. |
| **`/api/addresses`** | 162 Addresses | `ID`, `PersonID`, `AddressTypeID`, `Line1`, `Town`, `PostCode` | MSP constituency and parliamentary office addresses. |

---

## 2. Empirically Confirmed Native Data Gaps (HTTP 404 Endpoint Omissions)

The empirical sweep confirmed that Holyrood's Open Data API **does NOT serve the following datasets natively**:

1. **No Native Division / Vote Endpoint (`/api/votes` or `/api/divisions` $\rightarrow$ 404 Not Found):**
   * *Finding:* Roll-call division votes are published as text in the Official Report (Hansard) and HTML division pages, NOT as an API JSON dataset.
   * *Provenance Tier:* **`DERIVED_DETERMINISTIC`** (Requires web parsing of Official Report division logs).
2. **No Native Amendment Endpoint (`/api/amendments` $\rightarrow$ 404 Not Found):**
   * *Finding:* Marshalled Lists of Amendments and amendment outcomes are published as standalone PDF/HTML papers, NOT as an API dataset.
   * *Provenance Tier:* **`DERIVED_DETERMINISTIC`** / **`DERIVED_HUMAN_CODED`** (Requires PDF/HTML parsing of Marshalled Lists & PhD dataset ingestion).
3. **No Native Accompanying Document Text Endpoint (`/api/billdocuments` $\rightarrow$ 404 Not Found):**
   * *Finding:* Policy Memoranda, Financial Memoranda, and Explanatory Notes are hosted as PDF downloads on the website, NOT returned by the API.
   * *Provenance Tier:* **`DERIVED_DETERMINISTIC`** (Requires scraping document URLs from bill pages).

---

## 3. Potential New Institutional Variables Discovered from Live API Fields

The empirical sweep revealed several native API fields that lend themselves to capturing **new institutional variables**:

1. **`session_official_dates` (from `/api/sessions`):**
   * Serves exact statutory `StartDate` and `EndDate` for Sessions 1 through 6 out-of-the-box (e.g., Session 1: `1999-05-12` to `2003-03-31`).
2. **`third_party_organisation` (from `/api/bills`):**
   * Captures external non-governmental promoters for Private Bills (e.g. *National Galleries of Scotland*, *Edinburgh Tram Project*).
3. **`ministerial_portfolio_title` (from `/api/governmentroles`):**
   * Serves exact historical ministerial portfolio names for lead sponsors (251 distinct role titles, e.g. *Cabinet Secretary for Health and Social Care*).
4. **`petitions_count` & `petition_linked_committee` (from `/api/petitions`):**
   * Captures citizen mobilization around bills by linking citizen petitions assigned to scrutinizing committees.
5. **`party_leadership_role` (from `/api/memberpartyroles`):**
   * Identifies whether a sponsor or rebel MSP held a frontbench leadership position (Leader, Business Manager, Chief Whip) on vote date $T$.
6. **`committee_type` (from `/api/committeetypes`):**
   * Classifies lead committee as `Mandatory` (e.g. Finance, Standards, Delegated Powers) vs `Subject` (e.g. Health, Education, Justice).

---

## 4. Next Steps & Deductive Mapping Plan

With this empirical discovery sweep complete:
1. We now know **exactly** what Holyrood's API serves natively (Bills, Stage Types & Sequences, Sessions, Members, Member Parties, Government Roles, Committees, Petitions).
2. We know **exactly** what requires scraping or parsing (Roll-Call Votes, Marshalled Amendments, Document PDFs, Hansard Proceeding Word Counts).
3. We can update our institutional variables checklist with 100% accurate, verified **Provenance Tiers**!
