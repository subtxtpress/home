"""
Government Procurement Database Queries
Interfaces with USASpending.gov, FPDS.gov, and SAM.gov
"""

import requests
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
import time
import json

class ProcurementQueryService:
    """Service for querying government procurement databases"""
    
    def __init__(self):
        self.usaspending_base = "https://api.usaspending.gov/api/v2"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'DHS-Procurement-Research-API/1.0'
        })
    
    def search_usaspending(
        self, 
        vendor_name: str,
        agency: str = "Department of Homeland Security",
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Search USASpending.gov for contracts with a specific vendor
        
        Args:
            vendor_name: Company name to search for
            agency: Federal agency (default: DHS)
            limit: Max results to return
        
        Returns:
            Dictionary with contract awards
        """
        try:
            # USASpending API endpoint for searching
            url = f"{self.usaspending_base}/search/spending_by_award/"
            
            payload = {
                "filters": {
                    "recipient_search_text": [vendor_name],
                    "award_type_codes": ["A", "B", "C", "D"],  # Contract types
                    "agencies": [
                        {
                            "type": "awarding",
                            "tier": "toptier",
                            "name": agency
                        }
                    ]
                },
                "fields": [
                    "Award ID",
                    "Recipient Name", 
                    "Award Amount",
                    "Award Date",
                    "Description"
                ],
                "limit": limit,
                "page": 1,
                "sort": "Award Amount",
                "order": "desc"
            }
            
            response = self.session.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "vendor": vendor_name,
                    "agency": agency,
                    "results": data.get("results", []),
                    "total_found": data.get("page_metadata", {}).get("total", 0)
                }
            else:
                return {
                    "success": False,
                    "error": f"API returned status {response.status_code}",
                    "vendor": vendor_name
                }
        
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timed out",
                "vendor": vendor_name
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "vendor": vendor_name
            }
    
    def get_agency_spending_summary(
        self,
        agency: str = "Department of Homeland Security",
        fiscal_year: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get spending summary for an agency
        
        Args:
            agency: Federal agency name
            fiscal_year: Fiscal year (default: current)
        
        Returns:
            Spending summary data
        """
        if not fiscal_year:
            fiscal_year = datetime.now().year
        
        try:
            url = f"{self.usaspending_base}/agency/{agency}/budget_function/summary/"
            
            params = {
                "fiscal_year": fiscal_year
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "fiscal_year": fiscal_year,
                    "agency": agency,
                    "data": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": f"API returned status {response.status_code}"
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def search_fpds_contracts(
        self,
        vendor_name: str,
        agency: str = "HOMELAND SECURITY, DEPARTMENT OF"
    ) -> Dict[str, Any]:
        """
        Query FPDS (Federal Procurement Data System)
        Note: FPDS.gov doesn't have a public API, so this provides
        the search URL that would return results
        
        Args:
            vendor_name: Company name
            agency: Agency name in FPDS format
        
        Returns:
            Dictionary with search URL and parameters
        """
        # FPDS search URL construction
        base_url = "https://www.fpds.gov/ezsearch/fpdsportal"
        
        query = f'{vendor_name} DEPARTMENT_FULL_NAME:"{agency}"'
        
        return {
            "success": True,
            "vendor": vendor_name,
            "agency": agency,
            "search_url": f"{base_url}?q={query}&s=FPDS.GOV&templateName=1.5.3&indexName=awardfull",
            "note": "FPDS does not provide a public API. Visit this URL in a browser to see results."
        }
    
    def search_sam_contracts(
        self,
        keyword: str,
        agency_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search SAM.gov for contract opportunities
        Note: SAM.gov API requires authentication for most endpoints
        
        Args:
            keyword: Search term
            agency_code: Federal agency code (optional)
        
        Returns:
            Dictionary with search information
        """
        base_url = "https://sam.gov/search/"
        
        params = {
            "index": "opp",
            "page": "1",
            "q": keyword,
            "sort": "-relevance"
        }
        
        if agency_code:
            params["organizationId"] = agency_code
        
        search_url = base_url + "?" + "&".join([f"{k}={v}" for k, v in params.items()])
        
        return {
            "success": True,
            "keyword": keyword,
            "search_url": search_url,
            "note": "SAM.gov requires authentication for API access. Visit this URL in a browser for search results.",
            "api_info": "To use SAM.gov API, register at https://open.gsa.gov/api/sam-opportunities-api/"
        }
    
    def get_vendor_contract_history(
        self,
        vendor_name: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get contract history for a vendor from USASpending
        
        Args:
            vendor_name: Company name
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
        
        Returns:
            Contract history data
        """
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        
        try:
            url = f"{self.usaspending_base}/search/spending_by_award/"
            
            payload = {
                "filters": {
                    "recipient_search_text": [vendor_name],
                    "time_period": [
                        {
                            "start_date": start_date,
                            "end_date": end_date
                        }
                    ],
                    "award_type_codes": ["A", "B", "C", "D"]
                },
                "fields": [
                    "Award ID",
                    "Recipient Name",
                    "Award Amount", 
                    "Start Date",
                    "End Date",
                    "Awarding Agency",
                    "Awarding Sub Agency",
                    "Description"
                ],
                "limit": 100,
                "page": 1,
                "sort": "Start Date",
                "order": "desc"
            }
            
            response = self.session.post(url, json=payload, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                
                # Calculate totals
                total_amount = sum(
                    float(r.get("Award Amount", 0)) 
                    for r in results 
                    if r.get("Award Amount")
                )
                
                return {
                    "success": True,
                    "vendor": vendor_name,
                    "date_range": {
                        "start": start_date,
                        "end": end_date
                    },
                    "total_contracts": len(results),
                    "total_amount": total_amount,
                    "contracts": results
                }
            else:
                return {
                    "success": False,
                    "error": f"API returned status {response.status_code}",
                    "vendor": vendor_name
                }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "vendor": vendor_name
            }
    
    def compare_vendors(
        self,
        vendor_names: List[str],
        agency: str = "Department of Homeland Security"
    ) -> Dict[str, Any]:
        """
        Compare contract spending across multiple vendors
        
        Args:
            vendor_names: List of company names
            agency: Federal agency to filter by
        
        Returns:
            Comparative analysis
        """
        results = {}
        
        for vendor in vendor_names:
            time.sleep(0.5)  # Rate limiting
            vendor_data = self.search_usaspending(vendor, agency, limit=50)
            
            if vendor_data.get("success"):
                results[vendor] = {
                    "total_contracts": vendor_data.get("total_found", 0),
                    "sample_contracts": vendor_data.get("results", [])[:5]
                }
            else:
                results[vendor] = {
                    "error": vendor_data.get("error", "Unknown error")
                }
        
        return {
            "success": True,
            "agency": agency,
            "vendors_compared": len(vendor_names),
            "comparison": results
        }

# Example usage functions
def example_queries():
    """Example queries to demonstrate the service"""
    service = ProcurementQueryService()
    
    print("Example 1: Search for Palantir contracts with DHS")
    result = service.search_usaspending("Palantir Technologies")
    print(json.dumps(result, indent=2))
    
    print("\nExample 2: Get FPDS search URL for Anduril")
    result = service.search_fpds_contracts("Anduril")
    print(json.dumps(result, indent=2))
    
    print("\nExample 3: Search SAM.gov for surveillance contracts")
    result = service.search_sam_contracts("surveillance")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    example_queries()
