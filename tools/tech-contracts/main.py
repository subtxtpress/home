"""
DHS Procurement Research API
Combines EFF vendor dataset with live government database queries
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
import pandas as pd
from datetime import datetime
import uvicorn
from pathlib import Path

# Import government query service (it's in same directory)
from gov_queries import ProcurementQueryService

app = FastAPI(
    title="DHS Procurement Research API",
    description="Track homeland security vendors, contracts, and spending (EFF Dataset + Live Gov Queries)",
    version="1.0.0"
)

# Initialize government query service
gov_query_service = ProcurementQueryService()

# Enable CORS for web applications
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global data cache
data_cache = {}

def load_data():
    """Load all data from the EFF dataset"""
    if data_cache:
        return data_cache
    
    xlsx_path = "2025_update_us_border-homeland_security_tech_vendors_dataset_public_version_1-6-2026.xlsx"
    
    print("Loading data...")
    xlsx = pd.ExcelFile(xlsx_path)
    
    # Load vendor profiles
    vendors_df = pd.read_excel(xlsx, sheet_name="Vendor Profiles")
    data_cache['vendors'] = vendors_df
    
    # Load industry day attendees
    attendees_df = pd.read_excel(xlsx, sheet_name="CBP-ICE Industry Day Attendees ")
    data_cache['attendees'] = attendees_df
    
    # Load top 100 contractors (skip header rows)
    top100_df = pd.read_excel(xlsx, sheet_name="Top 100 DHS Contractors", skiprows=1)
    data_cache['top100'] = top100_df
    
    # Load consortium members
    consortium_df = pd.read_excel(xlsx, sheet_name="HSTech Consortium Membe", skiprows=1)
    data_cache['consortium'] = consortium_df
    
    print(f"Loaded {len(vendors_df)} vendors, {len(attendees_df)} industry day records")
    
    return data_cache

@app.on_event("startup")
async def startup_event():
    """Load data when API starts"""
    load_data()

@app.get("/")
async def root():
    """API information and available endpoints"""
    return {
        "name": "DHS Procurement Research API",
        "version": "1.0.0",
        "description": "Track homeland security vendors, contracts, and spending",
        "data_source": "Electronic Frontier Foundation Dataset (Jan 2026)",
        "endpoints": {
            "vendors": "/vendors - Search vendor database",
            "vendor_detail": "/vendors/{ref_id} - Get specific vendor",
            "search": "/search?q=keyword - Full text search",
            "categories": "/categories - List product/service categories",
            "prime_contractors": "/prime-contractors - List DHS prime contractors",
            "ai_vendors": "/ai-vendors - Vendors using AI/ML",
            "industry_events": "/industry-events - Industry day participation",
            "top_contractors": "/top-contractors - Top 100 DHS contractors",
            "consortium": "/consortium - HStech Consortium members",
            "stats": "/stats - Dataset statistics",
            "live_contracts": "/live/contracts/{vendor_name} - Query USASpending.gov",
            "live_history": "/live/history/{vendor_name} - Contract history",
            "live_compare": "/live/compare - Compare multiple vendors",
            "fpds_search": "/live/fpds/{vendor_name} - FPDS search URL",
            "sam_search": "/live/sam?q=keyword - SAM.gov search",
            "enriched_vendor": "/enriched/{ref_id} - Vendor + live contract data"
        }
    }

@app.get("/stats")
async def get_stats():
    """Get dataset statistics"""
    data = load_data()
    vendors = data['vendors']
    
    return {
        "total_vendors": len(vendors),
        "prime_contractors": int(vendors['DHS Prime Contractor'].notna().sum()),
        "ai_ml_vendors": int(vendors['AI/ML in Marketing'].notna().sum()),
        "border_expo_exhibitors": int(vendors['Border Security Expo Exhibitor/Sponsor(2022-2025)'].notna().sum()),
        "consortium_members": int(vendors['Homeland Security Technology Consortium Member'].notna().sum()),
        "vendors_with_contracts": int(vendors['Federal Agency Contracts'].notna().sum()),
        "data_updated": "2026-01-06"
    }

@app.get("/vendors")
async def search_vendors(
    q: Optional[str] = Query(None, description="Search term (name, category, summary)"),
    category: Optional[str] = Query(None, description="Filter by product/service category"),
    prime_only: bool = Query(False, description="Only DHS prime contractors"),
    ai_only: bool = Query(False, description="Only AI/ML vendors"),
    limit: int = Query(50, description="Max results to return")
):
    """
    Search vendor database with filters
    
    Examples:
    - /vendors?q=surveillance
    - /vendors?category=biometric&prime_only=true
    - /vendors?ai_only=true
    """
    data = load_data()
    df = data['vendors'].copy()
    
    # Apply filters
    if q:
        mask = (
            df['Company Name'].str.contains(q, case=False, na=False) |
            df['Categories of Products/Services'].str.contains(q, case=False, na=False) |
            df['Corporate Summary (Derived from company materials)'].str.contains(q, case=False, na=False)
        )
        df = df[mask]
    
    if category:
        df = df[df['Categories of Products/Services'].str.contains(category, case=False, na=False)]
    
    if prime_only:
        df = df[df['DHS Prime Contractor'].notna()]
    
    if ai_only:
        df = df[df['AI/ML in Marketing'].notna()]
    
    # Limit results
    df = df.head(limit)
    
    # Convert to records
    results = []
    for _, row in df.iterrows():
        results.append({
            "ref": row['Ref'],
            "name": row['Company Name'],
            "website": row['Website'] if pd.notna(row['Website']) else None,
            "categories": row['Categories of Products/Services'] if pd.notna(row['Categories of Products/Services']) else None,
            "summary": row['Corporate Summary (Derived from company materials)'][:200] + "..." if pd.notna(row['Corporate Summary (Derived from company materials)']) and len(str(row['Corporate Summary (Derived from company materials)'])) > 200 else row['Corporate Summary (Derived from company materials)'],
            "is_prime_contractor": pd.notna(row['DHS Prime Contractor']),
            "uses_ai_ml": pd.notna(row['AI/ML in Marketing']),
            "parent_company": row['Parent Company/Alternative Name/DBA'] if pd.notna(row['Parent Company/Alternative Name/DBA']) else None,
            "usaspending_link": row['USASpending.gov Link (DHS)'] if pd.notna(row['USASpending.gov Link (DHS)']) else None
        })
    
    return {
        "count": len(results),
        "vendors": results
    }

@app.get("/vendors/{ref_id}")
async def get_vendor_detail(ref_id: str):
    """Get complete details for a specific vendor by REF ID"""
    data = load_data()
    df = data['vendors']
    
    vendor = df[df['Ref'] == ref_id]
    
    if len(vendor) == 0:
        raise HTTPException(status_code=404, detail=f"Vendor {ref_id} not found")
    
    row = vendor.iloc[0]
    
    # Build comprehensive vendor profile
    detail = {
        "ref": row['Ref'],
        "name": row['Company Name'],
        "website": row['Website'] if pd.notna(row['Website']) else None,
        "categories": row['Categories of Products/Services'] if pd.notna(row['Categories of Products/Services']) else None,
        "corporate_summary": row['Corporate Summary (Derived from company materials)'] if pd.notna(row['Corporate Summary (Derived from company materials)']) else None,
        "uses_ai_ml": pd.notna(row['AI/ML in Marketing']),
        "is_prime_contractor": pd.notna(row['DHS Prime Contractor']),
        "border_expo_participation": row['Border Security Expo Exhibitor/Sponsor(2022-2025)'] if pd.notna(row['Border Security Expo Exhibitor/Sponsor(2022-2025)']) else None,
        "border_tech_summit": row['Border Technology Summit 2024-2025'] if pd.notna(row['Border Technology Summit 2024-2025']) else None,
        "consortium_member": pd.notna(row['Homeland Security Technology Consortium Member']),
        "notes": row['Additional notes'] if pd.notna(row['Additional notes']) else None,
        "parent_company": row['Parent Company/Alternative Name/DBA'] if pd.notna(row['Parent Company/Alternative Name/DBA']) else None,
        "related_companies": row['Related Companies (Subsidiaries, Distributors, Strategic Partners, Passthroughs)'] if pd.notna(row['Related Companies (Subsidiaries, Distributors, Strategic Partners, Passthroughs)']) else None,
        "dhs_programs": row['Official DHS Programs'] if pd.notna(row['Official DHS Programs']) else None,
        "agency_contracts": row['Federal Agency Contracts'] if pd.notna(row['Federal Agency Contracts']) else None,
        "links": {
            "usaspending": row['USASpending.gov Link (DHS)'] if pd.notna(row['USASpending.gov Link (DHS)']) else None,
            "fpds": row['Federal Procurement Data System Link (DHS)'] if pd.notna(row['Federal Procurement Data System Link (DHS)']) else None,
            "source1": row['Related/Source Links'] if pd.notna(row['Related/Source Links']) else None,
            "source2": row['Related/Source Links.1'] if pd.notna(row['Related/Source Links.1']) else None,
            "source3": row['Related/Source Links.2'] if pd.notna(row['Related/Source Links.2']) else None
        }
    }
    
    return detail

@app.get("/categories")
async def get_categories():
    """List all product/service categories in the database"""
    data = load_data()
    df = data['vendors']
    
    # Extract unique categories
    categories = set()
    for cat in df['Categories of Products/Services'].dropna():
        if isinstance(cat, str):
            categories.add(cat)
    
    return {
        "count": len(categories),
        "categories": sorted(list(categories))
    }

@app.get("/prime-contractors")
async def get_prime_contractors():
    """List all DHS prime contractors"""
    data = load_data()
    df = data['vendors']
    
    primes = df[df['DHS Prime Contractor'].notna()]
    
    results = []
    for _, row in primes.iterrows():
        results.append({
            "ref": row['Ref'],
            "name": row['Company Name'],
            "categories": row['Categories of Products/Services'] if pd.notna(row['Categories of Products/Services']) else None,
            "parent_company": row['Parent Company/Alternative Name/DBA'] if pd.notna(row['Parent Company/Alternative Name/DBA']) else None,
            "usaspending_link": row['USASpending.gov Link (DHS)'] if pd.notna(row['USASpending.gov Link (DHS)']) else None
        })
    
    return {
        "count": len(results),
        "contractors": results
    }

@app.get("/ai-vendors")
async def get_ai_vendors():
    """List vendors that market AI/ML capabilities"""
    data = load_data()
    df = data['vendors']
    
    ai_vendors = df[df['AI/ML in Marketing'].notna()]
    
    results = []
    for _, row in ai_vendors.iterrows():
        results.append({
            "ref": row['Ref'],
            "name": row['Company Name'],
            "categories": row['Categories of Products/Services'] if pd.notna(row['Categories of Products/Services']) else None,
            "is_prime": pd.notna(row['DHS Prime Contractor']),
            "dhs_programs": row['Official DHS Programs'] if pd.notna(row['Official DHS Programs']) else None
        })
    
    return {
        "count": len(results),
        "vendors": results
    }

@app.get("/industry-events")
async def get_industry_events(
    company: Optional[str] = Query(None, description="Filter by company name")
):
    """List industry day participation records"""
    data = load_data()
    df = data['attendees'].copy()
    
    if company:
        df = df[df['Company Name (Registered)'].str.contains(company, case=False, na=False)]
    
    results = []
    for _, row in df.head(100).iterrows():
        # Check which events they attended
        events = []
        for col in df.columns[1:7]:  # Event columns
            if pd.notna(row[col]) and row[col] == 'Y':
                events.append(col[:50] + "...")  # Truncate long column names
        
        if events:  # Only include if they attended something
            results.append({
                "company": row['Company Name (Registered)'],
                "events_attended": events,
                "event_count": len(events)
            })
    
    return {
        "count": len(results),
        "participants": results
    }

@app.get("/top-contractors")
async def get_top_contractors(
    year: Optional[int] = Query(None, description="Filter by fiscal year")
):
    """Get top 100 DHS contractors by year"""
    data = load_data()
    df = data['top100']
    
    # This needs custom parsing based on the complex structure
    # For now, return basic info
    return {
        "message": "Top 100 contractors data available",
        "years_available": "2006-2024",
        "note": "Use specific year parameter for detailed breakdown"
    }

@app.get("/consortium")
async def get_consortium_members():
    """Get Homeland Security Technology Consortium members"""
    data = load_data()
    df = data['consortium']
    
    results = []
    for _, row in df.iterrows():
        if pd.notna(row.get('Members of the Homeland Security Technology Consortium (Formerly Border Security Technonology Consortium)\nDetails: https://hstech.ati.org/about/\nDHS Documentation: https://www.dhs.gov/sites/default/files/publications/bstc_ota_2021dhsgov_webpage_508.pdf')):
            results.append({
                "company": row['Members of the Homeland Security Technology Consortium (Formerly Border Security Technonology Consortium)\nDetails: https://hstech.ati.org/about/\nDHS Documentation: https://www.dhs.gov/sites/default/files/publications/bstc_ota_2021dhsgov_webpage_508.pdf'],
                "website": row.get('Unnamed: 1'),
                "category": row.get('Unnamed: 2'),
                "non_traditional": row.get('Unnamed: 3')
            })
    
    return {
        "count": len(results),
        "members": results[:100]  # Limit for now
    }

@app.get("/search")
async def full_text_search(
    q: str = Query(..., description="Search term"),
    limit: int = Query(20, description="Max results")
):
    """
    Full text search across all vendor data
    Searches company names, summaries, categories, programs, and notes
    """
    data = load_data()
    df = data['vendors'].copy()
    
    # Search across multiple fields
    search_cols = [
        'Company Name',
        'Corporate Summary (Derived from company materials)',
        'Categories of Products/Services',
        'Official DHS Programs',
        'Additional notes',
        'Parent Company/Alternative Name/DBA',
        'Related Companies (Subsidiaries, Distributors, Strategic Partners, Passthroughs)'
    ]
    
    mask = False
    for col in search_cols:
        if col in df.columns:
            mask = mask | df[col].str.contains(q, case=False, na=False)
    
    results_df = df[mask].head(limit)
    
    results = []
    for _, row in results_df.iterrows():
        results.append({
            "ref": row['Ref'],
            "name": row['Company Name'],
            "categories": row['Categories of Products/Services'] if pd.notna(row['Categories of Products/Services']) else None,
            "summary_preview": str(row['Corporate Summary (Derived from company materials)'])[:200] + "..." if pd.notna(row['Corporate Summary (Derived from company materials)']) else None,
            "relevance_indicators": {
                "is_prime": pd.notna(row['DHS Prime Contractor']),
                "uses_ai": pd.notna(row['AI/ML in Marketing']),
                "has_contracts": pd.notna(row['Federal Agency Contracts'])
            }
        })
    
    return {
        "query": q,
        "count": len(results),
        "results": results
    }

# ===== LIVE GOVERNMENT DATABASE QUERIES =====

@app.get("/live/contracts/{vendor_name}")
async def query_live_contracts(
    vendor_name: str,
    agency: str = Query("Department of Homeland Security", description="Federal agency"),
    limit: int = Query(10, description="Max results")
):
    """
    Query USASpending.gov API for live contract data
    
    This makes a real-time query to the government database
    """
    result = gov_query_service.search_usaspending(vendor_name, agency, limit)
    return result

@app.get("/live/history/{vendor_name}")
async def query_contract_history(
    vendor_name: str,
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)")
):
    """
    Get complete contract history for a vendor from USASpending.gov
    """
    result = gov_query_service.get_vendor_contract_history(
        vendor_name, start_date, end_date
    )
    return result

@app.get("/live/compare")
async def compare_vendors_live(
    vendors: str = Query(..., description="Comma-separated vendor names"),
    agency: str = Query("Department of Homeland Security", description="Agency to filter by")
):
    """
    Compare contract spending across multiple vendors
    
    Example: /live/compare?vendors=Palantir,Anduril,Clearview AI
    """
    vendor_list = [v.strip() for v in vendors.split(",")]
    result = gov_query_service.compare_vendors(vendor_list, agency)
    return result

@app.get("/live/fpds/{vendor_name}")
async def get_fpds_search(vendor_name: str):
    """
    Get FPDS.gov search URL for a vendor
    
    FPDS doesn't have a public API, but this provides the direct search link
    """
    result = gov_query_service.search_fpds_contracts(vendor_name)
    return result

@app.get("/live/sam")
async def search_sam_gov(
    q: str = Query(..., description="Search keyword"),
    agency_code: Optional[str] = Query(None, description="Agency code")
):
    """
    Search SAM.gov for contract opportunities
    
    Returns search URL (SAM.gov requires auth for API access)
    """
    result = gov_query_service.search_sam_contracts(q, agency_code)
    return result

@app.get("/enriched/{ref_id}")
async def get_enriched_vendor(ref_id: str):
    """
    Get vendor profile enriched with live contract data
    
    Combines EFF dataset with real-time USASpending.gov query
    """
    # Get base vendor data
    data = load_data()
    df = data['vendors']
    
    vendor = df[df['Ref'] == ref_id]
    
    if len(vendor) == 0:
        raise HTTPException(status_code=404, detail=f"Vendor {ref_id} not found")
    
    row = vendor.iloc[0]
    vendor_name = row['Company Name']
    
    # Build base profile
    profile = {
        "ref": row['Ref'],
        "name": vendor_name,
        "website": row['Website'] if pd.notna(row['Website']) else None,
        "categories": row['Categories of Products/Services'] if pd.notna(row['Categories of Products/Services']) else None,
        "corporate_summary": row['Corporate Summary (Derived from company materials)'] if pd.notna(row['Corporate Summary (Derived from company materials)']) else None,
        "is_prime_contractor": pd.notna(row['DHS Prime Contractor']),
        "parent_company": row['Parent Company/Alternative Name/DBA'] if pd.notna(row['Parent Company/Alternative Name/DBA']) else None,
        "dhs_programs": row['Official DHS Programs'] if pd.notna(row['Official DHS Programs']) else None,
    }
    
    # Query live contract data
    live_contracts = gov_query_service.search_usaspending(vendor_name, limit=20)
    
    profile['live_contract_data'] = live_contracts
    profile['data_sources'] = {
        "base_profile": "EFF Dataset (Jan 2026)",
        "live_contracts": "USASpending.gov API (real-time)"
    }
    
    return profile

if __name__ == "__main__":
    print("Starting DHS Procurement Research API...")
    print("Access documentation at: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)