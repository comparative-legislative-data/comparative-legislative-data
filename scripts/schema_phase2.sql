-- Comparative Legislative Data Phase 2: PostgreSQL Schema definitions for raw GB-SCT OData mirroring

-- 1. DROP EXISTING RAW TABLES (IF ANY)
DROP TABLE IF EXISTS raw_gb_sct_sync_logs CASCADE;
DROP TABLE IF EXISTS raw_gb_sct_committee_reports CASCADE;
DROP TABLE IF EXISTS raw_gb_sct_plenary_reports CASCADE;
DROP TABLE IF EXISTS raw_gb_sct_votes CASCADE;
DROP TABLE IF EXISTS raw_gb_sct_motions CASCADE;
DROP TABLE IF EXISTS raw_gb_sct_personcommitteeroles CASCADE;
DROP TABLE IF EXISTS raw_gb_sct_committees CASCADE;
DROP TABLE IF EXISTS raw_gb_sct_memberparties CASCADE;
DROP TABLE IF EXISTS raw_gb_sct_members CASCADE;
DROP TABLE IF EXISTS raw_gb_sct_billstages CASCADE;
DROP TABLE IF EXISTS raw_gb_sct_bills CASCADE;
DROP TABLE IF EXISTS raw_gb_sct_committeetypes CASCADE;
DROP TABLE IF EXISTS raw_gb_sct_committeeroles CASCADE;
DROP TABLE IF EXISTS raw_gb_sct_parties CASCADE;
DROP TABLE IF EXISTS raw_gb_sct_billstagetypes CASCADE;
DROP TABLE IF EXISTS raw_gb_sct_billtypes CASCADE;

-- 2. CREATE LOOKUP TABLES
CREATE TABLE raw_gb_sct_billtypes (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE raw_gb_sct_billstagetypes (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    bill_type_id INT,
    sequence INT
);

CREATE TABLE raw_gb_sct_parties (
    id INT PRIMARY KEY,
    abbreviation VARCHAR(50),
    actual_name VARCHAR(255),
    preferred_name VARCHAR(255),
    notes TEXT,
    valid_from_date TIMESTAMP,
    valid_until_date TIMESTAMP
);

CREATE TABLE raw_gb_sct_committeeroles (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    notes TEXT
);

CREATE TABLE raw_gb_sct_committeetypes (
    id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- 3. CREATE CORE RELATIONAL TABLES
CREATE TABLE raw_gb_sct_bills (
    id INT PRIMARY KEY,
    reference VARCHAR(100),
    short_name VARCHAR(255),
    full_name TEXT,
    bill_type_id INT REFERENCES raw_gb_sct_billtypes(id),
    person_id INT,
    third_party_organisation TEXT
);

CREATE TABLE raw_gb_sct_billstages (
    id INT PRIMARY KEY,
    bill_id INT REFERENCES raw_gb_sct_bills(id),
    bill_stage_type_id INT REFERENCES raw_gb_sct_billstagetypes(id),
    stage_date TIMESTAMP
);

CREATE TABLE raw_gb_sct_members (
    person_id INT PRIMARY KEY,
    photo_url TEXT,
    notes TEXT,
    birth_date TIMESTAMP,
    birth_date_is_protected BOOLEAN,
    parliamentary_name VARCHAR(255),
    preferred_name VARCHAR(255),
    gender_type_id INT,
    is_current BOOLEAN
);

CREATE TABLE raw_gb_sct_memberparties (
    id INT PRIMARY KEY,
    person_id INT REFERENCES raw_gb_sct_members(person_id),
    party_id INT REFERENCES raw_gb_sct_parties(id),
    valid_from_date TIMESTAMP,
    valid_until_date TIMESTAMP
);

CREATE TABLE raw_gb_sct_committees (
    id INT PRIMARY KEY,
    short_name VARCHAR(100),
    name VARCHAR(255),
    description TEXT,
    committee_email_address VARCHAR(255),
    committee_telephone VARCHAR(100),
    valid_from_date TIMESTAMP,
    valid_until_date TIMESTAMP
);

CREATE TABLE raw_gb_sct_personcommitteeroles (
    id INT PRIMARY KEY,
    person_id INT REFERENCES raw_gb_sct_members(person_id),
    committee_role_id INT REFERENCES raw_gb_sct_committeeroles(id),
    committee_id INT REFERENCES raw_gb_sct_committees(id),
    valid_from_date TIMESTAMP,
    valid_until_date TIMESTAMP,
    notes TEXT
);

-- 4. CREATE COMPLEX TRANSACTIONAL TABLES
CREATE TABLE raw_gb_sct_motions (
    unique_id INT PRIMARY KEY,
    event_id VARCHAR(100),
    event_type_id INT,
    event_sub_type_id INT,
    msp_id INT,
    party VARCHAR(100),
    region_id INT,
    constituency_id INT,
    approved_date TIMESTAMP,
    submission_date_time TIMESTAMP,
    title VARCHAR(255),
    item_text TEXT
);

CREATE TABLE raw_gb_sct_votes (
    id VARCHAR(100) PRIMARY KEY,
    detail JSONB NOT NULL,
    motion JSONB NOT NULL,
    person JSONB NOT NULL,
    time JSONB NOT NULL,
    updated_elastic_date TIMESTAMP
);

CREATE TABLE raw_gb_sct_plenary_reports (
    id VARCHAR(100) PRIMARY KEY,
    meeting JSONB NOT NULL,
    committee JSONB NOT NULL,
    time JSONB NOT NULL,
    item_of_business JSONB NOT NULL,
    person JSONB NOT NULL,
    detail JSONB NOT NULL,
    updated_elastic_date TIMESTAMP
);

CREATE TABLE raw_gb_sct_committee_reports (
    id VARCHAR(100) PRIMARY KEY,
    record_type VARCHAR(100),
    sub_type VARCHAR(100),
    meeting JSONB NOT NULL,
    committee JSONB NOT NULL,
    time JSONB NOT NULL,
    item_of_business JSONB NOT NULL,
    person JSONB NOT NULL,
    detail JSONB NOT NULL,
    location JSONB,
    updated_date TIMESTAMP,
    updated_elastic_date TIMESTAMP
);

-- 5. CREATE SYNC LOG TABLE
CREATE TABLE raw_gb_sct_sync_logs (
    id SERIAL PRIMARY KEY,
    sync_time TIMESTAMP DEFAULT NOW(),
    endpoint_name VARCHAR(100) NOT NULL,
    records_fetched INT,
    reconciliation_status VARCHAR(50), -- 'PARITY_MATCH', 'GAP_DETECTED', 'SYNC_FAIL'
    error_message TEXT
);

-- 6. CREATE INDEXES FOR RELATIONSHIPS (to ensure fast joins and explorer performance)
CREATE INDEX idx_raw_gb_sct_billstages_bill ON raw_gb_sct_billstages(bill_id);
CREATE INDEX idx_raw_gb_sct_memberparties_person ON raw_gb_sct_memberparties(person_id);
CREATE INDEX idx_raw_gb_sct_personcommitteeroles_person ON raw_gb_sct_personcommitteeroles(person_id);
CREATE INDEX idx_raw_gb_sct_personcommitteeroles_committee ON raw_gb_sct_personcommitteeroles(committee_id);
