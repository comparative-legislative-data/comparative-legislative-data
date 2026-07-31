import os
import sys
import subprocess

ENDPOINTS = {
    "billtypes": {
        "table": "raw_gb_sct_billtypes",
        "fields": ["id as \"ID\"", "name as \"Name\""]
    },
    "billstagetypes": {
        "table": "raw_gb_sct_billstagetypes",
        "fields": ["id as \"ID\"", "name as \"Name\"", "billtypeid as \"BillTypeID\"", "sequence as \"Sequence\""]
    },
    "parties": {
        "table": "raw_gb_sct_parties",
        "fields": [
            "id as \"ID\"", "abbreviation as \"Abbreviation\"", "actualname as \"ActualName\"", 
            "preferredname as \"PreferredName\"", "notes as \"Notes\"", 
            "validfromdate as \"ValidFromDate\"", "validuntildate as \"ValidUntilDate\""
        ]
    },
    "committeeroles": {
        "table": "raw_gb_sct_committeeroles",
        "fields": ["id as \"ID\"", "name as \"Name\"", "notes as \"Notes\""]
    },
    "committeetypes": {
        "table": "raw_gb_sct_committeetypes",
        "fields": ["id as \"ID\"", "name as \"Name\""]
    },
    "bills": {
        "table": "raw_gb_sct_bills",
        "fields": [
            "id as \"ID\"", "reference as \"Reference\"", "shortname as \"ShortName\"", 
            "fullname as \"FullName\"", "billtypeid as \"BillTypeID\"", "personid as \"PersonID\"", 
            "thirdpartyorganisation as \"ThirdPartyOrganisation\""
        ]
    },
    "billstages": {
        "table": "raw_gb_sct_billstages",
        "fields": ["id as \"ID\"", "billid as \"BillID\"", "billstagetypeid as \"BillStageTypeID\"", "stagedate as \"StageDate\""]
    },
    "members": {
        "table": "raw_gb_sct_members",
        "fields": [
            "personid as \"PersonID\"", "photourl as \"PhotoURL\"", "notes as \"Notes\"", "birthdate as \"BirthDate\"", 
            "birthdateisprotected as \"BirthDateIsProtected\"", "parliamentaryname as \"ParliamentaryName\"", 
            "preferredname as \"PreferredName\"", "gendertypeid as \"GenderTypeID\"", "iscurrent as \"IsCurrent\""
        ]
    },
    "memberparties": {
        "table": "raw_gb_sct_memberparties",
        "fields": ["id as \"ID\"", "personid as \"PersonID\"", "partyid as \"PartyID\"", "validfromdate as \"ValidFromDate\"", "validuntildate as \"ValidUntilDate\""]
    },
    "committees": {
        "table": "raw_gb_sct_committees",
        "fields": [
            "id as \"ID\"", "shortname as \"ShortName\"", "name as \"Name\"", "description as \"Description\"", 
            "committeeemailaddress as \"CommitteeEmailAddress\"", "committeetelephone as \"CommitteeTelephone\"", 
            "validfromdate as \"ValidFromDate\"", "validuntildate as \"ValidUntilDate\""
        ]
    },
    "personcommitteeroles": {
        "table": "raw_gb_sct_personcommitteeroles",
        "fields": [
            "id as \"ID\"", "personid as \"PersonID\"", "committeeroleid as \"CommitteeRoleID\"", "committeeid as \"CommitteeID\"", 
            "validfromdate as \"ValidFromDate\"", "validuntildate as \"ValidUntilDate\"", "notes as \"Notes\""
        ]
    },
    "motionsquestionsanswersmotions": {
        "table": "raw_gb_sct_motions",
        "fields": [
            "uniqueid as \"UniqueID\"", "eventid as \"EventID\"", "eventtypeid as \"EventTypeID\"", "eventsubtypeid as \"EventSubTypeID\"", 
            "mspid as \"MSPID\"", "party as \"Party\"", "regionid as \"RegionID\"", "constituencyid as \"ConstituencyID\"", 
            "approveddate as \"ApprovedDate\"", "submissiondatetime as \"SubmissionDateTime\"", "title as \"Title\"", "itemtext as \"ItemText\""
        ]
    },
    "votesmotion": {
        "table": "raw_gb_sct_votes",
        "fields": ["id as \"ID\"", "detail as \"Detail\"", "motion as \"Motion\"", "person as \"Person\"", "time as \"Time\"", "updatedelasticdate as \"UpdatedElasticDate\""]
    },
    "orsplenarymeeting": {
        "table": "raw_gb_sct_plenary_reports",
        "fields": [
            "id as \"ID\"", "meeting as \"Meeting\"", "committee as \"Committee\"", "time as \"Time\"", 
            "itemofbusiness as \"ItemOfBusiness\"", "person as \"Person\"", "detail as \"Detail\"", "updatedelasticdate as \"UpdatedElasticDate\""
        ]
    },
    "orscommitteemeeting": {
        "table": "raw_gb_sct_committee_reports",
        "fields": [
            "id as \"ID\"", "recordtype as \"RecordType\"", "subtype as \"SubType\"", "meeting as \"Meeting\"", 
            "committee as \"Committee\"", "time as \"Time\"", "itemofbusiness as \"ItemOfBusiness\"", "person as \"Person\"", 
            "detail as \"Detail\"", "location as \"Location\"", "updateddate as \"UpdatedDate\"", "updatedelasticdate as \"UpdatedElasticDate\""
        ]
    }
}

# Add alias for motions
ENDPOINTS["motions"] = ENDPOINTS["motionsquestionsanswersmotions"]

OUTPUT_DIR = "/home/chessadmin/comparativelegislativedata/downloads/gb-sct"

def run_export():
    print("==================================================================")
    print("      SCOTTISH PARLIAMENT COMPRESSED CSV BULK EXPORT ENGINE")
    print("==================================================================")
    
    # Ensure directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    UNCOMPRESSED_ENDPOINTS = {
        "billtypes", "billstagetypes", "parties", "committeeroles", 
        "committeetypes", "bills", "members", "committees"
    }
    
    for name, ep in ENDPOINTS.items():
        table = ep["table"]
        fields_str = ", ".join(ep["fields"])
        
        is_uncompressed = name in UNCOMPRESSED_ENDPOINTS
        ext = "csv" if is_uncompressed else "csv.gz"
        
        output_file = os.path.join(OUTPUT_DIR, f"{name}.{ext}")
        print(f"[*] Exporting {name:32} (Table: {table}, Format: {ext})")
        
        # Build SQL copy query
        sql_query = f"SELECT {fields_str} FROM {table}"
        
        if is_uncompressed:
            cmd = (
                f"PGPASSWORD=chessadmin psql -h 127.0.0.1 -U chessadmin -d comparative_legislative_data "
                f"-c \"\\copy ({sql_query}) TO stdout WITH CSV HEADER\" > {output_file}"
            )
        else:
            cmd = (
                f"PGPASSWORD=chessadmin psql -h 127.0.0.1 -U chessadmin -d comparative_legislative_data "
                f"-c \"\\copy ({sql_query}) TO stdout WITH CSV HEADER\" | gzip > {output_file}"
            )
        
        try:
            subprocess.run(cmd, shell=True, check=True)
            # Print file size info
            size_bytes = os.path.getsize(output_file)
            size_mb = size_bytes / (1024 * 1024)
            print(f"    [+] Saved: {output_file} ({size_mb:.3f} MB)")
        except Exception as e:
            print(f"    [!] Export Failed: {e}")
            
    print("\n==================================================================")
    print("  BULK EXPORT COMPLETED SUCCESSFULLY!")
    print("==================================================================")

if __name__ == "__main__":
    run_export()
