#!/usr/bin/env python3
"""
Texas Civil Asset Forfeiture Data Pipeline
Processes OCA annual report data → tx_caf.geojson + summary.json

Input: pipeline/raw/caf_raw.csv (or .xlsx)
Expected columns (flexible — common OCA header variants accepted):
  county       — county name (ANDERSON, BEXAR, etc.)
  year         — reporting year (2018–2023)
  agency       — reporting law enforcement agency (optional; aggregated per county)
  seized       — total dollar amount seized ($1,234.56 or 1234.56)
  forfeited    — total dollar amount forfeited/proceeds
  cases_filed  — number of forfeiture cases filed (optional)
  convictions  — number of cases resulting in conviction (optional)

Data source: Texas OCA Annual Statistical Reports
  https://www.txcourts.gov/about-texas-courts/reports-statistics/
"""

import json
import sys
import warnings
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import geopandas as gpd
import requests
from scipy import stats

warnings.filterwarnings("ignore", category=FutureWarning)

ROOT = Path(__file__).parent
RAW = ROOT / "raw"
PROCESSED = ROOT / "processed"
DATA = ROOT.parent / "data"

for d in [RAW, PROCESSED, DATA]:
    d.mkdir(parents=True, exist_ok=True)

# OCA sometimes uses county abbreviations or alternate spellings
COUNTY_ALIASES = {
    "DE WITT": "DE WITT",
    "DEWITT": "DE WITT",
    "LA SALLE": "LA SALLE",
    "LASALLE": "LA SALLE",
    "MC CULLOCH": "MCCULLOCH",
    "MC LENNAN": "MCLENNAN",
    "MC MULLEN": "MCMULLEN",
}


# ─── Step 0: County GeoJSON from Census TIGER ────────────────────────────

def download_tx_counties():
    out = RAW / "tx_counties.geojson"
    if out.exists():
        print("[0] County GeoJSON already present — skipping download")
        return gpd.read_file(out)

    print("[0] Downloading Census TIGER/Line county shapefile...")
    url = "https://www2.census.gov/geo/tiger/TIGER2023/COUNTY/tl_2023_us_county.zip"
    r = requests.get(url, timeout=120)
    r.raise_for_status()

    zpath = RAW / "_county.zip"
    zpath.write_bytes(r.content)

    with zipfile.ZipFile(zpath, "r") as z:
        z.extractall(RAW / "_county_shp")
    zpath.unlink()

    gdf = gpd.read_file(RAW / "_county_shp" / "tl_2023_us_county.shp")
    tx = gdf[gdf["STATEFP"] == "48"][["GEOID", "NAME", "geometry"]].copy()
    tx = tx.to_crs("EPSG:4326")
    tx.to_file(out, driver="GeoJSON")
    print(f"    Saved {len(tx)} counties → {out.name}")
    return tx


# ─── Step 1: Load raw OCA data ───────────────────────────────────────────

def load_raw():
    xlsx = RAW / "caf_raw.xlsx"
    csv = RAW / "caf_raw.csv"

    if xlsx.exists():
        df = pd.read_excel(xlsx)
        print(f"[1] Loaded {len(df)} rows from caf_raw.xlsx")
    elif csv.exists():
        df = pd.read_csv(csv)
        print(f"[1] Loaded {len(df)} rows from caf_raw.csv")
    else:
        print("ERROR: No input data found.")
        print(f"  Drop OCA forfeiture data at: pipeline/raw/caf_raw.csv  (or .xlsx)")
        print("  Required columns: county, year, seized, forfeited")
        print("  Optional columns: agency, cases_filed, convictions")
        print("  Source: https://www.txcourts.gov/about-texas-courts/reports-statistics/")
        sys.exit(1)

    return df


# ─── Step 2: Normalize and clean ────────────────────────────────────────

def _clean_money(series):
    return (
        series.astype(str)
        .str.replace(r"[\$,\s]", "", regex=True)
        .replace(["", "nan", "N/A", "n/a", "-"], np.nan)
        .astype(float)
    )

def normalize(df):
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower().str.replace(r"\s+", "_", regex=True)

    # Accept common OCA header variants
    col_map = {
        "county":      ["county", "county_name", "cnty"],
        "year":        ["year", "fiscal_year", "fy", "report_year", "reporting_year"],
        "agency":      ["agency", "agency_name", "reporting_agency", "department", "dept"],
        "seized":      ["seized", "total_seized", "amount_seized", "seizure_amount", "total_amount_seized"],
        "forfeited":   ["forfeited", "total_forfeited", "proceeds", "amount_forfeited", "forfeiture_proceeds"],
        "cases_filed": ["cases_filed", "cases", "filings", "total_cases", "number_of_cases"],
        "convictions": ["convictions", "conviction", "cases_resulting_in_conviction", "criminal_convictions"],
    }

    rename = {}
    for canonical, aliases in col_map.items():
        for alias in aliases:
            if alias in df.columns and canonical not in rename.values():
                rename[alias] = canonical
                break
    df = df.rename(columns=rename)

    required = ["county", "year", "seized", "forfeited"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        print(f"ERROR: Missing required columns after normalization: {missing}")
        print(f"  Found: {list(df.columns)}")
        sys.exit(1)

    df["county"] = (
        df["county"].astype(str).str.upper().str.strip()
        .replace(COUNTY_ALIASES)
    )
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    df["seized"] = _clean_money(df["seized"])
    df["forfeited"] = _clean_money(df["forfeited"])

    for col in ["cases_filed", "convictions"]:
        if col not in df.columns:
            df[col] = pd.NA
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    # Editorial flag: seized with zero convictions
    df["no_conviction_seizure"] = (df["seized"] > 0) & (df["convictions"].fillna(0) == 0)

    df = df.dropna(subset=["county", "year"])

    out = PROCESSED / "caf_clean.csv"
    df.to_csv(out, index=False)
    print(f"[2] Cleaned → {out.name}  ({len(df)} rows, "
          f"{df['no_conviction_seizure'].sum()} no-conviction seizure rows)")
    return df


# ─── Step 3: Aggregate by county + year ─────────────────────────────────

def aggregate(df):
    grp = df.groupby(["county", "year"], as_index=False).agg(
        seized=("seized", "sum"),
        forfeited=("forfeited", "sum"),
        cases_filed=("cases_filed", "sum"),
        convictions=("convictions", "sum"),
        no_conviction_seizures=("no_conviction_seizure", "sum"),
    )

    # Avoid div/zero per plan spec
    grp["seizure_to_conviction_ratio"] = (
        grp["seized"] / grp["convictions"].fillna(0).clip(lower=1)
    )

    # Z-score per year; counties >1.5 SD above mean flagged as outliers
    grp["ratio_zscore"] = grp.groupby("year")["seizure_to_conviction_ratio"].transform(
        lambda x: stats.zscore(x, nan_policy="omit")
    )
    grp["outlier"] = grp["ratio_zscore"] > 1.5

    out = PROCESSED / "caf_aggregated.csv"
    grp.to_csv(out, index=False)
    print(f"[3] Aggregated → {out.name}  ({len(grp)} county-year rows, "
          f"{int(grp['outlier'].sum())} outliers)")
    return grp


# ─── Step 4: Merge population denominators ──────────────────────────────

def load_population():
    pop_path = RAW / "tx_population.csv"
    if not pop_path.exists():
        print("[4] WARNING: pipeline/raw/tx_population.csv not found")
        print("    Download county estimates from:")
        print("    https://demographics.texas.gov/Data/TPEPP/Estimates/")
        print("    Expected columns: county (all caps), year, population")
        print("    Continuing without per-capita normalization (columns will be null)")
        return None
    pop = pd.read_csv(pop_path)
    pop.columns = pop.columns.str.strip().str.lower()
    pop["county"] = pop["county"].str.upper().str.strip()
    return pop

def merge_population(grp, pop):
    if pop is None:
        grp["population"] = np.nan
        grp["seized_per_capita"] = np.nan
        grp["forfeited_per_capita"] = np.nan
    else:
        grp = grp.merge(pop[["county", "year", "population"]], on=["county", "year"], how="left")
        grp["seized_per_capita"] = grp["seized"] / grp["population"]
        grp["forfeited_per_capita"] = grp["forfeited"] / grp["population"]

    out = PROCESSED / "caf_final.csv"
    grp.to_csv(out, index=False)
    print(f"[4] Final CSV → {out.name}")
    return grp


# ─── Step 5: Merge onto GeoJSON ─────────────────────────────────────────

def _safe(val):
    if val is None:
        return None
    try:
        if pd.isna(val):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(val, (np.integer,)):
        return int(val)
    if isinstance(val, (np.floating,)):
        return None if np.isnan(val) else float(round(val, 4))
    if isinstance(val, (np.bool_,)):
        return bool(val)
    return val

def build_geojson(df, tx_gdf):
    # County name → 5-digit FIPS from the GeoJSON itself
    fips_map = {row["NAME"].upper(): row["GEOID"] for _, row in tx_gdf.iterrows()}

    df = df.copy()
    df["fips"] = df["county"].map(fips_map)

    unmatched = df[df["fips"].isna()]["county"].unique()
    if len(unmatched):
        print(f"[5] WARNING: {len(unmatched)} county name(s) didn't match Census:")
        for u in sorted(unmatched):
            print(f"    '{u}'  — add to COUNTY_ALIASES if this is a known variant")

    # Build per-county property dict with year-keyed data
    # Missing counties stay in the GeoJSON with null properties (per editorial spec)
    county_props = {}
    for _, row in df.iterrows():
        fips = row.get("fips")
        if not fips:
            continue
        yr = int(row["year"])
        if fips not in county_props:
            county_props[fips] = {"fips": fips, "county": row["county"], "years": {}}
        county_props[fips]["years"][yr] = {
            "seized":               _safe(row["seized"]),
            "forfeited":            _safe(row["forfeited"]),
            "cases_filed":          _safe(row["cases_filed"]),
            "convictions":          _safe(row["convictions"]),
            "no_conviction_seizures": _safe(row["no_conviction_seizures"]),
            "seized_per_capita":    _safe(row.get("seized_per_capita")),
            "forfeited_per_capita": _safe(row.get("forfeited_per_capita")),
            "ratio":                _safe(row["seizure_to_conviction_ratio"]),
            "outlier":              bool(row["outlier"]),
        }

    # Attach props to GeoJSON; counties absent from OCA data get null years dict
    prop_rows = [{"GEOID": fips, **props} for fips, props in county_props.items()]
    if prop_rows:
        prop_df = pd.DataFrame(prop_rows)
        merged = tx_gdf.merge(prop_df, on="GEOID", how="left")
    else:
        merged = tx_gdf.copy()
        merged["county"] = None
        merged["years"] = None

    out = DATA / "tx_caf.geojson"
    merged.to_file(out, driver="GeoJSON")
    data_counties = len(county_props)
    print(f"[5] GeoJSON → {out.name}  ({len(merged)} features, {data_counties} with data)")
    return merged


# ─── Step 6: Summary JSON ────────────────────────────────────────────────

def build_summary(df):
    by_year = (
        df.groupby("year")
        .agg(
            total_seized=("seized", "sum"),
            total_forfeited=("forfeited", "sum"),
            total_cases=("cases_filed", "sum"),
            total_convictions=("convictions", "sum"),
            counties_reporting=("county", "nunique"),
            outlier_count=("outlier", "sum"),
        )
        .reset_index()
    )
    by_year["unaccounted_gap"] = by_year["total_seized"] - by_year["total_forfeited"]
    by_year["year"] = by_year["year"].astype(int)

    top10 = (
        df.groupby("county")["seized"].sum()
        .nlargest(10)
        .reset_index()
        .rename(columns={"seized": "total_seized"})
    )
    top10["total_seized"] = top10["total_seized"].round(2)

    summary = {
        "years": sorted(df["year"].dropna().astype(int).unique().tolist()),
        "by_year": [
            {k: (_safe(v) if not isinstance(v, str) else v) for k, v in row.items()}
            for row in by_year.to_dict(orient="records")
        ],
        "top10_by_seized": top10.to_dict(orient="records"),
    }

    out = DATA / "summary.json"
    out.write_text(json.dumps(summary, indent=2))
    print(f"[6] Summary JSON → {out.name}")
    return summary


# ─── Main ────────────────────────────────────────────────────────────────

def main():
    print("Texas CAF Pipeline\n" + "─" * 40)
    tx_counties = download_tx_counties()
    raw = load_raw()
    clean = normalize(raw)
    aggregated = aggregate(clean)
    pop = load_population()
    final = merge_population(aggregated, pop)
    build_geojson(final, tx_counties)
    build_summary(final)

    print("\n" + "─" * 40)
    print("Output:")
    print(f"  data/tx_caf.geojson   ← frontend map layer")
    print(f"  data/summary.json     ← statewide stats + top 10")


if __name__ == "__main__":
    main()
