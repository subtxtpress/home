# Texas Civil Asset Forfeiture Dashboard
## Claude Code Project Handoff

---

## What We're Building

An interactive, publicly hosted data journalism tool that maps and visualizes civil asset forfeiture activity across all 254 Texas counties. The finished product lives at `subtxtpress.github.io/tx-caf` (or a subdirectory of your existing GitHub Pages site). It is self-contained — no backend, no server, no database. All data is processed offline and shipped as static JSON.

The editorial thesis: **Texas law enforcement agencies seize more than they ever convict.** Every visual decision should make that gap legible.

---

## Stack

| Layer | Tool | Reason |
|---|---|---|
| Map | MapLibre GL JS | Your existing strength; handles GeoJSON at county scale |
| Charts | Plotly.js (CDN) | Matches job posting requirements; no build step needed |
| Data pipeline | Python + pandas + geopandas | Preprocessing only; output is static JSON |
| Hosting | GitHub Pages | Existing infrastructure |
| Styling | Vanilla CSS | No framework overhead for a single-page tool |

No React. No bundler. One HTML file, one CSS file, one JS file, one data folder.

---

## Data Sources

Claude Code will need to fetch or you will need to manually download these:

**1. Forfeiture proceeds data**
- Texas Office of Court Administration Annual Reports
- URL: `https://www.txcourts.gov/about-texas-courts/reports-statistics/`
- Format: PDF tables (require extraction) or Excel, depending on year
- Years to target: 2018–2023 (5-year window gives trend lines)
- Fields we need: county, reporting agency, total seized ($), total forfeited ($), cases filed, cases resulting in conviction

**2. County boundaries GeoJSON**
- Source: Census Bureau TIGER/Line shapefiles, Texas counties
- URL: `https://www2.census.gov/geo/tiger/TIGER2023/COUNTY/`
- Filter to FIPS state code 48 (Texas)
- Convert to GeoJSON via geopandas

**3. Population denominators** (for per-capita normalization)
- Texas Demographic Center county estimates
- URL: `https://demographics.texas.gov/Data/TPEPP/Estimates/`
- Needed to make the comparison fair between Harris County and Loving County

---

## Data Pipeline (Python)

Claude Code should build `pipeline/process.py` that does the following in order:

**Step 1 — Load raw OCA data**
Read whichever format OCA provides (CSV preferred; if PDF, use `pdfplumber` to extract tables). Output: `raw/caf_raw.csv`

**Step 2 — Normalize and clean**
- Standardize county names (OCA uses inconsistent casing and abbreviations)
- Cast dollar fields to float, strip `$` and commas
- Cast year to int
- Flag rows where seized > 0 but convictions == 0 as `no_conviction_seizure: true`
- Output: `processed/caf_clean.csv`

**Step 3 — Aggregate by county + year**
- Total seized per county per year
- Total forfeited per county per year
- Count of no-conviction seizures
- Seizure-to-conviction ratio (seized / max(convictions, 1) to avoid div/zero)
- Z-score the ratio column across all counties for a given year — flag counties >1.5 SD above mean as `outlier: true`
- Output: `processed/caf_aggregated.csv`

**Step 4 — Merge with population**
- Join on county name (use FIPS as the join key after a lookup table maps names to FIPS)
- Add `seized_per_capita` and `forfeited_per_capita` columns
- Output: `processed/caf_final.csv`

**Step 5 — Merge with GeoJSON**
- Load Texas counties GeoJSON
- Left join `caf_final` onto features by FIPS
- Output: `data/tx_caf.geojson` — this is the only file the frontend loads

**Step 6 — Build summary JSON**
- Statewide totals by year (for the headline chart)
- Top 10 counties by total seized (for the sidebar table)
- Output: `data/summary.json`

---

## Frontend Architecture

Single HTML file: `index.html`

### Layout (three-panel)

```
┌─────────────────────────────────────────────────────┐
│  HEADER: title + year filter slider                  │
├───────────────────┬─────────────────────────────────┤
│                   │                                  │
│   MapLibre map    │   Plotly chart panel             │
│   (choropleth     │   (switches between views:       │
│    by county)     │    bar, scatter, trend line)     │
│                   │                                  │
├───────────────────┴─────────────────────────────────┤
│  FOOTER: data source attribution + methodology note  │
└─────────────────────────────────────────────────────┘
```

On mobile: map stacks above chart, header collapses to a compact filter bar.

### Map behavior
- Choropleth fill: `seized_per_capita`, 5-bucket quantile scale
- Color scale: light cream (#F5F0E8) to deep rust (#8B2500) — readable, editorially appropriate
- Hover tooltip: county name, total seized, total forfeited, conviction ratio, outlier flag
- Click on county: chart panel updates to show that county's 5-year trend

### Chart panel — three views, tab-switched

**View 1: Statewide trend** (default)
- Plotly grouped bar: seized vs. forfeited by year, statewide
- Annotation line marking 2021 (SB 2212, the reform that didn't pass) for editorial context

**View 2: County scatter**
- X axis: total seized; Y axis: conviction rate
- Points colored by outlier flag (outliers in rust, others in slate)
- Hovering a point highlights that county on the map

**View 3: County detail** (appears after map click)
- Line chart: selected county's seized vs. forfeited, 2018–2023
- Small table below: year-by-year breakdown with no-conviction seizure count

### Year filter
- Range slider: 2018–2023
- Drives both the map choropleth and the statewide trend chart simultaneously
- Single selected year or range (both modes)

---

## Outlier Detection

This is the "AI/ML" checkbox from the job posting, implemented honestly:

In `process.py`, for each year:
```python
df['ratio_zscore'] = stats.zscore(df['seizure_to_conviction_ratio'])
df['outlier'] = df['ratio_zscore'] > 1.5
```

In the UI, outlier counties get a distinct marker on the scatter plot and a small flag icon in the hover tooltip. A methodology note in the footer explains exactly what the z-score threshold means so it's defensible.

Do not oversell this as ML. It is statistical outlier detection. That is accurate and legitimate.

---

## File Structure Claude Code Should Create

```
tx-caf-dashboard/
├── pipeline/
│   ├── process.py
│   ├── requirements.txt
│   └── raw/                  ← manual data drop location
├── data/
│   ├── tx_caf.geojson        ← pipeline output, loaded by frontend
│   └── summary.json          ← pipeline output, loaded by frontend
├── index.html
├── style.css
├── app.js
└── README.md
```

---

## Visual Design

**Palette**
- Background: `#1A1A1A` (near-black, matches your existing dark-mode portfolio aesthetic)
- Surface: `#242424`
- Text primary: `#E8E0D4` (warm off-white)
- Accent / high seizure: `#8B2500` (deep rust — editorially loaded, appropriate)
- Accent / low / safe: `#4A6741` (muted sage)
- Outlier flag: `#C4622D` (mid-rust)
- Border / divider: `#333333`

**Typography**
- Display / header: `IBM Plex Mono` (consistent with your Fitzsimmons tool; readable as data journalism, not decorative)
- Body / labels: `Barlow Condensed` (same rationale — your existing system)
- Data values: `IBM Plex Mono` (monospace for numbers so decimal columns align)

Load both from Google Fonts. No other typefaces.

**Signature element**
On the statewide trend chart, a persistent annotation: a shaded band showing the gap between total seized and total forfeited, labeled "Unaccounted Gap." That band is the story. It should be visible before the user does anything.

---

## README Claude Code Should Write

The README needs to explain:
- What the tool is and the editorial question it answers
- Data sources with direct URLs and the years covered
- How to re-run the pipeline when OCA publishes new data
- The outlier detection methodology in plain language
- License (suggest CC BY 4.0 for the data work; MIT for the code)

---

## What Claude Code Should NOT Do

- Do not use React, Vue, or any JS framework
- Do not set up a Node.js build pipeline
- Do not use a mapping library other than MapLibre GL JS
- Do not invent forfeiture numbers — if a county is missing from OCA data, it gets a `null` fill on the map, not a zero
- Do not add a legend that says "AI-powered" — the outlier detection gets a plain methodology note

---

## First Task for Claude Code

Start with the pipeline, not the frontend. Run `pipeline/process.py` against real OCA data first. If OCA's published format is PDF-only for certain years, use `pdfplumber` to extract the tables before anything else. Validate the output `caf_final.csv` manually before touching the HTML.

The frontend is useless until the data is clean.
