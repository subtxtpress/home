#!/usr/bin/env python3
"""
courtlistener_toolkit.py — Enhanced reporter's toolkit for federal court data.

Builds on courtlistener_explorer.py with:
  - Full cursor pagination (get ALL results, not just first page)
  - Unified case lookup (one command → full picture)
  - CSV/JSON export on every command
  - Advanced search with named filters

Setup:
    export COURTLISTENER_TOKEN="your-token-here"

Usage:
    python courtlistener_toolkit.py case 67890123
    python courtlistener_toolkit.py case 67890123 --export csv
    python courtlistener_toolkit.py search "ineffective assistance of counsel" --court cand
    python courtlistener_toolkit.py dockets --party "Google" --court cand --export json
    python courtlistener_toolkit.py judge "Chutkan" --export csv
    python courtlistener_toolkit.py interactive
"""

import os
import sys
import csv
import json
import time
import argparse
import textwrap
import re
from datetime import datetime, date
from io import StringIO

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


# ── Configuration ──

API_BASE = "https://www.courtlistener.com/api/rest/v4"
SITE_BASE = "https://www.courtlistener.com"
DEFAULT_PAGE_SIZE = 20
MAX_PAGES = 50  # safety limit to avoid runaway pagination


class CourtListenerClient:
    """Client for the CourtListener REST API v4 with full pagination support."""

    def __init__(self, token):
        if not HAS_REQUESTS:
            raise ImportError("requests library required: pip install requests")
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Token {token}',
            'Accept': 'application/json',
        })
        self._request_count = 0

    def _get(self, endpoint, params=None, fields=None):
        """Single API request. Returns parsed JSON or None."""
        url = f"{API_BASE}/{endpoint}/"
        if params is None:
            params = {}
        if fields:
            params['fields'] = ','.join(fields)

        self._request_count += 1
        try:
            resp = self.session.get(url, params=params, timeout=30)
        except requests.exceptions.RequestException as e:
            print(f"  Network error: {e}")
            return None

        if resp.status_code == 401:
            print("ERROR: Authentication failed. Check your API token.")
            sys.exit(1)
        if resp.status_code == 429:
            # Rate limited — wait and retry once
            retry_after = int(resp.headers.get('Retry-After', 5))
            print(f"  Rate limited. Waiting {retry_after}s...")
            time.sleep(retry_after)
            resp = self.session.get(url, params=params, timeout=30)
            if resp.status_code != 200:
                print(f"  Still rate limited after retry.")
                return None
        if resp.status_code == 403:
            # Permission denied — free account can't access this endpoint
            return {'_forbidden': True, '_endpoint': endpoint}
        if resp.status_code != 200:
            print(f"  ERROR: HTTP {resp.status_code}")
            try:
                print(f"  {resp.text[:300]}")
            except Exception:
                pass
            return None

        return resp.json()

    def _get_url(self, url):
        """GET a full URL (for pagination cursor following)."""
        self._request_count += 1
        try:
            resp = self.session.get(url, timeout=30)
        except requests.exceptions.RequestException as e:
            print(f"  Network error: {e}")
            return None

        if resp.status_code == 429:
            retry_after = int(resp.headers.get('Retry-After', 5))
            print(f"  Rate limited. Waiting {retry_after}s...")
            time.sleep(retry_after)
            resp = self.session.get(url, timeout=30)
        if resp.status_code != 200:
            return None
        return resp.json()

    def _get_paginated(self, endpoint, params=None, fields=None,
                       max_results=None, show_progress=False):
        """
        Follow cursor pagination to collect results across pages.

        max_results: stop after collecting this many (None = get everything)
        show_progress: print page count as we go
        """
        all_results = []
        page = 0

        data = self._get(endpoint, params=params, fields=fields)
        if not data or 'results' not in data:
            return all_results

        total = data.get('count', '?')
        all_results.extend(data['results'])
        page += 1

        if show_progress:
            print(f"  Page {page} — {len(all_results)}/{total} results", end='\r')

        while data.get('next') and page < MAX_PAGES:
            if max_results and len(all_results) >= max_results:
                break

            data = self._get_url(data['next'])
            if not data or 'results' not in data:
                break

            all_results.extend(data['results'])
            page += 1

            if show_progress:
                print(f"  Page {page} — {len(all_results)}/{total} results", end='\r')

        if show_progress:
            print()  # newline after progress

        if max_results:
            return all_results[:max_results]
        return all_results

    # ── Search ──

    def search(self, query, search_type='o', court=None, date_after=None,
               date_before=None, order_by='score desc', max_results=20):
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
        if court:
            params['court'] = court
        if date_after:
            params['filed_after'] = date_after
        if date_before:
            params['filed_before'] = date_before

        data = self._get('search', params)
        if data and 'results' in data:
            return data['results'][:max_results], data.get('count', 0)
        return [], 0

    # ── Dockets ──

    def search_dockets(self, query=None, party=None, court=None, judge=None,
                       case_name=None, docket_number=None,
                       date_after=None, date_before=None,
                       nature_of_suit=None, max_results=20):
        """Search dockets with filters."""
        query_parts = []
        if query:
            query_parts.append(query)
        if party:
            query_parts.append(f'"{party}"')
        if case_name:
            query_parts.append(f'caseName:"{case_name}"')
        if judge:
            query_parts.append(f'assignedTo:"{judge}"')

        params = {
            'type': 'd',
        }
        if query_parts:
            params['q'] = ' '.join(query_parts)
        if court:
            params['court'] = court
        if date_after:
            params['filed_after'] = date_after
        if date_before:
            params['filed_before'] = date_before
        if docket_number:
            params['docket_number'] = docket_number

        data = self._get('search', params)
        if data and 'results' in data:
            return data['results'][:max_results], data.get('count', 0)
        return [], 0

    def get_docket(self, docket_id):
        """Get a specific docket by ID."""
        return self._get(f'dockets/{docket_id}')

    def get_docket_entries(self, docket_id, max_results=None, show_progress=False):
        """Get all docket entries for a case."""
        params = {
            'docket': docket_id,
            'order_by': 'entry_number',
        }
        return self._get_paginated(
            'docket-entries', params=params,
            fields=['id', 'entry_number', 'date_filed', 'description',
                    'recap_documents'],
            max_results=max_results,
            show_progress=show_progress,
        )

    # ── Parties & Attorneys ──

    def get_parties(self, docket_id):
        """Get all parties for a docket with nested attorney info."""
        params = {'docket': docket_id}
        return self._get_paginated('parties', params=params)

    def get_attorneys(self, docket_id):
        """Get all attorneys for a docket."""
        params = {'docket': docket_id, 'filter_nested_results': 'True'}
        return self._get_paginated('attorneys', params=params)

    # ── Judges ──

    def search_judges(self, name=None, court=None, max_results=20):
        """Search for judges."""
        params = {'type': 'p'}
        query_parts = []
        if name:
            query_parts.append(name)
        if court:
            query_parts.append(f'court:"{court}"')
        params['q'] = ' '.join(query_parts) if query_parts else '*'

        data = self._get('search', params)
        if data and 'results' in data:
            return data['results'][:max_results], data.get('count', 0)
        return [], 0

    def get_person(self, person_id):
        """Get detailed info about a judge/person."""
        return self._get(f'people/{person_id}')

    # ── Courts ──

    def get_courts(self, jurisdiction=None):
        """List courts."""
        params = {}
        if jurisdiction:
            params['jurisdiction'] = jurisdiction
        return self._get_paginated('courts', params=params)

    # ── Opinions ──

    def search_opinions(self, query, court=None, date_after=None,
                        date_before=None, max_results=20):
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
        if date_before:
            params['filed_before'] = date_before

        data = self._get('search', params)
        if data and 'results' in data:
            return data['results'][:max_results], data.get('count', 0)
        return [], 0

    # ── Unified Case Lookup ──

    def get_full_case(self, docket_id, max_entries=100):
        """
        Pull everything about a case. Handles 403s gracefully —
        if detailed endpoints are restricted, falls back to what's available.

        Returns a dict with keys: docket, parties, attorneys, entries, warnings
        """
        warnings = []

        print(f"  Fetching docket {docket_id}...")
        docket = self.get_docket(docket_id)
        if not docket:
            return None
        if isinstance(docket, dict) and docket.get('_forbidden'):
            print("  Docket endpoint requires membership. Trying search...")
            # Try finding basic info via search
            return None

        print(f"  Fetching parties...")
        parties = self.get_parties(docket_id)
        if not parties:
            warnings.append("parties (requires membership)")

        print(f"  Fetching attorneys...")
        attorneys = self.get_attorneys(docket_id)
        if not attorneys:
            warnings.append("attorneys (requires membership)")

        print(f"  Fetching docket entries...")
        entries = self.get_docket_entries(docket_id, max_results=max_entries,
                                          show_progress=True)
        if not entries:
            warnings.append("docket entries (requires membership)")

            # Fallback: try RECAP search using case name
            case_name = docket.get('case_name', '')
            if case_name:
                print(f"  Trying RECAP search as fallback...")
                recap_results, _ = self.search_recap(case_name, max_results=20)
                # Filter to matching docket
                docket_num = docket.get('docket_number', '')
                if docket_num and recap_results:
                    matched = [r for r in recap_results
                               if r.get('docketNumber', '') == docket_num]
                    if matched:
                        entries = matched
                        warnings[-1] = "docket entries (partial, from RECAP search)"

        return {
            'docket': docket,
            'parties': parties,
            'attorneys': attorneys,
            'entries': entries,
            'warnings': warnings,
        }

    # ── Financial Disclosures ──

    def get_financial_disclosures(self, person_id):
        """Get financial disclosures for a judge."""
        params = {'person': person_id}
        return self._get_paginated('financial-disclosures', params=params)

    # ── RECAP ──

    def search_recap(self, query, court=None, max_results=20):
        """Search RECAP docket entries."""
        params = {
            'q': query,
            'type': 'r',
        }
        if court:
            params['court'] = court

        data = self._get('search', params)
        if data and 'results' in data:
            return data['results'][:max_results], data.get('count', 0)
        return [], 0


# ── Export ──

class Exporter:
    """Export results to CSV or JSON."""

    @staticmethod
    def to_json(data, filepath):
        """Write data to JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str)
        print(f"  Exported to {filepath}")

    @staticmethod
    def to_csv(rows, filepath, fieldnames=None):
        """Write list of dicts to CSV."""
        if not rows:
            print("  No data to export.")
            return
        if fieldnames is None:
            fieldnames = list(rows[0].keys())

        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
            writer.writeheader()
            writer.writerows(rows)
        print(f"  Exported {len(rows)} rows to {filepath}")

    @staticmethod
    def flatten_docket(d):
        """Flatten a docket search result or API result into a flat dict for CSV."""
        return {
            'case_name': d.get('caseName', d.get('case_name', '')),
            'docket_number': d.get('docketNumber', d.get('docket_number', '')),
            'court': d.get('court', d.get('court_id', '')),
            'date_filed': d.get('dateFiled', d.get('date_filed', '')),
            'date_terminated': d.get('date_terminated', ''),
            'judge': d.get('assignedTo', d.get('assigned_to_str', '')),
            'nature_of_suit': d.get('suitNature', d.get('nature_of_suit', '')),
            'cause': d.get('cause', ''),
            'docket_id': d.get('docket_id', d.get('id', '')),
            'url': f"{SITE_BASE}/docket/{d.get('docket_id', d.get('id', ''))}/",
        }

    @staticmethod
    def flatten_opinion(o):
        """Flatten an opinion search result for CSV."""
        citation = o.get('citation', [])
        cite_str = ', '.join(citation) if isinstance(citation, list) else str(citation)
        return {
            'case_name': o.get('caseName', ''),
            'court': o.get('court', ''),
            'date_filed': o.get('dateFiled', ''),
            'citation': cite_str,
            'cite_count': o.get('citeCount', 0),
            'cluster_id': o.get('cluster_id', ''),
            'url': f"{SITE_BASE}/opinion/{o.get('cluster_id', '')}/",
        }

    @staticmethod
    def flatten_entry(e):
        """Flatten a docket entry for CSV."""
        docs = e.get('recap_documents', [])
        doc_count = len(docs) if isinstance(docs, list) else 0
        return {
            'entry_number': e.get('entry_number', ''),
            'date_filed': e.get('date_filed', ''),
            'description': e.get('description', ''),
            'document_count': doc_count,
        }

    @staticmethod
    def flatten_judge(j):
        """Flatten a judge search result for CSV."""
        return {
            'name': j.get('name_full',
                          f"{j.get('name_first', '')} {j.get('name_last', '')}".strip()),
            'court': j.get('court', ''),
            'political_affiliation': j.get('political_affiliation', ''),
            'appointer': j.get('appointer', ''),
            'dob': j.get('date_dob', ''),
            'url': f"{SITE_BASE}{j.get('absolute_url', '')}",
        }


# ── Display Helpers ──

def print_header(text):
    width = min(len(text) + 4, 70)
    print(f"\n{'─' * width}")
    print(f"  {text}")
    print(f"{'─' * width}\n")


def print_count(count, label="results"):
    if count and count != '?':
        print(f"  {count:,} total {label} found\n")


def clean_snippet(text):
    """Strip HTML from snippet text."""
    if not text:
        return ''
    text = text.replace('<mark>', '').replace('</mark>', '')
    text = re.sub(r'<[^>]+>', '', text)
    return text.strip()


def clean_court(court_val):
    """Clean court value — API returns URLs, search returns plain IDs."""
    court_str = str(court_val)
    if '/courts/' in court_str:
        return court_str.rstrip('/').split('/')[-1]
    return court_str


def print_docket(d, index=None):
    prefix = f"  {index}." if index else "  •"
    name = d.get('caseName', d.get('case_name', 'Unknown'))
    court = clean_court(d.get('court', d.get('court_id', '')))
    docket_num = d.get('docketNumber', d.get('docket_number', ''))
    date_filed = d.get('dateFiled', d.get('date_filed', ''))
    date_terminated = d.get('date_terminated', '')
    docket_id = d.get('docket_id', d.get('id', ''))
    judge = d.get('assignedTo', d.get('assigned_to_str', ''))

    print(f"{prefix} {name}")
    print(f"     {docket_num} | {court}")
    status_parts = [f"Filed: {date_filed}"]
    if date_terminated:
        status_parts.append(f"Terminated: {date_terminated}")
    if judge:
        status_parts.append(f"Judge: {judge}")
    print(f"     {' | '.join(status_parts)}")

    if docket_id:
        print(f"     {SITE_BASE}/docket/{docket_id}/")

    snippet = d.get('snippet', '')
    if snippet:
        clean = clean_snippet(snippet)
        if clean:
            wrapped = textwrap.fill(clean[:200], width=72,
                                     initial_indent='     ',
                                     subsequent_indent='     ')
            print(wrapped)
    print()


def print_opinion(o, index=None):
    prefix = f"  {index}." if index else "  •"
    name = o.get('caseName', 'Unknown')
    court = o.get('court', '')
    date_val = o.get('dateFiled', '')
    citation = o.get('citation', [])
    cite_str = ', '.join(citation) if isinstance(citation, list) else str(citation)
    cluster_id = o.get('cluster_id', '')
    cite_count = o.get('citeCount', 0)

    print(f"{prefix} {name}")
    print(f"     {court} | {date_val}")
    parts = []
    if cite_str:
        parts.append(f"Cite: {cite_str}")
    if cite_count:
        parts.append(f"Cited {cite_count}x")
    if parts:
        print(f"     {' | '.join(parts)}")
    if cluster_id:
        print(f"     {SITE_BASE}/opinion/{cluster_id}/")

    snippet = o.get('snippet', '')
    if snippet:
        clean = clean_snippet(snippet)
        if clean:
            wrapped = textwrap.fill(clean[:250], width=72,
                                     initial_indent='     ',
                                     subsequent_indent='     ')
            print(wrapped)
    print()


def print_judge(j, index=None):
    prefix = f"  {index}." if index else "  •"
    name = j.get('name_full',
                  f"{j.get('name_first', '')} {j.get('name_last', '')}".strip())
    court = j.get('court', '')
    political = j.get('political_affiliation', '')
    appointer = j.get('appointer', '')

    print(f"{prefix} {name}")
    parts = []
    if court:
        parts.append(f"Court: {court}")
    if political:
        parts.append(f"Affiliation: {political}")
    if appointer:
        parts.append(f"Appointed by: {appointer}")
    if parts:
        print(f"     {' | '.join(parts)}")

    absolute_url = j.get('absolute_url', '')
    if absolute_url:
        print(f"     {SITE_BASE}{absolute_url}")
    print()


def print_full_case(case_data):
    """Display unified case data."""
    d = case_data['docket']
    parties = case_data['parties']
    attorneys = case_data['attorneys']
    entries = case_data['entries']
    warnings = case_data.get('warnings', [])

    print_header(d.get('case_name', 'Unknown Case'))

    # Case metadata
    print(f"  Docket:        {d.get('docket_number', '')}")
    court = clean_court(d.get('court', ''))
    print(f"  Court:         {court}")
    print(f"  Filed:         {d.get('date_filed', '')}")
    terminated = d.get('date_terminated', '')
    print(f"  Status:        {'Terminated ' + terminated if terminated else 'Active'}")
    judge = d.get('assigned_to_str', '')
    if judge:
        print(f"  Judge:         {judge}")
    referred = d.get('referred_to_str', '')
    if referred:
        print(f"  Referred to:   {referred}")
    nos = d.get('nature_of_suit', '')
    if nos:
        print(f"  Nature of suit: {nos}")
    cause = d.get('cause', '')
    if cause:
        print(f"  Cause:         {cause}")
    jurisdiction = d.get('jurisdiction_type', '')
    if jurisdiction:
        print(f"  Jurisdiction:  {jurisdiction}")
    docket_id = d.get('id', '')
    print(f"  URL:           {SITE_BASE}/docket/{docket_id}/")

    # Warnings about restricted data
    if warnings:
        print(f"\n  ⚠ Could not fetch: {', '.join(warnings)}")
        print(f"  Tip: Join Free Law Project for full API access (free.law/membership)")

    # Parties
    if parties:
        print(f"\n  Parties ({len(parties)}):")
        for p in parties:
            pname = p.get('name', 'Unknown')
            ptype = ''
            party_type = p.get('party_type')
            if isinstance(party_type, dict):
                ptype = party_type.get('name', '')
            elif isinstance(party_type, str):
                ptype = party_type
            print(f"    • {pname} ({ptype})" if ptype else f"    • {pname}")

            # Nested attorneys
            atts = p.get('attorneys', [])
            for a in atts[:5]:
                aname = a.get('name', '')
                if aname:
                    role = ''
                    roles = a.get('roles', [])
                    if roles and isinstance(roles, list):
                        role_names = []
                        for r in roles:
                            if isinstance(r, dict):
                                role_names.append(r.get('role', ''))
                            elif isinstance(r, str):
                                role_names.append(r)
                        role = ', '.join(filter(None, role_names))
                    print(f"      Attorney: {aname}" + (f" [{role}]" if role else ""))

    # Attorneys (top-level, if nested didn't cover it)
    if attorneys and not parties:
        print(f"\n  Attorneys ({len(attorneys)}):")
        for att in attorneys[:20]:
            name = att.get('name', 'Unknown')
            contact = att.get('contact_raw', '')
            print(f"    • {name}")
            if contact:
                first_line = contact.split('\n')[0].strip()
                if first_line:
                    print(f"      {first_line}")

    # Docket entries (from API or RECAP search fallback)
    if entries:
        print(f"\n  Docket Entries ({len(entries)}):")
        for e in entries:
            # Handle both API format and RECAP search format
            num = e.get('entry_number', e.get('entry_id', '?'))
            edate = e.get('date_filed', e.get('dateFiled', ''))
            desc = e.get('description', '')
            if len(desc) > 90:
                desc = desc[:87] + '...'
            print(f"    #{str(num):<4s} {edate}  {desc}")

            # Show attached documents (API format only)
            docs = e.get('recap_documents', [])
            if isinstance(docs, list):
                for doc in docs[:3]:
                    if isinstance(doc, dict):
                        doc_desc = doc.get('description', '')
                        if doc_desc:
                            print(f"          └ {doc_desc[:70]}")

    print()


def make_export_filename(prefix, fmt):
    """Generate timestamped export filename."""
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"{prefix}_{ts}.{fmt}"


def handle_export(data, flatten_fn, prefix, fmt):
    """Handle --export flag for any command."""
    if fmt == 'json':
        filepath = make_export_filename(prefix, 'json')
        Exporter.to_json(data, filepath)
        return filepath
    elif fmt == 'csv':
        filepath = make_export_filename(prefix, 'csv')
        rows = [flatten_fn(item) for item in data]
        Exporter.to_csv(rows, filepath)
        return filepath
    return None


# ── Commands ──

def cmd_case(client, args):
    """Unified case lookup — everything about one docket."""
    docket_id = args.docket_id
    max_entries = getattr(args, 'max_entries', 100)

    case_data = client.get_full_case(docket_id, max_entries=max_entries)
    if not case_data:
        print("  Case not found.")
        return

    print_full_case(case_data)
    print(f"  API requests used: {client._request_count}")

    # Export
    fmt = getattr(args, 'export', None)
    if fmt:
        if fmt == 'json':
            filepath = make_export_filename(f'case_{docket_id}', 'json')
            # Build a clean export structure
            export_data = {
                'docket': case_data['docket'],
                'parties': case_data['parties'],
                'attorneys': case_data['attorneys'],
                'entries': case_data['entries'],
                'exported_at': datetime.now().isoformat(),
            }
            Exporter.to_json(export_data, filepath)
        elif fmt == 'csv':
            # CSV: export docket entries (most useful tabular format)
            filepath = make_export_filename(f'case_{docket_id}_entries', 'csv')
            rows = [Exporter.flatten_entry(e) for e in case_data['entries']]
            Exporter.to_csv(rows, filepath)


def cmd_search(client, args):
    """Search case law opinions."""
    print_header(f"Search: {args.query}")
    results, count = client.search_opinions(
        args.query, court=args.court,
        date_after=args.after, date_before=args.before,
        max_results=args.limit,
    )
    print_count(count)

    if not results:
        print("  No results found.")
        return

    for i, r in enumerate(results, 1):
        print_opinion(r, i)

    fmt = getattr(args, 'export', None)
    if fmt:
        handle_export(results, Exporter.flatten_opinion, 'opinions', fmt)


def cmd_dockets(client, args):
    """Search dockets."""
    desc = args.query or args.party or args.judge or "all"
    print_header(f"Dockets: {desc}")

    results, count = client.search_dockets(
        query=args.query, party=args.party, court=args.court,
        judge=args.judge, date_after=args.after, date_before=args.before,
        max_results=args.limit,
    )
    print_count(count)

    if not results:
        print("  No results found.")
        return

    for i, r in enumerate(results, 1):
        print_docket(r, i)

    fmt = getattr(args, 'export', None)
    if fmt:
        handle_export(results, Exporter.flatten_docket, 'dockets', fmt)


def cmd_judges(client, args):
    """Search judges."""
    print_header(f"Judges: {args.name or 'all'}")
    results, count = client.search_judges(name=args.name, court=args.court,
                                           max_results=args.limit)
    print_count(count)

    if not results:
        print("  No results found.")
        return

    for i, r in enumerate(results, 1):
        print_judge(r, i)

    fmt = getattr(args, 'export', None)
    if fmt:
        handle_export(results, Exporter.flatten_judge, 'judges', fmt)


def cmd_courts(client, args):
    """List courts."""
    jurisdiction = getattr(args, 'jurisdiction', 'F')
    print_header("Courts")
    results = client.get_courts(jurisdiction=jurisdiction)
    if not results:
        print("  No results.")
        return

    for c in results:
        cid = c.get('id', '')
        name = c.get('full_name', c.get('short_name', ''))
        print(f"  {cid:<12s} {name}")
    print(f"\n  {len(results)} courts listed")

    fmt = getattr(args, 'export', None)
    if fmt == 'csv':
        filepath = make_export_filename('courts', 'csv')
        rows = [{'id': c.get('id', ''), 'name': c.get('full_name', ''),
                 'short_name': c.get('short_name', ''),
                 'jurisdiction': c.get('jurisdiction', ''),
                 'url': c.get('url', '')}
                for c in results]
        Exporter.to_csv(rows, filepath)
    elif fmt == 'json':
        filepath = make_export_filename('courts', 'json')
        Exporter.to_json(results, filepath)


def cmd_recap(client, args):
    """Search RECAP archive."""
    print_header(f"RECAP: {args.query}")
    results, count = client.search_recap(args.query, court=args.court,
                                          max_results=args.limit)
    print_count(count, "RECAP entries")

    if not results:
        print("  No results found.")
        return

    for i, r in enumerate(results, 1):
        print(f"  {i}. [{r.get('dateFiled', '')}] {r.get('caseName', '')}")
        print(f"     {r.get('docketNumber', '')} | {r.get('court', '')}")
        desc = r.get('description', '')[:120]
        if desc:
            print(f"     {desc}")
        docket_id = r.get('docket_id', '')
        if docket_id:
            print(f"     {SITE_BASE}/docket/{docket_id}/")
        print()

    fmt = getattr(args, 'export', None)
    if fmt == 'json':
        filepath = make_export_filename('recap', 'json')
        Exporter.to_json(results, filepath)


# ── Interactive Mode ──

INTERACTIVE_HELP = """
  Commands:

    search <query>                     Search case law
    dockets <query>                    Search dockets (free text)
    dockets --party "Name"             Search by party name
    dockets --court cand --judge "Wu"  Filter by court and judge
    case <docket_id>                   Full case lookup
    judges <name>                      Search judges
    courts                             List federal courts
    recap <query>                      Search RECAP entries
    attorneys <docket_id>              List attorneys on a case
    entries <docket_id>                List docket entries

    export json                        Set export format to JSON
    export csv                         Set export format to CSV
    export off                         Disable auto-export

    help                               Show this help
    quit                               Exit
"""


def parse_interactive_args(arg_string):
    """Parse --flag value pairs from interactive input."""
    result = {'_positional': '', '_flags': {}}
    parts = arg_string.split()
    i = 0
    positional_parts = []

    while i < len(parts):
        if parts[i].startswith('--') and i + 1 < len(parts):
            flag = parts[i][2:]
            val = parts[i + 1]
            # Handle quoted values
            if val.startswith('"') and not val.endswith('"'):
                # Collect until closing quote
                quoted_parts = [val]
                i += 2
                while i < len(parts):
                    quoted_parts.append(parts[i])
                    if parts[i].endswith('"'):
                        i += 1
                        break
                    i += 1
                val = ' '.join(quoted_parts).strip('"')
            else:
                val = val.strip('"')
                i += 2
            result['_flags'][flag] = val
        else:
            positional_parts.append(parts[i])
            i += 1

    result['_positional'] = ' '.join(positional_parts)
    return result


def cmd_interactive(client, args):
    """Interactive exploration mode."""
    print_header("CourtListener Toolkit")
    print(INTERACTIVE_HELP)

    export_format = None

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
        if cmd.lower() == 'help':
            print(INTERACTIVE_HELP)
            continue

        parts = cmd.split(None, 1)
        action = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ''

        try:
            if action == 'export':
                if arg.lower() in ('json', 'csv'):
                    export_format = arg.lower()
                    print(f"  Auto-export set to {export_format}")
                elif arg.lower() == 'off':
                    export_format = None
                    print(f"  Auto-export disabled")
                else:
                    print("  Usage: export json|csv|off")
                continue

            if action == 'search':
                results, count = client.search_opinions(arg, max_results=10)
                print_count(count)
                for i, r in enumerate(results, 1):
                    print_opinion(r, i)
                if export_format and results:
                    handle_export(results, Exporter.flatten_opinion,
                                  'opinions', export_format)

            elif action == 'dockets':
                parsed = parse_interactive_args(arg)
                flags = parsed['_flags']
                positional = parsed['_positional']

                results, count = client.search_dockets(
                    query=positional if positional and 'party' not in flags else None,
                    party=flags.get('party', positional if not flags else None),
                    court=flags.get('court'),
                    judge=flags.get('judge'),
                    max_results=int(flags.get('limit', 10)),
                )
                print_count(count)
                for i, r in enumerate(results, 1):
                    print_docket(r, i)
                if export_format and results:
                    handle_export(results, Exporter.flatten_docket,
                                  'dockets', export_format)

            elif action == 'case':
                if not arg.strip().isdigit():
                    print("  Usage: case <docket_id>  (numeric ID, not docket number)")
                    print("  Find the ID first with: dockets <search term>")
                    continue
                case_data = client.get_full_case(int(arg.strip()))
                if case_data:
                    print_full_case(case_data)
                    print(f"  API requests: {client._request_count} this session")
                    if export_format:
                        filepath = make_export_filename(f'case_{arg.strip()}',
                                                         export_format)
                        if export_format == 'json':
                            Exporter.to_json({
                                'docket': case_data['docket'],
                                'parties': case_data['parties'],
                                'attorneys': case_data['attorneys'],
                                'entries': case_data['entries'],
                            }, filepath)
                        elif export_format == 'csv':
                            rows = [Exporter.flatten_entry(e)
                                    for e in case_data['entries']]
                            Exporter.to_csv(rows, filepath)
                else:
                    print("  Case not found.")

            elif action == 'judges':
                results, count = client.search_judges(name=arg, max_results=10)
                print_count(count)
                for i, r in enumerate(results, 1):
                    print_judge(r, i)
                if export_format and results:
                    handle_export(results, Exporter.flatten_judge,
                                  'judges', export_format)

            elif action == 'courts':
                results = client.get_courts(jurisdiction='F')
                for c in results:
                    print(f"  {c.get('id', ''):<12s} {c.get('full_name', '')}")
                print(f"\n  {len(results)} courts")

            elif action == 'recap':
                # Strip quotes from search term
                search_term = arg.strip().strip('"').strip("'")
                if not search_term:
                    print("  Usage: recap <search query>")
                    continue
                parsed = parse_interactive_args(arg)
                flags = parsed['_flags']
                positional = parsed['_positional'].strip('"').strip("'")
                if not positional:
                    positional = search_term

                results, count = client.search_recap(
                    positional,
                    court=flags.get('court'),
                    max_results=int(flags.get('limit', 10)),
                )
                print_count(count, "RECAP entries")
                for i, r in enumerate(results, 1):
                    print(f"  {i}. [{r.get('dateFiled', '')}] "
                          f"{r.get('caseName', '')}")
                    print(f"     {r.get('docketNumber', '')} | "
                          f"{r.get('court', '')}")
                    desc = r.get('description', '')[:120]
                    if desc:
                        print(f"     {desc}")
                    docket_id = r.get('docket_id', '')
                    if docket_id:
                        print(f"     {SITE_BASE}/docket/{docket_id}/")
                    print()
                if export_format and results:
                    handle_export(results,
                                  lambda r: {
                                      'case_name': r.get('caseName', ''),
                                      'docket_number': r.get('docketNumber', ''),
                                      'court': r.get('court', ''),
                                      'date_filed': r.get('dateFiled', ''),
                                      'description': r.get('description', ''),
                                      'docket_id': r.get('docket_id', ''),
                                  },
                                  'recap', export_format)

            elif action == 'attorneys':
                if not arg.strip().isdigit():
                    print("  Usage: attorneys <docket_id>")
                    continue
                results = client.get_attorneys(int(arg.strip()))
                if not results:
                    print("  No attorneys found.")
                else:
                    for att in results[:20]:
                        name = att.get('name', 'Unknown')
                        contact = att.get('contact_raw', '')
                        print(f"  • {name}")
                        if contact:
                            first_line = contact.split('\n')[0].strip()
                            if first_line:
                                print(f"    {first_line}")
                        att_parties = att.get('parties_represented', [])
                        for p in att_parties[:3]:
                            pname = p.get('name', '')
                            print(f"    Represents: {pname}")
                    print()

            elif action == 'entries':
                if not arg.strip().isdigit():
                    print("  Usage: entries <docket_id>")
                    continue
                entries = client.get_docket_entries(int(arg.strip()),
                                                    show_progress=True)
                for e in entries:
                    num = e.get('entry_number', '?')
                    edate = e.get('date_filed', '')
                    desc = e.get('description', '')[:90]
                    print(f"    #{str(num):<4s} {edate}  {desc}")
                print(f"\n  {len(entries)} entries")
                if export_format and entries:
                    handle_export(entries, Exporter.flatten_entry,
                                  'entries', export_format)

            else:
                print(f"  Unknown command: {action}")
                print("  Type 'help' for available commands")

        except Exception as e:
            print(f"  Error: {e}")

    print(f"\n  Total API requests this session: {client._request_count}")


# ── Main ──

def main():
    parser = argparse.ArgumentParser(
        description='CourtListener Toolkit — federal court data for reporters and researchers',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          %(prog)s case 67890123
          %(prog)s case 67890123 --export json
          %(prog)s search -q "ineffective assistance of counsel" --court cand
          %(prog)s dockets --party "Google" --court cand --export csv
          %(prog)s judges --name "Chutkan"
          %(prog)s courts --jurisdiction FB
          %(prog)s recap -q "motion to dismiss"
          %(prog)s interactive
        """)
    )
    parser.add_argument('--token', default=os.environ.get('COURTLISTENER_TOKEN', ''),
                        help='API token (or set COURTLISTENER_TOKEN env var)')

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # case (unified lookup)
    p = subparsers.add_parser('case', help='Full case lookup by docket ID')
    p.add_argument('docket_id', type=int, help='CourtListener docket ID')
    p.add_argument('--max-entries', type=int, default=100,
                   help='Max docket entries to fetch (default 100)')
    p.add_argument('--export', choices=['csv', 'json'], default=None)

    # search
    p = subparsers.add_parser('search', help='Search case law opinions')
    p.add_argument('--query', '-q', required=True)
    p.add_argument('--court', '-c', default=None)
    p.add_argument('--after', default=None, help='Filed after (YYYY-MM-DD)')
    p.add_argument('--before', default=None, help='Filed before (YYYY-MM-DD)')
    p.add_argument('--limit', '-n', type=int, default=20)
    p.add_argument('--export', choices=['csv', 'json'], default=None)

    # dockets
    p = subparsers.add_parser('dockets', help='Search dockets')
    p.add_argument('--query', '-q', default=None, help='Free text search')
    p.add_argument('--party', '-p', default=None)
    p.add_argument('--court', '-c', default=None)
    p.add_argument('--judge', '-j', default=None)
    p.add_argument('--after', default=None, help='Filed after (YYYY-MM-DD)')
    p.add_argument('--before', default=None, help='Filed before (YYYY-MM-DD)')
    p.add_argument('--limit', '-n', type=int, default=20)
    p.add_argument('--export', choices=['csv', 'json'], default=None)

    # judges
    p = subparsers.add_parser('judges', help='Search judges')
    p.add_argument('--name', '-n', default=None)
    p.add_argument('--court', '-c', default=None)
    p.add_argument('--limit', type=int, default=20)
    p.add_argument('--export', choices=['csv', 'json'], default=None)

    # courts
    p = subparsers.add_parser('courts', help='List courts')
    p.add_argument('--jurisdiction', '-j', default='F',
                   help='Jurisdiction type: F=federal, FB=bankruptcy, '
                        'FS=special, FBP=bankruptcy panel, S=state, etc.')
    p.add_argument('--export', choices=['csv', 'json'], default=None)

    # recap
    p = subparsers.add_parser('recap', help='Search RECAP archive')
    p.add_argument('--query', '-q', required=True)
    p.add_argument('--court', '-c', default=None)
    p.add_argument('--limit', '-n', type=int, default=20)
    p.add_argument('--export', choices=['csv', 'json'], default=None)

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
        'case': cmd_case,
        'search': cmd_search,
        'dockets': cmd_dockets,
        'judges': cmd_judges,
        'courts': cmd_courts,
        'recap': cmd_recap,
        'interactive': cmd_interactive,
    }

    cmd_func = commands.get(args.command)
    if cmd_func:
        cmd_func(client, args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
