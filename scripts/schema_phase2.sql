-- Comparative Legislative Data Phase 2: PostgreSQL Schema definitions for raw GB-SCT OData mirroring
-- Following ELT best practices, raw staging tables (Layer A) contain plain types and performance indexes,
-- but do not enforce strict foreign key constraints. This prevents ingestion failures due to upstream OData gaps
-- and enables resilient staged test runs.

-- 1. DROP EXISTING TABLES
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
    billtypeid INT,
    sequence INT
);

CREATE TABLE raw_gb_sct_parties (
    id INT PRIMARY KEY,
    abbreviation VARCHAR(50),
    actualname VARCHAR(255),
    preferredname VARCHAR(255),
    notes TEXT,
    validfromdate TIMESTAMP,
    validuntildate TIMESTAMP
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
    shortname VARCHAR(255),
    fullname TEXT,
    billtypeid INT,
    personid INT,
    thirdpartyorganisation TEXT
);

CREATE TABLE raw_gb_sct_billstages (
    id INT PRIMARY KEY,
    billid INT,
    billstagetypeid INT,
    stagedate TIMESTAMP
);

CREATE TABLE raw_gb_sct_members (
    personid INT PRIMARY KEY,
    photourl TEXT,
    notes TEXT,
    birthdate TIMESTAMP,
    birthdateisprotected BOOLEAN,
    parliamentaryname VARCHAR(255),
    preferredname VARCHAR(255),
    gendertypeid INT,
    iscurrent BOOLEAN
);

CREATE TABLE raw_gb_sct_memberparties (
    id INT PRIMARY KEY,
    personid INT,
    partyid INT,
    validfromdate TIMESTAMP,
    validuntildate TIMESTAMP
);

CREATE TABLE raw_gb_sct_committees (
    id INT PRIMARY KEY,
    shortname VARCHAR(100),
    name VARCHAR(255),
    description TEXT,
    committeeemailaddress VARCHAR(255),
    committeetelephone VARCHAR(100),
    validfromdate TIMESTAMP,
    validuntildate TIMESTAMP
);

CREATE TABLE raw_gb_sct_personcommitteeroles (
    id INT PRIMARY KEY,
    personid INT,
    committeeroleid INT,
    committeeid INT,
    validfromdate TIMESTAMP,
    validuntildate TIMESTAMP,
    notes TEXT
);

-- 4. CREATE COMPLEX TRANSACTIONAL TABLES
CREATE TABLE raw_gb_sct_motions (
    uniqueid INT PRIMARY KEY,
    eventid VARCHAR(100),
    eventtypeid INT,
    eventsubtypeid INT,
    mspid INT,
    party VARCHAR(100),
    regionid INT,
    constituencyid INT,
    approveddate TIMESTAMP,
    submissiondatetime TIMESTAMP,
    title VARCHAR(255),
    itemtext TEXT
);

CREATE TABLE raw_gb_sct_votes (
    id VARCHAR(100) PRIMARY KEY,
    detail JSONB NOT NULL,
    motion JSONB NOT NULL,
    person JSONB NOT NULL,
    time JSONB NOT NULL,
    updatedelasticdate TIMESTAMP
);

CREATE TABLE raw_gb_sct_plenary_reports (
    id VARCHAR(100) PRIMARY KEY,
    meeting JSONB NOT NULL,
    committee JSONB NOT NULL,
    time JSONB NOT NULL,
    itemofbusiness JSONB NOT NULL,
    person JSONB NOT NULL,
    detail JSONB NOT NULL,
    updatedelasticdate TIMESTAMP
);

CREATE TABLE raw_gb_sct_committee_reports (
    id VARCHAR(100) PRIMARY KEY,
    recordtype VARCHAR(100),
    subtype VARCHAR(100),
    meeting JSONB NOT NULL,
    committee JSONB NOT NULL,
    time JSONB NOT NULL,
    itemofbusiness JSONB NOT NULL,
    person JSONB NOT NULL,
    detail JSONB NOT NULL,
    location JSONB,
    updateddate TIMESTAMP,
    updatedelasticdate TIMESTAMP
);

-- 5. CREATE SYNC LOG TABLE
CREATE TABLE raw_gb_sct_sync_logs (
    id SERIAL PRIMARY KEY,
    sync_time TIMESTAMP DEFAULT NOW(),
    endpoint_name VARCHAR(100) NOT NULL,
    records_fetched INT,
    reconciliation_status VARCHAR(50),
    error_message TEXT
);

-- 6. CREATE INDEXES FOR RELATIONSHIPS (keeps analytical performance fast)
CREATE INDEX idx_raw_gb_sct_billstages_bill ON raw_gb_sct_billstages(billid);
CREATE INDEX idx_raw_gb_sct_memberparties_person ON raw_gb_sct_memberparties(personid);
CREATE INDEX idx_raw_gb_sct_personcommitteeroles_person ON raw_gb_sct_personcommitteeroles(personid);
CREATE INDEX idx_raw_gb_sct_personcommitteeroles_committee ON raw_gb_sct_personcommitteeroles(committeeid);
