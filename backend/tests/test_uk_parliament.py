"""
Unit tests for UK Parliament (GB-UKP) ingestion mapper
Updated with Peer Review Recommendations (v2.0)
"""

import pytest
from app.ingestion.uk_parliament import map_uk_bill_to_canonical
from app.models.bill import InitiatorType, InitiatorGovernanceRole, FinalStatus, TerminationMechanism, DerivationConfidence


def test_map_uk_bill_to_canonical_success():
    raw_payload = {
        "billId": 3156,
        "shortTitle": "Online Safety Act 2023",
        "isAct": True,
        "introducedDate": "2022-03-17T00:00:00Z",
        "actDate": "2023-10-26T00:00:00Z",
        "currentStatus": {
            "name": "Act of Parliament"
        },
        "billType": {
            "name": "Government Bill",
            "category": "Public"
        },
        "session": {
            "name": "2022-23",
            "startDate": "2022-05-10T00:00:00Z",
            "endDate": "2023-10-26T00:00:00Z"
        },
        "sponsors": [
            {
                "member": {
                    "memberId": 4532,
                    "name": "Nadine Dorries MP",
                    "party": "Conservative"
                }
            }
        ],
        "stages": [
            {
                "description": "1st reading",
                "house": "Commons",
                "stageDate": "2022-03-17T00:00:00Z",
                "hansardLink": "https://hansard.parliament.uk/commons/2022-03-17"
            },
            {
                "description": "Royal Assent",
                "house": "Lords",
                "stageDate": "2023-10-26T00:00:00Z",
                "hansardLink": "https://hansard.parliament.uk/lords/2023-10-26"
            }
        ]
    }

    source_url = "https://bills-api.parliament.uk/api/v1/Bills/3156"
    bill = map_uk_bill_to_canonical(raw_payload, source_url)

    assert bill is not None
    assert bill.canonical_id == "GB-UKP-P58-B3156"
    assert bill.jurisdiction_code == "GB-UKP"
    
    # Normalized fields
    assert bill.normalized.title == "Online Safety Act 2023"
    assert bill.normalized.initiator_type == InitiatorType.EXECUTIVE
    assert bill.normalized.initiator_party_governance_role == InitiatorGovernanceRole.GOVERNING_PARTY
    assert bill.normalized.final_status == FinalStatus.ENACTED
    assert bill.normalized.termination_mechanism == TerminationMechanism.ENACTMENT
    assert bill.normalized.derivation_confidence == DerivationConfidence.HIGH
    assert bill.normalized.duration_calendar_days == 588
    assert bill.normalized.duration_sitting_days > 0
    assert len(bill.normalized.stage_milestones) == 2
    assert bill.normalized.stage_milestones[0].proceedings_url == "https://hansard.parliament.uk/commons/2022-03-17"

    # Native fields
    assert bill.native.local_bill_id == "Bill 3156"
    assert bill.native.initiator_name == "Nadine Dorries MP"
    assert bill.native.initiator_member_id == "4532"
    assert bill.native.initiator_party == "Conservative"

    # Provenance fields
    assert bill.provenance.source_url == source_url
    assert bill.provenance.raw_payload_hash.startswith("sha256:")
    assert len(bill.provenance.raw_payload_hash.replace("sha256:", "")) == 64
