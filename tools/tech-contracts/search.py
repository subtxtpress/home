"""
Simple Interactive Search Tool
Just run this and answer the questions!
"""

from demo import ProcurementResearcher
import pandas as pd

def main():
    print("\n" + "="*70)
    print("DHS PROCUREMENT RESEARCH TOOL")
    print("="*70)
    
    # Load data
    print("\nLoading dataset...")
    researcher = ProcurementResearcher(
        "2025_update_us_border-homeland_security_tech_vendors_dataset_public_version_1-6-2026.xlsx"
    )
    
    while True:
        print("\n" + "="*70)
        print("WHAT DO YOU WANT TO DO?")
        print("="*70)
        print("\n1. Search for vendors by keyword")
        print("2. Show all AI/ML vendors")
        print("3. Show all prime contractors")
        print("4. Get a specific vendor's full profile")
        print("5. Export search results to CSV")
        print("6. Show dataset statistics")
        print("7. Quit")
        
        choice = input("\nEnter number (1-7): ").strip()
        
        if choice == "1":
            # Search by keyword
            keyword = input("\nWhat do you want to search for? (e.g., surveillance, drone, facial recognition): ").strip()
            
            ai_filter = input("Only AI/ML vendors? (y/n): ").strip().lower()
            ai_only = (ai_filter == 'y')
            
            prime_filter = input("Only prime contractors? (y/n): ").strip().lower()
            prime_only = (prime_filter == 'y')
            
            results = researcher.search_vendors(keyword, ai_only=ai_only, prime_only=prime_only, limit=50)
            
            print(f"\n{'='*70}")
            print(f"FOUND {len(results)} VENDORS:")
            print("="*70)
            
            for idx, vendor in results.iterrows():
                print(f"\n{vendor['Ref']}: {vendor['Company Name']}")
                if pd.notna(vendor['Categories of Products/Services']):
                    print(f"  Category: {vendor['Categories of Products/Services']}")
                if pd.notna(vendor['Official DHS Programs']):
                    print(f"  Programs: {vendor['Official DHS Programs']}")
            
            export = input("\nExport these results to CSV? (y/n): ").strip().lower()
            if export == 'y':
                filename = input("Filename (e.g., my_search.csv): ").strip()
                if not filename.endswith('.csv'):
                    filename += '.csv'
                researcher.export_to_csv(results, filename)
        
        elif choice == "2":
            # AI/ML vendors
            results = researcher.search_vendors(ai_only=True, limit=200)
            
            print(f"\n{'='*70}")
            print(f"FOUND {len(results)} AI/ML VENDORS:")
            print("="*70)
            
            for idx, vendor in results.iterrows():
                print(f"  • {vendor['Company Name']}")
            
            export = input("\nExport to CSV? (y/n): ").strip().lower()
            if export == 'y':
                researcher.export_to_csv(results, "ai_ml_vendors.csv")
        
        elif choice == "3":
            # Prime contractors
            results = researcher.search_vendors(prime_only=True, limit=50)
            
            print(f"\n{'='*70}")
            print(f"FOUND {len(results)} PRIME CONTRACTORS:")
            print("="*70)
            
            for idx, vendor in results.iterrows():
                print(f"\n{vendor['Company Name']}")
                if pd.notna(vendor['Categories of Products/Services']):
                    print(f"  Category: {vendor['Categories of Products/Services']}")
                if pd.notna(vendor['Official DHS Programs']):
                    print(f"  Programs: {vendor['Official DHS Programs']}")
            
            export = input("\nExport to CSV? (y/n): ").strip().lower()
            if export == 'y':
                researcher.export_to_csv(results, "prime_contractors.csv")
        
        elif choice == "4":
            # Get specific vendor
            search_term = input("\nEnter company name or REF ID (e.g., Palantir or TECH151): ").strip()
            
            # Try searching by name first
            results = researcher.search_vendors(search_term, limit=10)
            
            if len(results) == 0:
                print("\nNo vendors found with that name.")
            elif len(results) == 1:
                researcher.print_vendor(results.iloc[0])
            else:
                print(f"\nFound {len(results)} matches:")
                for idx, vendor in results.iterrows():
                    print(f"  {vendor['Ref']}: {vendor['Company Name']}")
                
                ref_choice = input("\nEnter REF ID to see full profile (or press Enter to skip): ").strip()
                if ref_choice:
                    vendor = researcher.get_vendor_detail(ref_choice)
                    if vendor is not None:
                        researcher.print_vendor(vendor)
                    else:
                        print("Invalid REF ID")
        
        elif choice == "5":
            # Custom export
            keyword = input("\nSearch keyword (or press Enter for all vendors): ").strip()
            
            if keyword:
                results = researcher.search_vendors(keyword, limit=500)
            else:
                results = researcher.vendors
            
            filename = input("Filename (e.g., my_export.csv): ").strip()
            if not filename.endswith('.csv'):
                filename += '.csv'
            
            researcher.export_to_csv(results, filename)
        
        elif choice == "6":
            # Statistics
            stats = researcher.get_stats()
            print(f"\n{'='*70}")
            print("DATASET STATISTICS")
            print("="*70)
            for key, value in stats.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
        
        elif choice == "7":
            print("\nGoodbye!")
            break
        
        else:
            print("\nInvalid choice. Please enter a number 1-7.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
