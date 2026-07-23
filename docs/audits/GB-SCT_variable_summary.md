# Scottish Parliament (GB-SCT) Audit Variable Summary

**Purpose:** A simplified, scannable checklist of all native Holyrood variables currently cataloged in the Audit Blueprint (`GB-SCT.yaml`).  
**Review Focus:** Skim this document to identify any missing variables from your PhD research or Scottish legislative studies.

---

## 1. Definitive Constants (Assembly Metadata)
* **`jurisdiction_code`**: `GB-SCT`
* **`name`**: Scottish Parliament (`Pàrlamaid na h-Alba`)
* **`chamber_type`**: `DEVOLVED_UNICAMERAL`
* **`statutory_seats_total`**: `129` MSP seats
* **`presiding_officer_neutral_count`**: `1` (Presiding Officer does not vote except to break ties)

---

## 2. Closed-Set Enums (Strictly Declared Options)

### `government_type` (Executive Arrangement)
* `SINGLE_PARTY_MAJORITY`
* `SINGLE_PARTY_MINORITY` *(SNP May 2011–2016, April 2024–Present)*
* `FORMAL_COALITION_MAJORITY` *(Lab/LibDem 1999–2007)*
* `FORMAL_COALITION_MINORITY`
* `CONFIDENCE_AND_SUPPLY`
* `COOPERATION_AGREEMENT` *(SNP/Scottish Greens Bute House Agreement Aug 2021–April 2024)*
* `CARETAKER_TECHNOCRATIC`

### `initiator_type` (Bill Sponsor Typology)
* `EXECUTIVE` *(Government Bill - Cabinet Secretary / Minister)*
* `INDIVIDUAL_MEMBER` *(Member's Bill)*
* `COMMITTEE` *(Committee Bill)*
* `PRIVATE_ORGANISATION` *(Private Bill / Hybrid Bill)*

### `final_status` (Terminal Outcome)
* `ENACTED` *(Received Royal Assent)*
* `DEFEATED` *(Defeated at Stage 1 or Stage 3 vote)*
* `WITHDRAWN` *(Withdrawn by sponsor)*
* `LAPSED` *(Lapsed at dissolution of Session)*
* `PENDING` *(Under active consideration)*
* `VETOED` *(Blocked by Section 35 Scotland Act Order)*

### `motion_type` (Stage Motion Classification)
* `STAGE_1_AGREEMENT` *(Motion to agree general principles)*
* `FINANCIAL_RESOLUTION` *(Motion required under Rule 9.12)*
* `EMERGENCY_BILL_DESIGNATION` *(Motion under Rule 9.21)*
* `STAGE_2_AMENDMENT` *(Committee stage amendment division)*
* `STAGE_3_PASSAGE` *(Final plenary passage vote)*

---

## 3. Result-Dependent Dynamic Measures (Empirical Values per Bill / Event)

### Stage Timelines & Intervals
* **`date_introduced`**: Date introduced.
* **`stage_1_lead_committee_report_date`**: Date of publication of Stage 1 report by lead committee.
* **`stage_1_parliament_agreement_vote_date`**: Date of Stage 1 plenary debate & agreement vote.
* **`duration_sitting_days`**: Total formal parliamentary sitting days elapsed.

### Bill Size & Text Growth
* **`bill_as_introduced_word_count`**: Word count of official text as introduced.
* **`bill_as_amended_stage_2_word_count`**: Word count after committee amendments.
* **`bill_as_enacted_word_count`**: Word count of final enacted Act.

### Amendments & PhD Hand-Coding
* **`amendments_tabled_stage_2_count`**: Count of amendments lodged for Stage 2 committee.
* **`non_executive_amendments_government_acceptance_rate`**: Proportion of opposition/backbench amendments accepted by Ministers *(from PhD dataset)*.

### Divisions, Voting & Party Dissent
* **`msp_party_affiliation_at_vote_date`**: MSP party status dynamically evaluated on exact vote date $T$.
* **`party_dissent_rate_at_event_date`**: Proportion of party MSPs voting against frontbench whip on vote date $T$.

---

## 4. Binary Flags (Procedural Triggers)
* **`financial_resolution_motion_flag`**: `True`/`False` (Rule 9.12 financial resolution required before Stage 2).
* **`emergency_bill_declaration_flag`**: `True`/`False` (Rule 9.21 emergency bill bypassing Stage 1 timelines).
* **`section_35_order_triggered_flag`**: `True`/`False` (Section 35 Scotland Act Order issued blocking Royal Assent, e.g. Gender Recognition Reform Bill).

---

## 5. Persistent Identifiers
* **`initiator_member_id`**: Wikidata QID for primary sponsor MSP.
* **`parlgov_cabinet_id`**: Linked cabinet ID from ParlGov benchmark dataset.

---

## 6. Institutional Hard Gaps
* **`committee_stage_2_informal_paper_gap`**: `RECORDED_BUT_UNDIGITIZED` (Informal Stage 2 committee working notes not published in open API format).

---

## 🔍 Skim Checklist for Review:
Are there any specific Holyrood procedural events, committee motions, member voting metrics, or PhD variables missing from this list?
