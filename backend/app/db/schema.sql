-- Comparative Legislative Data Platform
-- PostgreSQL Canonical Database Schema (matching docs/schema.md)

CREATE TABLE IF NOT EXISTS bills (
    canonical_id VARCHAR(128) PRIMARY KEY,
    jurisdiction_code VARCHAR(32) NOT NULL,
    
    -- Normalized Comparative Fields
    normalized_title TEXT NOT NULL,
    parliament_term VARCHAR(64) NOT NULL,
    session_subperiod VARCHAR(64),
    session_start_date DATE,
    session_end_date DATE,
    initiator_type VARCHAR(64) NOT NULL,
    initiator_party_governance_role VARCHAR(64),
    date_introduced DATE NOT NULL,
    date_final_outcome DATE,
    duration_calendar_days INT,
    duration_sitting_days INT,
    suspension_interrupted BOOLEAN DEFAULT FALSE,
    final_status VARCHAR(64) NOT NULL,
    termination_mechanism VARCHAR(64) NOT NULL,
    rebellions_flag BOOLEAN DEFAULT FALSE,
    cross_party_sponsorship_count INT DEFAULT 0,
    derivation_confidence VARCHAR(16) NOT NULL DEFAULT 'HIGH',
    
    -- Native Payload (Full raw JSON blob)
    native_payload JSONB NOT NULL,
    
    -- Timestamps
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Stage Milestones Table
CREATE TABLE IF NOT EXISTS stage_milestones (
    id BIGSERIAL PRIMARY KEY,
    canonical_id VARCHAR(128) NOT NULL REFERENCES bills(canonical_id) ON DELETE CASCADE,
    stage_canonical VARCHAR(64) NOT NULL,
    stage_raw VARCHAR(255) NOT NULL,
    chamber VARCHAR(64) NOT NULL,
    date_stage DATE,
    proceedings_url TEXT,
    seq_order INT NOT NULL
);

-- Sponsors & Initiators Table
CREATE TABLE IF NOT EXISTS sponsors (
    id BIGSERIAL PRIMARY KEY,
    canonical_id VARCHAR(128) NOT NULL REFERENCES bills(canonical_id) ON DELETE CASCADE,
    member_name VARCHAR(255) NOT NULL,
    member_id VARCHAR(128),
    party VARCHAR(128),
    is_primary BOOLEAN DEFAULT FALSE
);

-- Provenance Audit Log Table
CREATE TABLE IF NOT EXISTS provenance_audit_log (
    id BIGSERIAL PRIMARY KEY,
    canonical_id VARCHAR(128) NOT NULL REFERENCES bills(canonical_id) ON DELETE CASCADE,
    source_url TEXT NOT NULL,
    retrieved_at TIMESTAMPTZ NOT NULL,
    raw_payload_hash VARCHAR(64) NOT NULL,
    scraper_version VARCHAR(64) NOT NULL,
    zenodo_doi VARCHAR(128),
    license VARCHAR(128) NOT NULL DEFAULT 'Open Government Licence v3.0'
);

-- Indexes for high-speed queries
CREATE INDEX IF NOT EXISTS idx_bills_jurisdiction ON bills(jurisdiction_code);
CREATE INDEX IF NOT EXISTS idx_bills_term ON bills(parliament_term);
CREATE INDEX IF NOT EXISTS idx_bills_date_introduced ON bills(date_introduced);
CREATE INDEX IF NOT EXISTS idx_stage_milestones_canonical ON stage_milestones(canonical_id);
CREATE INDEX IF NOT EXISTS idx_sponsors_canonical ON sponsors(canonical_id);
CREATE INDEX IF NOT EXISTS idx_provenance_canonical ON provenance_audit_log(canonical_id);
