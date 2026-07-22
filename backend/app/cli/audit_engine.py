import argparse
import glob
import hashlib
import os
import sys
import time
from pathlib import Path
import yaml
import httpx
import psycopg

from app.models.audit_blueprint import AuditBlueprint
from app.ingestion.scottish_parliament import ScottishParliamentIngestor

# Database Connection Details
DB_HOST = os.environ.get("DB_HOST", "/var/run/postgresql")
DB_NAME = os.environ.get("DB_NAME", "comparative_legislative_data")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "")

def get_db_conn():
    conn_str = f"host={DB_HOST} dbname={DB_NAME} user={DB_USER}"
    if DB_PASS:
        conn_str += f" password={DB_PASS}"
    return psycopg.connect(conn_str)

def sync_audits(audits_dir: str):
    yaml_files = glob.glob(os.path.join(audits_dir, "*.yaml"))
    print(f"[*] Found {len(yaml_files)} audit definition file(s) in {audits_dir}")
    if not yaml_files:
        print(f"[!] No YAML files found in {audits_dir}. Check directory path.")
        return
    
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            for filepath in yaml_files:
                print(f"  --> Parsing {os.path.basename(filepath)}...")
                with open(filepath, "r", encoding="utf-8") as f:
                    raw_data = yaml.safe_load(f)
                
                # Validate against Pydantic schema
                blueprint = AuditBlueprint(**raw_data)
                asm = blueprint.assembly

                # Upsert top-level assembly audit record
                cur.execute("""
                    INSERT INTO assembly_audits (jurisdiction_code, name, location, chamber_type, official_portal_url, license_type, target_cohort, schema_version, last_synced_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
                    ON CONFLICT (jurisdiction_code) DO UPDATE SET
                        name = EXCLUDED.name,
                        location = EXCLUDED.location,
                        chamber_type = EXCLUDED.chamber_type,
                        official_portal_url = EXCLUDED.official_portal_url,
                        license_type = EXCLUDED.license_type,
                        target_cohort = EXCLUDED.target_cohort,
                        schema_version = EXCLUDED.schema_version,
                        last_synced_at = NOW();
                """, (asm.jurisdiction_code, asm.name, asm.location, asm.chamber_type, asm.official_portal_url, asm.license_type, asm.target_cohort, blueprint.schema_version))

                # Delete existing endpoints & field mappings for fresh upsert
                cur.execute("DELETE FROM audit_endpoints WHERE jurisdiction_code = %s", (asm.jurisdiction_code,))
                cur.execute("DELETE FROM audit_field_mappings WHERE jurisdiction_code = %s", (asm.jurisdiction_code,))

                # Insert endpoints
                for ep in blueprint.endpoints:
                    cur.execute("""
                        INSERT INTO audit_endpoints (jurisdiction_code, name, url, http_method, auth_required, rate_limit_per_min, response_format, pagination_mechanism)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                    """, (asm.jurisdiction_code, ep.name, ep.url, ep.http_method, ep.auth_required, ep.rate_limit_per_min, ep.response_format, ep.pagination_mechanism))

                # Insert field mappings
                for fm in blueprint.field_mappings:
                    cur.execute("""
                        INSERT INTO audit_field_mappings (jurisdiction_code, canonical_field, native_key, provenance_tier, derivation_confidence, notes)
                        VALUES (%s, %s, %s, %s, %s, %s);
                    """, (asm.jurisdiction_code, fm.canonical_field, fm.native_key, fm.provenance_tier, fm.derivation_confidence, fm.notes))

        conn.commit()
    print("[+] Audit blueprints successfully synced to PostgreSQL!")

def probe_endpoints():
    print("[*] Running continuous API health probes against active assembly endpoints...")
    with get_db_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT jurisdiction_code, name, url, http_method FROM audit_endpoints")
            endpoints = cur.fetchall()

    if not endpoints:
        print("[!] No endpoints found in audit_endpoints table to probe.")
        return

    with httpx.Client(timeout=10.0, follow_redirects=True) as client:
        with get_db_conn() as conn:
            with conn.cursor() as cur:
                for code, name, url, method in endpoints:
                    target_url = url.replace("{id}", "381").replace("{number}", "1")
                    print(f"  --> Probing {code} [{name}]: {target_url}...")
                    start_time = time.time()
                    try:
                        resp = client.request(method, target_url, headers={"User-Agent": "LegislativeDataAuditBot/1.0"})
                        latency_ms = int((time.time() - start_time) * 1000)
                        status_code = resp.status_code
                        probe_status = "HEALTHY" if resp.is_success else "DOWN"
                        resp_hash = hashlib.sha256(resp.content).hexdigest()[:16]
                        error_text = None if resp.is_success else f"HTTP {resp.status_code}"
                    except Exception as e:
                        latency_ms = int((time.time() - start_time) * 1000)
                        status_code = 500
                        probe_status = "DOWN"
                        resp_hash = None
                        error_text = str(e)

                    cur.execute("""
                        INSERT INTO audit_probe_logs (jurisdiction_code, endpoint_url, probed_at, http_status_code, latency_ms, status, response_hash, error_summary)
                        VALUES (%s, %s, NOW(), %s, %s, %s, %s, %s);
                    """, (code, target_url, status_code, latency_ms, probe_status, resp_hash, error_text))

            conn.commit()
    print("[+] All API probes completed and probe logs recorded!")

def ingest_jurisdiction(jurisdiction_code: str):
    code = jurisdiction_code.upper()
    print(f"[*] Starting Phase 1 Live Ingestion vertical slice for {code} (2019-2024 cohort)...")

    if code == "GB-SCT":
        ingestor = ScottishParliamentIngestor()
        bills = ingestor.fetch_all()
        print(f"[+] Fetched {len(bills)} canonical bill records for Holyrood (2019-2024).")

        with get_db_conn() as conn:
            with conn.cursor() as cur:
                for b in bills:
                    n = b.normalized
                    nat = b.native
                    prov = b.provenance

                    # Upsert Bill
                    cur.execute("""
                        INSERT INTO bills (
                            canonical_id, jurisdiction_code, normalized_title, parliament_term, session_subperiod,
                            session_start_date, session_end_date, initiator_type, initiator_party_governance_role,
                            date_introduced, date_final_outcome, duration_calendar_days, duration_sitting_days,
                            suspension_interrupted, final_status, termination_mechanism, rebellions_flag,
                            cross_party_sponsorship_count, derivation_confidence, native_payload, created_at, updated_at
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                        ON CONFLICT (canonical_id) DO UPDATE SET
                            normalized_title = EXCLUDED.normalized_title,
                            final_status = EXCLUDED.final_status,
                            date_final_outcome = EXCLUDED.date_final_outcome,
                            duration_calendar_days = EXCLUDED.duration_calendar_days,
                            native_payload = EXCLUDED.native_payload,
                            updated_at = NOW();
                    """, (
                        b.canonical_id, b.jurisdiction_code, n.title, n.parliament_term, n.session_subperiod,
                        n.session_start_date, n.session_end_date, n.initiator_type.value, n.initiator_party_governance_role.value,
                        n.date_introduced, n.date_final_outcome, n.duration_calendar_days, n.duration_sitting_days,
                        n.suspension_interrupted, n.final_status.value, n.termination_mechanism.value, n.rebellions_flag,
                        n.cross_party_sponsorship_count, n.derivation_confidence.value, psycopg.types.json.Jsonb(b.model_dump(mode="json"))
                    ))

                    # Re-insert Stages
                    cur.execute("DELETE FROM stage_milestones WHERE canonical_id = %s", (b.canonical_id,))
                    for idx, st in enumerate(n.stage_milestones, 1):
                        cur.execute("""
                            INSERT INTO stage_milestones (canonical_id, stage_canonical, stage_raw, chamber, date_stage, proceedings_url, seq_order)
                            VALUES (%s, %s, %s, %s, %s, %s, %s);
                        """, (b.canonical_id, st.stage_canonical.value, st.stage_raw, st.chamber.value, st.date_stage, st.proceedings_url, idx))

                    # Re-insert Sponsors
                    cur.execute("DELETE FROM sponsors WHERE canonical_id = %s", (b.canonical_id,))
                    cur.execute("""
                        INSERT INTO sponsors (canonical_id, member_name, member_id, party, is_primary)
                        VALUES (%s, %s, %s, %s, %s);
                    """, (b.canonical_id, nat.initiator_name, nat.initiator_member_id, nat.initiator_party, True))

                    # Provenance Audit Log Entry
                    cur.execute("""
                        INSERT INTO provenance_audit_log (canonical_id, source_url, retrieved_at, raw_payload_hash, scraper_version, zenodo_doi, license)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);
                    """, (b.canonical_id, prov.source_url, prov.retrieved_at, prov.raw_payload_hash, prov.scraper_version, getattr(prov, "zenodo_doi", None), prov.license))

            conn.commit()
        print(f"[+] Ingestion complete for {code}! {len(bills)} bills written to PostgreSQL.")
    else:
        print(f"[!] Ingestion pipeline for {code} is not yet implemented.")

def main():
    parser = argparse.ArgumentParser(description="Comparative Legislative Data Audit & Ingestion Engine")
    parser.add_argument("action", choices=["sync", "probe", "ingest", "all"], help="Action to perform: sync, probe, or ingest")
    parser.add_argument("--audits-dir", default="docs/audits", help="Directory containing YAML audit blueprints")
    parser.add_argument("--jurisdiction", default="GB-SCT", help="Jurisdiction code to ingest (e.g. GB-SCT)")
    args = parser.parse_args()

    if args.action in ["sync", "all"]:
        sync_audits(args.audits_dir)
    if args.action in ["probe", "all"]:
        probe_endpoints()
    if args.action in ["ingest"]:
        ingest_jurisdiction(args.jurisdiction)

if __name__ == "__main__":
    main()
