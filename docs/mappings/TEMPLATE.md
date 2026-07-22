# [JURISDICTION_NAME] ([JURISDICTION_CODE]) Data Mapping & Audit Profile

This document details the **Phase 0 Parliamentary Data Audit, Access Specification, and Field Mapping Rules** for **[JURISDICTION_NAME] (`[JURISDICTION_CODE]`)**.

---

## 1. Assembly Overview & Constitutional Framework

- **Official Assembly Name:** [e.g. UK Parliament / Scottish Parliament / States of Jersey]
- **Jurisdiction Code:** `[JURISDICTION_CODE]` (e.g. `GB-UKP`, `GB-SCT`, `JE-STJ`)
- **Chamber Structure:** [Sovereign Bicameral / Devolved Unicameral / Crown Dependency Consensus]
- **Primary Legislative Measures Included:** [e.g. Government Bills, Private Members' Bills]
- **Primary Legislative Measures Excluded:** [e.g. Statutory Instruments, Non-binding Motions]

---

## 2. Access Paradigm, Endpoints & Open License

- **Data Access Paradigm:** [Official REST API / Bulk XML / HTML Web Portal / PDF Papers]
- **Primary API Base URL:** `[ENDPOINT_URL]`
- **Authentication:** [Public (No Auth) / API Key Required]
- **Rate Limits:** [e.g. 10 requests/sec / None published]
- **Open Data License:** [e.g. Open Parliament Licence v3.0 / OGL v3.0 / Public Domain]

---

## 3. 5-Bill Typology Sample Audit Results

| Archetype | Sample Measure ID & Title | Native Outcome String | Audit Findings & Pipeline Derivation Notes |
| :--- | :--- | :--- | :--- |
| **1. Executive Bill (Enacted)** | [e.g. Online Safety Act 2023] | "Act of Parliament" | Clean stage dates, Hansard URLs resolved for all readings. |
| **2. Member Bill (Enacted)** | [e.g. Hunting Trophies Bill] | "Royal Assent" | Sponsor member ID resolved via Wikidata QID; non-executive role verified. |
| **3. Member Bill (Lapsed/Defeated)** | [e.g. Protection of Pensions Bill] | "Lapsed at Prorogation" | Mapped `final_status: LAPSED`, `termination_mechanism: SESSION_EXPIRY`. |
| **4. Contested / Highly Scrutinised** | [e.g. Illegal Migration Act] | "Act of Parliament" | Multi-stage Ping-Pong proceedings linked to Hansard transcripts. |
| **5. Private / Hybrid / Emergency** | [e.g. High Speed Rail Bill] | "Passed" | Non-standard hybrid committee track mapped cleanly. |

---

## 4. Field-by-Field 3-Tier Data Provenance Matrix

### 4.1 Root & Normalized Layers (`normalized.*`)

| Canonical Field | Data Type | Provenance Tier | Native Source Field / Derivation Logic |
| :--- | :--- | :--- | :--- |
| `canonical_id` | String | `ENRICHED_BY_PIPELINE` | Formatted `[JURISDICTION]-[TERM]-[LOCAL_ID]` (e.g. `GB-UKP-P58-B3156`). |
| `jurisdiction_code` | String | `NATIVE_DIRECT` | Constant `[JURISDICTION_CODE]`. |
| `title` | Text | `NATIVE_DIRECT` | Mapped from native title field. |
| `parliament_term` | String | `NATIVE_DIRECT` | Macro electoral term (e.g. `58th Parliament`, `Session 6`). |
| `session_subperiod` | String | `NATIVE_DIRECT` | Annual session subperiod (e.g. `2022-23`). |
| `initiator_type` | Enum | `ENRICHED_BY_PIPELINE` | Categorised from native bill type string (`EXECUTIVE`, `INDIVIDUAL_MEMBER`, etc.). |
| `initiator_party_governance_role` | Enum | `ENRICHED_BY_PIPELINE` | Derived by joining sponsor member ID + date against Executive Roster DB. |
| `date_introduced` | Date | `NATIVE_DIRECT` | Native introduction timestamp (`YYYY-MM-DD`). |
| `date_final_outcome` | Date | `NATIVE_DIRECT` | Native outcome timestamp (`YYYY-MM-DD`). |
| `duration_calendar_days` | Integer | `ENRICHED_BY_PIPELINE` | Calculated $\text{date\_final\_outcome} - \text{date\_introduced}$. |
| `duration_sitting_days` | Integer | `ENRICHED_BY_PIPELINE` | Calculated actual sitting days excluding official recess periods. |
| `suspension_interrupted` | Boolean | `ENRICHED_BY_PIPELINE` | Flagged `true` if passage spanned a formal parliamentary suspension. |
| `final_status` | Enum | `ENRICHED_BY_PIPELINE` | Derived canonical status (`ENACTED`, `DEFEATED`, `WITHDRAWN`, `LAPSED`). |
| `termination_mechanism` | Enum | `ENRICHED_BY_PIPELINE` | Derived mechanism (`ENACTMENT`, `EXECUTIVE_WITHDRAWAL`, `SESSION_EXPIRY`, etc.). |
| `rebellions_flag` | Boolean | `ENRICHED_BY_PIPELINE` | Derived from division vote records. |
| `cross_party_sponsorship_count` | Integer | `ENRICHED_BY_PIPELINE` | Calculated count of co-sponsors from non-governing parties. |
| `derivation_confidence` | Enum | `ENRICHED_BY_PIPELINE` | Derivation confidence level (`HIGH`, `MEDIUM`, `LOW`). |
| `stage_milestones` | Array | `ENRICHED_BY_PIPELINE` | Array of parsed `StageMilestone` objects. |

### 4.2 Native Layer (`native.*`)

| Native Field | Data Type | Provenance Tier | Description |
| :--- | :--- | :--- | :--- |
| `local_bill_id` | String | `NATIVE_DIRECT` | Host assembly reference string. |
| `title_native` | Text | `NATIVE_DIRECT` | Unmodified native title. |
| `initiator_raw` | Text | `NATIVE_DIRECT` | Unmodified native sponsor string. |
| `initiator_name` | Text | `NATIVE_DIRECT` | Member name string. |
| `initiator_member_id` | String | `ENRICHED_BY_PIPELINE` | Persistent Wikidata QID / native member ID. |
| `initiator_party` | Text | `NATIVE_DIRECT` | Native party affiliation string. |
| `raw_status` | Text | `NATIVE_DIRECT` | Unmodified status string from host feed. |
| `official_proceedings_url` | String | `NATIVE_DIRECT` | Direct URL to official assembly proceedings page. |
| `official_publication_ref` | Text | `NATIVE_DIRECT` | Native publication citation. |

---

## 5. Proceedings & Hansard Link Resolution

- **Debate Transcript Availability:** [Direct Hansard Links / Sitting Day Transcripts]
- **Linking Mechanism:** [Mapped via stage `hansardLink` / Mapped via sitting date & bill ID]
- **Hansard Citation Format:** [e.g. `HC Deb 14 June 2022 vol 716 c1-48`]

---

## 6. Consensus & Non-Partisan Rules

- **Party System:** [Standard Party System / Non-Partisan Consensus]
- **Governance Alignment Handling:** [e.g. Uses `GOVERNING_PARTY` vs `OPPOSITION_PARTY` / Uses `NON_PARTISAN` or `COMMITTEE_PROPOSED`]
