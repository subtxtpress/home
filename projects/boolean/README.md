# Boolean Search Generator

A visual tool for building boolean search queries without memorizing syntax. Part of [Subtxt Press](https://subtxtpress.github.io/home/).

## What it does

Lets you construct complex search queries by filling in plain-language fields instead of writing raw boolean syntax. Generates the correct operators for whichever platform you're targeting, then lets you copy the query or search directly.

## Supported platforms

| Platform | Search button | Notes |
|---|---|---|
| Google | Opens Google | Full operator support including AROUND, date params |
| Bing | Opens Bing | Uses NEAR/n, inbody: |
| DuckDuckGo | Opens DuckDuckGo | Basic boolean, no proximity |
| LinkedIn | Opens LinkedIn | AND/OR/NOT only, no advanced operators |
| Twitter / X | Opens X search | from:, to:, since:, until:, filter: |
| Reddit | Opens Google w/ site:reddit.com | Auto-adds site filter |
| PubMed | Opens PubMed | Field tags: [Title], [Author], [MeSH Terms] |
| LexisNexis | Opens Lexis+ | W/n proximity, PRE/n, wildcard truncation |
| Google Scholar | Opens Scholar | Case law, papers, author: search |
| CourtListener | Opens CourtListener | Court opinions, caseName:, judge:, court: |
| Wayback Machine | Opens archive.org | URL snapshots, wildcard paths |
| Generic Boolean | Opens Google | Standard AND/OR/NOT for any platform |

## Features

- **Three term groups**: "must contain all", "must contain at least one", "hide results containing" — maps to AND, OR, NOT
- **Exact match toggle**: Wraps terms in quotes per group
- **Filters**: Site/domain, file type, search location (title/URL/body), date range (preset or custom), related URLs, cache/info, proximity
- **Platform-aware UI**: Only shows filters the selected platform supports
- **Syntax highlighting**: Operators, quoted phrases, filters, and parentheses color-coded in the preview
- **Copy / Search**: One-click copy to clipboard or open results on the target platform
- **Saved searches**: Persisted in localStorage with platform label, timestamp, and delete
- **Cheat sheet**: Clickable operator reference that updates per platform
- **Raw append**: Manual input for anything the builder doesn't cover
- **Comma-separated input**: Add multiple terms at once

## Tech

Single HTML file, no build step, no dependencies beyond Google Fonts and Bootstrap Icons (loaded from the parent site's assets). All state is in-memory JS; saved searches use localStorage.

## File structure

```
tools/boolean/
├── index.html    # The tool (self-contained)
└── README.md     # This file
```
