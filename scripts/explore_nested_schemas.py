import urllib.request
import json
import sys

TARGETS = {
    "votesmotion": "https://data.parliament.scot/api/votesmotion?year=2024",
    "orsplenarymeeting": "https://data.parliament.scot/api/orsplenarymeeting?year=2024",
    "orscommitteemeeting": "https://data.parliament.scot/api/orscommitteemeeting?year=2024"
}

def get_live_sample(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Academic Schema Explorer'})
    try:
        with urllib.request.urlopen(req, timeout=30) as res:
            data = json.loads(res.read().decode('utf-8'))
            if isinstance(data, list) and len(data) > 0:
                return data[0]
            return data
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return None

def format_structure(obj, indent=0):
    lines = []
    pad = "  " * indent
    if isinstance(obj, dict):
        for k, v in obj.items():
            t = "null" if v is None else type(v).__name__
            if isinstance(v, dict):
                lines.append(f"{pad}- **{k}** (Object):")
                lines.extend(format_structure(v, indent + 1))
            elif isinstance(v, list):
                if len(v) > 0 and isinstance(v[0], dict):
                    lines.append(f"{pad}- **{k}** (Array of Objects):")
                    lines.extend(format_structure(v[0], indent + 1))
                else:
                    item_t = "unknown" if len(v) == 0 else type(v[0]).__name__
                    lines.append(f"{pad}- **{k}** (Array of {item_t})")
            else:
                lines.append(f"{pad}- **{k}** ({t})")
    elif isinstance(obj, list):
        if len(obj) > 0:
            lines.extend(format_structure(obj[0], indent))
    return lines

def main():
    report = [
        "# Detailed Audited Schemas for Complex Endpoints",
        "",
        "This document lists the complete nested structures of the Votes and Official Report endpoints, dynamically probed from the live data.",
        ""
    ]
    
    for name, url in TARGETS.items():
        print(f"Fetching sample for {name}...")
        sample = get_live_sample(url)
        if sample:
            report.append(f"## Endpoint: `{name}`")
            report.append(f"Source URL: `{url}`")
            report.append("")
            report.append("### Key Hierarchy:")
            structure_lines = format_structure(sample)
            report.extend(structure_lines)
            report.append("")
            report.append("---")
            report.append("")
            
    with open("docs/nested_schemas_audit.md", "w") as f:
        f.write("\n".join(report))
        
    print("Done! Audit written to docs/nested_schemas_audit.md")

if __name__ == "__main__":
    main()
