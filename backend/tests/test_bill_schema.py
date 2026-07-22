"""
Unit tests for Pydantic Bill Schema and Provenance Utility
"""

from datetime import date, datetime, timezone
import pytest
from app.models.bill import (
    Bill,
    NormalizedBill,
    NativeBill,
    InitiatorType,
    InitiatorGovernanceRole,
    FinalStatus,
)
from app.core.provenance import generate_provenance, compute_sha256


def test_sha256_computation():
    payload = '{"test": "data"}'
    digest = compute_sha256(payload)
    assert digest.startswith("sha256:")
    assert len(digest) == 7 + 64


def test_bill_schema_serialization():
    raw_content = "<xml><bill>Test</bill></xml>"
    provenance = generate_provenance(
        source_url="https://www.parliament.scot/api/bills/5",
        raw_content=raw_content,
        scraper_version="0.1.0-gb-sct",
        license_name="Open Government Licence v3.0",
    )

    intro_date = date(2022, 3, 3)
    outcome_date = date(2022, 12, 22)
    duration = (outcome_date - intro_date).days

    bill = Bill(
        canonical_id="GB-SCT-S6-SPB13",
        jurisdiction_code="GB-SCT",
        normalized=NormalizedBill(
            title="Gender Recognition Reform (Scotland) Bill",
            parliament_term="Session 6",
            session_subperiod="Session 6",
            session_start_date=date(2021, 5, 13),
            session_end_date=date(2026, 5, 7),
            initiator_type=InitiatorType.EXECUTIVE,
            initiator_party_governance_role=InitiatorGovernanceRole.GOVERNING_PARTY,
            date_introduced=intro_date,
            date_final_outcome=outcome_date,
            duration_calendar_days=duration,
            final_status=FinalStatus.ENACTED,
        ),
        native=NativeBill(
            local_bill_id="SP Bill 13",
            title_native="Gender Recognition Reform (Scotland) Bill",
            initiator_raw="Cabinet Secretary for Social Justice",
            initiator_name="Shona Robison MSP",
            initiator_party="Scottish National Party",
            raw_status="Passed",
            parliament_term_raw="Session 6 (2021-2026)",
        ),
        provenance=provenance,
    )

    data = bill.model_dump()
    assert data["canonical_id"] == "GB-SCT-S6-SPB13"
    assert data["normalized"]["initiator_type"] == "EXECUTIVE"
    assert data["normalized"]["final_status"] == "ENACTED"
    assert data["normalized"]["duration_calendar_days"] == 294
    assert data["native"]["local_bill_id"] == "SP Bill 13"
    assert data["provenance"]["raw_payload_hash"].startswith("sha256:")
