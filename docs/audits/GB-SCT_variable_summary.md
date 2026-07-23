# Scottish Parliament (GB-SCT) Audit Variable Summary

**Specification Version:** 2.5.0 (Dual Entity: Bill + Amendment)  
**Purpose:** A simplified, scannable checklist of all native Holyrood variables cataloged in the Audit Blueprint (`GB-SCT.yaml`).  
**Review Focus:** Skim this checklist to see what native Scottish Parliament variables might be missing from your PhD research or Holyrood experience.

---

## 1. Definitive Constants (Assembly Metadata)
* **`jurisdiction_code`**: `GB-SCT`
* **`name`**: Scottish Parliament (`Pàrlamaid na h-Alba`)
* **`chamber_type`**: `DEVOLVED_UNICAMERAL`
* **`statutory_seats_total`**: `129` MSP seats
* **`presiding_officer_neutral_count`**: `1` (Presiding Officer does not vote except to break ties)

---

## 2. Entity 1: Bill-Level Variables (`CanonicalBill`)

### Closed-Set Enums (Strictly Declared Options)
* **`government_type`**: `[SINGLE_PARTY_MAJORITY, SINGLE_PARTY_MINORITY, FORMAL_COALITION_MAJORITY, FORMAL_COALITION_MINORITY, CONFIDENCE_AND_SUPPLY, COOPERATION_AGREEMENT, CARETAKER_TECHNOCRATIC]`
* **`initiator_type`**: `[EXECUTIVE, INDIVIDUAL_MEMBER, COMMITTEE, PRIVATE_ORGANISATION]`
* **`final_status`**: `[ENACTED, DEFEATED, WITHDRAWN, LAPSED, PENDING, VETOED]`

### Timelines & Stage Intervals
* **`date_introduced`**: Date introduced.
* **`stage_1_lead_committee_report_date`**: Date Stage 1 report published by lead committee.
* **`duration_sitting_days`**: Total formal parliamentary sitting days elapsed.

### Bill Text Size & Growth
* **`bill_as_introduced_word_count`**: Word count as introduced.
* **`bill_as_amended_stage_2_word_count`**: Word count post-Stage 2 committee amendments.
* **`bill_as_enacted_word_count`**: Word count of final enacted Act.

### Binary Procedural Flags
* **`financial_resolution_motion_flag`**: `True`/`False` (Rule 9.12 Financial Resolution required).
* **`emergency_bill_declaration_flag`**: `True`/`False` (Rule 9.21 Emergency Bill bypassing Stage 1 timelines).
* **`section_35_order_triggered_flag`**: `True`/`False` (Section 35 Scotland Act Order issued blocking Royal Assent).

---

## 3. Entity 2: Amendment-Level Variables (`CanonicalAmendment`)

### Micro Identifiers & Stage Context
* **`local_amendment_number`**: Holyrood Marshalled List amendment number (e.g. `Amd 42`, `LOD 104`).
* **`stage_canonical`**: `[COMMITTEE_STAGE, REPORT_STAGE, FINAL_PASSAGE]` (Stage 2 Committee vs Stage 3 Plenary).
* **`committee_name`**: Name of scrutinising committee (e.g. *Equalities, Human Rights and Civil Justice Committee*).

### Sponsor Alignment & Governance Role
* **`sponsor_member_id`**: Lead MSP sponsor Wikidata QID.
* **`sponsor_governance_role`**: `[EXECUTIVE_MINISTER, GOVERNING_BACKBENCH, OPPOSITION_MEMBER, CROSS_PARTY]`.

### Text Alteration & Executive Stance
* **`amendment_action_type`**: `[INSERTION, DELETION, SUBSTITUTION, PROBING]` *(from PhD hand-coded dataset)*.
* **`government_position`**: `[SUPPORTED, OPPOSED, NEUTRAL_NO_STANCE, MINISTERIAL_OWN_AMENDMENT]`.

### Outcome, Division & Member Rebellion
* **`disposition_canonical`**: `[AGREED_TO, DEFEATED, WITHDRAWN, NOT_MOVED, FALLEN]`.
* **`decision_mechanism`**: `[VOICE_VOTE_UNANIMOUS, DIVISION_ROLL_CALL, WITHDRAWN_WITHOUT_VOTE]`.
* **`party_dissent_rate_on_amendment`**: Proportion of governing party MSPs voting against frontbench whip on this amendment division.

---

## 🔍 Skim Checklist for Review:
Are there any specific Holyrood procedural events, amendment fields, committee motions, member voting metrics, or PhD variables missing from this list?
