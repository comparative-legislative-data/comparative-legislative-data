"""
Pydantic Canonical Data Schema for Phase 1: Bill Quantitative Data & Proceedings
Updated with Peer Review Recommendations (v2.0)
Matches specification in docs/schema.md
"""

from datetime import date
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

from app.core.provenance import Provenance


class InitiatorType(str, Enum):
    """Globally neutral classification of the originating sponsor/author."""
    EXECUTIVE = "EXECUTIVE"
    INDIVIDUAL_MEMBER = "INDIVIDUAL_MEMBER"
    GROUP_MEMBERS = "GROUP_MEMBERS"
    COMMITTEE = "COMMITTEE"
    CITIZEN_INITIATIVE = "CITIZEN_INITIATIVE"
    OTHER = "OTHER"


class InitiatorGovernanceRole(str, Enum):
    """Alignment of the primary sponsor relative to the executive at introduction."""
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
    """Specific procedural mechanism causing bill termination or enactment."""
    ENACTMENT = "ENACTMENT"
    EXECUTIVE_WITHDRAWAL = "EXECUTIVE_WITHDRAWAL"
    AGENDA_DISPLACEMENT = "AGENDA_DISPLACEMENT"
    VOTE_DEFEAT = "VOTE_DEFEAT"
    SESSION_EXPIRY = "SESSION_EXPIRY"
    SUSPENSION_TERMINATION = "SUSPENSION_TERMINATION"
    PENDING = "PENDING"


class DerivationConfidence(str, Enum):
    """Confidence level of pipeline-derived fields."""
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


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


class ChamberType(str, Enum):
    """Chamber in which a procedural stage occurred."""
    PRIMARY_CHAMBER = "PRIMARY_CHAMBER"
    SECONDARY_CHAMBER = "SECONDARY_CHAMBER"
    JOINT_SESSION = "JOINT_SESSION"
    DEVOLVED_UNICAMERAL = "DEVOLVED_UNICAMERAL"


class StageMilestone(BaseModel):
    """
    Key procedural stage progression event in official parliamentary proceedings.
    """
    stage_canonical: StageCanonical = Field(..., description="Standardised stage category")
    stage_raw: str = Field(..., description="Native stage name (e.g. 'Public Bill Committee', 'Mark-up')")
    chamber: ChamberType = Field(default=ChamberType.PRIMARY_CHAMBER, description="Chamber where stage occurred")
    date_stage: date = Field(..., description="Date of stage event/completion")
    proceedings_url: Optional[str] = Field(None, description="Direct URL to official Hansard/Journal transcript for stage")


class NormalizedBill(BaseModel):
    """
    Standardised comparative layer for cross-national queries and statistical analysis.
    """
    title: str = Field(..., description="Primary title of the bill in English (or translated canonical title)")
    parliament_term: str = Field(..., description="Macro Electoral Term (e.g. '58th Parliament', 'Session 6', '118th Congress')")
    session_subperiod: Optional[str] = Field(None, description="Sessional sub-period if applicable (e.g. '2022-23', '1st Session')")
    session_start_date: Optional[date] = Field(None, description="Opening/start date of the parliamentary term or session")
    session_end_date: Optional[date] = Field(None, description="Prorogation/dissolution date of the term or session")
    initiator_type: InitiatorType = Field(..., description="Standardised sponsor classification")
    initiator_party_governance_role: InitiatorGovernanceRole = Field(
        default=InitiatorGovernanceRole.UNKNOWN,
        description="Sponsor's governance alignment at introduction"
    )
    date_introduced: date = Field(..., description="Formal submission / introduction date")
    date_final_outcome: Optional[date] = Field(None, description="Date of final disposition (or None if PENDING)")
    duration_calendar_days: Optional[int] = Field(None, description="Calculated days elapsed between introduction and final outcome")
    duration_sitting_days: Optional[int] = Field(None, description="Calculated actual sitting days elapsed excluding recesses")
    suspension_interrupted: bool = Field(default=False, description="Whether bill passage spanned a formal parliamentary suspension")
    final_status: FinalStatus = Field(..., description="Standardised outcome of the legislation")
    termination_mechanism: TerminationMechanism = Field(default=TerminationMechanism.PENDING, description="Procedural mechanism of termination")
    rebellions_flag: bool = Field(default=False, description="Whether bill experienced formal party rebellions/divisions")
    cross_party_sponsorship_count: int = Field(default=0, description="Number of cross-party co-sponsors")
    derivation_confidence: DerivationConfidence = Field(default=DerivationConfidence.HIGH, description="Confidence level of derived fields")
    stage_milestones: List[StageMilestone] = Field(default_factory=list, description="Procedural stage progression milestones")


class NativeBill(BaseModel):
    """
    Legislature-specific layer preserving raw local terminology and native fields for country specialists.
    """
    local_bill_id: str = Field(..., description="Local reference assigned by host legislature (e.g. 'Bill 102', 'SP Bill 13')")
    title_native: str = Field(..., description="Title in the official native language of the jurisdiction")
    initiator_raw: Optional[str] = Field(None, description="Unmodified raw sponsor/author string from host feed")
    initiator_name: Optional[str] = Field(None, description="Unmodified sponsor or member name string")
    initiator_member_id: Optional[str] = Field(None, description="Persistent disambiguated member ID (Wikidata QID / native ID)")
    initiator_party: Optional[str] = Field(None, description="Native political party affiliation string")
    raw_status: str = Field(..., description="Unmodified status string from host feed")
    parliament_term_raw: Optional[str] = Field(None, description="Native parliamentary term or session string")
    official_proceedings_url: Optional[str] = Field(None, description="Direct URL to official Hansard/Journal proceedings page")
    official_publication_ref: Optional[str] = Field(None, description="Native Hansard or Official Journal publication citation")


class Bill(BaseModel):
    """
    Root Canonical Bill Record combining Normalized, Native, and Provenance layers.
    """
    canonical_id: str = Field(..., description="Global unique ID '[JURISDICTION]-[TERM]-[LOCAL_ID]'")
    jurisdiction_code: str = Field(..., description="ISO-style jurisdiction code (e.g. 'GB-UKP', 'GB-SCT', 'US-FED', 'DE-BT')")
    normalized: NormalizedBill = Field(..., description="Harmonised comparative fields")
    native: NativeBill = Field(..., description="Legislature-specific raw detail")
    provenance: Provenance = Field(..., description="Audit trail and data provenance metadata")
