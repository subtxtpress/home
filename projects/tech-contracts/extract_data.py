"""
Extract Excel data to static JSON for GitHub Pages deployment.
Run this locally whenever the EFF dataset is updated.

Usage: python3 extract_data.py
"""

import pandas as pd
import json
from pathlib import Path

XLSX_FILE = "2025_update_us_border-homeland_security_tech_vendors_dataset_public_version_1-6-2026.xlsx"
OUTPUT_FILE = "vendors.json"


def safe(val):
    """Return None for NaN/NaT, otherwise the value."""
    if pd.isna(val):
        return None
    return val


def extract_vendors(xlsx):
    df = pd.read_excel(xlsx, sheet_name="Vendor Profiles")
    vendors = []
    for _, row in df.iterrows():
        summary = safe(row.get("Corporate Summary (Derived from company materials)"))
        vendors.append({
            "ref": safe(row["Ref"]),
            "name": safe(row["Company Name"]),
            "website": safe(row.get("Website")),
            "categories": safe(row.get("Categories of Products/Services")),
            "summary": summary,
            "summary_preview": (str(summary)[:200] + "...") if summary and len(str(summary)) > 200 else summary,
            "ai_ml": safe(row.get("AI/ML in Marketing")) is not None,
            "prime_contractor": safe(row.get("DHS Prime Contractor")) is not None,
            "border_expo": safe(row.get("Border Security Expo Exhibitor/Sponsor(2022-2025)")),
            "border_tech_summit": safe(row.get("Border Technology Summit 2024-2025")),
            "consortium_member": safe(row.get("Homeland Security Technology Consortium Member")) is not None,
            "notes": safe(row.get("Additional notes")),
            "parent_company": safe(row.get("Parent Company/Alternative Name/DBA")),
            "related_companies": safe(row.get("Related Companies (Subsidiaries, Distributors, Strategic Partners, Passthroughs)")),
            "dhs_programs": safe(row.get("Official DHS Programs")),
            "agency_contracts": safe(row.get("Federal Agency Contracts")),
            "usaspending_link": safe(row.get("USASpending.gov Link (DHS)")),
            "fpds_link": safe(row.get("Federal Procurement Data System Link (DHS)")),
            "source_links": [
                safe(row.get("Related/Source Links")),
                safe(row.get("Related/Source Links.1")),
                safe(row.get("Related/Source Links.2")),
            ],
        })
    return vendors


def extract_attendees(xlsx):
    df = pd.read_excel(xlsx, sheet_name="CBP-ICE Industry Day Attendees ")
    event_cols = list(df.columns[1:7])
    attendees = []
    for _, row in df.iterrows():
        events = []
        for col in event_cols:
            if safe(row[col]) == "Y":
                # Extract short event name from the long column header
                short_name = col.split("\n")[0].strip()
                events.append(short_name)
        if events:
            attendees.append({
                "company": safe(row["Company Name (Registered)"]),
                "events": events,
                "event_count": len(events),
            })
    return attendees


def extract_consortium(xlsx):
    df = pd.read_excel(xlsx, sheet_name="HSTech Consortium Membe", skiprows=2)
    members = []
    for _, row in df.iterrows():
        name = safe(row.iloc[0])
        if name and isinstance(name, str) and name.strip():
            members.append({
                "company": name.strip(),
                "website": safe(row.iloc[1]),
                "category": safe(row.iloc[2]),
                "non_traditional": safe(row.iloc[3]),
            })
    return members


def compute_stats(vendors):
    return {
        "total_vendors": len(vendors),
        "prime_contractors": sum(1 for v in vendors if v["prime_contractor"]),
        "ai_ml_vendors": sum(1 for v in vendors if v["ai_ml"]),
        "border_expo_exhibitors": sum(1 for v in vendors if v["border_expo"]),
        "consortium_members": sum(1 for v in vendors if v["consortium_member"]),
        "vendors_with_contracts": sum(1 for v in vendors if v["agency_contracts"]),
        "data_updated": "2026-01-06",
    }


def main():
    print(f"Reading {XLSX_FILE}...")
    xlsx = pd.ExcelFile(XLSX_FILE)

    vendors = extract_vendors(xlsx)
    attendees = extract_attendees(xlsx)
    consortium = extract_consortium(xlsx)
    stats = compute_stats(vendors)

    data = {
        "stats": stats,
        "vendors": vendors,
        "attendees": attendees,
        "consortium": consortium,
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, default=str)

    size_kb = Path(OUTPUT_FILE).stat().st_size / 1024
    print(f"Wrote {OUTPUT_FILE} ({size_kb:.0f} KB)")
    print(f"  {len(vendors)} vendors, {len(attendees)} attendees, {len(consortium)} consortium members")


if __name__ == "__main__":
    main()
