"""
DHS Procurement Research Tool - Standalone Demo
Test the dataset without running the full API server
"""

import pandas as pd
from pathlib import Path
import json

class ProcurementResearcher:
    """Standalone tool for procurement research"""
    
    def __init__(self, xlsx_path):
        print("Loading DHS Procurement Dataset...")
        self.xlsx = pd.ExcelFile(xlsx_path)
        
        # Load all sheets
        self.vendors = pd.read_excel(self.xlsx, sheet_name="Vendor Profiles")
        self.attendees = pd.read_excel(self.xlsx, sheet_name="CBP-ICE Industry Day Attendees ")
        self.top100 = pd.read_excel(self.xlsx, sheet_name="Top 100 DHS Contractors", skiprows=1)
        self.consortium = pd.read_excel(self.xlsx, sheet_name="HSTech Consortium Membe", skiprows=1)
        
        print(f"✓ Loaded {len(self.vendors)} vendors")
        print(f"✓ Loaded {len(self.attendees)} industry day records")
        print(f"✓ Loaded Top 100 contractors data")
        print(f"✓ Loaded {len(self.consortium)} consortium members")
    
    def search_vendors(self, query=None, category=None, prime_only=False, ai_only=False, limit=50):
        """Search vendor database"""
        df = self.vendors.copy()
        
        # Apply filters
        if query:
            mask = (
                df['Company Name'].str.contains(query, case=False, na=False) |
                df['Categories of Products/Services'].str.contains(query, case=False, na=False) |
                df['Corporate Summary (Derived from company materials)'].str.contains(query, case=False, na=False)
            )
            df = df[mask]
        
        if category:
            df = df[df['Categories of Products/Services'].str.contains(category, case=False, na=False)]
        
        if prime_only:
            df = df[df['DHS Prime Contractor'].notna()]
        
        if ai_only:
            df = df[df['AI/ML in Marketing'].notna()]
        
        return df.head(limit)
    
    def get_vendor_detail(self, ref_id):
        """Get detailed vendor profile"""
        vendor = self.vendors[self.vendors['Ref'] == ref_id]
        if len(vendor) == 0:
            return None
        return vendor.iloc[0]
    
    def get_stats(self):
        """Get dataset statistics"""
        return {
            "total_vendors": len(self.vendors),
            "prime_contractors": int(self.vendors['DHS Prime Contractor'].notna().sum()),
            "ai_ml_vendors": int(self.vendors['AI/ML in Marketing'].notna().sum()),
            "border_expo_exhibitors": int(self.vendors['Border Security Expo Exhibitor/Sponsor(2022-2025)'].notna().sum()),
            "consortium_members": int(self.vendors['Homeland Security Technology Consortium Member'].notna().sum()),
            "vendors_with_contracts": int(self.vendors['Federal Agency Contracts'].notna().sum())
        }
    
    def export_to_csv(self, results, filename):
        """Export search results to CSV"""
        results.to_csv(filename, index=False)
        print(f"✓ Exported {len(results)} results to {filename}")
    
    def print_vendor(self, vendor):
        """Pretty print vendor details"""
        print("\n" + "="*70)
        print(f"REF: {vendor['Ref']}")
        print(f"COMPANY: {vendor['Company Name']}")
        print("="*70)
        
        if pd.notna(vendor['Website']):
            print(f"Website: {vendor['Website']}")
        
        if pd.notna(vendor['Categories of Products/Services']):
            print(f"\nCategories: {vendor['Categories of Products/Services']}")
        
        print(f"\nPrime Contractor: {'Yes' if pd.notna(vendor['DHS Prime Contractor']) else 'No'}")
        print(f"Uses AI/ML: {'Yes' if pd.notna(vendor['AI/ML in Marketing']) else 'No'}")
        
        if pd.notna(vendor['Parent Company/Alternative Name/DBA']):
            print(f"Parent Company: {vendor['Parent Company/Alternative Name/DBA']}")
        
        if pd.notna(vendor['Official DHS Programs']):
            print(f"\nDHS Programs: {vendor['Official DHS Programs']}")
        
        if pd.notna(vendor['Federal Agency Contracts']):
            print(f"Agency Contracts: {vendor['Federal Agency Contracts']}")
        
        if pd.notna(vendor['Corporate Summary (Derived from company materials)']):
            summary = str(vendor['Corporate Summary (Derived from company materials)'])
            print(f"\nSummary: {summary[:300]}{'...' if len(summary) > 300 else ''}")
        
        print("\nLinks:")
        if pd.notna(vendor['USASpending.gov Link (DHS)']):
            print(f"  USASpending: {vendor['USASpending.gov Link (DHS)']}")
        if pd.notna(vendor['Federal Procurement Data System Link (DHS)']):
            print(f"  FPDS: {vendor['Federal Procurement Data System Link (DHS)']}")


def run_demo():
    """Run demonstration queries"""
    
    # Initialize
    researcher = ProcurementResearcher(
        "2025_update_us_border-homeland_security_tech_vendors_dataset_public_version_1-6-2026.xlsx"
    )
    
    # Show stats
    print("\n" + "="*70)
    print("DATASET STATISTICS")
    print("="*70)
    stats = researcher.get_stats()
    for key, value in stats.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    # Example 1: Search for surveillance vendors
    print("\n" + "="*70)
    print("EXAMPLE 1: Search for 'surveillance' vendors")
    print("="*70)
    results = researcher.search_vendors("surveillance", limit=5)
    print(f"\nFound {len(results)} vendors:")
    for idx, vendor in results.iterrows():
        print(f"  - {vendor['Company Name']} ({vendor['Ref']})")
    
    # Example 2: AI/ML vendors
    print("\n" + "="*70)
    print("EXAMPLE 2: Vendors using AI/ML")
    print("="*70)
    ai_vendors = researcher.search_vendors(ai_only=True, limit=10)
    print(f"\nFound {len(ai_vendors)} AI/ML vendors:")
    for idx, vendor in ai_vendors.iterrows():
        print(f"  - {vendor['Company Name']}")
    
    # Example 3: Prime contractors with AI
    print("\n" + "="*70)
    print("EXAMPLE 3: Prime contractors using AI/ML")
    print("="*70)
    prime_ai = researcher.search_vendors(prime_only=True, ai_only=True, limit=10)
    print(f"\nFound {len(prime_ai)} prime contractors with AI:")
    for idx, vendor in prime_ai.iterrows():
        print(f"  - {vendor['Company Name']}")
        if pd.notna(vendor['Official DHS Programs']):
            print(f"    Programs: {vendor['Official DHS Programs']}")
    
    # Example 4: Detailed vendor profile
    print("\n" + "="*70)
    print("EXAMPLE 4: Detailed vendor profile (Palantir)")
    print("="*70)
    
    # Find Palantir
    palantir_search = researcher.search_vendors("Palantir", limit=1)
    if len(palantir_search) > 0:
        palantir = palantir_search.iloc[0]
        researcher.print_vendor(palantir)
    
    # Example 5: Search by category
    print("\n" + "="*70)
    print("EXAMPLE 5: Biometric technology vendors")
    print("="*70)
    biometric = researcher.search_vendors(category="biometric", limit=10)
    print(f"\nFound {len(biometric)} biometric vendors:")
    for idx, vendor in biometric.iterrows():
        print(f"  - {vendor['Company Name']}")
    
    # Example 6: Export results
    print("\n" + "="*70)
    print("EXAMPLE 6: Export surveillance vendors to CSV")
    print("="*70)
    surveillance_all = researcher.search_vendors("surveillance", limit=100)
    output_file = "surveillance_vendors.csv"
    researcher.export_to_csv(surveillance_all, output_file)
    
    print("\n" + "="*70)
    print("DEMO COMPLETE")
    print("="*70)
    print("\nYou can use this tool to:")
    print("  • Search for vendors by keyword, category, or attributes")
    print("  • Filter by prime contractor status or AI/ML usage")
    print("  • Get detailed vendor profiles with programs and links")
    print("  • Export results for further analysis")
    print("\nFor API access with live government queries, install FastAPI")
    print("and run: python main.py")


if __name__ == "__main__":
    run_demo()