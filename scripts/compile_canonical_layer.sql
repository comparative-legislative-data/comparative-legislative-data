-- scripts/compile_canonical_layer.sql

-- ==================================================================
-- 1. DEFINE VIEW FOR CANONICAL BILLS
-- ==================================================================
DROP VIEW IF EXISTS view_canonical_bills CASCADE;
CREATE OR REPLACE VIEW view_canonical_bills AS
WITH stage_dates AS (
    -- Retrieve the completion dates for each stage based on official sequence numbers
    SELECT 
        bs.billid,
        COALESCE(MIN(CASE WHEN bt.sequence = 0 THEN bs.stagedate::date END), MIN(bs.stagedate::date)) AS intro_date,
        MAX(CASE WHEN bt.sequence = 1 THEN bs.stagedate::date END) AS s1_date,
        MAX(CASE WHEN bt.sequence = 2 THEN bs.stagedate::date END) AS s2_date,
        MAX(CASE WHEN bt.sequence = 3 THEN bs.stagedate::date END) AS s3_date,
        MAX(CASE WHEN bt.sequence = 5 THEN bs.stagedate::date END) AS recon_date
    FROM raw_mirror.raw_gb_sct_billstages bs
    JOIN raw_mirror.raw_gb_sct_billstagetypes bt ON bs.billstagetypeid = bt.id
    GROUP BY bs.billid
),
bill_sessions AS (
    -- Resolve session boundaries strictly based on the introduction date
    SELECT 
        b.id AS bill_id,
        sd.intro_date,
        COALESCE(s.id, 1) AS session_id,
        COALESCE(s.startdate::date, '1999-05-12'::date) AS session_start_date
    FROM raw_mirror.raw_gb_sct_bills b
    LEFT JOIN stage_dates sd ON sd.billid = b.id
    LEFT JOIN raw_mirror.raw_gb_sct_sessions s
      ON sd.intro_date >= s.startdate::date 
     AND (s.enddate IS NULL OR sd.intro_date <= s.enddate::date)
),
sponsor_party AS (
    -- Resolve the sponsor party temporally on the date of introduction
    SELECT 
        b.id AS bill_id,
        mp.partyid AS sponsor_party_id
    FROM raw_mirror.raw_gb_sct_bills b
    LEFT JOIN stage_dates sd ON sd.billid = b.id
    LEFT JOIN raw_mirror.raw_gb_sct_memberparties mp ON mp.personid = b.personid
      AND mp.validfromdate <= COALESCE(sd.intro_date, '9999-12-31')
      AND (mp.validuntildate IS NULL OR mp.validuntildate >= COALESCE(sd.intro_date, '1900-01-01'))
),
first_time_check AS (
    -- Calculate if the sponsor is a first-time MSP (first entry is in current session)
    SELECT 
        b.id AS bill_id,
        CASE 
            WHEN MIN(mp.validfromdate) >= bs.session_start_date THEN TRUE 
            ELSE FALSE 
        END AS sponsor_is_first_time
    FROM raw_mirror.raw_gb_sct_bills b
    JOIN bill_sessions bs ON bs.bill_id = b.id
    LEFT JOIN raw_mirror.raw_gb_sct_memberparties mp ON mp.personid = b.personid
    GROUP BY b.id, bs.session_start_date
)
SELECT 
    b.id AS bill_id,
    b.shortname AS short_name,
    bs.session_id,
    CASE 
        WHEN b.billtypeid IN (1, 3, 7) THEN 'Government'
        WHEN b.billtypeid = 2 THEN 'Member''s'
        WHEN b.billtypeid = 4 THEN 'Committee'
        WHEN b.billtypeid = 5 THEN 'Private'
        WHEN b.billtypeid = 6 THEN 'Hybrid'
        ELSE 'Unknown'
    END AS bill_type,
    CASE 
        WHEN b.billtypeid IN (1, 3, 7) THEN 'GOVERNMENT'
        ELSE 'NON_GOVERNMENT' 
    END AS sponsor_type,
    CASE 
        WHEN b.billtypeid = 5 THEN 'External Private Promoter'
        WHEN m.personid IS NULL AND b.billtypeid IN (1, 3, 7) THEN 'Lord Advocate (Law Officer)'
        ELSE COALESCE(m.parliamentaryname, 'Unknown')
    END AS sponsor_name,
    m.gendertypeid AS sponsor_gender_id,
    CASE 
        WHEN b.billtypeid = 5 THEN 98
        WHEN m.personid IS NULL AND b.billtypeid IN (1, 3, 7) THEN 99
        ELSE sp.sponsor_party_id
    END AS sponsor_party_id,
    ft.sponsor_is_first_time,
    -- Sessional Bill Load
    (COUNT(*) OVER (PARTITION BY bs.session_id))::integer AS sessional_bill_load,
    -- Stage 3 Passed
    CASE WHEN sd.s3_date IS NOT NULL THEN TRUE ELSE FALSE END AS passed_stage_3,
    -- Went to Reconsideration
    CASE WHEN sd.recon_date IS NOT NULL THEN TRUE ELSE FALSE END AS went_to_reconsideration,
    -- Bill Outcome (Defaulting to Fallen if not completed Stage 3)
    CASE 
        WHEN sd.s3_date IS NOT NULL THEN 'PASSED'
        ELSE 'FALLEN'
    END AS bill_outcome,
    sd.intro_date AS introduction_date,
    -- Calendar Durations
    (sd.s1_date - sd.intro_date)::integer AS t1_duration_calendar,
    (sd.s2_date - sd.s1_date)::integer AS t2_duration_calendar,
    (sd.s3_date - sd.s2_date)::integer AS t3_duration_calendar,
    CASE WHEN sd.recon_date IS NOT NULL THEN TRUE ELSE FALSE END AS viscosity_outlier
FROM raw_mirror.raw_gb_sct_bills b
LEFT JOIN stage_dates sd ON sd.billid = b.id
LEFT JOIN bill_sessions bs ON bs.bill_id = b.id
LEFT JOIN raw_mirror.raw_gb_sct_members m ON m.personid = b.personid
LEFT JOIN sponsor_party sp ON sp.bill_id = b.id
LEFT JOIN first_time_check ft ON ft.bill_id = b.id
LEFT JOIN raw_mirror.raw_gb_sct_billtypes bt ON bt.id = b.billtypeid;


-- ==================================================================
-- 2. DEFINE VIEW FOR CANONICAL MEMBER PARTY SNAPSHOTS
-- ==================================================================
DROP VIEW IF EXISTS view_canonical_member_party_history CASCADE;
CREATE OR REPLACE VIEW view_canonical_member_party_history AS
WITH date_series AS (
    -- Generate monthly dates series since the start of Session 1
    SELECT generate_series('1999-05-01'::date, CURRENT_DATE::date, '1 month'::interval)::date AS snapshot_date
),
active_member_parties AS (
    -- Count unique active members for each party on each snapshot date
    SELECT 
        ds.snapshot_date,
        mp.partyid,
        COUNT(DISTINCT mp.personid) AS member_count
    FROM date_series ds
    JOIN raw_mirror.raw_gb_sct_memberparties mp ON mp.validfromdate <= ds.snapshot_date
      AND (mp.validuntildate IS NULL OR mp.validuntildate >= ds.snapshot_date)
    GROUP BY ds.snapshot_date, mp.partyid
)
SELECT 
    amp.snapshot_date,
    amp.partyid AS party_id,
    COALESCE(p.preferredname, 'Independent') AS party_name,
    amp.member_count::integer
FROM active_member_parties amp
LEFT JOIN raw_mirror.raw_gb_sct_parties p ON p.id = amp.partyid;


-- ==================================================================
-- 3. COMPILE DATA (INSERT INTO PHYSICAL TABLES)
-- ==================================================================
-- Truncate physical tables to clean old compiles
TRUNCATE TABLE canonical_gb_sct_bills, canonical_gb_sct_member_party_history CASCADE;

-- Insert calculations into bills table
INSERT INTO canonical_gb_sct_bills
SELECT * FROM view_canonical_bills;

-- Insert calculations into member party snapshots table
INSERT INTO canonical_gb_sct_member_party_history
SELECT * FROM view_canonical_member_party_history;
