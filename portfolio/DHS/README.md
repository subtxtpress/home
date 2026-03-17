# DHS Surveillance Infrastructure Dashboard

An interactive dashboard mapping ICE's secret watchlists, Palantir's deportation machine and the network of surveillance systems tracking millions of Americans.

**Live:** [subtxtpress.github.io/home/portfolio/DHS/dhs-dashboard.html](https://subtxtpress.github.io/home/portfolio/DHS/dhs-dashboard.html)

---

## Overview

This dashboard synthesizes reporting from investigative journalists, leaked government documents, federal contracts and FOIA requests into a navigable reference for understanding DHS surveillance infrastructure. It covers six layers:

| Layer | Section | What It Maps |
|-------|---------|-------------|
| 01 | Data Collection | Raw data sources: IDENT (270M+ biometrics), Medicaid (80M patients), IRS, TECS, SEVIS, SSA + social media surveillance tools (ShadowDragon/SocialNet, Fivecast ONYX, Babel X, Cobwebs/Pen-Link, Skopenow) — sourced from UAW v. DOS complaint |
| 02 | Watchlists | Secret systems (SPARTA, GRAPEVINE, SLIPSTREAM, HUMMINGBIRD, REAPER, BLUEKEY/SIENNA) + federal watchlisting pipeline (TIDE → TSDB → screeners), reasonable suspicion standard, biometric-only nominations, No Fly criteria — sourced from the 2013 Watchlisting Guidance |
| 03 | Palantir Layer | Integration platform: FALCON, ICM, ImmigrationOS, Foundry, Gotham, IRS-NG, LEAD TRACKER |
| 04 | Field Tools | Mobile surveillance: ELITE targeting, Mobile Fortify facial recognition, I.R.I.S./MORIS iris scanning |
| 05 | Policy Framework | Legal basis: NSPM-7, EO 14161 (viewpoint screening), EO 14188 (immigration emergency), "Eliminating Silos" EO, IRS-ICE agreement, HHS Medicaid order, 287(g), Secure Communities, "Catch and Revoke" pipeline |
| 06 | Contractor Ecosystem | Leaked March 2026: 6,800+ DHS contractor applicants, 1,409 awarded contracts ($844.6M) |

Additional sections: Real Cases, Network Map (Thiel-Musk-Miller), Timeline (2003-2026) and Sources.

---

## Data Files

### Leaked Data (March 1, 2026)

On March 1, 2026, a group calling themselves the "Department of Peace" breached DHS's Office of Industry Partnership (oip.dhs.gov) and leaked contractor data via [Distributed Denial of Secrets](https://ddosecrets.org/article/ice-contracts).

#### `dhs_contractors_won.json` (3.6 MiB)

Awarded contracts from DHS SBIR, LRBAA and SVIP programs (2004-2025).

**Records:** 1,409 contracts | **Total value:** $844,599,807

**Schema:**

| Field | Type | Description |
|-------|------|-------------|
| `awardId` | int | Unique award identifier |
| `proposalId` | int | Linked proposal identifier |
| `proposalNumber` | string | Proposal tracking number |
| `proposalTitle` | string | Project name |
| `phaseType` | string | `PHASE_1`, `PHASE_2`, `2nd_PHASE_II` |
| `phaseTypeDesc` | string | Human-readable phase name |
| `proposalAbstract` | string | Project description (often detailed) |
| `programName` | string | `SBIR`, `LRBAA`, or `SVIP` |
| `awardNumber` | string | Federal award number |
| `awardType` | string | Contract type |
| `topicId` | int | DHS topic area identifier |
| `topicNumber` | string | Topic tracking number |
| `topicTitle` | string | DHS research topic name |
| `solicitationId` | int | Solicitation identifier |
| `solicitationNo` | string | Solicitation tracking number |
| `companyName` | string | Awardee company name |
| `companyContactName` | string | Company point of contact |
| `companyContactTitle` | string | Contact title |
| `companyAddress` | string | Company address |
| `companyCity` | string | City |
| `companyStateCd` | string | State code |
| `companyState` | string | State name |
| `companyZipCode` | string | Zip code |
| `popStartDate` | string | Period of performance start (YYYY-MM-DD) |
| `popEndDate` | string | Period of performance end (YYYY-MM-DD) |
| `awardAmount` | float | Award dollar amount |
| `currentObligationAmount` | float | Current obligation amount |
| `awardStatusCode` | string | `AWARDED` |
| `awardStatusDesc` | string | Status description |
| `govContactList` | array | Government contacts (usually empty) |

#### `dhs_contractors_applied.json` (13.4 MiB)

All organizations that applied for DHS contracts through the Office of Industry Partnership.

**Records:** 6,885 companies

**Schema:**

| Field | Type | Description |
|-------|------|-------------|
| `companyId` | int | Unique company identifier |
| `name` | string | Company name |
| `companyURL` | string | Company website |
| `tin` | string | Tax identification number |
| `duns` | string | DUNS number |
| `ueiNumber` | string | Unique Entity Identifier |
| `cageCode` | string | CAGE code (govt contractor ID) |
| `yearFounded` | string | Year founded |
| `companyContact` | object | Primary contact (name, address, phone, email, state) |
| `companyPOC` | object | Point of contact (name, phone, email) |

**Privacy note:** The applied contractors file contains personal identifying information (employee names, phone numbers, emails, tax IDs). This PII is **not** published in the dashboard. Only corporate-level identities and aggregate statistics are used.

---

## Querying the Data

### Using jq

**Search contracts by company name:**
```bash
cat dhs_contractors_won.json | jq '.[] | select(.companyName | test("Palantir"))'
```

**Get all companies that won contracts:**
```bash
cat dhs_contractors_won.json | jq -r '.[].companyName' | sort -u
```

**Search contracts by keyword in proposal title:**
```bash
cat dhs_contractors_won.json | jq -r '.[] | select(.proposalTitle | test("biometric"; "i")) | "\(.companyName): \(.proposalTitle) ($\(.awardAmount))"'
```

**Top 20 contracts by award amount:**
```bash
cat dhs_contractors_won.json | jq -r 'sort_by(-.awardAmount) | .[:20][] | "\(.companyName): $\(.awardAmount) — \(.proposalTitle)"'
```

**Search by topic area:**
```bash
cat dhs_contractors_won.json | jq -r '.[] | select(.topicTitle | test("surveillance"; "i")) | .companyName' | sort -u
```

**Find contractor in applicant pool:**
```bash
cat dhs_contractors_applied.json | jq '.[] | select(.name | test("Raytheon"))'
```

**Get all applicant company names:**
```bash
cat dhs_contractors_applied.json | jq -r '.[].name' | sort -u
```

### Using Python

```python
import json
from collections import defaultdict

with open('dhs_contractors_won.json') as f:
    contracts = json.load(f)

# Category analysis
keywords = {
    'Biometrics': ['biometric', 'fingerprint', 'facial', 'iris', 'identity', 'dna', 'recognition'],
    'Surveillance': ['surveillance', 'tracking', 'monitor', 'sensor', 'camera', 'radar', 'drone'],
    'Border': ['border', 'maritime', 'coast', 'port', 'cargo', 'vessel'],
    'Cyber': ['cyber', 'malware', 'botnet', 'encrypt', 'forensic', 'intrusion'],
    'Social Media': ['social media', 'social network', 'voice', 'intercept'],
}

for category, kws in keywords.items():
    matches = [c for c in contracts
               if any(kw in (c.get('proposalTitle','') + ' ' + c.get('proposalAbstract','')).lower()
                      for kw in kws)]
    total = sum(c.get('awardAmount', 0) or 0 for c in matches)
    print(f"{category}: {len(matches)} contracts, ${total:,.0f}")
```

---

## Key Statistics

| Metric | Value | Source |
|--------|-------|--------|
| IDENT biometric records | 270M+ | DHS Privacy Impact Assessment |
| Medicaid patients transferred to ICE | 80M | HHS Medicaid Data Order (June 2025) |
| Mobile Fortify field scans | 100K+ | 404 Media investigation |
| Palantir contracts (2025) | $970M | SAM.gov federal contracts |
| DHS contractor applicants | 6,885 | OIP breach (March 2026) |
| Awarded contracts | 1,409 | OIP breach (March 2026) |
| Total award value | $844.6M | OIP breach (March 2026) |
| IRS-NG database access | 28+ databases | Leaked DHS documents |
| ITIN taxpayers at risk | 4.8M | IRS-ICE data sharing agreement |
| Noncitizens self-censoring | 84.4% | UAW v. DOS survey data (Oct 2025) |
| Social media tools licensed | 5+ | UAW v. DOS complaint (Oct 2025) |

---

## Primary Sources

- **Ken Klippenstein** — "Feds Identify 'Leader of Antifa'"
- **404 Media** — ELITE system exposure (Jan 2026)
- **POGO** — Stephen Miller Palantir stock investigation (June 2025)
- **Distributed Denial of Secrets** — ICE Contracts leak (March 2026)
- **Snowden Archive (via DDoSecrets)** — 2013 Watchlisting Guidance (U//FOUO), 166-page interagency document detailing TIDE/TSDB nomination procedures, reasonable suspicion standards, No Fly/Selectee criteria, and encounter management
- **UAW v. Department of State** — Case 1:25-cv-08566 (Oct 16, 2025), 95-page federal complaint detailing social media surveillance tools, "Catch and Revoke" pipeline, Tiger Team operations, EOs 14161/14188, chilling effects survey data and specific targeting cases
- **SAM.gov** — ImmigrationOS contract 70CMSD24F00000213
- **DHS Privacy Impact Assessments** — IRS-NG system documentation

---

## Editorial Standards

- All claims are sourced from publicly available documents, verified reporting, or leaked government records
- Personal identifying information from the OIP breach is excluded from the dashboard
- Contract data uses only corporate-level identities, award amounts, project names and dates
- The dashboard is a living document updated as new information becomes available

---

## License

Content and analysis by [Subtxt Press](https://substack.com/@subtxtpress). Leaked data published by [Distributed Denial of Secrets](https://ddosecrets.org/) under their standard distribution terms.
