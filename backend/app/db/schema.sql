-- Comparative Legislative Data Platform
-- PostgreSQL Canonical & Audit Engine Schema (matching Option 3 Hybrid Architecture)

-- ============================================================================
-- 1. CANONICAL INGESTION TABLES
-- ============================================================================

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

CREATE TABLE IF NOT EXISTS sponsors (
    id BIGSERIAL PRIMARY KEY,
    canonical_id VARCHAR(128) NOT NULL REFERENCES bills(canonical_id) ON DELETE CASCADE,
    member_name VARCHAR(255) NOT NULL,
    member_id VARCHAR(128),
    party VARCHAR(128),
    is_primary BOOLEAN DEFAULT FALSE
);

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

-- ============================================================================
-- 2. OPERATIONAL AUDIT ENGINE TABLES (Option 3 Hybrid Model)
-- ============================================================================

CREATE TABLE IF NOT EXISTS assembly_audits (
    jurisdiction_code VARCHAR(32) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    chamber_type VARCHAR(64) NOT NULL,
    official_portal_url TEXT NOT NULL,
    license_type VARCHAR(128) NOT NULL,
    target_cohort VARCHAR(128) NOT NULL DEFAULT '2019-2024 BICD Cohort 1',
    schema_version VARCHAR(32) NOT NULL DEFAULT '1.0.0',
    last_synced_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS audit_endpoints (
    id BIGSERIAL PRIMARY KEY,
    jurisdiction_code VARCHAR(32) NOT NULL REFERENCES assembly_audits(jurisdiction_code) ON DELETE CASCADE,
    name VARCHAR(128) NOT NULL,
    url TEXT NOT NULL,
    http_method VARCHAR(16) NOT NULL DEFAULT 'GET',
    auth_required BOOLEAN DEFAULT FALSE,
    rate_limit_per_min INT,
    response_format VARCHAR(32) DEFAULT 'JSON',
    pagination_mechanism VARCHAR(128)
);

CREATE TABLE IF NOT EXISTS audit_field_mappings (
    id BIGSERIAL PRIMARY KEY,
    jurisdiction_code VARCHAR(32) NOT NULL REFERENCES assembly_audits(jurisdiction_code) ON DELETE CASCADE,
    canonical_field VARCHAR(128) NOT NULL,
    native_key TEXT NOT NULL,
    provenance_tier VARCHAR(32) NOT NULL,
    derivation_confidence VARCHAR(16) NOT NULL DEFAULT 'HIGH',
    notes TEXT
);

CREATE TABLE IF NOT EXISTS audit_probe_logs (
    id BIGSERIAL PRIMARY KEY,
    jurisdiction_code VARCHAR(32) NOT NULL REFERENCES assembly_audits(jurisdiction_code) ON DELETE CASCADE,
    endpoint_url TEXT NOT NULL,
    probed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    http_status_code INT NOT NULL,
    latency_ms INT NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'HEALTHY', -- HEALTHY, DRIFT_DETECTED, DOWN
    response_hash VARCHAR(64),
    error_summary TEXT
);

-- Indexes for performance & query speed
CREATE INDEX IF NOT EXISTS idx_bills_jurisdiction ON bills(jurisdiction_code);
CREATE INDEX IF NOT EXISTS idx_bills_term ON bills(parliament_term);
CREATE INDEX IF NOT EXISTS idx_stage_milestones_canonical ON stage_milestones(canonical_id);
CREATE INDEX IF NOT EXISTS idx_sponsors_canonical ON sponsors(canonical_id);
CREATE INDEX IF NOT EXISTS idx_provenance_canonical ON provenance_audit_log(canonical_id);

CREATE INDEX IF NOT EXISTS idx_audit_endpoints_jurisdiction ON audit_endpoints(jurisdiction_code);
CREATE INDEX IF NOT EXISTS idx_audit_field_mappings_jurisdiction ON audit_field_mappings(jurisdiction_code);
CREATE INDEX IF NOT EXISTS idx_audit_probe_logs_jurisdiction ON audit_probe_logs(jurisdiction_code);
CREATE INDEX IF NOT EXISTS idx_audit_probe_logs_probed_at ON audit_probe_logs(probed_at);
