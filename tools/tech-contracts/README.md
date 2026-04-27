# DHS Procurement Research Dashboard

A static web dashboard for tracking Department of Homeland Security vendors, contracts, and spending. Combines the Electronic Frontier Foundation's vendor dataset with live queries to USASpending.gov — deployed on GitHub Pages with no backend required.

**Live site**: [subtxtpress.github.io/home/tools/tech-contracts/tech-contracts.html](https://subtxtpress.github.io/home/tools/tech-contracts/tech-contracts.html)

## How It Works

The dashboard loads a pre-extracted JSON file (`vendors.json`) containing 310 vendor profiles, 870 industry day records, and 123 consortium members from the EFF dataset. All search and filtering happens client-side in the browser. Live contract lookups query USASpending.gov directly from the browser (their API supports CORS).

## Project Structure

```
tech-contracts/
├── tech-contracts.html    # Static web dashboard (deployed on GitHub Pages)
├── vendors.json           # Pre-extracted data from EFF Excel dataset
├── extract_data.py        # Script to regenerate vendors.json from Excel
├── main.py                # FastAPI server (local development only)
├── gov_queries.py         # Government database query module
├── client.py              # Python client library for the FastAPI server
├── demo.py                # Standalone pandas-based research tool
├── search.py              # Interactive CLI search tool
├── search_contracts.py    # CSV contract file searcher
├── requirements.txt       # Python dependencies
├── Palantir/              # Vendor-specific research files
├── *.csv                  # Downloaded contract data from USASpending.gov
└── *.xlsx                 # EFF source dataset
```

## Deployed Dashboard (GitHub Pages)

The primary interface is `tech-contracts.html` — a fully static single-page app:

- **Vendor search**: Filter 310 vendors by keyword, prime contractor status, AI/ML usage
- **Live contract lookup**: Queries USASpending.gov API directly from the browser
- **FPDS/SAM.gov links**: Generates search URLs for federal procurement databases
- **CSV export**: Download search results
- **Dataset stats**: Total vendors, prime contractors, AI vendors, consortium members

No server needed. Works anywhere static HTML is served.

### Updating the Data

When the EFF dataset is updated, regenerate `vendors.json`:

```bash
pip install pandas openpyxl
python extract_data.py
```

Then commit and push `vendors.json` to deploy.

## Local Development Tools

The Python files provide additional capabilities for local analysis:

### Standalone Research (no API needed)
```bash
python demo.py
```
Loads the Excel dataset directly with pandas. Search vendors, view profiles, export to CSV.

### Interactive CLI Search
```bash
python search.py
```
Menu-driven interface for searching and filtering vendor data.

### CSV Contract Search
```bash
python search_contracts.py
```
Search through downloaded CSV files from USASpending.gov.

### Full API Server
```bash
pip install -r requirements.txt
python main.py
# Visit http://localhost:8000/docs
```
Runs a FastAPI server with 15+ endpoints, live government queries, and enriched vendor profiles. Useful for building integrations or running in Jupyter notebooks.

## Data Sources

- **EFF Dataset**: Electronic Frontier Foundation & Heinrich Boell Foundation (January 6, 2026)
- **USASpending.gov**: Official federal spending data (queried live from the browser)
- **FPDS.gov**: Federal Procurement Data System (search URL generation)
- **SAM.gov**: System for Award Management (search URL generation)

## License

Aggregates public data from the EFF and U.S. government sources. Respect the original data licenses.
