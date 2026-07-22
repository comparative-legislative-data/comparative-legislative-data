# UK Parliament (GB-UKP) Data Mapping & Audit Profile

This document details the **Phase 0 Parliamentary Data Audit, Access Specification, and Field Mapping Rules** for the **UK Parliament (`GB-UKP`)**.

---

## 1. Assembly Overview & Constitutional Framework

- **Official Assembly Name:** UK Parliament (Westminster)
- **Jurisdiction Code:** `GB-UKP`
- **Chamber Structure:** Sovereign Bicameral (House of Commons & House of Lords)
- **Primary Legislative Measures Included:** Government Bills, Private Members' Bills (Ballot, Ten Minute Rule, Presentation), Private Bills, Hybrid Bills.
- **Primary Legislative Measures Excluded:** Statutory Instruments (SIs), Delegated Legislation, Non-binding House Resolutions.

---

## 2. Access Paradigm, Endpoints & Open License

- **Data Access Paradigm:** Official REST API (`https://bills-api.parliament.uk/api/v1`)
- **Primary API Endpoints:**
  - Bills Search: `GET https://bills-api.parliament.uk/api/v1/Bills`
  - Bill Detail: `GET https://bills-api.parliament.uk/api/v1/Bills/{id}`
  - Bill Stages: `GET https://bills-api.parliament.uk/api/v1/Bills/{id}/Stages`
  - Hansard Debates: `https://hansard-api.parliament.uk/`
- **Authentication:** Public (No API key required)
- **Rate Limits:** No formal throttling published; standard polite polling (1–2 req/sec).
- **Open Data License:** Open Parliament Licence v3.0 / Open Government Licence (OGL) v3.0

---

## 3. 5-Bill Typology Sample Audit Results

| Archetype | Sample Measure ID & Title | Native Outcome String | Audit Findings & Pipeline Derivation Notes |
| :--- | :--- | :--- | :--- |
| **1. Executive Bill (Enacted)** | Bill 3156: *Online Safety Act 2023* | "Act of Parliament" | Clean stage dates (588 calendar days), Hansard URLs resolved for Commons & Lords readings. |
| **2. Member Bill (Enacted)** | Bill 3012: *Co-operatives etc. Act 2023* | "Royal Assent" | Primary sponsor mapped to Wikidata QID; `initiator_type: INDIVIDUAL_MEMBER`, `governance_role: OPPOSITION_PARTY`. |
| **3. Member Bill (Lapsed/Defeated)** | Bill 2940: *Pensions Bill* | "Dropped at Prorogation" | Mapped `final_status: LAPSED`, `termination_mechanism: SESSION_EXPIRY`. |
| **4. Contested / Highly Scrutinised** | Bill 3201: *Illegal Migration Act 2023* | "Act of Parliament" | Multi-stage Ping-Pong proceedings linked to Hansard debate transcripts. |
| **5. Private / Hybrid / Emergency** | Bill 2800: *High Speed Rail Bill* | "Passed" | Hybrid committee stage milestones parsed into `stage_milestones`. |

---

## 4. Field-by-Field 3-Tier Data Provenance Matrix

### 4.1 Root & Normalized Layers (`normalized.*`)

| Canonical Field | Data Type | Provenance Tier | Native Source Field / Derivation Logic |
| :--- | :--- | :--- | :--- |
| `canonical_id` | String | `ENRICHED_BY_PIPELINE` | Formatted `GB-UKP-P58-B{billId}`. |
| `jurisdiction_code` | String | `NATIVE_DIRECT` | Constant `GB-UKP`. |
| `title` | Text | `NATIVE_DIRECT` | `shortTitle` |
| `parliament_term` | String | `NATIVE_DIRECT` | `session.name` (e.g. `58th Parliament (2022-23)`). |
| `session_subperiod` | String | `NATIVE_DIRECT` | `session.name` (e.g. `2022-23`). |
| `initiator_type` | Enum | `ENRICHED_BY_PIPELINE` | Derived from `billType.name` & `category` (`Government Bill` $\rightarrow$ `EXECUTIVE`, `Private Member...` $\rightarrow$ `INDIVIDUAL_MEMBER`). |
| `initiator_party_governance_role` | Enum | `ENRICHED_BY_PIPELINE` | Derived by joining `sponsors[0].member.memberId` + `introducedDate` against UK Ministerial Roster DB. |
| `date_introduced` | Date | `NATIVE_DIRECT` | `introducedDate` (`YYYY-MM-DD`). |
| `date_final_outcome` | Date | `NATIVE_DIRECT` | `actDate` or `lastUpdate` (`YYYY-MM-DD`). |
| `duration_calendar_days` | Integer | `ENRICHED_BY_PIPELINE` | Calculated `date_final_outcome` - `date_introduced`. |
| `duration_sitting_days` | Integer | `ENRICHED_BY_PIPELINE` | Calculated actual sitting days excluding recess periods. |
| `suspension_interrupted` | Boolean | `ENRICHED_BY_PIPELINE` | Flagged `false` for standard UK sessions. |
| `final_status` | Enum | `ENRICHED_BY_PIPELINE` | Derived from `isAct` and `currentStatus.name` (`ENACTED`, `DEFEATED`, `WITHDRAWN`, `LAPSED`). |
| `termination_mechanism` | Enum | `ENRICHED_BY_PIPELINE` | Derived mechanism (`ENACTMENT`, `EXECUTIVE_WITHDRAWAL`, `SESSION_EXPIRY`). |
| `rebellions_flag` | Boolean | `ENRICHED_BY_PIPELINE` | Derived from Commons division records. |
| `cross_party_sponsorship_count` | Integer | `ENRICHED_BY_PIPELINE` | Calculated count of co-sponsors from non-governing parties. |
| `derivation_confidence` | Enum | `ENRICHED_BY_PIPELINE` | High confidence (`HIGH`). |
| `stage_milestones` | Array | `ENRICHED_BY_PIPELINE` | Array of parsed `StageMilestone` objects from `stages[]`. |

### 4.2 Native Layer (`native.*`)

| Native Field | Data Type | Provenance Tier | Description |
| :--- | :--- | :--- | :--- |
| `local_bill_id` | String | `NATIVE_DIRECT` | `Bill {billId}` |
| `title_native` | Text | `NATIVE_DIRECT` | `shortTitle` |
| `initiator_raw` | Text | `NATIVE_DIRECT` | `billType.name` |
| `initiator_name` | Text | `NATIVE_DIRECT` | `sponsors[0].member.name` |
| `initiator_member_id` | String | `NATIVE_DIRECT` | `sponsors[0].member.memberId` |
| `initiator_party` | Text | `NATIVE_DIRECT` | `sponsors[0].member.party` |
| `raw_status` | Text | `NATIVE_DIRECT` | `currentStatus.name` |
| `official_proceedings_url` | String | `NATIVE_DIRECT` | `https://bills.parliament.uk/bills/{billId}` |
| `official_publication_ref` | Text | `NATIVE_DIRECT` | `Bill {billId} ({session.name})` |

---

## 5. Proceedings & Hansard Link Resolution

- **Debate Transcript Availability:** Direct Hansard links embedded in API `stages[].hansardLink`.
- **Linking Mechanism:** Stage milestones link directly to Commons/Lords Hansard transcript entries.
- **Hansard Citation Format:** `HC Deb {date} vol {vol} c{col}` / `HL Deb {date} vol {vol} c{col}`.

---

## 6. Consensus & Non-Partisan Rules

- **Party System:** Standard Party System (Government vs. Opposition).
- **Governance Alignment Handling:** Uses standard `GOVERNING_PARTY` vs `OPPOSITION_PARTY` rules based on the 2010–2024 Conservative Government and post-July 2024 Labour Government boundary dates.
