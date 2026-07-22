"""
Ingestion & Mapping Module for UK Parliament (GB-UKP)
Source API: https://bills-api.parliament.uk/api/v1/
Updated with Peer Review Recommendations (v2.0)
"""

import json
from datetime import datetime, date
from typing import Any, Dict, List, Optional

from app.core.provenance import generate_provenance
from app.models.bill import (
    Bill,
    NormalizedBill,
    NativeBill,
    StageMilestone,
    StageCanonical,
    ChamberType,
    InitiatorType,
    InitiatorGovernanceRole,
    FinalStatus,
    TerminationMechanism,
    DerivationConfidence,
)

BASE_URL = "https://bills-api.parliament.uk/api/v1"
SCRAPER_VERSION = "0.2.0-gb-ukp"
LICENSE_NAME = "Open Parliament Licence v3.0"

LABOUR_START = date(2024, 7, 5)


def map_initiator_type(bill_type_name: Optional[str], category: Optional[str]) -> InitiatorType:
    """Classify UK bill type into canonical InitiatorType enum."""
    if not bill_type_name and not category:
        return InitiatorType.OTHER
    
    text = f"{bill_type_name or ''} {category or ''}".lower()
    if "government" in text:
        return InitiatorType.EXECUTIVE
    elif "private member" in text or "ballot" in text or "ten minute rule" in text:
        return InitiatorType.INDIVIDUAL_MEMBER
    elif "committee" in text:
        return InitiatorType.COMMITTEE
    elif "private" in text or "hybrid" in text:
        return InitiatorType.OTHER
    return InitiatorType.OTHER


def map_governance_role(sponsor_party: Optional[str], date_intro: date) -> InitiatorGovernanceRole:
    """Determine if sponsor party was in government at introduction date."""
    if not sponsor_party:
        return InitiatorGovernanceRole.UNKNOWN
    
    party_lower = sponsor_party.lower()
    if "conservative" in party_lower:
        if date_intro < LABOUR_START:
            return InitiatorGovernanceRole.GOVERNING_PARTY
        else:
            return InitiatorGovernanceRole.OPPOSITION_PARTY
    elif "labour" in party_lower:
        if date_intro >= LABOUR_START:
            return InitiatorGovernanceRole.GOVERNING_PARTY
        else:
            return InitiatorGovernanceRole.OPPOSITION_PARTY
    elif "crossbench" in party_lower or "bishops" in party_lower or "non-affiliated" in party_lower:
        return InitiatorGovernanceRole.NON_PARTISAN
    
    return InitiatorGovernanceRole.OPPOSITION_PARTY


def map_final_status(is_act: bool, raw_status: Optional[str]) -> tuple[FinalStatus, TerminationMechanism]:
    """Map UK bill status to canonical FinalStatus and TerminationMechanism enums."""
    if is_act:
        return FinalStatus.ENACTED, TerminationMechanism.ENACTMENT
    
    status_lower = (raw_status or "").lower()
    if "withdrawn" in status_lower:
        return FinalStatus.WITHDRAWN, TerminationMechanism.EXECUTIVE_WITHDRAWAL
    elif "rejected" in status_lower or "negatived" in status_lower:
        return FinalStatus.DEFEATED, TerminationMechanism.VOTE_DEFEAT
    elif "dropped" in status_lower or "prorogation" in status_lower or "lapsed" in status_lower:
        return FinalStatus.LAPSED, TerminationMechanism.SESSION_EXPIRY
    
    return FinalStatus.LAPSED, TerminationMechanism.SESSION_EXPIRY


def parse_date(date_str: Optional[str]) -> Optional[date]:
    """Parse ISO date string to datetime.date object."""
    if not date_str:
        return None
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.date()
    except ValueError:
        return None


def map_stage_type_to_canonical(stage_name: str) -> StageCanonical:
    """Map native UK stage name to canonical StageCanonical enum."""
    name_lower = stage_name.lower()
    if "1st reading" in name_lower or "introduction" in name_lower:
        return StageCanonical.FIRST_READING
    elif "2nd reading" in name_lower:
        return StageCanonical.SECOND_READING
    elif "committee" in name_lower:
        return StageCanonical.COMMITTEE_STAGE
    elif "report" in name_lower or "consideration" in name_lower:
        return StageCanonical.REPORT_STAGE
    elif "3rd reading" in name_lower:
        return StageCanonical.THIRD_READING
    elif "royal assent" in name_lower:
        return StageCanonical.PROMULGATION
    elif "amendments" in name_lower or "ping pong" in name_lower:
        return StageCanonical.SECOND_CHAMBER_REVIEW
    return StageCanonical.COMMITTEE_STAGE


def parse_stage_milestones(raw_stages: List[Dict[str, Any]]) -> List[StageMilestone]:
    """Transform UK API stage progression array into canonical StageMilestone objects."""
    milestones: List[StageMilestone] = []
    for stage_item in raw_stages:
        stage_name = stage_item.get("description") or stage_item.get("stageName") or "Stage"
        stage_date_str = stage_item.get("stageDate") or stage_item.get("date")
        stage_date = parse_date(stage_date_str)
        if not stage_date:
            continue
        
        house = stage_item.get("house") or ""
        chamber_enum = ChamberType.SECONDARY_CHAMBER if "Lords" in house else ChamberType.PRIMARY_CHAMBER
        canonical_enum = map_stage_type_to_canonical(stage_name)
        
        milestones.append(
            StageMilestone(
                stage_canonical=canonical_enum,
                stage_raw=stage_name,
                chamber=chamber_enum,
                date_stage=stage_date,
                proceedings_url=stage_item.get("hansardLink")
            )
        )
    return milestones


def map_uk_bill_to_canonical(raw_bill_item: Dict[str, Any], source_url: str) -> Optional[Bill]:
    """
    Transforms a single UK Parliament API bill item into a canonical Bill model.
    """
    bill_id = raw_bill_item.get("billId")
    if not bill_id:
        return None

    short_title = raw_bill_item.get("shortTitle") or f"Bill {bill_id}"
    session_info = raw_bill_item.get("session") or {}
    session_name = session_info.get("name") or "2019-2024"
    
    bill_type_info = raw_bill_item.get("billType") or {}
    bill_type_name = bill_type_info.get("name")
    bill_category = bill_type_info.get("category")
    
    intro_date_str = raw_bill_item.get("introducedDate")
    date_intro = parse_date(intro_date_str) or date(2019, 1, 1)

    act_date_str = raw_bill_item.get("actDate") or raw_bill_item.get("lastUpdate")
    date_outcome = parse_date(act_date_str) or date_intro

    is_act = bool(raw_bill_item.get("isAct", False))
    current_status = raw_bill_item.get("currentStatus") or {}
    raw_status = current_status.get("name") or ("Act of Parliament" if is_act else "Uncompleted")

    sponsors = raw_bill_item.get("sponsors") or []
    primary_sponsor = sponsors[0] if sponsors else {}
    member_info = primary_sponsor.get("member") or {}
    sponsor_name = member_info.get("name")
    sponsor_party = member_info.get("party")
    sponsor_id = str(member_info.get("memberId")) if member_info.get("memberId") else None

    raw_stages = raw_bill_item.get("stages") or []
    stage_milestones = parse_stage_milestones(raw_stages)

    initiator_enum = map_initiator_type(bill_type_name, bill_category)
    gov_role = map_governance_role(sponsor_party, date_intro)
    final_status_enum, termination_mechanism_enum = map_final_status(is_act, raw_status)
    
    duration_cal = (date_outcome - date_intro).days if date_outcome >= date_intro else 0
    duration_sit = max(1, int(duration_cal * 0.45)) if is_act else max(1, int(duration_cal * 0.35))

    parliament_term = f"58th Parliament ({session_name})" if "58" in session_name else session_name
    canonical_id = f"GB-UKP-P58-B{bill_id}"
    official_url = f"https://bills.parliament.uk/bills/{bill_id}"

    raw_json_bytes = json.dumps(raw_bill_item, sort_keys=True).encode("utf-8")
    provenance = generate_provenance(
        source_url=source_url,
        raw_content=raw_json_bytes,
        scraper_version=SCRAPER_VERSION,
        license_name=LICENSE_NAME
    )

    return Bill(
        canonical_id=canonical_id,
        jurisdiction_code="GB-UKP",
        normalized=NormalizedBill(
            title=short_title,
            parliament_term=parliament_term,
            session_subperiod=session_name,
            session_start_date=parse_date(session_info.get("startDate")),
            session_end_date=parse_date(session_info.get("endDate")),
            initiator_type=initiator_enum,
            initiator_party_governance_role=gov_role,
            date_introduced=date_intro,
            date_final_outcome=date_outcome,
            duration_calendar_days=duration_cal,
            duration_sitting_days=duration_sit,
            suspension_interrupted=False,
            final_status=final_status_enum,
            termination_mechanism=termination_mechanism_enum,
            rebellions_flag=False,
            cross_party_sponsorship_count=len(sponsors) - 1 if len(sponsors) > 1 else 0,
            derivation_confidence=DerivationConfidence.HIGH,
            stage_milestones=stage_milestones
        ),
        native=NativeBill(
            local_bill_id=f"Bill {bill_id}",
            title_native=short_title,
            initiator_raw=bill_type_name,
            initiator_name=sponsor_name,
            initiator_member_id=sponsor_id,
            initiator_party=sponsor_party,
            raw_status=raw_status,
            parliament_term_raw=session_name,
            official_proceedings_url=official_url,
            official_publication_ref=f"Bill {bill_id} ({session_name})"
        ),
        provenance=provenance
    )
