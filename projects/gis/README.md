# GIS Procurement Intelligence Dashboard

A single-page web application for searching federal and state GIS contract awards, discovering active solicitations, and generating public records requests — all from the browser with no backend required.

## Features

### Federal Contracts
Live queries against the [USASpending.gov](https://usaspending.gov) API for GIS-related contract awards (FY2008–present). Filter by keyword, vendor, awarding agency, state, fiscal year, award amount, and NAICS code. Results display in a sortable, paginated table with aggregate stats (total obligated, unique vendors, unique agencies). Export results to CSV.

**Supported NAICS codes:** 541370 (Surveying & Mapping), 541360 (Geophysical Surveying), 541511 (Custom Programming), 541512 (Systems Design), 541330 (Engineering Services), 541990 (Other Professional/Technical Services).

### SAM.gov Opportunities
Search active federal solicitations on [SAM.gov](https://sam.gov) with filters for keyword, NAICS, state, notice type (solicitation, presolicitation, sources sought, etc.), set-aside category (small business, 8(a), HUBZone, SDVOSB, WOSB), date range, and active/inactive status. Includes pre-built quick-search links for common GIS procurement categories.

### State Procurement
- **Live API search** for states with open data portals (NY, VA, and others via Socrata-compatible APIs)
- **Portal redirects** for all other states — opens the state's procurement search page directly
- **50-state portal directory** with links to each state's procurement portal and NASPO profile, filterable by name, exportable to CSV

### Records Request Generator
Generate pre-filled FOIA/open records request letters for bid tabulations, evaluation criteria, scoring sheets, and award documents. Supports:
- **Federal** requests citing 5 U.S.C. § 552
- **State** requests that auto-insert the correct open records statute for all 50 states + DC
- **Local** (city/county) requests

Copy to clipboard or download as `.txt`.

### Batch Request Tracker
Manage public records requests across multiple jurisdictions:
- Import jurisdictions via CSV (location, state, title, year, identifier)
- Add jurisdictions individually
- Auto-match each jurisdiction to its state procurement portal and open records statute
- Batch-generate request letters for all jurisdictions
- Track status per jurisdiction (not started → submitted → fulfilled)
- Export tracker data to CSV or download all letters as `.txt`
- Data persists in `localStorage`

## Data Sources

| Source | Usage |
|---|---|
| [USASpending.gov API](https://api.usaspending.gov) | Federal contract award data |
| [SAM.gov](https://sam.gov) | Federal solicitation search (via URL construction) |
| State open data APIs (Socrata) | NY, VA, and other state procurement records |
| NASPO state profiles | State procurement portal directory |

## Tech Stack

- **Single HTML file** — no build step, no dependencies, no framework
- Vanilla JavaScript with `fetch` for API calls
- CSS custom properties for theming (dark, warm-toned palette)
- IBM Plex Sans / IBM Plex Mono typography (Google Fonts)
- Responsive layout (mobile-friendly at 600px and 900px breakpoints)
- `localStorage` for batch tracker persistence

## Usage

Open `gis-procurement.html` in any modern browser. No server required — all API calls go directly to public government endpoints.

## License

Subtxt Press
