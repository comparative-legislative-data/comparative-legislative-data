# Canonical Legislative Data Schema Specification

**Comparative Legislative Data Platform**  
*Version 2.0.0 (North Star Reset)*

---

## 1. Overview & Architectural Principles

This document specifies the **Pydantic v2 Canonical Data Schema** for the Comparative Legislative Data Platform. The schema models all legislative data ingested, mirrored, and served by the platform across 8 Quantitative Research Domains established in the [Master Canonical Variable Catalog](file:///home/steven/Documents/github/comparativelegislativedata/docs/canonical_variable_catalog.md).

### The 5-Tier Data Availability & Provenance Framework

Every field in the canonical bill record is assigned a provenance classification evaluating host API availability:

- **`NATIVE_DIRECT`:** Available directly in the host assembly's official API or raw feed (JSON/XML).
- **`DERIVED_DETERMINISTIC`:** Derived deterministically via pipeline joins, date arithmetic, or lookup tables (e.g. Executive Rosters). Includes an explicit `derivation_confidence` rating (`HIGH`, `MEDIUM`, `LOW`).
- **`DERIVED_SYNTHETIC_AI`:** Synthesized using advanced NLP/LLM text processing, topic modeling, or structural parsing of unstructured Hansard/PDF text.
- **`UNAVAILABLE_HARD_GAP`:** Missing natively from the host assembly, unrecorded, or resource-prohibitive to generate (Documented Open Data Gap).

---

## 2. Core Enum Definitions

```python
from enum import Enum

class InitiatorType(str, Enum):
    """Globally neutral classification of the originating sponsor/author."""
    EXECUTIVE = "EXECUTIVE"
    INDIVIDUAL_MEMBER = "INDIVIDUAL_MEMBER"
    GROUP_MEMBERS = "GROUP_MEMBERS"
    COMMITTEE = "COMMITTEE"
    CITIZEN_INITIATIVE = "CITIZEN_INITIATIVE"
    PRIVATE_HYBRID = "PRIVATE_HYBRID"
    OTHER = "OTHER"

class InitiatorGovernanceRole(str, Enum):
    """Alignment of the primary sponsor relative to executive power at introduction."""
    GOVERNING_PARTY = "GOVERNING_PARTY"
    OPPOSITION_PARTY = "OPPOSITION_PARTY"
    CROSS_PARTY = "CROSS_PARTY"
    NON_PARTISAN = "NON_PARTISAN"
    COMMITTEE_PROPOSED = "COMMITTEE_PROPOSED"
    UNKNOWN = "UNKNOWN"

class FinalStatus(str, Enum):
    """Standardized terminal disposition or pending status of the legislation."""
    ENACTED = "ENACTED"
    DEFEATED = "DEFEATED"
    WITHDRAWN = "WITHDRAWN"
    LAPSED = "LAPSED"
    PENDING = "PENDING"

class TerminationMechanism(str, Enum):
    """Specific procedural mechanism resulting in bill termination or enactment."""
    ENACTMENT = "ENACTMENT"
    EXECUTIVE_WITHDRAWAL = "EXECUTIVE_WITHDRAWAL"
    VOTE_DEFEAT = "VOTE_DEFEAT"
    SESSION_EXPIRY = "SESSION_EXPIRY"
    SECTION_35_VETO = "SECTION_35_VETO"
    SUSPENSION_TERMINATION = "SUSPENSION_TERMINATION"
    PENDING = "PENDING"

class StageCanonical(str, Enum):
    """Globally neutral stage milestones in parliamentary proceedings."""
    FIRST_READING = "FIRST_READING"
    SECOND_READING = "SECOND_READING"
    COMMITTEE_STAGE = "COMMITTEE_STAGE"
    REPORT_STAGE = "REPORT_STAGE"
    THIRD_READING = "THIRD_READING"
    SECOND_CHAMBER_REVIEW = "SECOND_CHAMBER_REVIEW"
    CONCILIATION = "CONCILIATION"
    FINAL_PASSAGE = "FINAL_PASSAGE"
    PROMULGATION = "PROMULGATION"

class ProvenanceTier(str, Enum):
    """5-Tier Data Availability & Provenance Classification."""
    NATIVE_DIRECT = "NATIVE_DIRECT"
    DERIVED_DETERMINISTIC = "DERIVED_DETERMINISTIC"
    DERIVED_SYNTHETIC_AI = "DERIVED_SYNTHETIC_AI"
    UNAVAILABLE_HARD_GAP = "UNAVAILABLE_HARD_GAP"

class DerivationConfidence(str, Enum):
    """Confidence level of pipeline-derived fields."""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
```

---

## 3. Pydantic Model Hierarchy

### A. Stage Milestone Model
```python
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

class StageMilestone(BaseModel):
    stage_canonical: StageCanonical = Field(..., description="Standardized stage milestone")
    stage_raw: str = Field(..., description="Native stage name from host feed")
    chamber: str = Field(default="PRIMARY_CHAMBER", description="Chamber where stage occurred")
    date_stage: date = Field(..., description="Date stage was completed")
    proceedings_url: Optional[str] = Field(None, description="URL to official Hansard/Journal transcript")
    seq_order: int = Field(..., description="Sequential order in bill progression (1-indexed)")
```

### B. Sponsor Information Model
```python
class SponsorInfo(BaseModel):
    member_name: str = Field(..., description="Name string of the sponsor/minister")
    member_id: Optional[str] = Field(None, description="Persistent member ID (Wikidata QID / native ID)")
    party: Optional[str] = Field(None, description="Political party affiliation")
    is_primary: bool = Field(default=True, description="True if primary sponsor, False if co-sponsor")
```

### C. Division Record Model
```python
class DivisionRecord(BaseModel):
    division_id: str = Field(..., description="Local division/roll-call vote identifier")
    stage_raw: str = Field(..., description="Stage where division vote occurred")
    date_division: date = Field(..., description="Date of division vote")
    yeas_count: int = Field(..., description="Total Yea / For votes")
    nays_count: int = Field(..., description="Total Nay / Against votes")
    abstentions_count: int = Field(default=0, description="Total Abstentions / Present")
    passed_flag: bool = Field(..., description="True if division motion carried")
    rebellions_flag: bool = Field(default=False, description="True if >=5% party defiance occurred")
```

### D. Normalized Bill Model
```python
class NormalizedBill(BaseModel):
    title: str = Field(..., description="Primary title in English (Domain 2)")
    parliament_term: str = Field(..., description="Macro electoral period, e.g. Session 6 (Domain 1)")
    session_subperiod: Optional[str] = Field(None, description="Sessional sub-period (Domain 1)")
    session_start_date: Optional[date] = Field(None, description="Opening date of session (Domain 1)")
    session_end_date: Optional[date] = Field(None, description="Dissolution date of session (Domain 1)")
    
    # Origin & Sponsorship (Domain 2)
    initiator_type: InitiatorType = Field(..., description="Standardized sponsor classification")
    initiator_party_governance_role: InitiatorGovernanceRole = Field(
        default=InitiatorGovernanceRole.UNKNOWN,
        description="Sponsor alignment relative to executive"
    )
    co_sponsorship_count: int = Field(default=0, description="Total co-sponsors attached")
    cross_party_sponsorship_count: int = Field(default=0, description="Opposition co-sponsors attached")
    
    # Timelines (Domain 3)
    date_introduced: date = Field(..., description="Introduction date")
    date_final_outcome: Optional[date] = Field(None, description="Final outcome date")
    duration_calendar_days: Optional[int] = Field(None, description="Elapsed calendar days")
    duration_sitting_days: Optional[int] = Field(None, description="Elapsed sitting days")
    suspension_interrupted_flag: bool = Field(default=False, description="Spanned parliamentary recess")
    stage_milestones: List[StageMilestone] = Field(default_factory=list, description="Stage timeline array")
    
    # Final Disposition (Domain 4)
    final_status: FinalStatus = Field(..., description="Terminal status")
    termination_mechanism: TerminationMechanism = Field(default=TerminationMechanism.PENDING)
    royal_assent_date: Optional[date] = Field(None, description="Royal assent date")
    
    # Documents Chain (Domain 5)
    doc_as_introduced_url: Optional[str] = Field(None)
    doc_as_passed_url: Optional[str] = Field(None)
    doc_policy_memorandum_url: Optional[str] = Field(None)
    doc_financial_memorandum_url: Optional[str] = Field(None)
    doc_explanatory_notes_url: Optional[str] = Field(None)
    doc_marshalled_amendments_urls: List[str] = Field(default_factory=list)
    
    # Committee Proceedings (Domain 6)
    lead_committee_name: Optional[str] = Field(None)
    committee_referral_date: Optional[date] = Field(None)
    committee_report_date: Optional[date] = Field(None)
    committee_report_url: Optional[str] = Field(None)
    committee_evidence_submissions_count: Optional[int] = Field(None)
    
    # Amendments (Domain 7)
    amendments_tabled_count: Optional[int] = Field(None)
    amendments_agreed_count: Optional[int] = Field(None)
    amendments_rejected_count: Optional[int] = Field(None)
    amendments_executive_count: Optional[int] = Field(None)
    amendments_backbench_count: Optional[int] = Field(None)
    bill_text_alteration_score: Optional[float] = Field(None)
    
    # Divisions & Hansard (Domain 8)
    divisions_count: Optional[int] = Field(None)
    division_records: List[DivisionRecord] = Field(default_factory=list)
    rebellions_flag: bool = Field(default=False)
    voting_coalition_type: Optional[str] = Field(None)
    hansard_debate_urls: List[str] = Field(default_factory=list)
    
    derivation_confidence: DerivationConfidence = Field(default=DerivationConfidence.HIGH)
```

### E. Root Canonical Bill Model
```python
from datetime import datetime
from app.core.provenance import Provenance

class Bill(BaseModel):
    canonical_id: str = Field(..., description="Global unique ID '[JURISDICTION]-[TERM]-[LOCAL_ID]'")
    jurisdiction_code: str = Field(..., description="ISO-style jurisdiction code (e.g. GB-SCT, GB-UKP)")
    normalized: NormalizedBill = Field(..., description="Harmonized 8-domain comparative record")
    native: dict = Field(default_factory=dict, description="Unmodified native host feed payload")
    provenance: Provenance = Field(..., description="Audit trail and SHA-256 provenance block")
```
