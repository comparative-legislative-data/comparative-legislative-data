# Active Canonical Research Variables Manual: Scottish Parliament (GB-SCT)

This document serves as the master codebook and single source of truth for all derived and canonical research variables implemented in the **Scottish Parliament (`GB-SCT`)** datasets. 

For the system architecture, ingestion pipelines, and database infrastructure backing these variables, see the [System Architecture Specification: Scottish Parliament](file:///home/steven/Documents/github/comparativelegislativedata/docs/gb-sct/architecture.md).

---

## 1. Canonical Bills Table (`canonical_gb_sct_bills`)

This physical table resides in Database B (`comparative_legislative_data_canonical`). It is fully self-contained, duplicating key raw identifiers (such as short names and sponsor names) directly into each row so the SvelteKit frontend or researchers can query it without running cross-database joins to the raw mirror tables in Database A.

| Variable Name | Data Type | Provenance Tier | Calculation SQL Formula | Academic Description |
| :--- | :--- | :--- | :--- | :--- |
| **`bill_id`** | `INTEGER` | Tier 1 (`NATIVE_DIRECT`) | `b.id` | Unique primary key ID mapping directly to raw bills ID. |
| **`short_name`** | `VARCHAR(250)`| Tier 2 (`DERIVED_DETERMINISTIC`) | `b.shortname` | Short title of the Bill (e.g. "Land") duplicated from raw to allow standalone querying. |
| **`session_id`** | `INTEGER` | Tier 2 (`DERIVED_DETERMINISTIC`) | Temporal join: `raw_gb_sct_sessions.id` matching introduction date | Resolved parliamentary session (1 to 6) based on date ranges of each opening parliament day. |
| **`sponsor_type`** | `VARCHAR(20)` | Tier 2 (`DERIVED_DETERMINISTIC`) | `CASE WHEN b.billtypeid IN (1, 3, 7) THEN 'GOVERNMENT' ELSE 'NON_GOVERNMENT' END` | Normalized sponsor: `GOVERNMENT` (consolidating Executive, Government, and Budget types) or `NON_GOVERNMENT`. |
| **`sponsor_name`** | `VARCHAR(150)`| Tier 2 (`DERIVED_DETERMINISTIC`) | `CASE WHEN billtypeid = 5 THEN 'External Private Promoter' ... END` | Sponsoring member's parliamentary name, resolved Law Officer title, or 'External Private Promoter' for Private bills. |
| **`sponsor_gender_id`** | `INTEGER` | Tier 2 (`DERIVED_DETERMINISTIC`) | `m.gendertypeid` | Gender identifier code of the sponsor joined from raw members. |
| **`sponsor_party_id`** | `INTEGER` | Tier 2 (`DERIVED_DETERMINISTIC`) | Temporal join / Rule fallback | Sponsor party ID on intro date. Non-MSP government leads map to synthetic ID 99 (Law Officer (Non-Party)). Private bills map to synthetic ID 98 (Private Promoter (Non-Party)) to avoid blending with Independent MSPs. |
| **`sponsor_is_first_time`**| `BOOLEAN` | Tier 2 (`DERIVED_DETERMINISTIC`) | Valid dates check | `TRUE` if the sponsor's first term of service started in the current session; else `FALSE`. |
| **`sessional_bill_load`** | `INTEGER` | Tier 2 (`DERIVED_DETERMINISTIC`) | `(COUNT(*) OVER (PARTITION BY session_id))` | Workload count: total bills introduced in the session. |
| **`passed_stage_3`** | `BOOLEAN` | Tier 2 (`DERIVED_DETERMINISTIC`) | Stages check | `TRUE` if a `Stage 3 Passed` stage event is present; else `FALSE`. |
| **`went_to_reconsideration`**| `BOOLEAN`| Tier 2 (`DERIVED_DETERMINISTIC`) | Stages check | `TRUE` if a `Reconsideration Stage` event is logged subsequent to the Stage 3 date; else `FALSE`. |
| **`bill_outcome`** | `VARCHAR(20)`| Tier 2 (`DERIVED_DETERMINISTIC`) | `CASE WHEN s3_date IS NOT NULL THEN 'PASSED' ELSE 'FALLEN' END` | Unified outcome: `PASSED` (Stage 3 completed) or `FALLEN` (covering withdrawn, voted down, and lapsed bills). |
| **`bill_type`** | `VARCHAR(50)`| Tier 2 (`DERIVED_DETERMINISTIC`) | `CASE WHEN b.billtypeid IN (1, 3, 7) THEN 'Government' ... END` | Normalized bill type: `Government` (consolidating Executive, Government, and Budget), `Member's`, `Committee`, `Private`, `Hybrid`. |
| **`introduction_date`**| `DATE` | Tier 1 (`NATIVE_DIRECT`) | `sd.intro_date` | The resolved calendar date of the Bill's introduction. |
| **`t1_duration_calendar`**| `INTEGER` | Tier 2 (`DERIVED_DETERMINISTIC`) | `(sd.s1_date - sd.intro_date)` | Calendar days elapsed between introduction date and Stage 1 completion. |
| **`t2_duration_calendar`**| `INTEGER` | Tier 2 (`DERIVED_DETERMINISTIC`) | `(sd.s2_date - sd.s1_date)` | Calendar days elapsed between Stage 1 completion and Stage 2 completion. |
| **`t3_duration_calendar`**| `INTEGER` | Tier 2 (`DERIVED_DETERMINISTIC`) | `(sd.s3_date - sd.s2_date)` | Calendar days elapsed between Stage 2 completion and Stage 3 Passage. |
| **`viscosity_outlier`** | `BOOLEAN` | Tier 2 (`DERIVED_DETERMINISTIC`) | `went_to_reconsideration` | `TRUE` if the bill was referred back for Reconsideration, causing abnormal delays. |

---

## 2. Member Party Snapshots Table (`canonical_gb_sct_member_party_history`)

This physical table resides in Database B. It documents historical monthly counts of parliamentary seats held by each political party in the chamber.

| Variable Name | Data Type | Provenance Tier | Calculation SQL Formula | Academic Description |
| :--- | :--- | :--- | :--- | :--- |
| **`snapshot_date`** | `DATE` | Tier 1 (`NATIVE_DIRECT`) | `generate_series('1999-05-01'::date, CURRENT_DATE::date, '1 month')` | First day of the month for the snapshot date, generated natively in a monthly series. |
| **`party_id`** | `INTEGER` | Tier 1 (`NATIVE_DIRECT`) | `mp.partyid` | Unique political party identifier mapping to raw parties. |
| **`party_name`** | `VARCHAR(150)`| Tier 2 (`DERIVED_DETERMINISTIC`) | `COALESCE(p.preferredname, 'Independent')` | Preferred text name of the political party. |
| **`member_count`** | `INTEGER` | Tier 2 (`DERIVED_DETERMINISTIC`) | `COUNT(DISTINCT mp.personid)` | Number of unique members holding seats for that party on the snapshot date. |

---

## 3. SvelteKit Endpoint Models Registry

These configurations define the schemas mapped in the canonical router at `frontend/src/routes/api/v2/canonical/gb-sct/[endpoint]/+server.ts`:

### 3.1 Endpoint `bills`
*   **Table:** `canonical_gb_sct_bills`
*   **Key Field:** `BillID`
*   **Fields:**
    ```typescript
    fields: {
      BillID: { dbColumn: 'bill_id', type: 'int' },
      ShortName: { dbColumn: 'short_name', type: 'str' },
      SessionID: { dbColumn: 'session_id', type: 'int' },
      SponsorType: { dbColumn: 'sponsor_type', type: 'str' },
      SponsorName: { dbColumn: 'sponsor_name', type: 'str' },
      SponsorPartyID: { dbColumn: 'sponsor_party_id', type: 'int' },
      SponsorGenderID: { dbColumn: 'sponsor_gender_id', type: 'int' },
      SponsorGoverningStatus: { dbColumn: 'sponsor_governing_status', type: 'bool' },
      SponsorIsFirstTime: { dbColumn: 'sponsor_is_first_time', type: 'bool' },
      GovMinorityStatus: { dbColumn: 'gov_minority_status', type: 'bool' },
      SessionalBillLoad: { dbColumn: 'sessional_bill_load', type: 'int' },
      PassedStage3: { dbColumn: 'passed_stage_3', type: 'bool' },
      WentToReconsideration: { dbColumn: 'went_to_reconsideration', type: 'bool' },
      BillOutcome: { dbColumn: 'bill_outcome', type: 'str' },
      IntroductionDate: { dbColumn: 'introduction_date', type: 'date' },
      T1DurationCalendar: { dbColumn: 't1_duration_calendar', type: 'int' },
      T2DurationCalendar: { dbColumn: 't2_duration_calendar', type: 'int' },
      T3DurationCalendar: { dbColumn: 't3_duration_calendar', type: 'int' },
      ViscosityOutlier: { dbColumn: 'viscosity_outlier', type: 'bool' }
    }
    ```

### 3.2 Endpoint `memberpartyhistory`
*   **Table:** `canonical_gb_sct_member_party_history`
*   **Key Field:** `SnapshotDate`
*   **Fields:**
    ```typescript
    fields: {
      SnapshotDate: { dbColumn: 'snapshot_date', type: 'date' },
      PartyID: { dbColumn: 'party_id', type: 'int' },
      PartyName: { dbColumn: 'party_name', type: 'str' },
      MemberCount: { dbColumn: 'member_count', type: 'int' }
    }
    ```
