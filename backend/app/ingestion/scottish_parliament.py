import hashlib
import json
from datetime import datetime, date
from typing import List, Dict, Any, Optional
import httpx

from app.core.provenance import Provenance
from app.models.bill import (
    Bill, NormalizedBill, NativeBill, StageMilestone, StageCanonical,
    InitiatorType, FinalStatus, TerminationMechanism, DerivationConfidence, ChamberType
)

HOLYROOD_BASE_URL = "https://data.parliament.scot/api"

class ScottishParliamentIngestor:
    def __init__(self, timeout: float = 15.0):
        self.timeout = timeout
        self.client = httpx.Client(timeout=timeout, follow_redirects=True)
        self.bill_types: Dict[int, str] = {}
        self.stage_types: Dict[int, str] = {}
        self.members: Dict[int, str] = {}

    def load_lookups(self):
        """Fetch lookup tables from Holyrood API."""
        # Bill Types
        resp_bt = self.client.get(f"{HOLYROOD_BASE_URL}/billtypes")
        if resp_bt.is_success:
            for item in resp_bt.json():
                if "ID" in item:
                    self.bill_types[item["ID"]] = item.get("Name", f"Type #{item['ID']}")

        # Stage Types
        resp_st = self.client.get(f"{HOLYROOD_BASE_URL}/billstagetypes")
        if resp_st.is_success:
            for item in resp_st.json():
                if "ID" in item:
                    self.stage_types[item["ID"]] = item.get("Name", f"Stage #{item['ID']}")

        # Members
        resp_m = self.client.get(f"{HOLYROOD_BASE_URL}/members")
        if resp_m.is_success:
            for item in resp_m.json():
                pid = item.get("PersonID") or item.get("ID")
                name = item.get("ParliamentaryName") or item.get("Name") or f"Member #{pid}"
                if pid:
                    self.members[pid] = name

    def fetch_all(self) -> List[Bill]:
        """Fetch all bills and filter for the 2019-2024 cohort."""
        self.load_lookups()
        
        resp_bills = self.client.get(f"{HOLYROOD_BASE_URL}/bills")
        resp_stages = self.client.get(f"{HOLYROOD_BASE_URL}/billstages")
        
        if not resp_bills.is_success or not resp_stages.is_success:
            raise RuntimeError(f"Failed to fetch Holyrood API data: {resp_bills.status_code} / {resp_stages.status_code}")

        raw_bills = resp_bills.json()
        raw_stages = resp_stages.json()

        # Group stages by BillID
        stages_by_bill: Dict[int, List[Dict[str, Any]]] = {}
        for s in raw_stages:
            bid = s.get("BillID")
            if bid:
                if bid not in stages_by_bill:
                    stages_by_bill[bid] = []
                stages_by_bill[bid].append(s)

        canonical_bills: List[Bill] = []

        for b in raw_bills:
            bill_id = b["ID"]
            b_stages = sorted(stages_by_bill.get(bill_id, []), key=lambda x: x.get("StageDate") or "")
            
            # Determine dates
            intro_date = None
            final_date = None
            if b_stages:
                for stg in b_stages:
                    if stg.get("StageDate") and not intro_date:
                        try:
                            intro_date = date.fromisoformat(stg["StageDate"].split("T")[0])
                        except Exception:
                            pass
                    if stg.get("StageDate"):
                        try:
                            final_date = date.fromisoformat(stg["StageDate"].split("T")[0])
                        except Exception:
                            pass

            # Filter for 2019–2024 cohort boundary
            if intro_date:
                if intro_date.year < 2019 or intro_date.year > 2024:
                    continue
            elif final_date:
                if final_date.year < 2019 or final_date.year > 2024:
                    continue
            else:
                continue

            canonical_bill = self.parse_single_bill(b, b_stages, intro_date, final_date)
            if canonical_bill:
                canonical_bills.append(canonical_bill)

        return canonical_bills

    def parse_single_bill(
        self,
        b: Dict[str, Any],
        b_stages: List[Dict[str, Any]],
        intro_date: Optional[date],
        final_date: Optional[date]
    ) -> Optional[Bill]:
        bill_id = b["ID"]
        ref = b.get("Reference") or f"SP Bill {bill_id}"
        short_name = b.get("ShortName") or b.get("FullName") or f"Bill {bill_id}"
        
        # Calculate SHA-256 hash of raw JSON payload
        raw_json_str = json.dumps({"bill": b, "stages": b_stages}, sort_keys=True)
        raw_hash = hashlib.sha256(raw_json_str.encode("utf-8")).hexdigest()

        # Determine Initiator Type
        type_id = b.get("BillTypeID")
        type_name = self.bill_types.get(type_id, "Executive")
        if "Member" in type_name:
            initiator_type = InitiatorType.INDIVIDUAL_MEMBER
        elif "Private" in type_name:
            initiator_type = InitiatorType.INDIVIDUAL_MEMBER
        elif "Committee" in type_name:
            initiator_type = InitiatorType.COMMITTEE
        else:
            initiator_type = InitiatorType.EXECUTIVE

        # Map Stages to Milestone Models
        stage_milestones: List[StageMilestone] = []
        has_passed_final_stage = False

        for idx, s in enumerate(b_stages):
            st_id = s.get("BillStageTypeID")
            st_name = self.stage_types.get(st_id, f"Stage #{st_id}")
            st_date = date(2019, 1, 1)
            if s.get("StageDate"):
                try:
                    st_date = date.fromisoformat(s["StageDate"].split("T")[0])
                except Exception:
                    pass

            if "Stage 3" in st_name or "Final Stage" in st_name:
                has_passed_final_stage = True
                canonical_stage = StageCanonical.FINAL_PASSAGE
            elif "Stage 1" in st_name or "Introduced" in st_name:
                canonical_stage = StageCanonical.FIRST_READING
            elif "Stage 2" in st_name or "Committee" in st_name or "Consideration" in st_name:
                canonical_stage = StageCanonical.COMMITTEE_STAGE
            else:
                canonical_stage = StageCanonical.FIRST_READING

            stage_milestones.append(
                StageMilestone(
                    stage_canonical=canonical_stage,
                    stage_raw=st_name,
                    chamber=ChamberType.DEVOLVED_UNICAMERAL,
                    date_stage=st_date,
                    proceedings_url=f"https://www.parliament.scot/bills-and-laws/bills/{bill_id}"
                )
            )

        # Final Status & Duration
        # Holyrood Stage 3 / Final Stage completion = Passed / Enacted
        if has_passed_final_stage:
            final_status = FinalStatus.ENACTED
            term_mechanism = TerminationMechanism.ENACTMENT
        else:
            final_status = FinalStatus.PENDING
            term_mechanism = TerminationMechanism.PENDING

        duration_cal = None
        if intro_date and final_date:
            duration_cal = (final_date - intro_date).days

        # Session mapping (e.g. 2021+ is Session 6)
        parliament_term = "Session 6" if (intro_date and intro_date >= date(2021, 5, 13)) else "Session 5"

        # Sponsor Person
        person_id = b.get("PersonID")
        person_name = self.members.get(person_id, f"Sponsor #{person_id}") if person_id else "Scottish Government"

        normalized = NormalizedBill(
            title=short_name,
            parliament_term=parliament_term,
            session_subperiod=parliament_term,
            session_start_date=date(2021, 5, 13) if parliament_term == "Session 6" else date(2016, 5, 12),
            session_end_date=date(2026, 5, 7) if parliament_term == "Session 6" else date(2021, 5, 12),
            initiator_type=initiator_type,
            date_introduced=intro_date or date(2019, 1, 1),
            date_final_outcome=final_date,
            duration_calendar_days=duration_cal,
            duration_sitting_days=None,
            suspension_interrupted=False,
            final_status=final_status,
            termination_mechanism=term_mechanism,
            rebellions_flag=False,
            cross_party_sponsorship_count=0,
            derivation_confidence=DerivationConfidence.HIGH,
            stage_milestones=stage_milestones
        )

        native = NativeBill(
            local_bill_id=ref,
            title_native=b.get("FullName") or short_name,
            initiator_raw=type_name,
            initiator_name=person_name,
            initiator_member_id=str(person_id) if person_id else None,
            initiator_party=None,
            raw_status="Passed (Stage 3)" if has_passed_final_stage else "In Progress",
            parliament_term_raw=parliament_term,
            official_proceedings_url=f"https://www.parliament.scot/bills-and-laws/bills/{bill_id}",
            official_publication_ref=ref
        )

        provenance = Provenance(
            source_url=f"https://data.parliament.scot/api/bills/{bill_id}",
            retrieved_at=datetime.utcnow(),
            raw_payload_hash=raw_hash,
            scraper_version="0.2.0-gb-sct",
            license="Open Government Licence v3.0"
        )

        clean_ref = ref.replace(" ", "_").replace("/", "_")
        return Bill(
            canonical_id=f"GB-SCT-{parliament_term.replace(' ', '')}-{clean_ref}",
            jurisdiction_code="GB-SCT",
            normalized=normalized,
            native=native,
            provenance=provenance,
            raw_payload={"bill": b, "stages": b_stages}
        )
