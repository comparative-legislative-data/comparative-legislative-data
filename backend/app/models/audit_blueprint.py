from datetime import datetime
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, HttpUrl

ProvenanceTier = Literal["NATIVE_DIRECT", "ENRICHED_BY_PIPELINE", "UNAVAILABLE_GAP"]
DerivationConfidence = Literal["HIGH", "MEDIUM", "LOW", "NOT_APPLICABLE"]
ChamberType = Literal["SOVEREIGN_BICAMERAL", "DEVOLVED_UNICAMERAL", "DEVOLVED_ASSEMBLY", "CROWN_DEPENDENCY_BICAMERAL", "CROWN_DEPENDENCY_CONSENSUS", "OVERSEAS_TERRITORY"]

class AssemblyMetadata(BaseModel):
    jurisdiction_code: str = Field(..., description="ISO/BICD jurisdiction code (e.g. GB-UKP)")
    name: str = Field(..., description="Official assembly name")
    location: str = Field(..., description="Physical location / seat")
    chamber_type: ChamberType
    official_portal_url: str
    license_type: str = Field(..., description="e.g. Open Parliament Licence v3.0 / OGL v3.0")
    target_cohort: str = Field(default="2019-2024 BICD Cohort 1")

class EndpointSpec(BaseModel):
    name: str = Field(..., description="Endpoint identifier/name")
    url: str = Field(..., description="Target HTTP endpoint URL")
    http_method: str = Field(default="GET")
    auth_required: bool = Field(default=False)
    rate_limit_per_min: Optional[int] = Field(default=None, description="Requests per minute limit")
    response_format: str = Field(default="JSON", description="JSON, XML, HTML, PDF")
    pagination_mechanism: Optional[str] = Field(default=None, description="e.g. skip/take, page, cursor")

class FieldMapping(BaseModel):
    canonical_field: str = Field(..., description="Field in canonical Bill model (e.g. normalized.initiator_type)")
    native_key: str = Field(..., description="Native payload path or JSON pointer")
    provenance_tier: ProvenanceTier
    derivation_confidence: DerivationConfidence = Field(default="HIGH")
    notes: Optional[str] = Field(default=None, description="Mapping nuances or transformation logic")

class HansardSpec(BaseModel):
    transcript_format: str = Field(..., description="XML, HTML, PDF, API")
    speaker_disambiguation_method: str = Field(..., description="Member ID, Wikidata QID, Plain Text String")
    timestamp_granularity: str = Field(default="SPEECH_LEVEL", description="SPEECH_LEVEL, SITTING_LEVEL, NONE")
    interruption_flags_available: bool = Field(default=False)

class TypologyTestCase(BaseModel):
    bill_id: str = Field(..., description="Sample bill identifier")
    title: str = Field(..., description="Bill title")
    typology_category: str = Field(..., description="Government, Private Member, Fast-Track, Hybrid, Vetoed")
    expected_stages_count: int
    notes: Optional[str] = None

class AuditBlueprint(BaseModel):
    schema_version: str = Field(default="1.0.0")
    last_updated: str = Field(default_factory=lambda: datetime.utcnow().strftime("%Y-%m-%d"))
    assembly: AssemblyMetadata
    endpoints: List[EndpointSpec]
    field_mappings: List[FieldMapping]
    hansard: HansardSpec
    typology_tests: List[TypologyTestCase]
    procedural_notes: List[str] = Field(default_factory=list)
