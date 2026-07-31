-- scripts/schema_canonical.sql
-- Create FDW extension to allow linking to raw Database A
CREATE EXTENSION IF NOT EXISTS postgres_fdw;

-- Create foreign server pointing to Database A (mirror_db)
CREATE SERVER IF NOT EXISTS mirror_server
  FOREIGN DATA WRAPPER postgres_fdw
  OPTIONS (host '127.0.0.1', port '5432', dbname 'comparative_legislative_data');

-- Create user mapping for database connections
CREATE USER MAPPING IF NOT EXISTS FOR chessadmin
  SERVER mirror_server
  OPTIONS (user 'chessadmin', password 'chessadmin');

CREATE USER MAPPING IF NOT EXISTS FOR postgres
  SERVER mirror_server
  OPTIONS (user 'chessadmin', password 'chessadmin');

-- Create a dedicated raw_mirror schema in canonical_db to hold virtual tables
CREATE SCHEMA IF NOT EXISTS raw_mirror;

-- Import selected raw mirror tables from Database A
IMPORT FOREIGN SCHEMA public
  LIMIT TO (
    raw_gb_sct_bills,
    raw_gb_sct_billstages,
    raw_gb_sct_members,
    raw_gb_sct_memberparties,
    raw_gb_sct_parties,
    raw_gb_sct_billstagetypes,
    raw_gb_sct_billtypes,
    raw_gb_sct_sessions
  )
  FROM SERVER mirror_server
  INTO raw_mirror;

-- Create canonical physical tables
CREATE TABLE IF NOT EXISTS canonical_gb_sct_bills (
    bill_id INTEGER PRIMARY KEY,
    short_name VARCHAR(250) NOT NULL,
    session_id INTEGER NOT NULL,
    bill_type VARCHAR(50) NOT NULL,
    sponsor_type VARCHAR(20) NOT NULL,
    sponsor_name VARCHAR(150) NOT NULL,
    sponsor_gender_id INTEGER,
    sponsor_party_id INTEGER,
    sponsor_is_first_time BOOLEAN,
    sessional_bill_load INTEGER,
    passed_stage_3 BOOLEAN,
    went_to_reconsideration BOOLEAN,
    bill_outcome VARCHAR(20),
    introduction_date DATE,
    t1_duration_calendar INTEGER,
    t2_duration_calendar INTEGER,
    t3_duration_calendar INTEGER,
    viscosity_outlier BOOLEAN
);

CREATE TABLE IF NOT EXISTS canonical_gb_sct_member_party_history (
    snapshot_date DATE,
    party_id INTEGER,
    party_name VARCHAR(100),
    member_count INTEGER,
    PRIMARY KEY (snapshot_date, party_id)
);
