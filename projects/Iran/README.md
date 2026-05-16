# MERIDIAN

**Middle East Regional Intelligence Dashboard for Infrared Anomaly Notification**

A zero-dependency, single-file OSINT tool for monitoring thermal anomalies, infrastructure impact, conflict events, satellite imagery, maritime boundaries, and live aircraft tracking across the Middle East theater. Built for investigative journalists, OSINT analysts, and GIS researchers.

![MERIDIAN](img/meridian.png)

## What It Does

MERIDIAN fuses multiple open-source intelligence layers into a single interactive map:

- **Thermal Anomalies** — Near real-time fire and heat detections from NASA FIRMS across four satellite sensors (VIIRS NOAA-20, NOAA-21, Suomi-NPP, MODIS Aqua/Terra). Filterable by confidence level, satellite source, time range, and geographic region.
- **Industrial Sites** — 108 known refineries, power plants, gas processing facilities, and petrochemical complexes. Detections within ~2km of these sites are automatically tagged and visually de-emphasized to separate routine industrial flaring from conflict-relevant activity.
- **Conflict Events** — Triple-source conflict intelligence: live GDELT Global Knowledge Graph data (armed conflict, terror/explosions, violence, protests, military activity), ACLED expert-coded events (human-verified with actor details, fatality counts, and event sub-types; rolling 30-day window), and UCDP GED verified archive (through Dec 2024 with fatality estimates and conflict classifications). Switchable source tabs with event-type filtering and temporal alignment to thermal detections.
- **Nighttime Lights** — NASA GIBS VIIRS Day/Night Band imagery with before/after comparison mode for assessing infrastructure damage and power grid disruption.
- **MODIS True-Color** — NASA GIBS MODIS Terra Corrected Reflectance daily imagery with date picker and opacity controls for visual corroboration of thermal detections.
- **Sentinel-2 Optical** — On-demand 10m true-color imagery via AWS Earth Search STAC API. Queries recent cloud-free scenes for the current map view, with date-labeled footprints, thumbnail previews, and direct links to Copernicus Browser for full-resolution viewing.
- **Maxar Crisis Imagery** — High-resolution event-driven imagery from the Maxar Open Data Program (CC-BY-NC 4.0). Displays available crisis imagery footprints with metadata and optional COG overlay loading.
- **Maritime Boundaries** — Interactive territorial waters layer from Marine Regions/VLIZ showing EEZ boundaries, 12nm territorial seas, and 24nm contiguous zones. Click anywhere in the water to identify the maritime zone via WFS queries.
- **Aircraft Tracking** — Live ADS-B aircraft positions from airplanes.live, adsb.lol, and OpenSky Network (automatic fallback chain) across the Middle East bounding box. Filterable by aircraft type (large, medium, rotorcraft, ground vehicle), with 30-second auto-refresh, click popups showing callsign, altitude, velocity, heading, and squawk code.

## Key Features

- **Live data** — Pulls directly from NASA FIRMS API with CORS proxy fallback. No API key required for open data mode.
- **Confidence filtering** — Defaults to high-confidence detections only. Nominal and low thresholds available for full coverage including agricultural burns and sensor noise.
- **Proximity tagging** — Automatic spatial analysis flags detections near known industrial infrastructure, helping analysts distinguish conflict signatures from routine operations.
- **Satellite imagery** — Three toggleable optical imagery layers (MODIS, Sentinel-2, Maxar) for visual corroboration of thermal detections. All free and open, no API keys needed.
- **Maritime awareness** — Interactive maritime boundary layers (EEZ, territorial seas, contiguous zones) for understanding territorial context of offshore activity.
- **Aircraft surveillance** — ADS-B integration via airplanes.live/adsb.lol/OpenSky shows live air traffic with type filtering, callsign labels, and detailed metadata popups.
- **Timeline animation** — Step through each day of the observation window with play/pause controls at 1x/2x/4x speed.
- **Shareable views** — Current map state (position, zoom, active layers, filters) encoded into a URL hash for one-click sharing.
- **Export** — Screenshot the current view as a PNG with title bar, legend overlay, detection stats, and source attribution baked in.
- **Responsive** — Works on desktop, tablet, and mobile. Sidebar auto-collapses on small screens.

## Architecture

The entire application is a single HTML file (~5,000 lines). No build step, no backend, no dependencies to install. Open it in a browser and it works.

**Stack:** MapLibre GL JS v4.1.2 / Turf.js v7 / IBM Plex typography / CartoDB + Esri basemaps

**Data sources:**
| Layer | Source | Update Frequency |
|-------|--------|-----------------|
| Thermal | [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/) | Near real-time (~3hr latency) |
| Industrial | [EOG/VIIRS Nightfire](https://eogdata.mines.edu/products/vnf/global_gas_flare.html), [World Bank GGFR](https://www.worldbank.org/en/programs/gasflaringreduction) | Static catalog |
| Conflict (Live) | [GDELT](https://www.gdeltproject.org/) GKG | Live, 24-hour rolling window |
| Conflict (Coded) | [ACLED](https://acleddata.com/) | Expert-coded, ~1-2 week lag, rolling 30-day window |
| Conflict (Archive) | [UCDP GED](https://ucdp.uu.se/) v25.1 | Annual release (through Dec 2024) |
| Nighttime | [NASA GIBS](https://earthdata.nasa.gov/gibs) VIIRS DNB | Daily composites |
| MODIS True-Color | [NASA GIBS](https://earthdata.nasa.gov/gibs) MODIS Terra | Daily composites |
| Sentinel-2 | [AWS Earth Search](https://earth-search.aws.element84.com/v1) STAC | On-demand query |
| Maxar Crisis | [Maxar Open Data](https://www.maxar.com/open-data) | Event-driven |
| Maritime | [Marine Regions](https://marineregions.org/) / VLIZ WMS+WFS | Static boundaries |
| Aircraft | [airplanes.live](https://airplanes.live), [adsb.lol](https://adsb.lol), [OpenSky](https://opensky-network.org) ADS-B | Live, 30-second refresh |

## Usage

```
# No install required — just open in a browser
open meridian.html
```

1. Click **Load Satellite Data** to pull the latest detections from NASA FIRMS
2. Use the confidence, satellite, and time filters to narrow the signal
3. Toggle overlay layers (Industrial Sites, Conflict Events, Nighttime Lights, Satellite Imagery, Maritime Boundaries, Aircraft Tracking) for multi-source analysis
4. Click any detection for full metadata including satellite, FRP, brightness temperature, and industrial proximity
5. Use **Share View** to copy a stateful URL or **Export** to save a publication-ready screenshot

## User Guide

### 1. Load the data
Click **Load Satellite Data** in the sidebar. This pulls the latest thermal anomaly detections from NASA FIRMS. It takes a few seconds.

### 2. Explore the map
Heat detections appear as colored dots across the Middle East. Red/orange = high confidence, yellow = nominal. Click any dot for details like satellite source, fire radiative power, and whether it's near known infrastructure.

### 3. Filter what you see
Use the sidebar panels to narrow results:
- **Region** — Focus on a specific country (Iran, Iraq, Syria, etc.)
- **Confidence** — Default is "high" only. Lower it to see more detections (includes agricultural burns and noise)
- **Satellite** — Toggle individual sensors on/off
- **Time Window** — Adjust the date range

### 4. Add overlay layers
Toggle these in the sidebar for multi-source analysis:
- **Industrial Sites** — Shows refineries and plants so you can distinguish routine flaring from unusual activity
- **Conflict Events** — GDELT (live), ACLED (expert-coded), and UCDP GED (archive) data showing armed conflict, protests, and military activity
- **Nighttime Lights** — Before/after satellite imagery to spot power grid disruption
- **MODIS / Sentinel-2 / Maxar** — Optical satellite imagery for visual confirmation
- **Maritime Boundaries** — EEZ, territorial seas, and contiguous zones
- **Aircraft Tracking** — Live air traffic with callsigns and altitude

### 5. Share or export
- **Share View** (utility bar) — Copies a URL that preserves your exact map state, filters, and layers
- **Export** (utility bar) — Saves a publication-ready PNG screenshot with stats and attribution

### Tips
- Use the **Timeline Player** at the bottom to animate detections day-by-day
- Switch basemaps (bottom of sidebar) between dark, satellite, and terrain views
- The sidebar auto-collapses on mobile — tap the toggle to reopen it

## Data Attribution & Terms of Use

This project uses the following data sources in compliance with their respective terms of service:

- **[NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/)** — Near real-time fire data from VIIRS and MODIS instruments. Open data, no restrictions on use. Credit: NASA/GSFC, LANCE FIRMS.
- **[NASA GIBS](https://earthdata.nasa.gov/gibs)** — VIIRS Day/Night Band and MODIS imagery tiles. Open data. Credit: NASA Worldview, EOSDIS.
- **[GDELT](https://www.gdeltproject.org/)** — Global Database of Events, Language & Tone. Open data under GDELT's open research terms. All GDELT data is free and open for any use.
- **[ACLED](https://acleddata.com/)** — Armed Conflict Location & Event Data. Used under ACLED's terms of use for non-commercial research and journalism. ACLED data must be attributed as: "Armed Conflict Location & Event Data Project (ACLED); www.acleddata.com". ACLED data is not to be redistributed.
- **[UCDP GED](https://ucdp.uu.se/)** — Uppsala Conflict Data Program Georeferenced Event Dataset. Open academic data. Citation: Davies et al. (2024). UCDP Georeferenced Event Dataset Codebook, Version 25.1.
- **[EOG/VIIRS Nightfire](https://eogdata.mines.edu/products/vnf/global_gas_flare.html)**, **[World Bank GGFR](https://www.worldbank.org/en/programs/gasflaringreduction)** — Industrial gas flare site locations. Open data.
- **[ESA Copernicus Sentinel-2](https://earth-search.aws.element84.com/v1)** — 10m optical imagery via AWS Earth Search STAC. Open data under Copernicus license (free, full, and open).
- **[Maxar Open Data](https://www.maxar.com/open-data)** — Crisis imagery under CC-BY-NC 4.0 license. Attribution: "Maxar Open Data Program".
- **[Marine Regions](https://marineregions.org/) / VLIZ** — Maritime boundary data. Credit: Flanders Marine Institute (VLIZ). Data used in accordance with Marine Regions' terms of use.
- **[airplanes.live](https://airplanes.live)**, **[adsb.lol](https://adsb.lol)**, **[OpenSky Network](https://opensky-network.org)** — Live ADS-B aircraft positions. OpenSky data used under Creative Commons Attribution 4.0 license.
- **[OpenStreetMap](https://www.openstreetmap.org/)** — Base map data. &copy; OpenStreetMap contributors, ODbL license.
- **[Natural Earth](https://www.naturalearthdata.com/)** — Country boundary data. Public domain.

Built by [Subtxt Press](https://subtxtpress.github.io/home/)
