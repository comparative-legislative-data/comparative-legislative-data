# Scottish Parliament (GB-SCT) Deterministic Transformation Specification

**Specification Version:** 2.8.0  
**Scope:** 21 `DERIVED_DETERMINISTIC` Variables (Pass 1 Baseline)  
**Methodological Mandate:** 100% Deterministic — 0% Parsing Ambiguity — Zero Black-Box Code  
**Last Updated:** July 24, 2026

---

## Overview

This document specifies the exact, line-by-line mathematical formulas, relational joins, and temporal window evaluations used to calculate our 21 `DERIVED_DETERMINISTIC` variables from the raw Scottish Parliament open API feeds (`data.parliament.scot/api`).

All transformations are evaluated at specific **Decision-Point Dates ($T$)** (e.g. Bill Introduction Date $T_{\text{intro}}$ or Final Vote Date $T_{\text{vote}}$).

---

## Transformation Codebook

### 1. Executive & Party Alignment Variables

#### 1.1 `government_type`
- **Definition:** Classification of the active Scottish Executive on Date $T_{\text{intro}}$.
- **Derivation Rule:**
  - Evaluate governing coalition roster active on $T_{\text{intro}}$ from `/api/parties` and `/api/MemberGovernmentRoles`.
  - IF total governing party seats $> 65$ (out of 129 total seats) AND governing parties count $= 1$ $\rightarrow$ `SINGLE_PARTY_MAJORITY`.
  - IF total governing party seats $> 65$ AND governing parties count $> 1$ $\rightarrow$ `COALITION_MAJORITY`.
  - IF total governing party seats $\le 65$ AND governing parties count $= 1$ $\rightarrow$ `SINGLE_PARTY_MINORITY`.
  - IF total governing party seats $\le 65$ AND governing parties count $> 1$ $\rightarrow$ `COALITION_MINORITY`.

#### 1.2 `governing_parties_list`
- **Definition:** Array of political party abbreviations forming the Scottish Executive on Date $T_{\text{intro}}$.
- **Derivation Rule:**
  - Query `/api/MemberGovernmentRoles` WHERE $T_{\text{intro}} \in [\text{ValidFromDate}, \text{ValidUntilDate}]$.
  - Extract distinct `PartyID` from `/api/memberparties` for appointed Ministers.
  - Map `PartyID` to `Abbreviation` in `/api/parties`. Output sorted Array (e.g., `["SNP", "SGreen"]`).

#### 1.3 `initiator_type`
- **Definition:** Typology classification of the lead bill sponsor.
- **Derivation Rule:**
  - Join `BillTypeID` from `/api/bills` to `ID` in `/api/billtypes`.
  - IF `billtypes.Name` contains `"Government"` or `"Executive"` $\rightarrow$ `EXECUTIVE`.
  - IF `billtypes.Name` contains `"Member"` $\rightarrow$ `INDIVIDUAL_MEMBER`.
  - IF `billtypes.Name` contains `"Committee"` $\rightarrow$ `COMMITTEE`.
  - IF `billtypes.Name` contains `"Private"` $\rightarrow$ `PRIVATE_ORGANISATION`.

#### 1.4 `initiator_party_governance_role`
- **Definition:** Alignment of the lead sponsor's political party relative to the governing executive on Date $T_{\text{intro}}$.
- **Derivation Rule:**
  - Determine lead sponsor `PersonID` from `/api/bills`.
  - Determine sponsor `PartyID` on Date $T_{\text{intro}}$ from `/api/memberparties`.
  - IF `PartyID` $\in$ `governing_parties_list` $\rightarrow$ `GOVERNING_PARTY`.
  - IF `PartyID` $\notin$ `governing_parties_list` $\rightarrow$ `OPPOSITION_PARTY`.

#### 1.5 `ministerial_portfolio_title`
- **Definition:** Portfolio title held by the bill sponsor on Date $T_{\text{intro}}$.
- **Derivation Rule:**
  - Join sponsor `PersonID` to `/api/MemberGovernmentRoles` WHERE $T_{\text{intro}} \in [\text{ValidFromDate}, \text{ValidUntilDate}]$.
  - Join `GovernmentRoleID` to `Name` in `/api/GovernmentRoles`. Output string (or `null` if non-minister).

---

### 2. Legislative Duration Variables

#### 2.1 `duration_calendar_days`
- **Definition:** Total calendar days elapsed from bill introduction to final enactment/outcome.
- **Formula:** $T_{\text{outcome}} - T_{\text{intro}}$ (ISO 8601 date difference in calendar days).

#### 2.2 `duration_sitting_days`
- **Definition:** Total parliamentary sitting days elapsed between $T_{\text{intro}}$ and $T_{\text{outcome}}$.
- **Formula:** Count of sittings in `/api/events` WHERE `EventDate` $\in [T_{\text{intro}}, T_{\text{outcome}}]$ AND `EventType` $=$ Plenary/Committee Sitting.

#### 2.3 `stage_1_debate_days_count`
- **Formula:** $T_{\text{stage1\_end}} - T_{\text{stage1\_start}} + 1$.

#### 2.4 `stage_3_debate_days_count`
- **Formula:** $T_{\text{stage3\_end}} - T_{\text{stage3\_start}} + 1$.

---

### 3. Roll-Call Voting & Dissent Variables

#### 3.1 `financial_resolution_required_flag`
- **Derivation Rule:** Boolean `true` IF `/api/events` contains a Financial Resolution motion event for `local_bill_id`, ELSE `false`.

#### 3.2 `financial_resolution_approved_flag`
- **Derivation Rule:** Boolean `true` IF `financial_resolution_aye_count` $>$ `financial_resolution_no_count`, ELSE `false`.

#### 3.3 `decision_point_motion_type`
- **Derivation Rule:** String classification from `/api/events` (e.g., `"STAGE_3_PASSAGE_MOTION"`, `"FINANCIAL_RESOLUTION"`).

#### 3.4 `effective_majority_margin_at_event_date`
- **Definition:** Voting majority margin as a percentage of voting MSPs.
- **Formula:** $\frac{\text{AyeCount} - \text{NoCount}}{\text{AyeCount} + \text{NoCount}} \times 100$.

#### 3.5 `party_dissent_rate_at_event_date`
- **Definition:** Percentage of MSPs voting against their party majority on decision Date $T$.
- **Formula:** $\frac{\sum \text{Dissenting Member Votes}}{\text{Total Party Member Votes}} \times 100$.

#### 3.6 `voting_coalition_type`
- **Derivation Rule:**
  - IF all governing parties vote Aye AND all opposition parties vote No $\rightarrow$ `PARTISAN_GOVERNMENT_VS_OPPOSITION`.
  - IF all governing parties AND lead opposition party vote Aye $\rightarrow$ `CROSS_PARTY_CONSENSUS`.
  - IF opposition party votes with governing party against main opposition $\rightarrow$ `VARIABLE_GEOMETRY_MAJORITY`.

---

### 4. Committee & Disposition Variables

#### 4.1 `committee_type`
- **Derivation Rule:** Joined from `/api/committees.Description` (`"Mandatory Mandatory Committee"`, `"Subject Committee"`, `"Ad-hoc Select Committee"`).

#### 4.2 `committee_convener_member_id`
- **Derivation Rule:** `PersonID` from `/api/PersonCommitteeRoles` WHERE `CommitteeRoleID` $=$ Convener AND $T \in [\text{ValidFromDate}, \text{ValidUntilDate}]$.

#### 4.3 `committee_deputy_convener_member_id`
- **Derivation Rule:** `PersonID` from `/api/PersonCommitteeRoles` WHERE `CommitteeRoleID` $=$ Deputy Convener AND $T \in [\text{ValidFromDate}, \text{ValidUntilDate}]$.

#### 4.4 `final_status`
- **Derivation Rule:** `PASSED_ENACTED` IF `royal_assent_date` IS NOT NULL, `FALLEN_REJECTED` IF final stage motion failed, `WITHDRAWN_LAPSED` IF withdrawn by sponsor.

#### 4.5 `termination_mechanism`
- **Derivation Rule:** Specific procedural code explaining bill termination (e.g. `STAGE_1_DEBATE_REJECTION`, `WITHDRAWN_BY_SPONSOR`, `SESSION_DISSOLUTION_LAPSE`).
