#!/usr/bin/env python3
"""
courtlistener_explorer.py — Reporter's toolkit for querying federal court data.

Uses the CourtListener REST API (v4) to search dockets, judges, attorneys,
opinions, and RECAP archive data. No PACER fees.

Setup:
    1. Get your API token from https://www.courtlistener.com/help/api/rest/
    2. Set it as an environment variable:
       export COURTLISTENER_TOKEN="your-token-here"
    
    Or pass it with --token on the command line.

Usage:
    # Search for dockets by party name
    python courtlistener_explorer.py dockets --party "Smith" --court "ilnd"

    # Search case law
    python courtlistener_explorer.py search --query "public defender caseload"

    # Look up a judge
    python courtlistener_explorer.py judges --name "Gull"

    # Look up attorneys on a docket
    python courtlistener_explorer.py attorneys --docket 12345678

    # List available federal courts
    python courtlistener_explorer.py courts

    # Interactive mode
    python courtlistener_explorer.py interactive
"""

import os
import sys
import json
import argparse
import textwrap
from urllib.parse import urlencode

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# ── Configuration ──

API_BASE = "https://www.courtlistener.com/api/rest/v4"
SITE_BASE = "https://www.courtlistener.com"


class CourtListenerClient:
    """Lightweight client for the CourtListener REST API v4."""

    def __init__(self, token):
        if not HAS_REQUESTS:
            raise ImportError("requests library required: pip install requests")
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Token {token}',
            'Accept': 'application/json',
        })

    def _get(self, endpoint, params=None, fields=None):
        """Make a GET request to the API."""
        url = f"{API_BASE}/{endpoint}/"
        if params is None:
            params = {}
        if fields:
            params['fields'] = ','.join(fields)
        
        resp = self.session.get(url, params=params, timeout=30)
        
        if resp.status_code == 401:
            print("ERROR: Authentication failed. Check your API token.")
            sys.exit(1)
        if resp.status_code == 429:
            print("ERROR: Rate limited. Wait a moment and try again.")
            return None
        if resp.status_code != 200:
            print(f"ERROR: HTTP {resp.status_code}")
            print(resp.text[:500])
            return None
        
        return resp.json()

    # ── Search ──

    def search(self, query, search_type='o', order_by='score desc', max_results=10):
        """
        Search CourtListener.
        
        search_type:
            'o'  = opinions/case law
            'r'  = RECAP docket entries  
            'rd' = RECAP documents
            'd'  = dockets
            'p'  = people/judges
            'oa' = oral arguments
        """
        params = {
            'q': query,
            'type': search_type,
            'order_by': order_by,
        }
        data = self._get('search', params)
        if data and 'results' in data:
            return data['results'][:max_results]
        return []

    # ── Dockets ──

    def search_dockets(self, party=None, court=None, judge=None, 
                       date_filed_after=None, date_filed_before=None,
                       docket_number=None, case_name=None, max_results=20):
        """Search dockets with filters."""
        params = {}
        if court:
            params['court'] = court
        if date_filed_after:
            params['date_filed__gte'] = date_filed_after
        if date_filed_before:
            params['date_filed__lte'] = date_filed_before
        if docket_number:
            params['docket_number'] = docket_number
        
        # For party/case_name/judge text search, use the search endpoint
        if party or case_name or judge:
            query_parts = []
            if party:
                query_parts.append(f'"{party}"')
            if case_name:
                query_parts.append(f'caseName:"{case_name}"')
            if judge:
                query_parts.append(f'assignedTo:"{judge}"')
            
            params['q'] = ' '.join(query_parts)
            params['type'] = 'd'
            data = self._get('search', params)
        else:
            data = self._get('dockets', params)
        
        if data and 'results' in data:
            return data['results'][:max_results]
        return []

    def get_docket(self, docket_id):
        """Get a specific docket by ID."""
        return self._get(f'dockets/{docket_id}')

    def get_docket_entries(self, docket_id, max_results=50):
        """Get docket entries for a specific docket."""
        params = {
            'docket': docket_id,
            'order_by': 'entry_number',
        }
        data = self._get('docket-entries', params,
                        fields=['id', 'entry_number', 'date_filed', 'description',
                               'recap_documents'])
        if data and 'results' in data:
            return data['results'][:max_results]
        return []

    # ── Parties & Attorneys ──

    def get_parties(self, docket_id):
        """Get parties for a docket."""
        params = {'docket': docket_id}
        data = self._get('parties', params)
        if data and 'results' in data:
            return data['results']
        return []

    def get_attorneys(self, docket_id):
        """Get attorneys for a docket."""
        params = {'docket': docket_id, 'filter_nested_results': 'True'}
        data = self._get('attorneys', params)
        if data and 'results' in data:
            return data['results']
        return []

    # ── Judges ──

    def search_judges(self, name=None, court=None, max_results=10):
        """Search for judges/people."""
        params = {'type': 'p'}
        query_parts = []
        if name:
            query_parts.append(name)
        if court:
            query_parts.append(f'court:"{court}"')
        params['q'] = ' '.join(query_parts) if query_parts else '*'
        
        data = self._get('search', params)
        if data and 'results' in data:
            return data['results'][:max_results]
        return []

    def get_person(self, person_id):
        """Get detailed info about a judge/person."""
        return self._get(f'people/{person_id}')

    # ── Courts ──

    def get_courts(self, jurisdiction=None):
        """List courts. jurisdiction: 'F' federal, 'FB' bankruptcy, etc."""
        params = {}
        if jurisdiction:
            params['jurisdiction'] = jurisdiction
        data = self._get('courts', params)
        if data and 'results' in data:
            return data['results']
        return []

    # ── Opinions ──

    def search_opinions(self, query, court=None, date_after=None, max_results=10):
        """Search case law opinions."""
        params = {
            'q': query,
            'type': 'o',
            'order_by': 'score desc',
        }
        if court:
            params['court'] = court
        if date_after:
            params['filed_after'] = date_after
        
        data = self._get('search', params)
        if data and 'results' in data:
            return data['results'][:max_results]
        return []

    # ── Financial Disclosures ──

    def get_financial_disclosures(self, person_id):
        """Get financial disclosures for a judge."""
        params = {'person': person_id}
        data = self._get('financial-disclosures', params)
        if data and 'results' in data:
            return data['results']
        return []


# ── Display Helpers ──

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def print_docket(d, index=None):
    """Display a docket search result."""
    prefix = f"  {index}." if index else "  •"
    name = d.get('caseName', d.get('case_name', 'Unknown'))
    court = d.get('court', d.get('court_id', ''))
    docket_num = d.get('docketNumber', d.get('docket_number', ''))
    date_filed = d.get('dateFiled', d.get('date_filed', ''))
    date_terminated = d.get('date_terminated', '')
    docket_id = d.get('docket_id', d.get('id', ''))
    
    print(f"{prefix} {name}")
    print(f"     Docket: {docket_num} | Court: {court}")
    print(f"     Filed: {date_filed}{' | Terminated: ' + date_terminated if date_terminated else ''}")
    if docket_id:
        print(f"     ID: {docket_id} | {SITE_BASE}/docket/{docket_id}/")
    
    # Show snippet if available
    snippet = d.get('snippet', '')
    if snippet:
        clean = snippet.replace('<mark>', '**').replace('</mark>', '**')
        wrapped = textwrap.fill(clean, width=72, initial_indent='     ', subsequent_indent='     ')
        print(wrapped)
    print()


def print_opinion(o, index=None):
    """Display an opinion search result."""
    prefix = f"  {index}." if index else "  •"
    name = o.get('caseName', 'Unknown')
    court = o.get('court', '')
    date = o.get('dateFiled', '')
    citation = o.get('citation', [])
    cite_str = ', '.join(citation) if isinstance(citation, list) else str(citation)
    cluster_id = o.get('cluster_id', '')
    
    print(f"{prefix} {name}")
    print(f"     Court: {court} | Date: {date}")
    if cite_str:
        print(f"     Citation: {cite_str}")
    if cluster_id:
        print(f"     {SITE_BASE}/opinion/{cluster_id}/")
    
    snippet = o.get('snippet', '')
    if snippet:
        clean = snippet.replace('<mark>', '**').replace('</mark>', '**')
        # Strip HTML tags
        import re
        clean = re.sub(r'<[^>]+>', '', clean)
        wrapped = textwrap.fill(clean[:300], width=72, initial_indent='     ', subsequent_indent='     ')
        print(wrapped)
    print()


def print_judge(j, index=None):
    """Display a judge search result."""
    prefix = f"  {index}." if index else "  •"
    name = j.get('name_full', f"{j.get('name_first', '')} {j.get('name_last', '')}".strip())
    court = j.get('court', '')
    dob = j.get('date_dob', j.get('dob_city', ''))
    political = j.get('political_affiliation', '')
    
    print(f"{prefix} {name}")
    if court:
        print(f"     Court: {court}")
    if political:
        print(f"     Political affiliation: {political}")
    
    # Position info from search results
    appointer = j.get('appointer', '')
    if appointer:
        print(f"     Appointed by: {appointer}")
    
    absolute_url = j.get('absolute_url', '')
    if absolute_url:
        print(f"     {SITE_BASE}{absolute_url}")
    print()


# ── Commands ──

def cmd_search(client, args):
    """Search case law."""
    print_header(f"Case Law Search: {args.query}")
    results = client.search_opinions(args.query, court=args.court, 
                                      date_after=args.after, max_results=args.limit)
    if not results:
        print("  No results found.")
        return
    for i, r in enumerate(results, 1):
        print_opinion(r, i)


def cmd_dockets(client, args):
    """Search dockets."""
    desc = args.party or args.case_name or args.judge or "all"
    print_header(f"Docket Search: {desc}")
    results = client.search_dockets(
        party=args.party, court=args.court, judge=args.judge,
        date_filed_after=args.after, date_filed_before=args.before,
        case_name=args.case_name, max_results=args.limit
    )
    if not results:
        print("  No results found.")
        return
    for i, r in enumerate(results, 1):
        print_docket(r, i)


def cmd_judges(client, args):
    """Search judges."""
    print_header(f"Judge Search: {args.name or 'all'}")
    results = client.search_judges(name=args.name, court=args.court, 
                                    max_results=args.limit)
    if not results:
        print("  No results found.")
        return
    for i, r in enumerate(results, 1):
        print_judge(r, i)


def cmd_courts(client, args):
    """List federal courts."""
    print_header("Federal Courts")
    results = client.get_courts(jurisdiction='F')
    if not results:
        print("  No results.")
        return
    for c in results:
        cid = c.get('id', '')
        name = c.get('full_name', c.get('short_name', ''))
        url = c.get('url', '')
        print(f"  {cid:<12s} {name}")


def cmd_docket_detail(client, args):
    """Get details for a specific docket."""
    print_header(f"Docket Detail: {args.docket_id}")
    
    docket = client.get_docket(args.docket_id)
    if not docket:
        print("  Docket not found.")
        return
    
    print(f"  Case: {docket.get('case_name', 'Unknown')}")
    print(f"  Number: {docket.get('docket_number', '')}")
    print(f"  Court: {docket.get('court', '')}")
    print(f"  Filed: {docket.get('date_filed', '')}")
    print(f"  Terminated: {docket.get('date_terminated', 'Active')}")
    print(f"  Judge: {docket.get('assigned_to_str', 'Unknown')}")
    print(f"  Referred to: {docket.get('referred_to_str', 'N/A')}")
    print(f"  Nature of suit: {docket.get('nature_of_suit', '')}")
    print(f"  Cause: {docket.get('cause', '')}")
    print(f"  Jurisdiction: {docket.get('jurisdiction_type', '')}")
    print(f"  URL: {SITE_BASE}/docket/{args.docket_id}/")
    
    # Get entries
    print(f"\n  Recent docket entries:")
    entries = client.get_docket_entries(args.docket_id, max_results=15)
    for entry in entries:
        num = entry.get('entry_number', '?')
        date = entry.get('date_filed', '')
        desc = entry.get('description', '')[:100]
        print(f"    #{num:<4s} {date}  {desc}")


def cmd_attorneys(client, args):
    """Get attorneys for a docket."""
    print_header(f"Attorneys on Docket {args.docket_id}")
    results = client.get_attorneys(args.docket_id)
    if not results:
        print("  No attorneys found.")
        return
    for att in results:
        name = att.get('name', 'Unknown')
        contact = att.get('contact_raw', '')
        print(f"  • {name}")
        if contact:
            for line in contact.split('\n')[:3]:
                print(f"    {line.strip()}")
        # Show parties represented
        parties = att.get('parties_represented', [])
        for p in parties[:3]:
            pname = p.get('name', '')
            role = p.get('party_type', {}).get('name', '') if isinstance(p.get('party_type'), dict) else ''
            print(f"    Represents: {pname} ({role})")
        print()


def cmd_interactive(client, args):
    """Interactive exploration mode."""
    print_header("CourtListener Interactive Explorer")
    print("  Commands:")
    print("    search <query>              Search case law")
    print("    dockets <party name>        Search dockets by party")
    print("    dockets-court <court> <party>  Search dockets in specific court")
    print("    judges <name>               Search judges")
    print("    docket <id>                 Get docket details")
    print("    attorneys <docket_id>       Get attorneys on a docket")
    print("    courts                      List federal courts")
    print("    recap <query>               Search RECAP docket entries")
    print("    quit                        Exit")
    print()
    
    while True:
        try:
            cmd = input("cl> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBye.")
            break
        
        if not cmd:
            continue
        if cmd.lower() in ('quit', 'exit', 'q'):
            print("Bye.")
            break
        
        parts = cmd.split(None, 1)
        action = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ''
        
        try:
            if action == 'search':
                results = client.search_opinions(arg, max_results=5)
                for i, r in enumerate(results, 1):
                    print_opinion(r, i)
            
            elif action == 'dockets':
                results = client.search_dockets(party=arg, max_results=10)
                for i, r in enumerate(results, 1):
                    print_docket(r, i)
            
            elif action == 'dockets-court':
                court_parts = arg.split(None, 1)
                if len(court_parts) < 2:
                    print("  Usage: dockets-court <court_id> <party name>")
                    continue
                court_id, party = court_parts
                results = client.search_dockets(party=party, court=court_id, max_results=10)
                for i, r in enumerate(results, 1):
                    print_docket(r, i)

            elif action == 'judges':
                results = client.search_judges(name=arg, max_results=5)
                for i, r in enumerate(results, 1):
                    print_judge(r, i)
            
            elif action == 'docket':
                if not arg.isdigit():
                    print("  Usage: docket <docket_id>")
                    continue
                docket = client.get_docket(int(arg))
                if docket:
                    print(f"\n  {docket.get('case_name', 'Unknown')}")
                    print(f"  Number: {docket.get('docket_number', '')}")
                    print(f"  Court: {docket.get('court', '')}")
                    print(f"  Filed: {docket.get('date_filed', '')}")
                    print(f"  Judge: {docket.get('assigned_to_str', '')}")
                    print(f"  {SITE_BASE}/docket/{arg}/")
                    print()
                    
                    entries = client.get_docket_entries(int(arg), max_results=10)
                    if entries:
                        print("  Recent entries:")
                        for e in entries:
                            num = e.get('entry_number', '?')
                            date = e.get('date_filed', '')
                            desc = e.get('description', '')[:80]
                            print(f"    #{num:<4} {date}  {desc}")
                    print()
            
            elif action == 'attorneys':
                if not arg.isdigit():
                    print("  Usage: attorneys <docket_id>")
                    continue
                results = client.get_attorneys(int(arg))
                for att in results[:10]:
                    name = att.get('name', 'Unknown')
                    print(f"  • {name}")
                print()
            
            elif action == 'courts':
                results = client.get_courts(jurisdiction='F')
                for c in results:
                    print(f"  {c.get('id', ''):<12s} {c.get('full_name', '')}")
                print()
            
            elif action == 'recap':
                results = client.search(arg, search_type='r', max_results=5)
                for i, r in enumerate(results, 1):
                    print(f"  {i}. [{r.get('dateFiled', '')}] {r.get('caseName', '')}")
                    print(f"     {r.get('docketNumber', '')} | {r.get('court', '')}")
                    desc = r.get('description', '')[:120]
                    if desc:
                        print(f"     {desc}")
                    print()
            
            else:
                print(f"  Unknown command: {action}")
                print("  Type 'quit' to exit or try: search, dockets, judges, docket, courts, recap")
        
        except Exception as e:
            print(f"  Error: {e}")


# ── Main ──

def main():
    parser = argparse.ArgumentParser(
        description='CourtListener Explorer — reporter toolkit for federal court data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          %(prog)s search --query "public defender ineffective assistance"
          %(prog)s dockets --party "Google" --court "cand"
          %(prog)s judges --name "Jackson"
          %(prog)s docket-detail --docket-id 67890123
          %(prog)s courts
          %(prog)s interactive
        """)
    )
    parser.add_argument('--token', default=os.environ.get('COURTLISTENER_TOKEN', ''),
                       help='API token (or set COURTLISTENER_TOKEN env var)')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # search
    p = subparsers.add_parser('search', help='Search case law opinions')
    p.add_argument('--query', '-q', required=True)
    p.add_argument('--court', '-c', default=None)
    p.add_argument('--after', default=None, help='Filed after date (YYYY-MM-DD)')
    p.add_argument('--limit', '-n', type=int, default=10)
    
    # dockets
    p = subparsers.add_parser('dockets', help='Search dockets')
    p.add_argument('--party', '-p', default=None)
    p.add_argument('--case-name', default=None)
    p.add_argument('--court', '-c', default=None)
    p.add_argument('--judge', '-j', default=None)
    p.add_argument('--after', default=None, help='Filed after (YYYY-MM-DD)')
    p.add_argument('--before', default=None, help='Filed before (YYYY-MM-DD)')
    p.add_argument('--limit', '-n', type=int, default=20)
    
    # judges
    p = subparsers.add_parser('judges', help='Search judges')
    p.add_argument('--name', required=True)
    p.add_argument('--court', '-c', default=None)
    p.add_argument('--limit', '-n', type=int, default=10)
    
    # courts
    subparsers.add_parser('courts', help='List federal courts')
    
    # docket-detail
    p = subparsers.add_parser('docket-detail', help='Get docket details')
    p.add_argument('--docket-id', required=True, type=int)
    
    # attorneys
    p = subparsers.add_parser('attorneys', help='Get attorneys for a docket')
    p.add_argument('--docket-id', required=True, type=int)
    
    # interactive
    subparsers.add_parser('interactive', help='Interactive exploration mode')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    token = args.token
    if not token:
        print("ERROR: No API token provided.")
        print("Set COURTLISTENER_TOKEN environment variable or use --token flag.")
        print("Get your token at: https://www.courtlistener.com/help/api/rest/")
        return
    
    client = CourtListenerClient(token)
    
    commands = {
        'search': cmd_search,
        'dockets': cmd_dockets,
        'judges': cmd_judges,
        'courts': cmd_courts,
        'docket-detail': cmd_docket_detail,
        'attorneys': cmd_attorneys,
        'interactive': cmd_interactive,
    }
    
    cmd_func = commands.get(args.command)
    if cmd_func:
        cmd_func(client, args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
