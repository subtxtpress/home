# Texas Data Centers Investigation

A comprehensive investigative database tracking 112+ registered qualifying data centers under the Texas Comptroller's tax exemption program. This project exposes ownership structures, shell entities, cryptocurrency mining operations, and the environmental and fiscal cost of Texas's data center tax shelter.

## What's Here

### `/dashboard.html`
The main interactive database dashboard featuring:
- **Overview tab**: Summary of the tax exemption program, key findings, and investigation status
- **Full Database tab**: Searchable, filterable table of all 112 registered facilities with occupant, operator, location, and exemption status
- **Shell Entities tab**: Detailed analysis of corporate structures hiding beneficial ownership (Design LLC, OBOE LLC, Green Chile Ventures, Core42, etc.)
- **FOIA Targets tab**: List of specific records requests pending with state and local agencies
- **Methodology tab**: Sources, data collection process, and research limitations
- **Map tab**: Interactive Leaflet map showing facility locations across Texas

### `/aquifer-map/aquifer-map.html`
Standalone interactive map focused on **San Antonio's data center cluster**:
- Edwards Aquifer recharge, transition, and contributing zones from TCEQ regulations
- 18 mapped facilities (Microsoft, Oracle, Google, Meta, Rackspace, CyrusOne, etc.)
- Overlay analysis showing ~4 facilities on the recharge zone and ~9 on the contributing zone
- Highlights the water contamination risk for 2 million San Antonio residents
- No water disclosure requirement despite location in sensitive aquifer zones

## Key Findings

### The Numbers
- **112 unique facilities** registered as of February 2026 (114 Comptroller entries)
- **106 addresses confirmed** at street level; 5 remain road/county-level; 1 blank
- **22 crypto mining operations** using the same exemption as cloud infrastructure
- **~40 facilities** with owner ≠ occupant ≠ operator (shell entity patterns)
- **10+ foreign-registered entities** operating under the exemption

### Top Occupants
1. Microsoft Corporation (14 facilities, including OBOE LLC shell)
2. Oracle America, Inc. (13)
3. CoreWeave, Inc. (7)
4. Google "Design LLC" (6)
5. Amazon Data Services (3)
6. Riot Platforms, Inc. (3 — cryptocurrency mining)
7. American Bitcoin Operating LLC/Hut 8 (3)
8. NTT Global Data Centers (3)

### Red Flags

**Cryptocurrency Mining on Cloud Exemption**
- Riot Platforms, Whinstone, Cipher Mining, and others use the same sales tax exemption designed for cloud infrastructure
- Texas HB 1750 (2023) explicitly extended the exemption to crypto mining
- Riot's Rockdale campus alone draws 750 MW
- Several receive double incentives: tax exemption + ERCOT Large Flexible Load program payments

**Shell Entities & Beneficial Ownership**
- **Design LLC** (Google): Six facilities using "Design LLC" or "Design LLC" as occupant entity across multiple Texas registrations
- **OBOE LLC** (Microsoft): Appears to be music-named shell entity; inconsistent with Microsoft's other direct registrations
- **Green Chile Ventures LLC**: Unconfirmed beneficial occupant at four identical DataBank facilities (registered Oct 2025)
- **Core42 Holding US LLC**: Abu Dhabi-based parent (G42) with alleged ties to Chinese technology firms; owner not listed in Comptroller registry

**Water & Environmental Risk**
- San Antonio cluster: ~4 facilities on Edwards Aquifer recharge zone (rainwater sinks directly into drinking water source)
- Recharge zone requires TCEQ Edwards Aquifer Protection Plan but **no water usage disclosure required**
- Lancium's Childress campus (1 GW) draws from already water-stressed counties
- Large impervious cover increases runoff during storm events

**Foreign Sovereign Control**
- IE US Cluster (Childress, TX): 4 facilities operated by foreign entity, ~GW scale
- G42/Core42: UAE government-linked with US national security scrutiny

## Data Structure

```
tx-data-centers/
├── dashboard.html                 ← Main interactive database
├── aquifer-map/
│   └── aquifer-map.html          ← San Antonio aquifer overlay
├── README.md                      ← This file
└── [other supporting files]
```

## Project Status

**Active investigation** as of August 2026.

- ✅ 106 of 112 addresses confirmed at street level
- ✅ Ownership and occupancy patterns documented
- ✅ Crypto mining registrations identified and cross-referenced
- ⏳ FOIA requests pending with:
  - Texas Comptroller (ownership disclosures, exemption amendment history)
  - ERCOT (demand response contracts, curtailment agreements, power draw data)
  - Local water authorities (usage records for Childress, Pecos, Medina Counties)
  - County appraisers (local tax abatements, property valuations)

**Corrections & tips welcome.** Special interest in:
- West Texas facility locations and operators
- ERCOT curtailment agreements and incentive payments
- Beneficial ownership documentation for Green Chile Ventures LLC entities
- Local community agreements and tax abatement terms

## Sources

- Texas Comptroller STAR Registry (February 2026 snapshot)
- TCEQ 30 TAC Chapter 213 (Edwards Aquifer Protection boundaries)
- Edwards Aquifer Authority permit database
- Corporate filings (Texas SOS, SEC Edgar)
- Subtxt Press field research and FOIA responses
- ERCOT Large Flexible Load program documentation
- FTX/Alameda bankruptcy records (Genesis Digital Assets)

## About

This investigation is published by **Subtxt Press**, an independent publication focused on accountability, infrastructure, and the public interest in Texas.

- Web: https://subtxtpress.github.io/home/
- Contact: See dashboard for submission methods

## License

The data and findings in this project are published for public interest journalism. Attribution to Subtxt Press is appreciated but not required for educational or research use.

---

*Last updated: July 2026 | Database snapshot: February 2026 | Investigation status: Ongoing*
