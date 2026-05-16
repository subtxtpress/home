"""
DHS Procurement Research API Client
Simple Python client for investigative journalism workflows
"""

import requests
from typing import Optional, List, Dict, Any
from datetime import datetime

class DHSProcurementClient:
    """
    Client for DHS Procurement Research API
    
    Usage:
        client = DHSProcurementClient()
        vendors = client.search_vendors("surveillance")
        contracts = client.get_live_contracts("Palantir")
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
    
    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """Make GET request to API"""
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    # ===== Dataset Queries =====
    
    def search_vendors(
        self,
        query: Optional[str] = None,
        category: Optional[str] = None,
        prime_only: bool = False,
        ai_only: bool = False,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Search vendor database
        
        Args:
            query: Search term
            category: Filter by category
            prime_only: Only DHS prime contractors
            ai_only: Only AI/ML vendors
            limit: Max results
        
        Returns:
            Dictionary with vendor results
        """
        params = {
            "limit": limit,
            "prime_only": prime_only,
            "ai_only": ai_only
        }
        if query:
            params["q"] = query
        if category:
            params["category"] = category
        
        return self._get("/vendors", params)
    
    def get_vendor(self, ref_id: str) -> Dict[str, Any]:
        """
        Get detailed vendor profile
        
        Args:
            ref_id: Vendor reference ID (e.g., "TECH002")
        
        Returns:
            Complete vendor profile
        """
        return self._get(f"/vendors/{ref_id}")
    
    def full_text_search(self, query: str, limit: int = 20) -> Dict[str, Any]:
        """
        Full text search across all vendor data
        
        Args:
            query: Search term
            limit: Max results
        
        Returns:
            Search results
        """
        return self._get("/search", {"q": query, "limit": limit})
    
    def get_prime_contractors(self) -> List[Dict]:
        """Get all DHS prime contractors"""
        result = self._get("/prime-contractors")
        return result.get("contractors", [])
    
    def get_ai_vendors(self) -> List[Dict]:
        """Get all vendors using AI/ML"""
        result = self._get("/ai-vendors")
        return result.get("vendors", [])
    
    def get_categories(self) -> List[str]:
        """Get all product/service categories"""
        result = self._get("/categories")
        return result.get("categories", [])
    
    def get_stats(self) -> Dict[str, Any]:
        """Get dataset statistics"""
        return self._get("/stats")
    
    # ===== Live Government Queries =====
    
    def get_live_contracts(
        self,
        vendor_name: str,
        agency: str = "Department of Homeland Security",
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Query USASpending.gov for live contract data
        
        Args:
            vendor_name: Company name
            agency: Federal agency
            limit: Max results
        
        Returns:
            Live contract data
        """
        return self._get(
            f"/live/contracts/{vendor_name}",
            {"agency": agency, "limit": limit}
        )
    
    def get_contract_history(
        self,
        vendor_name: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get contract history for a vendor
        
        Args:
            vendor_name: Company name
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
        
        Returns:
            Contract history with totals
        """
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        return self._get(f"/live/history/{vendor_name}", params)
    
    def compare_vendors(
        self,
        vendor_names: List[str],
        agency: str = "Department of Homeland Security"
    ) -> Dict[str, Any]:
        """
        Compare contract spending across vendors
        
        Args:
            vendor_names: List of company names
            agency: Federal agency
        
        Returns:
            Comparative analysis
        """
        vendors_str = ",".join(vendor_names)
        return self._get(
            "/live/compare",
            {"vendors": vendors_str, "agency": agency}
        )
    
    def get_fpds_search_url(self, vendor_name: str) -> str:
        """
        Get FPDS.gov search URL for vendor
        
        Args:
            vendor_name: Company name
        
        Returns:
            Search URL
        """
        result = self._get(f"/live/fpds/{vendor_name}")
        return result.get("search_url", "")
    
    def get_enriched_vendor(self, ref_id: str) -> Dict[str, Any]:
        """
        Get vendor profile with live contract data
        
        Args:
            ref_id: Vendor reference ID
        
        Returns:
            Enriched profile combining dataset + live data
        """
        return self._get(f"/enriched/{ref_id}")
    
    # ===== Convenience Methods for Journalists =====
    
    def investigate_vendor(self, vendor_name: str) -> Dict[str, Any]:
        """
        Get comprehensive investigation package for a vendor
        
        Args:
            vendor_name: Company name
        
        Returns:
            Dictionary with all available data
        """
        investigation = {
            "vendor_name": vendor_name,
            "timestamp": datetime.now().isoformat()
        }
        
        # Search for vendor in dataset
        search_results = self.search_vendors(vendor_name, limit=1)
        if search_results.get("vendors"):
            vendor = search_results["vendors"][0]
            investigation["dataset_profile"] = vendor
            
            # Get detailed profile if we have ref
            if vendor.get("ref"):
                investigation["detailed_profile"] = self.get_vendor(vendor["ref"])
        
        # Get live contracts
        try:
            investigation["live_contracts"] = self.get_live_contracts(vendor_name)
        except:
            investigation["live_contracts"] = {"error": "Could not fetch live data"}
        
        # Get FPDS search URL
        investigation["fpds_search"] = self.get_fpds_search_url(vendor_name)
        
        return investigation
    
    def track_technology(self, tech_keyword: str) -> Dict[str, Any]:
        """
        Track vendors working on specific technology
        
        Args:
            tech_keyword: Technology keyword (e.g., "facial recognition", "drone")
        
        Returns:
            Dictionary with vendors and contracts related to technology
        """
        return {
            "technology": tech_keyword,
            "vendors": self.search_vendors(tech_keyword, limit=50),
            "full_text_results": self.full_text_search(tech_keyword, limit=30)
        }
    
    def build_foia_target_list(
        self,
        category: Optional[str] = None,
        prime_only: bool = True
    ) -> List[Dict]:
        """
        Build list of vendors for FOIA requests
        
        Args:
            category: Technology category
            prime_only: Only prime contractors
        
        Returns:
            List of vendors with contract info
        """
        vendors = self.search_vendors(
            category=category,
            prime_only=prime_only,
            limit=100
        )
        
        target_list = []
        for vendor in vendors.get("vendors", []):
            target = {
                "vendor_name": vendor["name"],
                "ref": vendor["ref"],
                "categories": vendor.get("categories"),
                "usaspending_link": vendor.get("usaspending_link"),
                "is_prime": vendor.get("is_prime_contractor"),
                "uses_ai": vendor.get("uses_ai_ml")
            }
            target_list.append(target)
        
        return target_list


# Example usage
def example_investigations():
    """Example investigation workflows"""
    
    client = DHSProcurementClient()
    
    print("=" * 60)
    print("Example 1: Investigate a specific vendor")
    print("=" * 60)
    investigation = client.investigate_vendor("Palantir")
    print(f"Found: {investigation.get('dataset_profile', {}).get('name')}")
    print(f"Is Prime Contractor: {investigation.get('dataset_profile', {}).get('is_prime_contractor')}")
    print()
    
    print("=" * 60)
    print("Example 2: Track surveillance technology")
    print("=" * 60)
    surveillance = client.track_technology("surveillance")
    print(f"Found {surveillance['vendors']['count']} vendors")
    print()
    
    print("=" * 60)
    print("Example 3: Build FOIA target list")
    print("=" * 60)
    targets = client.build_foia_target_list(prime_only=True)
    print(f"Generated target list with {len(targets)} vendors")
    for target in targets[:5]:
        print(f"  - {target['vendor_name']}")
    print()
    
    print("=" * 60)
    print("Example 4: Compare major contractors")
    print("=" * 60)
    comparison = client.compare_vendors([
        "Palantir Technologies",
        "Accenture",
        "Anduril"
    ])
    print(f"Compared {comparison['vendors_compared']} vendors")


if __name__ == "__main__":
    example_investigations()
