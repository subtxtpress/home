"""
Contract Data Search Tool
Searches through all the contract CSVs you've downloaded
"""

import pandas as pd
from pathlib import Path
import glob

class ContractSearcher:
    """Search through downloaded contract CSVs"""
    
    def __init__(self, folder_path="."):
        self.folder_path = folder_path
        self.contracts = None
        print("Loading contract CSVs...")
        self.load_contracts()
    
    def load_contracts(self):
        """Load all CSV files in the folder"""
        csv_files = glob.glob(f"{self.folder_path}/*.csv")
        
        if not csv_files:
            print("No CSV files found!")
            return
        
        dfs = []
        for csv_file in csv_files:
            try:
                df = pd.read_csv(csv_file)
                # Add source file column
                df['source_file'] = Path(csv_file).name
                dfs.append(df)
                print(f"  ✓ Loaded {csv_file} ({len(df)} rows)")
            except Exception as e:
                print(f"  ✗ Could not load {csv_file}: {e}")
        
        if dfs:
            self.contracts = pd.concat(dfs, ignore_index=True)
            print(f"\n✓ Total: {len(self.contracts)} contract records")
        else:
            print("No contracts loaded")
    
    def search(self, keyword=None, min_amount=None, max_amount=None, 
               start_date=None, end_date=None):
        """Search contracts with filters"""
        
        if self.contracts is None or len(self.contracts) == 0:
            print("No contract data loaded!")
            return pd.DataFrame()
        
        df = self.contracts.copy()
        
        # Search across all text columns
        if keyword:
            text_columns = df.select_dtypes(include=['object']).columns
            mask = False
            for col in text_columns:
                mask = mask | df[col].str.contains(keyword, case=False, na=False)
            df = df[mask]
        
        # Filter by amount if column exists
        amount_cols = [col for col in df.columns if 'amount' in col.lower() or 'obligated' in col.lower()]
        if amount_cols and (min_amount or max_amount):
            amount_col = amount_cols[0]
            if min_amount:
                df = df[pd.to_numeric(df[amount_col], errors='coerce') >= min_amount]
            if max_amount:
                df = df[pd.to_numeric(df[amount_col], errors='coerce') <= max_amount]
        
        # Filter by date if column exists
        date_cols = [col for col in df.columns if 'date' in col.lower()]
        if date_cols and (start_date or end_date):
            date_col = date_cols[0]
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            if start_date:
                df = df[df[date_col] >= start_date]
            if end_date:
                df = df[df[date_col] <= end_date]
        
        return df
    
    def get_summary(self):
        """Get summary statistics"""
        if self.contracts is None:
            return {}
        
        # Find amount column
        amount_cols = [col for col in self.contracts.columns if 'amount' in col.lower() or 'obligated' in col.lower()]
        
        summary = {
            'total_records': len(self.contracts),
            'unique_vendors': self.contracts['Recipient Name'].nunique() if 'Recipient Name' in self.contracts.columns else 'N/A',
            'source_files': self.contracts['source_file'].nunique()
        }
        
        if amount_cols:
            amount_col = amount_cols[0]
            amounts = pd.to_numeric(self.contracts[amount_col], errors='coerce')
            summary['total_amount'] = amounts.sum()
            summary['avg_amount'] = amounts.mean()
            summary['max_amount'] = amounts.max()
        
        return summary
    
    def get_top_vendors(self, n=10):
        """Get top vendors by total contract amount"""
        if self.contracts is None or 'Recipient Name' not in self.contracts.columns:
            return pd.DataFrame()
        
        amount_cols = [col for col in self.contracts.columns if 'amount' in col.lower() or 'obligated' in col.lower()]
        if not amount_cols:
            return pd.DataFrame()
        
        amount_col = amount_cols[0]
        
        df = self.contracts.copy()
        df[amount_col] = pd.to_numeric(df[amount_col], errors='coerce')
        
        top = df.groupby('Recipient Name')[amount_col].sum().sort_values(ascending=False).head(n)
        
        return top.reset_index()
    
    def export_results(self, results, filename):
        """Export search results to CSV"""
        results.to_csv(filename, index=False)
        print(f"✓ Exported {len(results)} results to {filename}")


def interactive_search():
    """Interactive search interface"""
    
    print("\n" + "="*70)
    print("CONTRACT DATA SEARCH TOOL")
    print("="*70)
    
    searcher = ContractSearcher()
    
    if searcher.contracts is None:
        print("\nNo contract data found. Download some CSVs from USASpending.gov first!")
        return
    
    while True:
        print("\n" + "="*70)
        print("WHAT DO YOU WANT TO DO?")
        print("="*70)
        print("\n1. Search contracts by keyword")
        print("2. Filter by amount")
        print("3. Show top vendors")
        print("4. Show summary statistics")
        print("5. Export search results")
        print("6. View available columns")
        print("7. Quit")
        
        choice = input("\nEnter number (1-7): ").strip()
        
        if choice == "1":
            keyword = input("\nSearch for: ").strip()
            results = searcher.search(keyword=keyword)
            
            print(f"\n{'='*70}")
            print(f"FOUND {len(results)} CONTRACTS")
            print("="*70)
            
            # Show first 20 results
            for idx, row in results.head(20).iterrows():
                print(f"\n{row.get('Recipient Name', 'Unknown')}")
                if 'Award ID' in row:
                    print(f"  Award ID: {row['Award ID']}")
                amount_cols = [col for col in results.columns if 'amount' in col.lower()]
                if amount_cols:
                    print(f"  Amount: ${row[amount_cols[0]]:,.2f}")
                if 'Start Date' in row:
                    print(f"  Date: {row['Start Date']}")
                if 'Description' in row and pd.notna(row['Description']):
                    desc = str(row['Description'])[:100]
                    print(f"  Description: {desc}...")
            
            if len(results) > 20:
                print(f"\n... and {len(results) - 20} more results")
            
            export = input("\nExport these results? (y/n): ").strip().lower()
            if export == 'y':
                filename = input("Filename: ").strip()
                if not filename.endswith('.csv'):
                    filename += '.csv'
                searcher.export_results(results, filename)
        
        elif choice == "2":
            min_amt = input("\nMinimum amount (or press Enter): ").strip()
            max_amt = input("Maximum amount (or press Enter): ").strip()
            
            min_amt = float(min_amt) if min_amt else None
            max_amt = float(max_amt) if max_amt else None
            
            results = searcher.search(min_amount=min_amt, max_amount=max_amt)
            
            print(f"\nFound {len(results)} contracts")
            print(f"Total: ${pd.to_numeric(results[results.columns[results.columns.str.contains('amount', case=False)][0]], errors='coerce').sum():,.2f}")
        
        elif choice == "3":
            n = input("\nHow many top vendors? (default 10): ").strip()
            n = int(n) if n else 10
            
            top = searcher.get_top_vendors(n)
            
            print(f"\n{'='*70}")
            print(f"TOP {n} VENDORS BY CONTRACT VALUE")
            print("="*70)
            
            for idx, row in top.iterrows():
                print(f"{idx+1}. {row['Recipient Name']}")
                print(f"   Total: ${row[row.index[1]]:,.2f}\n")
        
        elif choice == "4":
            summary = searcher.get_summary()
            
            print(f"\n{'='*70}")
            print("SUMMARY STATISTICS")
            print("="*70)
            
            for key, value in summary.items():
                if isinstance(value, float):
                    print(f"{key.replace('_', ' ').title()}: ${value:,.2f}")
                else:
                    print(f"{key.replace('_', ' ').title()}: {value}")
        
        elif choice == "5":
            keyword = input("\nSearch keyword (or press Enter for all): ").strip()
            keyword = keyword if keyword else None
            
            results = searcher.search(keyword=keyword)
            
            filename = input("Export filename: ").strip()
            if not filename.endswith('.csv'):
                filename += '.csv'
            
            searcher.export_results(results, filename)
        
        elif choice == "6":
            print(f"\n{'='*70}")
            print("AVAILABLE COLUMNS")
            print("="*70)
            
            for col in searcher.contracts.columns:
                print(f"  • {col}")
        
        elif choice == "7":
            print("\nGoodbye!")
            break
        
        else:
            print("\nInvalid choice.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    interactive_search()
