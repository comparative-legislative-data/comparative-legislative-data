# Canonical Data Schema Specification

**Comparative Legislative Data Platform**  
*Pydantic v2 Canonical Models & Database Schema Standard*  
*Version 2.2.0 (7-Tier Provenance, Government Typologies & Temporal Decision-Point Specification)*

---

## 1. Overview & Data Model Principles

The **Canonical Data Schema** defines the core Pydantic v2 models and database relational structures for storing, querying, and auditing legislative data across global parliamentary and presidential assemblies.

### Key Schema Features
1. **7-Tier Data Availability & Provenance Tagging:** Every record and variable is explicitly assigned a provenance tier:
   - `CANONICAL_WISHLIST_TARGET`
   - `NATIVE_DIRECT`
   - `DERIVED_DETERMINISTIC`
   - `DERIVED_HUMAN_CODED` *(Manual expert/PhD hand-coding)*
   - `DERIVED_SYNTHETIC_AI` *(NLP/LLM text extraction)*
   - `LINKED_EXTERNAL_AUTHORITY` *(Linked from ParlGov, Wikidata, CAP, MARPOR)*
   - `UNAVAILABLE_HARD_GAP` *(Institutional data omission)*
2. **Temporal Decision-Point Member Affiliation Engine:** Evaluates politician party affiliation, party role, and floor seat shares at **every decision point** (bill introduction date, amendment tabling date, division vote date).
3. **AI Validation Lifecycle Metadata:** Tier 5 (`DERIVED_SYNTHETIC_AI`) data includes an explicit validation status: `UNVERIFIED_DRAFT`, `SAMPLE_VALIDATED`, `GOLD_BENCHMARKED`.
4. **Hard Gap Sub-Taxonomy:** Tier 7 (`UNAVAILABLE_HARD_GAP`) carries sub-reason codes: `NOT_RECORDED_BY_ASSEMBLY`, `RECORDED_BUT_UNDIGITIZED`, `RESTRICTED_ACCESS`, `COST_PROHIBITIVE`.

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
    LINKED_EXTERNAL_AUTHORITY = "LINKED_EXTERNAL_AUTHORITY"
    UNAVAILABLE_HARD_GAP = "UNAVAILABLE_HARD_GAP"

class GovernmentType(str, Enum):
    SINGLE_PARTY_MAJORITY = "SINGLE_PARTY_MAJORITY"
    SINGLE_PARTY_MINORITY = "SINGLE_PARTY_MINORITY"
    FORMAL_COALITION_MAJORITY = "FORMAL_COALITION_MAJORITY"
    FORMAL_COALITION_MINORITY = "FORMAL_COALITION_MINORITY"
    CONFIDENCE_AND_SUPPLY = "CONFIDENCE_AND_SUPPLY"
    COOPERATION_AGREEMENT = "COOPERATION_AGREEMENT"  # e.g. SNP/Greens Bute House Agreement
    CARETAKER_TECHNOCRATIC = "CARETAKER_TECHNOCRATIC"

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
    hard_gap_reason: Optional[HardGapReason] = Field(default=None, description="For Tier 7 UNAVAILABLE_HARD_GAP")
    linked_authority_source: Optional[str] = Field(default=None, description="ParlGov, Wikidata, CAP, MARPOR")
    source_feed: Optional[str] = Field(default=None, description="Raw feed, API endpoint, or paper source")
    citation: Optional[str] = Field(default=None, description="Academic paper or PhD dataset reference for Tier 4")

# --- TEMPORAL MEMBER AFFILIATION ENGINE MODEL ---

class MemberPartyAffiliation(BaseModel):
    member_id: str
    jurisdiction_code: str
    party_id: str
    party_name: str
    party_role: str = Field(default="OFFICIAL_PARTY_MEMBER", description="OFFICIAL_PARTY_MEMBER, INDEPENDENT, SPEAKER_NEUTRAL")
    valid_from: date
    valid_to: Optional[date] = None

# --- CORE CANONICAL BILL MODEL ---

class StageMilestone(BaseModel):
    stage_canonical: str
    stage_raw: str
    date_stage: date
    proceedings_url: Optional[HttpUrl] = None

class CanonicalBill(BaseModel):
    # Domain 1: Assembly & Executive Context
    jurisdiction_code: str = Field(..., example="GB-SCT")
    parliament_term: str = Field(..., example="Session 6")
    chamber_type: ChamberType
    government_type: GovernmentType
    parlgov_cabinet_id: Optional[str] = None
    
    # Domain 2: Bill Identity & Sponsorship
    local_bill_id: str = Field(..., example="SP Bill 13")
    title_canonical: str
    title_native: Optional[str] = None
    initiator_type: InitiatorType
    initiator_party_governance_role: PartyGovernanceRole  # Evaluated on date_introduced
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
    
    # Domain 5: Documentation Chain & External Linking
    doc_as_introduced_url: Optional[HttpUrl] = None
    doc_as_passed_url: Optional[HttpUrl] = None
    doc_policy_memorandum_url: Optional[HttpUrl] = None
    doc_financial_memorandum_url: Optional[HttpUrl] = None
    doc_explanatory_notes_url: Optional[HttpUrl] = None
    cap_topic_code: Optional[str] = None
    fiscal_impact_flag: Optional[bool] = None
    regulatory_impact_flag: Optional[bool] = None
    
    # Domain 6: Committee Proceedings
    lead_committee_name: Optional[str] = None
    committee_referral_date: Optional[date] = None
    committee_report_date: Optional[date] = None
    committee_evidence_submissions_count: int = 0
    committee_public_hearings_count: int = 0
    
    # Domain 7: Decision-Point Amendments & Alteration
    amendments_tabled_count: int = 0
    amendments_agreed_count: int = 0
    amendments_rejected_count: int = 0
    amendments_withdrawn_count: int = 0
    amendments_executive_count: int = 0  # Evaluated on tabling date
    amendments_non_executive_count: int = 0  # Evaluated on tabling date
    committee_amendments_tabled_count: int = 0
    committee_amendments_executive_acceptance_rate: Optional[float] = None
    bill_text_alteration_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    
    # Domain 8: Temporal Divisions & Coalitions
    divisions_count: int = 0
    effective_majority_margin_at_event_date: Optional[int] = None  # Evaluated on division date
    governing_seats_at_event_date: Optional[int] = None
    rebellions_flag: bool = False
    voting_coalition_type: VotingCoalitionType
    plenary_record_urls: List[HttpUrl] = []
    
    # Variable Provenance Map & Edge Case Flags
    variable_provenance_map: Dict[str, VariableProvenance] = Field(default_factory=dict)
    schema_review_required: bool = Field(default=False, description="Flagged for Edge-Case Schema Review")
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
    'LINKED_EXTERNAL_AUTHORITY',
    'UNAVAILABLE_HARD_GAP'
);

CREATE TYPE government_type_enum AS ENUM (
    'SINGLE_PARTY_MAJORITY',
    'SINGLE_PARTY_MINORITY',
    'FORMAL_COALITION_MAJORITY',
    'FORMAL_COALITION_MINORITY',
    'CONFIDENCE_AND_SUPPLY',
    'COOPERATION_AGREEMENT',
    'CARETAKER_TECHNOCRATIC'
);

-- Member Party Affiliation Timeline Table
CREATE TABLE member_party_affiliations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    member_id VARCHAR(64) NOT NULL,
    jurisdiction_code VARCHAR(32) NOT NULL,
    party_id VARCHAR(64) NOT NULL,
    party_role VARCHAR(32) NOT NULL DEFAULT 'OFFICIAL_PARTY_MEMBER',
    valid_from DATE NOT NULL,
    valid_to DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_member_affiliation_dates ON member_party_affiliations (member_id, valid_from, valid_to);

-- Canonical Bills Table
CREATE TABLE canonical_bills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    jurisdiction_code VARCHAR(32) NOT NULL,
    parliament_term VARCHAR(64) NOT NULL,
    local_bill_id VARCHAR(64) NOT NULL,
    title_canonical TEXT NOT NULL,
    title_native TEXT,
    initiator_type VARCHAR(32) NOT NULL,
    initiator_party_governance_role VARCHAR(32) NOT NULL,
    government_type government_type_enum NOT NULL,
    parlgov_cabinet_id VARCHAR(64),
    date_introduced DATE NOT NULL,
    date_final_outcome DATE,
    final_status VARCHAR(32) NOT NULL,
    head_of_state_promulgation_date DATE,
    bill_text_alteration_score NUMERIC(5, 4),
    voting_coalition_type VARCHAR(32) NOT NULL,
    schema_review_required BOOLEAN DEFAULT FALSE,
    payload JSONB NOT NULL,
    variable_provenance JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_jurisdiction_bill UNIQUE (jurisdiction_code, parliament_term, local_bill_id)
);
```
