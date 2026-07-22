import pytest
from datetime import date
from app.ingestion.scottish_parliament import ScottishParliamentIngestor
from app.models.bill import InitiatorType, FinalStatus, DerivationConfidence

def test_scottish_parliament_parse_single_bill():
    ingestor = ScottishParliamentIngestor()
    ingestor.bill_types = {1: "Executive", 2: "Member's", 3: "Budget"}
    ingestor.stage_types = {1: "Introduced", 2: "Stage 1", 3: "Stage 2", 4: "Stage 3", 5: "Royal Assent"}
    ingestor.members = {100: "Shona Robison MSP"}

    sample_bill = {
        "ID": 13,
        "Reference": "SP Bill 13",
        "ShortName": "Gender Recognition Reform (Scotland) Bill",
        "FullName": "Gender Recognition Reform (Scotland) Bill",
        "BillTypeID": 1,
        "PersonID": 100
    }

    sample_stages = [
        {"ID": 1, "BillID": 13, "BillStageTypeID": 1, "StageDate": "2022-03-03T00:00:00"},
        {"ID": 2, "BillID": 13, "BillStageTypeID": 2, "StageDate": "2022-10-06T00:00:00"},
        {"ID": 3, "BillID": 13, "BillStageTypeID": 4, "StageDate": "2022-12-22T00:00:00"},
        {"ID": 4, "BillID": 13, "BillStageTypeID": 5, "StageDate": "2023-01-15T00:00:00"}
    ]

    intro_date = date(2022, 3, 3)
    final_date = date(2023, 1, 15)

    bill = ingestor.parse_single_bill(sample_bill, sample_stages, intro_date, final_date)

    assert bill is not None
    assert bill.jurisdiction_code == "GB-SCT"
    assert bill.normalized.title == "Gender Recognition Reform (Scotland) Bill"
    assert bill.normalized.initiator_type == InitiatorType.EXECUTIVE
    assert bill.normalized.final_status == FinalStatus.ENACTED
    assert bill.normalized.duration_calendar_days == 318
    assert bill.provenance.raw_payload_hash is not None
    assert len(bill.normalized.stage_milestones) == 4
    assert bill.native.initiator_name == "Shona Robison MSP"
