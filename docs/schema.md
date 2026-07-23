# Core Platform Database & Schema Specification

**Comparative Legislative Data Platform**  
**Version:** 2.7.0  
**Specification:** PostgreSQL DDL & Pydantic v2 Multi-Entity Architecture

---

## 1. Relational Schema Architecture (PostgreSQL DDL)

The database schema models 4 core entities:
1. `canonical_bills` (Macro legislative journey, timelines, stage milestones, accompanying documents)
2. `canonical_amendments` (Micro amendment records, Marshalled List numbers, text alterations, government stances)
3. `committee_memberships` (Temporal MSP committee assignments, Convener/Deputy Convener roles, active date bounds)
4. `parsed_proceedings` (Hansard Official Report debate transcripts, speech interventions, word count shares)

```sql
-- Core Entity 1: Canonical Bills
CREATE TABLE canonical_bills (
    canonical_id VARCHAR(64) PRIMARY KEY,
    jurisdiction_code VARCHAR(16) NOT NULL,
    local_bill_id VARCHAR(64) NOT NULL,
    title_canonical TEXT NOT NULL,
    parliament_term VARCHAR(32) NOT NULL,
    initiator_type VARCHAR(32) NOT NULL,
    initiator_party_governance_role VARCHAR(32) NOT NULL,
    initiator_member_id VARCHAR(64),
    ministerial_portfolio_title TEXT,
    initiator_organisation_name TEXT,
    third_party_organisation TEXT,
    
    date_introduced DATE NOT NULL,
    date_final_outcome DATE,
    duration_calendar_days INT,
    duration_sitting_days INT,
    
    stage_milestones JSONB NOT NULL DEFAULT '[]',
    
    financial_resolution_required_flag BOOLEAN NOT NULL DEFAULT FALSE,
    financial_resolution_approved_flag BOOLEAN DEFAULT FALSE,
    financial_resolution_vote_date DATE,
    financial_resolution_aye_count INT,
    financial_resolution_no_count INT,
    financial_resolution_abstain_count INT,
    
    emergency_procedure_flag BOOLEAN NOT NULL DEFAULT FALSE,
    section_35_order_triggered_flag BOOLEAN NOT NULL DEFAULT FALSE,
    
    doc_as_introduced_url TEXT,
    doc_as_passed_url TEXT,
    policy_memorandum_url TEXT,
    financial_memorandum_url TEXT,
    explanatory_notes_url TEXT,
    delegated_powers_memorandum_url TEXT,
    stage_1_lead_committee_report_url TEXT,
    
    word_count_introduced INT,
    word_count_post_committee INT,
    word_count_enacted INT,
    text_expansion_ratio FLOAT,
    
    final_status VARCHAR(32) NOT NULL,
    termination_mechanism VARCHAR(32) NOT NULL,
    
    amendments_tabled_count INT DEFAULT 0,
    amendments_agreed_count INT DEFAULT 0,
    amendments_non_executive_count INT DEFAULT 0,
    committee_amendments_executive_acceptance_rate FLOAT,
    bill_text_alteration_score FLOAT,
    
    payload_native JSONB NOT NULL DEFAULT '{}',
    provenance_hash VARCHAR(64) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Core Entity 2: Canonical Amendments
CREATE TABLE canonical_amendments (
    canonical_amendment_id VARCHAR(64) PRIMARY KEY,
    bill_id VARCHAR(64) NOT NULL REFERENCES canonical_bills(canonical_id) ON DELETE CASCADE,
    jurisdiction_code VARCHAR(16) NOT NULL,
    local_amendment_number VARCHAR(32) NOT NULL,
    marshalled_list_url TEXT,
    
    stage_canonical VARCHAR(32) NOT NULL,
    stage_raw TEXT NOT NULL,
    committee_name TEXT,
    committee_type VARCHAR(32),
    
    date_tabled DATE NOT NULL,
    date_decided DATE,
    
    sponsor_member_id VARCHAR(64),
    sponsor_name VARCHAR(128) NOT NULL,
    sponsor_party_on_tabling_date VARCHAR(64),
    sponsor_party_leadership_role TEXT,
    sponsor_governance_role VARCHAR(32) NOT NULL,
    co_sponsors_count INT DEFAULT 0,
    
    target_clause_or_schedule TEXT,
    amendment_action_type VARCHAR(32) NOT NULL,
    government_position VARCHAR(32) NOT NULL,
    disposition_canonical VARCHAR(32) NOT NULL,
    decision_mechanism VARCHAR(32) NOT NULL,
    
    division_id VARCHAR(64),
    aye_count INT,
    no_count INT,
    abstain_count INT,
    party_dissent_rate_on_amendment FLOAT,
    
    payload_native JSONB NOT NULL DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Core Entity 3: Committee Memberships & Convener Roles
CREATE TABLE committee_memberships (
    membership_id SERIAL PRIMARY KEY,
    jurisdiction_code VARCHAR(16) NOT NULL,
    committee_id INT NOT NULL,
    committee_name VARCHAR(256) NOT NULL,
    committee_type VARCHAR(32) NOT NULL,
    person_id INT NOT NULL,
    member_name VARCHAR(128) NOT NULL,
    committee_role VARCHAR(32) NOT NULL, -- Convener, Deputy Convener, Member
    valid_from_date DATE NOT NULL,
    valid_until_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Core Entity 4: Parsed Official Report Proceedings
CREATE TABLE parsed_proceedings (
    proceedings_id SERIAL PRIMARY KEY,
    bill_id VARCHAR(64) NOT NULL REFERENCES canonical_bills(canonical_id) ON DELETE CASCADE,
    official_report_proceedings_url TEXT NOT NULL,
    proceedings_total_word_count INT NOT NULL,
    proceedings_interventions_count INT NOT NULL,
    proceedings_msps_speaking_count INT NOT NULL,
    executive_ministers_word_count_share FLOAT NOT NULL,
    backbench_msps_word_count_share FLOAT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```
