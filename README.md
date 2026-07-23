# Subtxt Press, home

Irreverent, adversarial reporting on corruption, due process, and institutional failures. Interactive dashboards and case maps built to make complex data, systems, and information useful.

## Contents

- `index.html`, `policies.html`, `tools.html`, top-level pages
- `projects/`, interactive tools and dashboards
- `dockets/`, investigation case files and supporting documents
- `case/`, interactive case maps and dual-narrative timelines
- `img/`, `icons/`, shared assets

## Interactive Tools & Dashboards (`projects/`)

- **DHS Surveillance Infrastructure Dashboard**: maps ICE/DHS surveillance infrastructure across six layers, raw data collection, the federal watchlisting pipeline, Palantir's integration platforms, mobile field tools, the legal/policy framework, and a contractor ecosystem built from a real 2026 data breach (1,409 awarded contracts, $844,599,807.43, 6,885 applicants, independently verified)
- **Jeffrey Epstein's Amazon Account**: data visualization analyzing 654 real Amazon orders shipped to 7 Epstein properties (Sept. 2007 to Jul. 2019), sourced from the JMail files published by Dropsite News
- **TX Data Centers Investigation** (includes Edwards Aquifer overlay): investigative database of 112 registered qualifying data centers in Texas, tracking ownership, shell entities, crypto miners on cloud exemptions, and aquifer-proximity risk; includes an automated shell-entity detection heuristic beyond its hand-researched list
- **FOIA.io**: FOIA/public-records request management SaaS (deadline tracking, appeal letter generation, Stripe billing), built and functional, tested with a small group, not yet publicly launched
- **MERIDIAN**: live multi-source intelligence dashboard for the Middle East (Iran, Iraq, Syria, Israel/Palestine, Lebanon, Yemen, Strait of Hormuz), fusing NASA FIRMS thermal data with GDELT, ACLED, and UCDP conflict events, maritime boundaries, satellite imagery, and live aircraft tracking, backed by three self-built serverless functions
- **TX GIS Solutions**: a technical demonstration of enterprise GIS work (parcel mapping, flood zone analysis, pipeline risk overlays, zoning atlases) built on real government source data; not currently an active client-services offering
- **Tech Contracts**: DHS/border-tech vendor and procurement research combining an EFF and Heinrich Böll Foundation dataset (310 vendors) with live USASpending.gov queries; includes a local Python toolkit (FastAPI server, CLI tools, a data pipeline) beyond the deployed dashboard
- **GIS Procurement Intelligence**: federal and state GIS contract search, live for USASpending.gov, SAM.gov, and four state open-data portals (NY, VA, CT, TX), with a 50-state portal directory and a records-request generator
- **Boolean Search Generator**: visual query builder for 12 research platforms (Google, Bing, LexisNexis, PubMed, CourtListener, and others), with real platform-specific operator logic, not just labels
- **CourtListener Search Tool**: full legal research interface (docket search, semantic case-law search, judge financial disclosures, RECAP archive) on a FastAPI backend deployed to a Google Cloud VM

## Investigative Case Maps (`case/`)

- **Kelsey Fitzsimmons**: 11 documented inconsistencies in Officer Noonan's testimony in a cop-on-cop shooting, cross-checked against real floor plan measurements, full source transcripts included
- **Zach Adams (Holly Bobo case)**: trial-evidence geographic map with real historical cell-site sector analysis (bearing/radius geometry, not just ping locations) building a specific timing-based physical-possibility argument
- **Tiera Strand**: scroll-driven investigative timeline for an active, unsolved case, with public tip-line information and a factual person-of-interest description
- **Magnolia (JLR domestic violence)**: multi-jurisdictional case reconstruction (WA, FL, AR) from sheriff's records, dispatch logs, and phone records, with a real distance-measurement feature between key locations
- **Matthias v. Reality (Hidden True Crime)**: dual-narrative timeline in seven acts for a closed civil case, sourced to numbered exhibits and real cited statutes
- **Klein v. Samsen**: three-era comparative framework tracking a public figure's documented statements, tied to an active defamation case's legal strategy
- **Arrington Trust Properties**: 203-transaction county deed record timeline spanning 43 years and 21 properties
- **Tricia Griffith Property Records**: a distinct, sharply analytical piece flagging a subprime lender, three default cycles cancelled without foreclosure, and a recurring third-party tax-payment pattern
- **Othram Inc.**: corporate/organizational research into a real forensic genetic genealogy company's growth, leadership, and government partnerships
- **Nancy Guthrie**: real-time investigative resource map (Titan II silo sites, a time-limited route simulator cross-checked against camera coverage, live Tucson PD crime-feed integration) plus an independently verified bitcoin ransom-trace analysis
- **Tucson Streamers**: parasocial escalation timeline using streamers' own livestream footage as cited evidence, tied to a real PCSD incident report

## Court Dockets (`dockets/`)

Organized filing chronologies and background records supporting the case maps above, including Richard Allen (Indiana Court of Appeals), Klein v. Samsen, Tricia Griffith, Sarah Grace Patrick, Jonathan Lee Riches, Hidden True Crime, CC Suarez, and Tucson Streamers.

## Tools With a Real Backend

Most tools above run entirely client-side. A few have a real backend and include their own setup instructions:

- **CourtListener search**: FastAPI backend (`app.py`) deployed on a Google Cloud VM
- **Tech Contracts**: FastAPI backend (`main.py`) for local analysis and live government queries
- **FOIA.io**: Supabase backend (Postgres, Auth, Storage, Edge Functions)
- **MERIDIAN**: three Supabase edge functions for live conflict-data and OSINT feeds
