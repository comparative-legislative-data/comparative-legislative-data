# Canonical Data Schema Specification

**Comparative Legislative Data Platform**  
*Pydantic v2 Canonical Models & Database Schema Standard*  
*Version 2.1.0 (6-Tier Provenance & AI Validation Lifecycle Specification)*

---

## 1. Overview & Data Model Principles

The **Canonical Data Schema** defines the core Pydantic v2 models and database relational structures for storing, querying, and auditing legislative data across global parliamentary and presidential assemblies.

### Key Schema Features
1. **6-Tier Data Availability & Provenance Tagging:** Every record and variable is explicitly assigned a provenance tier:
   - `CANONICAL_WISHLIST_TARGET`
   - `NATIVE_DIRECT`
   - `DERIVED_DETERMINISTIC`
   - `DERIVED_HUMAN_CODED` *(Manual expert/PhD hand-coding)*
   - `DERIVED_SYNTHETIC_AI` *(NLP/LLM text extraction)*
   - `UNAVAILABLE_HARD_GAP` *(Institutional data omission)*
2. **AI Validation Lifecycle Metadata:** Tier 5 (`DERIVED_SYNTHETIC_AI`) data includes an explicit validation status:
   - `UNVERIFIED_DRAFT` (Live exploratory data)
   - `SAMPLE_VALIDATED` (Audited on randomized human sample)
   - `GOLD_BENCHMARKED` (Benchmarked against Tier 4 ground truth)
3. **Hard Gap Sub-Taxonomy:** Tier 6 (`UNAVAILABLE_HARD_GAP`) carries sub-reason codes:
   - `NOT_RECORDED_BY_ASSEMBLY`
   - `RECORDED_BUT_UNDIGITIZED`
   - `RESTRICTED_ACCESS`
   - `COST_PROHIBITIVE`

---

## 2. Pydantic v2 Models Specification

```python
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl
from datetime import date, datetime

# --- ENUM DEFINITIONS ---

class ProvenanceTier(str, Enum):
    CANONICAL_WISHLIST_TARGET = "CANONICAL_WISHLIST_TARGET"
    NATIVE_DIRECT = "NATIVE_DIRECT"
    DERIVED_DETERMINISTIC = "DERIVED_DETERMINISTIC"
    DERIVED_HUMAN_CODED = "DERIVED_HUMAN_CODED"
    DERIVED_SYNTHETIC_AI = "DERIVED_SYNTHETIC_AI"
    UNAVAILABLE_HARD_GAP = "UNAVAILABLE_HARD_GAP"

class AIValidationStatus(str, Enum):
    UNVERIFIED_DRAFT = "UNVERIFIED_DRAFT"
    SAMPLE_VALIDATED = "SAMPLE_VALIDATED"
    GOLD_BENCHMARKED = "GOLD_BENCHMARKED"

class HardGapReason(str, Enum):
    NOT_RECORDED_BY_ASSEMBLY = "NOT_RECORDED_BY_ASSEMBLY"
    RECORDED_BUT_UNDIGITIZED = "RECORDED_BUT_UNDIGITIZED"
    RESTRICTED_ACCESS = "RESTRICTED_ACCESS"
    COST_PROHIBITIVE = "COST_PROHIBITIVE"

class ChamberType(str, Enum):
    SOVEREIGN_BICAMERAL = "SOVEREIGN_BICAMERAL"
    DEVOLVED_UNICAMERAL = "DEVOLVED_UNICAMERAL"
    FEDERAL_UPPER = "FEDERAL_UPPER"
    FEDERAL_LOWER = "FEDERAL_LOWER"
    CONCURRENT_ELECTED = "CONCURRENT_ELECTED"

class InitiatorType(str, Enum):
    EXECUTIVE = "EXECUTIVE"
    INDIVIDUAL_MEMBER = "INDIVIDUAL_MEMBER"
    GROUP_MEMBERS = "GROUP_MEMBERS"
    COMMITTEE = "COMMITTEE"
    PRIVATE_HYBRID = "PRIVATE_HYBRID"

class PartyGovernanceRole(str, Enum):
    GOVERNING_PARTY = "GOVERNING_PARTY"
    OPPOSITION_PARTY = "OPPOSITION_PARTY"
    CROSS_PARTY = "CROSS_PARTY"
    NON_PARTISAN = "NON_PARTISAN"

class FinalBillStatus(str, Enum):
    ENACTED = "ENACTED"
    DEFEATED = "DEFEATED"
    WITHDRAWN = "WITHDRAWN"
    LAPSED = "LAPSED"
    PENDING = "PENDING"
    VETOED = "VETOED"

class VotingCoalitionType(str, Enum):
    UNANIMOUS = "UNANIMOUS"
    GOVERNMENT_PARTY_LINE = "GOVERNMENT_PARTY_LINE"
    CROSS_PARTY_MAJORITY = "CROSS_PARTY_MAJORITY"
    MINORITY_PASSED = "MINORITY_PASSED"
    OPPOSITION_DEFEAT = "OPPOSITION_DEFEAT"

# --- PROVENANCE METADATA SUB-MODEL ---

class VariableProvenance(BaseModel):
    tier: ProvenanceTier
    confidence: str = Field(default="HIGH", description="HIGH, MEDIUM, or LOW")
    ai_validation_status: Optional[AIValidationStatus] = Field(default=None, description="For Tier 5 DERIVED_SYNTHETIC_AI")
    hard_gap_reason: Optional[HardGapReason] = Field(default=None, description="For Tier 6 UNAVAILABLE_HARD_GAP")
    source_feed: Optional[str] = Field(default=None, description="Raw feed, API endpoint, or paper source")
    citation: Optional[str] = Field(default=None, description="Academic paper or PhD dataset reference for Tier 4")

# --- CORE CANONICAL BILL MODEL ---

class StageMilestone(BaseModel):
    stage_canonical: str
    stage_raw: str
    date_stage: date
    proceedings_url: Optional[HttpUrl] = None

class CanonicalBill(BaseModel):
    # Domain 1: Assembly Context
    jurisdiction_code: str = Field(..., example="GB-SCT")
    parliament_term: str = Field(..., example="Session 6")
    chamber_type: ChamberType
    
    # Domain 2: Bill Identity & Sponsorship
    local_bill_id: str = Field(..., example="SP Bill 13")
    title_canonical: str
    title_native: Optional[str] = None
    initiator_type: InitiatorType
    initiator_party_governance_role: PartyGovernanceRole
    initiator_member_id: Optional[str] = None
    co_sponsorship_count: int = 0
    cross_party_sponsorship_count: int = 0
    
    # Domain 3: Procedural Progression & Control
    date_introduced: date
    date_final_outcome: Optional[date] = None
    duration_calendar_days: Optional[int] = None
    duration_sitting_days: Optional[int] = None
    term_interruption_flag: bool = False
    programme_motion_flag: bool = False
    guillotine_invoked_flag: bool = False
    debate_time_allocated_minutes: Optional[int] = None
    emergency_procedure_flag: bool = False
    stages_compressed_count: int = 0
    prior_executive_consent_required_flag: bool = False
    prior_executive_consent_granted_date: Optional[date] = None
    stage_milestones: List[StageMilestone] = []
    
    # Domain 4: Disposition & Inter-Chamber Mechanisms
    final_status: FinalBillStatus
    termination_mechanism: str
    head_of_state_promulgation_date: Optional[date] = None
    chamber_ping_pong_count: int = 0
    chamber_disagreement_flag: bool = False
    
    # Domain 5: Documentation Chain & Impact
    doc_as_introduced_url: Optional[HttpUrl] = None
    doc_as_passed_url: Optional[HttpUrl] = None
    doc_policy_memorandum_url: Optional[HttpUrl] = None
    doc_financial_memorandum_url: Optional[HttpUrl] = None
    doc_explanatory_notes_url: Optional[HttpUrl] = None
    fiscal_impact_flag: Optional[bool] = None
    regulatory_impact_flag: Optional[bool] = None
    
    # Domain 6: Committee Proceedings
    lead_committee_name: Optional[str] = None
    committee_referral_date: Optional[date] = None
    committee_report_date: Optional[date] = None
    committee_evidence_submissions_count: int = 0
    committee_public_hearings_count: int = 0
    
    # Domain 7: Amendments & Alteration
    amendments_tabled_count: int = 0
    amendments_agreed_count: int = 0
    amendments_rejected_count: int = 0
    amendments_withdrawn_count: int = 0
    amendments_executive_count: int = 0
    amendments_non_executive_count: int = 0
    committee_amendments_tabled_count: int = 0
    committee_amendments_executive_acceptance_rate: Optional[float] = None
    bill_text_alteration_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    
    # Domain 8: Divisions & Coalitions
    divisions_count: int = 0
    rebellions_flag: bool = False
    voting_coalition_type: VotingCoalitionType
    plenary_record_urls: List[HttpUrl] = []
    
    # Comprehensive Variable Provenance Map
    variable_provenance_map: Dict[str, VariableProvenance] = Field(
        default_factory=dict, 
        description="Explicit 6-tier provenance metadata key-value mapping per variable"
    )
```

---

## 3. PostgreSQL Database Schema DDL

```sql
CREATE TYPE provenance_tier_enum AS ENUM (
    'CANONICAL_WISHLIST_TARGET',
    'NATIVE_DIRECT',
    'DERIVED_DETERMINISTIC',
    'DERIVED_HUMAN_CODED',
    'DERIVED_SYNTHETIC_AI',
    'UNAVAILABLE_HARD_GAP'
);

CREATE TYPE ai_validation_status_enum AS ENUM (
    'UNVERIFIED_DRAFT',
    'SAMPLE_VALIDATED',
    'GOLD_BENCHMARKED'
);

CREATE TYPE hard_gap_reason_enum AS ENUM (
    'NOT_RECORDED_BY_ASSEMBLY',
    'RECORDED_BUT_UNDIGITIZED',
    'RESTRICTED_ACCESS',
    'COST_PROHIBITIVE'
);

CREATE TABLE canonical_bills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    jurisdiction_code VARCHAR(32) NOT NULL,
    parliament_term VARCHAR(64) NOT NULL,
    local_bill_id VARCHAR(64) NOT NULL,
    title_canonical TEXT NOT NULL,
    title_native TEXT,
    initiator_type VARCHAR(32) NOT NULL,
    initiator_party_governance_role VARCHAR(32) NOT NULL,
    date_introduced DATE NOT NULL,
    date_final_outcome DATE,
    final_status VARCHAR(32) NOT NULL,
    head_of_state_promulgation_date DATE,
    bill_text_alteration_score NUMERIC(5, 4),
    voting_coalition_type VARCHAR(32) NOT NULL,
    payload JSONB NOT NULL,
    variable_provenance JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_jurisdiction_bill UNIQUE (jurisdiction_code, parliament_term, local_bill_id)
);
```
