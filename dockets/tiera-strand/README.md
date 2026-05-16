# Tiera Strand — Investigative Timeline

An interactive scroll-driven investigative map tracing the disappearance and death of **Tiera Strand**, 25, last seen April 16, 2023, on Austin's 6th Street. Her remains were recovered in Bell County, Texas. The case remains active.

Published by [Subtxt Press](https://subtxtpress.github.io/home/).

## Overview

This is a single-page investigative timeline that pairs a scrolling narrative with a synchronized Leaflet map. As the reader scrolls through each event in the case, the map flies to the relevant location, renders markers and routes, and updates a clock overlay with corresponding dates and times. The experience is designed for both desktop and mobile.

## Features

- **Scroll-driven map narrative** — 14 timeline steps synchronized with map state via Scrollama + a fallback scroll listener for iOS compatibility
- **Leaflet map** — dark CARTO basemap with custom `divIcon` markers, pulsing animations, labeled locations, and dashed polyline routes
- **Progress bar** — fixed top bar tracking scroll position through the narrative
- **Video and photo modals** — embedded media with keyboard (Escape) and overlay-click dismissal
- **Clock overlay** — date/time display updating per step to anchor the reader in the timeline
- **Full OG/Twitter meta** — social preview cards with custom image, canonical URL, and Subtxt Press branding
- **Responsive layout** — narrative panel adapts between desktop sidebar and mobile overlay

## Tech Stack

- **Leaflet 1.9.4** — map rendering and marker management
- **Scrollama** — Intersection Observer–based scroll triggers
- **CARTO Dark** — basemap tiles via OpenStreetMap/CARTO
- **Google Fonts** — Cormorant Garamond, Barlow Condensed, IBM Plex Mono, Inter
- **Vanilla JS/CSS** — no build step, no framework dependencies

## File Structure

```
tiera-strand/
├── case-map.html          # Full application (single-file)
├── tiera-strand.png       # OG/social preview image
├── README.md              # This file
└── public/
    └── icons/
        ├── favicon.ico
        ├── icon-16.png
        ├── icon-32.png
        ├── icon-180.png
        └── site.webmanifest
```

## Running Locally

No build step required. Serve the directory with any static server:

```bash
npx serve .
# or
python3 -m http.server 8000
```

Open `http://localhost:8000/case-map.html`.

## Deployment

The timeline is published via GitHub Pages at:

```
https://subtxtpress.github.io/home/cases/tiera-strand/case-map
```