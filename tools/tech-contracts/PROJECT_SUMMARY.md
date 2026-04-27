# DHS Procurement Research Dashboard — Project Summary

A procurement research tool combining the Electronic Frontier Foundation's DHS vendor dataset with live government database queries. Deployed as a static site on GitHub Pages.

## Architecture

### Static Dashboard (Primary)
`tech-contracts.html` is a self-contained single-page app deployed on GitHub Pages. It loads `vendors.json` (pre-extracted from the EFF Excel dataset) and handles all search/filtering client-side. Live contract lookups go directly to USASpending.gov's API from the browser — no backend needed.

### Data Pipeline
`extract_data.py` converts the EFF Excel file into `vendors.json` containing:
- 310 vendor profiles with categories, summaries, contract links
- 870 industry day participation records
- 123 Homeland Security Technology Consortium members
- Computed statistics (prime contractors, AI vendors, etc.)

Run this script locally whenever the source dataset updates, then commit `vendors.json`.

### Local Python Tools
For analysis beyond what the dashboard offers:
- `demo.py` — Standalone research tool (pandas, no server)
- `search.py` — Interactive CLI search interface
- `search_contracts.py` — Search downloaded CSV contract files
- `main.py` — FastAPI server with 15+ endpoints and live government queries
- `client.py` — Python client library for the FastAPI server
- `gov_queries.py` — USASpending.gov, FPDS, SAM.gov query module

## Dataset Coverage
- **310 vendor profiles** from EFF's January 2026 research
- **870 industry day participation records** (CBP/ICE)
- **Top 100 DHS contractors** (2006-2024)
- **123 Homeland Security Technology Consortium members**
- Corporate relationships, AI/ML tracking, program involvement

## Data Sources
- **EFF Dataset**: Electronic Frontier Foundation & Heinrich Boell Foundation (Jan 6, 2026)
- **USASpending.gov**: Live federal spending data (free public API, queried from browser)
- **FPDS.gov**: Federal Procurement Data System (search URL generation)
- **SAM.gov**: System for Award Management (search URL generation)
