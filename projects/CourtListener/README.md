# CourtListener Search Tool

An interactive web interface for searching federal court data using the CourtListener API v4.

## Features

- **Case/Docket Search** - Find cases by party name, judge, or court
- **Case Law Search** - Search published opinions and decisions
- **Judge Lookup** - Find federal judges by name and court
- **Judge Profile** - One-click bio, positions, and recent assigned dockets for a single judge
- **RECAP Archive Search** - Access free PACER documents
- **Court Directory** - Browse all available federal courts
- **Court dropdown** - All federal courts populated from the API and cached per session
- **CSV Export** - Download any result set (including a judge's docket list) as CSV
- **Pagination** - Navigate through large result sets
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Light Theme UI** - Warm light-mode palette with modern aesthetic

## Setup

### 1. Get Your API Token

Visit the [CourtListener API page](https://www.courtlistener.com/help/api/rest/) to sign up for a free account and obtain your API token.

### 2. Configure Your Token

The easiest way is to copy `.env.example` to `.env` and paste your token:

```bash
cp .env.example .env
# then edit .env and replace `your-token-here` with your real token
```

`app.py` auto-loads `.env` from this folder on startup. The `.env` file is gitignored so the token will not be committed.

Alternatively, export it in your shell:

```bash
export COURTLISTENER_TOKEN="your-token-here"
```

### 3. Install Dependencies

```bash
pip install fastapi uvicorn requests
```

(If you don't have `requests` installed, the CourtListener toolkit requires it as a dependency.)

### 4. Run the Backend Server

```bash
python app.py
```

The server will start on `http://localhost:8000`

Output:
```
🚀 Starting CourtListener Search API...
   Open: http://localhost:8000/search.html
   Docs: http://localhost:8000/docs
```

### 5. Access the Web Interface

Open your browser to:
- **Web Interface**: http://localhost:8000/search.html
- **API Documentation**: http://localhost:8000/docs (interactive API explorer)

## Usage

### Web Interface

1. Select a search type from the tabs (Cases, Opinions, Judges, Judge Profile, RECAP, Courts)
2. Enter your search criteria (party name, judge name, keywords, etc.) and pick a court from the dropdown if you want to narrow it
3. Click "Search" to submit
4. Results appear below with pagination controls
5. Click **Export CSV** in the results header to download the current result set
6. The Judge Profile tab returns a single judge's bio, positions, and recent dockets in one shot — Export CSV downloads the docket list

### API Endpoints

If you prefer to interact directly with the API:

```bash
# Search cases by party
curl "http://localhost:8000/api/search/cases?party=Apple&limit=10"

# Search case law
curl "http://localhost:8000/api/search/opinions?query=patent&court=cafc&limit=10"

# Find judges
curl "http://localhost:8000/api/search/judges?name=Roberts&limit=10"

# Pull a full judge profile (bio + recent dockets) in one call
curl "http://localhost:8000/api/judge-profile?name=Tanya+Chutkan&max_cases=25"

# List federal courts
curl "http://localhost:8000/api/courts"

# Get case details
curl "http://localhost:8000/api/case/12345"
```

See `http://localhost:8000/docs` for complete API documentation.

## API Reference

### Search Endpoints

- `GET /api/search/cases` - Docket search by party, judge, court
- `GET /api/search/opinions` - Case law search by keywords
- `GET /api/search/judges` - Judge lookup by name
- `GET /api/judge-profile` - Single-judge bio + recent assigned dockets
- `GET /api/search/recap` - RECAP archive search
- `POST /api/search/advanced` - Combined filter search
- `GET /api/courts` - List all federal courts
- `GET /api/case/{case_id}` - Get single case details
- `GET /api/health` - Backend health check

### Response Format

All successful responses return:

```json
{
  "status": "success",
  "total": 42,
  "page": 1,
  "count": 20,
  "results": [ /* ... */ ],
  "timestamp": "2024-04-27T14:30:00.000Z"
}
```

## Limitations

- **Rate Limits**: CourtListener API applies rate limiting. Free accounts have limits on requests per day. Check their [API documentation](https://www.courtlistener.com/help/api/rest/) for current limits.
- **Search Delay**: Large datasets may take several seconds to return. The interface shows a loading spinner while fetching.
- **Token Required**: All requests require a valid `COURTLISTENER_TOKEN`. If the token is not set, searches will fail with a 503 error.
- **Backend Deploy is Manual**: Pushing to GitHub auto-deploys the frontend (GitHub Pages) but not the backend API on the GCP VM (see Deployment below).

## Deployment

### Architecture

The frontend and backend are deployed separately:

- **Frontend** (`search.html`, `readme.html`) — hosted on **GitHub Pages** at `subtxtpress.github.io`. Pushing to the `main` branch auto-deploys the static files.
- **Backend** (`app.py`) — runs on a **Google Cloud Compute Engine** VM (`courtlistener` instance, `us-west1-b`) under the `subtxtpress` project. The API is at `courtlistener.subtxtpress.com`.

### Frontend Deploys

Pushing to `main` on GitHub auto-deploys the HTML files via GitHub Pages. No extra steps needed for frontend changes.

### Backend Deploys (Manual)

The VM has no git repo — backend files were copied manually. Pushing to GitHub does **not** update the API server.

```bash
# SSH into the VM
gcloud compute ssh courtlistener --zone=us-west1-b --project=subtxtpress

# Backend files live at ~/courtlistener
cd ~/courtlistener

# Copy updated files (e.g. via scp or paste)
# Then restart the server
sudo systemctl restart courtlistener  # or however the process is managed
```

To streamline this, you could initialize a git repo on the VM (`git init` + add a remote) so future updates are just `git pull`.

## Troubleshooting

### "CourtListener API not initialized" Error

**Problem**: You see a 503 error or warning about the token not being set.

**Solution**: Make sure the `COURTLISTENER_TOKEN` environment variable is set:

```bash
export COURTLISTENER_TOKEN="your-actual-token"
python app.py
```

### CORS Errors in Browser Console

**Problem**: You see "No 'Access-Control-Allow-Origin' header" errors.

**Solution**: Make sure `app.py` is running and the API base URL in `search.html` matches your backend URL. For local development, it should be `http://localhost:8000`.

### "Module Not Found" Error

**Problem**: `ImportError: No module named 'fastapi'`

**Solution**: Install dependencies:

```bash
pip install fastapi uvicorn requests
```

### Slow Searches

**Problem**: Searches are taking longer than expected.

**Solution**: CourtListener queries can be slow depending on:
- Query complexity (more filters = slower)
- Result set size (large result sets take longer to fetch)
- Network latency
- CourtListener API server load

Try narrowing your search with more specific filters.

## Files

- `search.html` - Interactive web interface (served at `/` and `/search.html`)
- `app.py` - FastAPI backend wrapper around the CourtListener API (auto-loads `.env`)
- `.env.example` - Template for your API token; copy to `.env` and fill in
- `.env` - Your local token (gitignored, not committed)
- `courtlistener_toolkit.py` - Core Python client library (do not modify)
- `courtlistener_explorer.py` - Alternative CLI tool (not used by web interface)

## Related Resources

- [CourtListener Official Website](https://www.courtlistener.com/)
- [CourtListener API Documentation](https://www.courtlistener.com/help/api/rest/)
- [Federal Court Jurisdiction Guide](https://www.courtlistener.com/help/citations/)
- [PACER Document Search](https://pacer.uscourts.gov/)

## License

CourtListener data is provided under the terms of their API agreement. See [CourtListener Terms of Service](https://www.courtlistener.com/terms/).

---

**Last Updated**: April 27, 2026
