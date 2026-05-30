# Subtxt Press — Static Site (gh-pages)

Static HTML site hosted on GitHub Pages at `subtxtpress.github.io/home/`.
No build system — all pages are standalone HTML files with inline CSS/JS.

## Design System

- **Palette**: cream `#F4EDE3`, peach `#E8956A`, plum `#3E2436`, carmine `#7A5063`, ink `#241620`
- **Fonts**: Barlow Condensed (headings), IBM Plex Mono (labels/mono), Inter (body), Raleway (card titles)
- **Dark theme** (case maps/timelines): bg `#060B14`, teal `#4a8a7c`, red `#C04E01`, accent `#ebe2cd`
- **Date format**: always `MM-DD-YYYY` (dashes, not slashes)
- Vendor deps: Bootstrap Icons, AOS (scroll animations), Leaflet (maps)

## Templates

### Dockets (`dockets/_templates/`)

| File | Use |
|---|---|
| `docket.html` | Embedded PDF docket (Google Drive iframe) |
| `docket-typed.html` | Typed-in docket — filing entries, case headers, tables |
| `card-snippet.html` | Card block to paste into `dockets/cases.html` |

**Workflow — new docket page:**
1. Create folder: `dockets/{SLUG}/`
2. Copy the appropriate template into it as `docket.html`
3. Replace all `{{PLACEHOLDER}}` values
4. Add a card entry to `dockets/cases.html` using `card-snippet.html`

**Typed docket entry types** (in `docket-typed.html`):
- `.filing` with `a.filing-link` — linked document + date
- `.filing` with `.filing-note` — filing + blockquote (court orders, quotes)
- `.filing` with `span.filing-bold` — bold text entry (hearings, clerk notes)
- `.case-block` — two-column case header with OPEN/CLOSED badge
- `.docket-table` — tabular data (case events, documents)

**Multi-case docket pages:**
- For subjects with multiple cases (e.g., JLR), repeat the `case-block` + `section-label` + `filings` pattern for each case
- For standalone filings that don't belong to a specific case (prior records, incident reports, background docs), use a `.filings` block without a `.case-block` header — just a `.section-label` above it
- Case meta grid is flexible — add/remove `case-meta-item` rows as needed (not all cases have the same fields)

### Case Maps (`case/_templates/`)

| File | Use |
|---|---|
| `scrolly-map.html` | Scrollytelling timeline with Leaflet map |

**Workflow — new scrolly timeline:**
1. Create folder: `case/{slug}/`
2. Copy `scrolly-map.html` into it as `timeline.html`
3. Replace meta tag placeholders
4. Fill in the JS data section at top of `<script>`: `KML_DATA`, `FOCUS_POINTS`, `COLORS`, `STEP_META`, `MAP_CENTER`, `MAP_ZOOM`
5. Write `.step` content blocks in `#narrative`
6. Add case-specific marker logic in the `activateStep()` function if needed

**Step content blocks** (mix and match inside each `.step`):
- `.step-time` + `.step-title` + `p` — basic narrative beat
- `.person-pill` — colored dot + name label
- `.step-figure` — single image with caption
- `.step-gallery` — 2-column image grid (lightbox on click)
- `.step-embed` with `.embed-placeholder` — click-to-load iframe (transcripts, audio)
- `.callout` — highlighted callout box

## Case Input Format

When the user provides case details in this format, use the appropriate template and fill everything in:

```
Type: docket | docket-typed | scrolly-map
Name: [case/person name]
Folder: [slug for the folder name]
Masthead: [title shown in the hero banner]
Court: [jurisdiction · court · case type]
Case number: [case number]
Status: open | closed
Judge: [judge name]
Petitioner: [name]
Attorney for Petitioner: [name]
Respondent: [name]
Attorney for Respondent: [name]
Drive folder ID: [Google Drive folder ID]
Documents:
  - 01: [title] | [Google Drive file ID]
  - 02: [title] | [Google Drive file ID]
Card description: [1-2 sentence summary for cases.html]
Tags: [tag1, tag2, tag3]
```

Not all fields are required — use what's provided. For scrolly-map type, also expect:
```
Map center: [lat, lng]
Map zoom: [number]
Locations:
  - [name] | [lat, lng] | [description]
```

## File Structure

```
home/
├── index.html, policies.html
├── assets/img/, assets/vendor/
├── icons/
├── dockets/
│   ├── cases.html          ← docket index (card grid)
│   ├── _templates/         ← docket templates
│   ├── HTC/, JLR/, SGP/    ← individual docket pages
│   └── Klein-v-Samsen/, tricia-griffith/
├── case/
│   ├── maps.html           ← case map index
│   ├── _templates/         ← case map templates
│   ├── magnolia/, zach-adams/, tiera-strand/
│   ├── HTC/, kelsey-fitzsimmons/
```

## Asset Paths

From `dockets/{SLUG}/docket.html`: icons at `../../icons/`, assets at `../../assets/`, cases index at `../cases`
From `case/{slug}/timeline.html`: icons at `../../icons/`, assets at `../../assets/`
