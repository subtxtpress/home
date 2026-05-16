#!/usr/bin/env python3
"""
CourtListener API wrapper for web interface.

Wraps courtlistener_toolkit.py to expose search functions as REST endpoints.

Setup:
    export COURTLISTENER_TOKEN="your-token-here"
    pip install fastapi uvicorn requests
    python app.py

Then visit: http://localhost:8000/search.html
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, List

# Load .env file from this directory if present (no python-dotenv dependency)
_env_path = Path(__file__).parent / ".env"
if _env_path.exists():
    for line in _env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import FileResponse, JSONResponse
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.staticfiles import StaticFiles
    import requests
except ImportError:
    print("ERROR: Required packages not installed.")
    print("Run: pip install fastapi uvicorn requests")
    sys.exit(1)

# Import the existing toolkit
try:
    from courtlistener_toolkit import CourtListenerClient
except ImportError:
    print("ERROR: courtlistener_toolkit.py not found in this directory.")
    sys.exit(1)

app = FastAPI(
    title="CourtListener Search API",
    description="REST API wrapper for federal court data search",
    version="1.0.0"
)

# Enable CORS for all origins (allows gh-pages to call this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve search.html at root
@app.get("/")
async def root():
    if os.path.exists("search.html"):
        return FileResponse("search.html")
    return {"message": "CourtListener Search API", "docs": "/docs"}

@app.get("/search.html")
async def serve_html():
    if os.path.exists("search.html"):
        return FileResponse("search.html", media_type="text/html")
    raise HTTPException(status_code=404, detail="search.html not found")

# Initialize client
token = os.getenv("COURTLISTENER_TOKEN")
if not token:
    print("WARNING: COURTLISTENER_TOKEN env var not set.")
    print("Set it before running: export COURTLISTENER_TOKEN='your-token-here'")
    print("Get your token at: https://www.courtlistener.com/help/api/rest/")
    client = None
else:
    try:
        client = CourtListenerClient(token)
    except Exception as e:
        print(f"ERROR initializing client: {e}")
        client = None

def require_client():
    if not client:
        raise HTTPException(
            status_code=503,
            detail="CourtListener API not initialized. Set COURTLISTENER_TOKEN environment variable."
        )

def format_response(results, total=None, page=None):
    """Format results into standard response."""
    return {
        "status": "success",
        "total": total,
        "page": page,
        "count": len(results) if isinstance(results, list) else 1,
        "results": results,
        "timestamp": datetime.utcnow().isoformat()
    }

# ─── Search Endpoints ───────────────────────────────────────

@app.get("/api/search/cases")
async def search_cases(
    query: Optional[str] = None,
    party: Optional[str] = None,
    judge: Optional[str] = None,
    court: Optional[str] = None,
    limit: int = 20
):
    """Search dockets by party name, judge, or keywords."""
    require_client()

    if not query and not party:
        raise HTTPException(status_code=400, detail="Provide either 'query' or 'party' parameter")

    try:
        results, total = client.search_dockets(
            query=query,
            party=party,
            judge=judge,
            court=court,
            max_results=limit
        )
        return format_response(results, total=total)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search/opinions")
async def search_opinions(
    query: str,
    court: Optional[str] = None,
    limit: int = 20
):
    """Search case law / opinions."""
    require_client()

    if not query:
        raise HTTPException(status_code=400, detail="'query' parameter required")

    try:
        results, total = client.search_opinions(
            query=query,
            court=court,
            max_results=limit
        )
        return format_response(results, total=total)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search/judges")
async def search_judges(
    name: str,
    court: Optional[str] = None,
    limit: int = 20
):
    """Search federal judges by name."""
    require_client()

    if not name:
        raise HTTPException(status_code=400, detail="'name' parameter required")

    try:
        results, total = client.search_judges(
            name=name,
            court=court,
            max_results=limit
        )
        return format_response(results, total=total)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search/recap")
async def search_recap(
    query: str,
    court: Optional[str] = None,
    limit: int = 20
):
    """Search RECAP archive (free PACER)."""
    require_client()

    if not query:
        raise HTTPException(status_code=400, detail="'query' parameter required")

    try:
        results, total = client.search_recap(
            query=query,
            court=court,
            max_results=limit
        )
        return format_response(results, total=total)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/courts")
async def list_courts(jurisdiction: str = "F"):
    """List available federal courts."""
    require_client()

    try:
        results = client.get_courts(jurisdiction=jurisdiction)
        return format_response(results, total=len(results) if results else 0)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/judge-profile")
async def judge_profile(
    name: str,
    court: Optional[str] = None,
    max_cases: int = 25
):
    """
    Look up a judge by name and return their bio + recent dockets.
    Used by the Judge Profile tab in the web UI.
    """
    require_client()

    if not name:
        raise HTTPException(status_code=400, detail="'name' parameter required")

    try:
        # Step 1: find the judge (best match)
        judges, _ = client.search_judges(name=name, court=court, max_results=1)
        if not judges:
            raise HTTPException(status_code=404, detail=f"No judge found matching '{name}'")
        judge = judges[0]

        # Step 2: pull their assigned dockets
        # CourtListener's docket search uses the judge's display name.
        cases, total_cases = client.search_dockets(
            judge=judge.get('name', name),
            max_results=max_cases
        )

        # Light disposition signal: count terminated vs open
        open_cases = sum(1 for c in cases if not c.get('dateTerminated'))
        terminated_cases = sum(1 for c in cases if c.get('dateTerminated'))

        return {
            "status": "success",
            "judge": judge,
            "cases": cases,
            "total_cases": total_cases,
            "sample_open": open_cases,
            "sample_terminated": terminated_cases,
            "timestamp": datetime.utcnow().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/case/{case_id}")
async def get_case(case_id: int):
    """Get details for a specific case."""
    require_client()

    try:
        result = client.get_docket(case_id)
        if result:
            return format_response(result)
        raise HTTPException(status_code=404, detail="Case not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/search/advanced")
async def advanced_search(
    query: Optional[str] = None,
    party: Optional[str] = None,
    judge: Optional[str] = None,
    court: Optional[str] = None,
    search_type: str = "dockets",
    limit: int = 20
):
    """Advanced search combining multiple filters."""
    require_client()

    try:
        if search_type == "dockets":
            results, total = client.search_dockets(
                query=query, party=party, judge=judge, court=court, max_results=limit
            )
        elif search_type == "opinions":
            if not query:
                raise HTTPException(status_code=400, detail="opinions search requires 'query'")
            results, total = client.search_opinions(query=query, court=court, max_results=limit)
        else:
            raise HTTPException(status_code=400, detail=f"Unknown search_type: {search_type}")

        return format_response(results, total=total)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "client_initialized": client is not None,
        "timestamp": datetime.utcnow().isoformat()
    }

# ─── Main ───────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    if not client:
        print("\n⚠️  WARNING: CourtListener token not configured.")
        print("   The web interface will load, but searches won't work.")
        print("\n   To enable searches, set your token:")
        print("   export COURTLISTENER_TOKEN='your-token-here'")
        print("\n   Get a token at: https://www.courtlistener.com/help/api/rest/\n")

    print("\n🚀 Starting CourtListener Search API...")
    print("   Open: http://localhost:8000/search.html")
    print("   Docs: http://localhost:8000/docs\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
