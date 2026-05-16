# State v. Zachary Adams — Interactive Case Map

An interactive map built for the Holly Bobo murder case (*State v. Zachary Rye Adams*), allowing users to explore geographic data introduced at trial — including evidence sites, cell tower records, GPS trail data, and a chronological phone timeline.

## Features

- **Satellite & Dark basemaps** — toggle between Esri World Imagery and CartoDB Dark Matter
- **8 toggleable data layers** — case locations, evidence sites, residences, cell towers, route markers, and more
- **Animated Phone Timeline** — step through call/ping events chronologically with per-step popups
- **Animated GPS Trail** — replay a step-by-step reconstruction of a GPS path with coordinate popups
- **Info cards section** — scrollable layer descriptions with map toggle buttons
- **Mobile responsive** — collapsible panel, touch-friendly controls

## Data Layers

| Layer | Description |
|---|---|
| Major Events | Abduction site, recovery location, and other key case locations |
| Evidence & Key Locations | Physical evidence collection and forensically significant sites |
| People & Residences | Addresses of defendants, witnesses, and persons of interest |
| Cell Towers | Tower locations used to reconstruct movement via call records |
| Other Locations | Roads, landmarks, and contextual geographic references |
| Phone GPS Trail | Animated replay of GPS coordinates from a recovered device |
| Route Markers | Annotated paths and roads referenced in trial testimony |
| Phone Timeline | Chronological phone activity mapped to geographic locations |

## Tech Stack

- [Leaflet.js](https://leafletjs.com/) v1.9.4
- Esri World Imagery (satellite tiles, no API key required)
- CartoDB Dark Matter (dark tiles, no API key required)
- KML data parsed to embedded JSON — no server-side dependencies
- Single self-contained HTML file

## Usage

Open `index.html` in any modern browser, or serve locally:

```bash
python3 -m http.server 4321
```

Then visit `http://localhost:4321`.

## Source Data

Geographic data derived from KML files referencing locations introduced in evidence and public court records from the *State v. Zachary Rye Adams* trial (Decatur County, Tennessee).

This project is based on an original Google Earth map compiled by DB:
[earth.google.com/earth/d/1GEM-lvKOTMQt5XfsM0KHNccPl-ajy_vU](https://earth.google.com/earth/d/1GEM-lvKOTMQt5XfsM0KHNccPl-ajy_vU)
