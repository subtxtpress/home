# Preservation Slate and Tile — Handoff Info

Static reference design for migration to Wix. Four pages, one shared stylesheet.

---

## Pages

| File | Page | Description |
|---|---|---|
| `home.html` | Home | Full-viewport hero, credentials strip, key points, structures photo strip, CTA |
| `about.html` | About | Three text sections with sidebar labels, commitment block, CTA |
| `gallery.html` | Gallery | 9-photo 3-column grid with lightbox, CTA |
| `contact.html` | Contact | Two-column layout: info sidebar + project request form |

All pages share:
- Navigation (header): fixed to top, collapses to hamburger on mobile (≤640px)
- Footer: dark background, logo + nav links + copyright
- Stylesheet: `assets/css/main.css`

---

## Assets

```
assets/
  css/
    main.css                         ← entire site stylesheet
    association-memberships/         ← 4 certification logos (used in credentials strip on home page)
    roof-photos/                     ← 9 project photos (used in gallery and home structures strip)
    patents/                         ← historical patent PDFs (not yet placed on any page)
    public-domain-artwork/           ← archival images and PDFs (not yet placed on any page)
    logo.png                         ← site logo (not yet placed in nav — wordmark text is used as placeholder)
    stock-1.png through stock-4.png  ← NOT REFERENCED on any page; confirm with client before discarding
    stock-5.png                      ← used on home structures strip (landmark/institutional panel)
```

---

## Open Items — Resolve Before Launch

### 1. Service Area — Contact Page
**File:** `contact.html`, look for `[Service Region]`  
Replace the placeholder with the actual geographic area the client serves.

### 2. Contact Form — Not Connected
The form on `contact.html` runs client-side validation only. Currently: On submit it shows a success message but sends nothing.

**Recommended for Wix:** Replace with a native Wix Form widget. The field structure is:
- Full Name (required)
- Organization (optional)
- Project Address (required)
- Preservation/Heritage Status (dropdown — see options in `contact.html`)
- Scope Summary (required)
- Email (required)
- Phone (optional)

**Alternative (non-Wix):** Connect to Formspree by adding `action="https://formspree.io/f/{id}" method="POST"` to the `<form>` tag.

### 3. Domain Placeholders — OG and Canonical Tags
All pages now have full Open Graph, Twitter Card, and canonical URL tags. Every URL in those tags uses `[YOUR-DOMAIN]` as a placeholder. Before launch, do a find-and-replace across all four HTML files:

- Find: `[YOUR-DOMAIN]`
- Replace with: the actual Wix domain (e.g. `www.preservationslateandtile.com`)

Also check the canonical paths (`/`, `/about`, `/projects`, `/contact`) match the actual Wix page URLs — Wix may use different slugs.

### 4. OG Images — Replace Placeholders with Proper Sized Images
The OG image tags currently point to existing roof photos. These will work but the photos are not cropped to the optimal 1200×630 px ratio for link previews. Recommended: create a purpose-built 1200×630 image for each page (or one shared image for the whole site) and update `og:image` and `twitter:image` accordingly. A simple branded composition with the logo and a cropped photo works well.

### 5. Favicon Files Missing
The HTML now references these favicon files in `icons/`, but none of them exist yet:
- `icons/favicon.ico`
- `icons/icon-192.png`
- `icons/icon-512.png`
- `icons/apple-touch-icon.png`

Recommended: go to [realfavicongenerator.net](https://realfavicongenerator.net), upload a 512×512 PNG of the logo, download the package, and place the files in `icons/`. The webmanifest (`icons/site.webmanifest`) has been updated for this project — do not replace it with the one from the generator unless you merge the fields.

**Note:** The `icons/site.webmanifest` that was in this folder previously belonged to a different project (MERIDIAN satellite dashboard). It has been replaced with a correct manifest for Preservation Slate and Tile.

### 5. Logo
`assets/logo.png` exists but is not used in the nav. Currently the nav uses the wordmark as styled text. If the client wants the logo image in the nav, swap the `.nav-logo` content accordingly.

### 6. Patents and Public Domain Artwork
`assets/patents/` and `assets/public-domain-artwork/` contain historical documents and images. These are not linked from any page yet. If the client wants a resources, history, or reference section, these are the source materials.

### 7. Unused Stock Images
`assets/stock-1.png` through `stock-4.png` are not referenced on any page. Confirm with client whether these should be used, swapped, or discarded.

---

## Design System

**Fonts:** Cormorant Garamond (headings), Source Sans 3 (body).  
Both are available in Wix's font library. Load them from Google Fonts or upload OTF/TTF files for print use.

**Colors** (defined as CSS custom properties in `main.css`):

| Token | Hex | Use |
|---|---|---|
| `--copper` | `#967244` | Primary accent, buttons, borders, eyebrow labels |
| `--copper-dark` | `#7A5C38` | Hover state for copper elements |
| `--ink` | `#1B1916` | Headings, dark section backgrounds, footer |
| `--charcoal` | `#2E2A26` | Body text |
| `--parchment` | `#F0E8D6` | Light text on dark backgrounds |
| `--bg` | `#F7F3EB` | Page background |
| `--cream` | `#E4D8C2` | CTA strip background |
| `--stone` | `#8C8080` | Secondary/muted text |
| `--stone-light` | `#BEB6A6` | Secondary text on dark backgrounds |

To change a color site-wide, update the token value in `:root` in `main.css` — do not change individual selectors.

---

## Wix Migration Notes

Wix does not import HTML files directly. This folder is the reference design. Rebuild pages in the Wix editor using the HTML structure and CSS design tokens as a spec.

**Key Wix equivalents:**

| This site | Wix approach |
|---|---|
| Fixed nav with hamburger | Wix Header component, set sticky |
| Credentials strip logos | Strip with image boxes, grayscale effect via image settings |
| Hero with background image | Full-width strip, background image set to cover |
| Gallery with lightbox | Wix Pro Gallery widget |
| Contact form | Wix Form widget |
| Footer | Wix Footer component |
| Sticky sidebar labels (about page) | Two-column strip, left column set sticky while scrolling |

**Custom code blocks (Wix):** Any interaction that cannot be built with Wix native widgets — such as the current JS lightbox or the hamburger animation — can be implemented in Wix using an HTML iframe element or Wix's Velo (JavaScript) platform.

---

## Responsive Breakpoints

| Breakpoint | Layout changes |
|---|---|
| ≤860px | About page sidebar stacks above content; contact layout stacks; footer nav goes horizontal |
| ≤720px | Structures strip goes 2-column (third panel hidden) |
| ≤640px | Nav collapses to hamburger; gallery goes 2-column; key points go 1-column; structures strip goes 1-column |

---

## File Naming

All asset filenames have been normalized to lowercase-hyphenated format (e.g. `vermont-blend-slate.jpg`) and uppercase extensions lowercased (`.PNG` → `.png`). Two typos were corrected in the process:

- `Memebership TRIA.png` → `membership-tria.png` (extra "e" fixed)
- `Chimey Flashing.PNG` → `chimney-flashing.png` ("Chimney" spelling fixed)

All HTML references have been updated to match.
