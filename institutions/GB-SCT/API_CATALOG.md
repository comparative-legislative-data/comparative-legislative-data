# Scottish Parliament (Holyrood / GB-SCT) Native API Catalog & Codebook

**Specification Version:** 2.8.0  
**Host Authority:** Scottish Parliament Open Data API (`data.parliament.scot/api`)  
**Historical Coverage:** May 1999 – Present (Sessions 1–6)  
**Last Updated:** July 24, 2026

---

## Endpoint Inventory & Coverage Matrix

| Endpoint Name | Target API URL | Temporal Range | Format | Primary Entity | Raw Native Keys Revealed |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`bills`** | `https://data.parliament.scot/api/bills` | 1999–Present | JSON | Bill Entity | `ID`, `Reference`, `ShortName`, `FullName`, `BillTypeID`, `PersonID`, `ThirdPartyOrganisation` |
| **`billtypes`** | `https://data.parliament.scot/api/billtypes` | 1999–Present | JSON | Bill Metadata | `ID`, `Name` |
| **`members`** | `https://data.parliament.scot/api/members` | 1999–Present | JSON | Member Entity | `PersonID`, `PhotoURL`, `Notes`, `BirthDate`, `BirthDateIsProtected`, `ParliamentaryName`, `PreferredName`, `GenderTypeID`, `IsCurrent` |
| **`memberparties`** | `https://data.parliament.scot/api/memberparties` | 1999–Present | JSON | Party Membership | `ID`, `PersonID`, `PartyID`, `ValidFromDate`, `ValidUntilDate`, `MemberPartyRoles` |
| **`parties`** | `https://data.parliament.scot/api/parties` | 1999–Present | JSON | Party Metadata | `ID`, `Abbreviation`, `ActualName`, `PreferredName`, `Notes`, `ValidFromDate`, `ValidUntilDate`, `MemberParties`, `PartyRoles` |
| **`PersonCommitteeRoles`** | `https://data.parliament.scot/api/PersonCommitteeRoles` | 1999–Present | JSON | Committee Role | `ID`, `PersonID`, `CommitteeRoleID`, `CommitteeID`, `ValidFromDate`, `ValidUntilDate`, `Notes` |
| **`committees`** | `https://data.parliament.scot/api/committees` | 1999–Present | JSON | Committee Context | `ID`, `ShortName`, `Name`, `Description`, `CommitteeEmailAddress`, `CommitteeTelephone`, `ValidFromDate`, `ValidUntilDate`, `BlogWebsite` |
| **`MemberGovernmentRoles`** | `https://data.parliament.scot/api/MemberGovernmentRoles` | 1999–Present | JSON | Executive Portfolio | `ID`, `PersonID`, `GovernmentRoleID`, `ValidFromDate`, `ValidUntilDate` |
| **`GovernmentRoles`** | `https://data.parliament.scot/api/GovernmentRoles` | 1999–Present | JSON | Ministerial Role | `ID`, `Name`, `Notes` |
| **`sessions`** | `https://data.parliament.scot/api/sessions` | 1999–Present | JSON | Term Context | `ID`, `ShortName`, `Name`, `StartDate`, `EndDate` |
| **`events`** | `https://data.parliament.scot/api/events` | 1999–Present | JSON | Event Metadata | `ID`, `Date`, `Title`, `Sponsor` |
| **`orsplenarymeeting`** | `https://data.parliament.scot/api/orsplenarymeeting?year={YYYY}` | 1999–Present | JSON (`octet-stream`) | Plenary Debate | `ID`, `Meeting`, `Committee`, `Time`, `ItemOfBusiness`, `Person`, `Detail`, `UpdatedElasticDate` |
| **`orscommitteemeeting`** | `https://data.parliament.scot/api/orscommitteemeeting?year={YYYY}` | 1999–Present | JSON (`octet-stream`) | Committee Debate | `ID`, `Meeting`, `Committee`, `Time`, `ItemOfBusiness`, `Person`, `Detail`, `UpdatedElasticDate` |

---

## Endpoint Details & Mapping Integrity

### 1. Bills API (`/api/bills`)
- **Description:** Master list of all Public, Private, and Hybrid Bills introduced in the Scottish Parliament since May 1999.
- **Key Attributes:**
  - `ID`: Unique integer identifier assigned by Holyrood.
  - `Reference`: Official bill reference number (e.g. `SP Bill 42`).
  - `ShortName`: Short canonical title of the bill.
  - `FullName`: Official long statutory title.
  - `BillTypeID`: Foreign key referencing `/api/billtypes` (Executive Bill, Member's Bill, Committee Bill, Private Bill).
  - `PersonID`: Lead sponsor MSP ID (for Member's Bills).

### 2. Members API (`/api/members`)
- **Description:** Complete directory of all Members of the Scottish Parliament (MSPs) serving in Sessions 1 through 6.
- **Key Attributes:**
  - `PersonID`: Unique MSP integer identifier.
  - `ParliamentaryName`: Official name string used in parliamentary record.
  - `BirthDate`: ISO 8601 birth date.
  - `GenderTypeID`: Gender classification code.
  - `PhotoURL`: Official portrait photo URL on parliament server.

### 3. Member Government Roles API (`/api/MemberGovernmentRoles`)
- **Description:** Point-in-time record of all ministerial and executive portfolio appointments.
- **Key Attributes:**
  - `PersonID`: Appointed MSP ID.
  - `GovernmentRoleID`: Foreign key referencing `/api/GovernmentRoles`.
  - `ValidFromDate` & `ValidUntilDate`: Temporal date window evaluated on Date $T$.

### 4. Official Report Debate APIs (`/api/orsplenarymeeting` & `/api/orscommitteemeeting`)
- **Description:** Complete verbatim Hansard speech intervention transcripts for all Plenary sittings and Committee sittings from 1999 to Present.
- **HTTP Header Quirk:** Server returns `Content-Type: application/octet-stream`. Data is UTF-8 encoded JSON array.
- **Key Attributes:**
  - `ID`: Intervention record ID.
  - `Time`: Exact timestamp of speech intervention.
  - `Person`: Speaker identification object (`PersonID`, `Name`).
  - `Detail`: Speech text HTML content.
