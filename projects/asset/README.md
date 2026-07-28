# Texas Civil Asset Forfeiture Dashboard

An interactive data journalism tool mapping civil asset forfeiture activity across all 254 Texas counties. Built on static JSON — no backend, no server.

**Editorial thesis:** Texas law enforcement agencies seize more than they ever convict. Every visual decision makes that gap legible.

---

## Data Sources

### 1. Forfeiture proceeds (manual download required)

**Texas Office of Court Administration Annual Reports**  
URL: https://www.txcourts.gov/about-texas-courts/reports-statistics/

Navigate to "Annual Statistical Report" for each year. The Chapter 59 (civil asset forfeiture) tables list proceeds by county and agency. Download the Excel or CSV export where available; use pdfplumber for PDF-only years.

Target years: **2018–2023**

Save the combined file as `pipeline/raw/caf_raw.csv` with these columns:

| Column | Format | Notes |
|---|---|---|
| `county` | BEXAR | All caps, no "County" suffix |
| `year` | 2021 | Integer |
| `agency` | BEXAR COUNTY SO | Optional; aggregated per county |
| `seized` | 1234567.89 | Dollar amount; `$` and commas stripped automatically |
| `forfeited` | 987654.32 | Net proceeds returned/forfeited |
| `cases_filed` | 42 | Optional |
| `convictions` | 7 | Optional; drives outlier detection |

### 2. County boundaries (auto-downloaded)

Census Bureau TIGER/Line shapefiles — the pipeline downloads and caches these automatically on first run.

### 3. Population denominators (optional, manual download)

**Texas Demographic Center county population estimates**  
URL: https://demographics.texas.gov/Data/TPEPP/Estimates/

Save as `pipeline/raw/tx_population.csv` with columns: `county` (all caps), `year`, `population`. Without this file the dashboard still works but per-capita columns will be null.

---

## Running the Pipeline

```bash
cd pipeline
pip install -r requirements.txt
python process.py
```

Pipeline stages:
1. Downloads Census county GeoJSON (once, cached)
2. Loads and cleans `raw/caf_raw.csv`
3. Aggregates by county + year, flags no-conviction seizures
4. Merges population denominators (if available)
5. Outputs `data/tx_caf.geojson` — the only file the frontend loads
6. Outputs `data/summary.json` — statewide totals + top 10 counties

Re-run whenever OCA publishes new data. Replace `caf_raw.csv` with updated data and re-run `process.py`.

---

## Outlier Detection

For each reporting year, the pipeline computes a z-score on each county's seizure-to-conviction ratio:

```python
ratio = seized / max(convictions, 1)
z_score = stats.zscore(ratio, per_year)
outlier = z_score > 1.5
```

Counties flagged as outliers appear with a distinct marker on the scatter plot and a flag icon in hover tooltips. This is statistical outlier detection — not machine learning. The 1.5 SD threshold and methodology are documented in the dashboard footer.

Counties missing from OCA data receive `null` in the GeoJSON — not zero. Null counties render as no-data gray on the map.

---

## License

Data pipeline and dashboard code: **MIT**  
Processed data derived from public OCA records: **CC BY 4.0**
