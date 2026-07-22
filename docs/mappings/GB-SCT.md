# Scottish Parliament (GB-SCT) Data Mapping & Audit Profile

This document details the **Phase 0 Parliamentary Data Audit, Access Specification, and Field Mapping Rules** for the **Scottish Parliament (`GB-SCT`)**.

---

## 1. Assembly Overview & Constitutional Framework

- **Official Assembly Name:** Scottish Parliament (Pàrlamaid na h-Alba)
- **Jurisdiction Code:** `GB-SCT`
- **Chamber Structure:** Devolved Unicameral (129 Members of the Scottish Parliament - MSPs)
- **Primary Legislative Measures Included:** Executive Bills (Government Bills), Member Bills, Committee Bills, Private Bills, Hybrid Bills.
- **Primary Legislative Measures Excluded:** Subordinate Legislation (Scottish Statutory Instruments - SSIs), Legislative Consent Motions (LCMs), Non-binding Motions.

---

## 2. Access Paradigm, Endpoints & Open License

- **Data Access Paradigm:** Official REST API (`https://www.parliament.scot/api/`) & Web Open Data Portal
- **Primary API Endpoints:**
  - Bills Feed: `GET https://www.parliament.scot/api/bills`
  - Bill Details: `GET https://www.parliament.scot/api/bills/{id}`
  - MSPs & Members: `GET https://data.parliament.scot/api/members`
- **Authentication:** Public (No API key required)
- **Rate Limits:** Standard polite web polling (1–2 req/sec)
- **Open Data License:** Open Government Licence (OGL) v3.0 / Scottish Parliament Open Data Licence

---

## 3. 5-Bill Typology Sample Audit Results

| Archetype | Sample Measure ID & Title | Native Outcome String | Audit Findings & Pipeline Derivation Notes |
| :--- | :--- | :--- | :--- |
| **1. Executive Bill (Enacted)** | SP Bill 13: *Gender Recognition Reform (Scotland) Bill* | "Passed" | Clean Stage 1, 2, 3 dates; note Section 35 Order challenge flagged in `native.raw_status`. |
| **2. Member Bill (Enacted)** | SP Bill 24: *Dog Abduction (Scotland) Bill* | "Royal Assent" | Primary sponsor mapped to Wikidata QID `Q...`; `initiator_type: INDIVIDUAL_MEMBER`, `governance_role: OPPOSITION_PARTY`. |
| **3. Member Bill (Lapsed/Defeated)** | SP Bill 08: *Restitution for Mining Communities Bill* | "Lapsed" | Mapped `final_status: LAPSED`, `termination_mechanism: SESSION_EXPIRY`. |
| **4. Contested / Highly Scrutinised** | SP Bill 18: *Hate Crime and Public Order (Scotland) Act 2021* | "Royal Assent" | Multi-stage amendments parsed cleanly into `stage_milestones`. |
| **5. Private / Hybrid / Emergency** | SP Bill 01: *Coronavirus (Scotland) Act 2020* | "Royal Assent" | Accelerated emergency passage (3 calendar days) mapped cleanly. |

---

## 4. Field-by-Field 3-Tier Data Provenance Matrix

### 4.1 Root & Normalized Layers (`normalized.*`)

| Canonical Field | Data Type | Provenance Tier | Native Source Field / Derivation Logic |
| :--- | :--- | :--- | :--- |
| `canonical_id` | String | `ENRICHED_BY_PIPELINE` | Formatted `GB-SCT-S{session}-SPB{billId}`. |
| `jurisdiction_code` | String | `NATIVE_DIRECT` | Constant `GB-SCT`. |
| `title` | Text | `NATIVE_DIRECT` | `Title` |
| `parliament_term` | String | `NATIVE_DIRECT` | `Session` (e.g. `Session 6`). |
| `session_subperiod` | String | `NATIVE_DIRECT` | `Session` (e.g. `Session 6 (2021-2026)`). |
| `initiator_type` | Enum | `ENRICHED_BY_PIPELINE` | Derived from `BillType` (`Executive Bill` $\rightarrow$ `EXECUTIVE`, `Member's Bill` $\rightarrow$ `INDIVIDUAL_MEMBER`). |
| `initiator_party_governance_role` | Enum | `ENRICHED_BY_PIPELINE` | Derived by joining sponsor MSP ID + date against Scottish Government Cabinet Roster. |
| `date_introduced` | Date | `NATIVE_DIRECT` | `IntroducedDate` (`YYYY-MM-DD`). |
| `date_final_outcome` | Date | `NATIVE_DIRECT` | `PassedDate` or `RoyalAssentDate` (`YYYY-MM-DD`). |
| `duration_calendar_days` | Integer | `ENRICHED_BY_PIPELINE` | Calculated `date_final_outcome` - `date_introduced`. |
| `duration_sitting_days` | Integer | `ENRICHED_BY_PIPELINE` | Calculated actual sitting days excluding Holyrood recess dates. |
| `suspension_interrupted` | Boolean | `ENRICHED_BY_PIPELINE` | Flagged `false` for standard Scottish Parliament sessions. |
| `final_status` | Enum | `ENRICHED_BY_PIPELINE` | Derived from native status string (`ENACTED`, `DEFEATED`, `WITHDRAWN`, `LAPSED`). |
| `termination_mechanism` | Enum | `ENRICHED_BY_PIPELINE` | Derived mechanism (`ENACTMENT`, `EXECUTIVE_WITHDRAWAL`, `SESSION_EXPIRY`). |
| `rebellions_flag` | Boolean | `ENRICHED_BY_PIPELINE` | Derived from Stage 3 division records. |
| `cross_party_sponsorship_count` | Integer | `ENRICHED_BY_PIPELINE` | Calculated count of co-sponsor MSPs from other parties. |
| `derivation_confidence` | Enum | `ENRICHED_BY_PIPELINE` | High confidence (`HIGH`). |
| `stage_milestones` | Array | `ENRICHED_BY_PIPELINE` | Array of parsed `StageMilestone` objects (Stage 1, Stage 2, Stage 3, Royal Assent). |

### 4.2 Native Layer (`native.*`)

| Native Field | Data Type | Provenance Tier | Description |
| :--- | :--- | :--- | :--- |
| `local_bill_id` | String | `NATIVE_DIRECT` | `SP Bill {billNumber}` |
| `title_native` | Text | `NATIVE_DIRECT` | `Title` |
| `initiator_raw` | Text | `NATIVE_DIRECT` | `MemberName` or `MinisterTitle` |
| `initiator_name` | Text | `NATIVE_DIRECT` | `MemberName` |
| `initiator_member_id` | String | `ENRICHED_BY_PIPELINE` | Persistent Wikidata QID / native MSP ID. |
| `initiator_party` | Text | `NATIVE_DIRECT` | `PartyName` |
| `raw_status` | Text | `NATIVE_DIRECT` | `CurrentStatus` |
| `official_proceedings_url` | String | `NATIVE_DIRECT` | `https://www.parliament.scot/bills-and-laws/bills/{billSlug}` |
| `official_publication_ref` | Text | `NATIVE_DIRECT` | `SP Bill {billNumber} Session {session}` |

---

## 5. Proceedings & Hansard Link Resolution

- **Debate Transcript Availability:** Official Official Report (Hansard) links available via `parliament.scot/chamber-and-committees/official-report`.
- **Linking Mechanism:** Stage 1, Stage 2, and Stage 3 milestone records link directly to Official Report debate logs.
- **Hansard Citation Format:** `Official Report, Scottish Parliament, {date}, Col {col}`.

---

## 6. Consensus & Non-Partisan Rules

- **Party System:** Multi-Party System (Minority / Coalition / Majority Governments).
- **Governance Alignment Handling:** Uses Scottish Cabinet Roster boundary dates (e.g. SNP-Green Bute House Agreement period 2021–2024 mapped as governing coalition).
