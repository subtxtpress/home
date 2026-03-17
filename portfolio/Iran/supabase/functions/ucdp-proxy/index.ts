import "@supabase/functions-js/edge-runtime.d.ts"

const UCDP_API = "https://ucdpapi.pcr.uu.se/api/gedevents/25.1";
const UCDP_TOKEN = "3d37d99d971b0583";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
};

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: CORS_HEADERS });
  }

  try {
    const url = new URL(req.url);
    const params = new URLSearchParams();

    // Forward allowed query params to UCDP API
    for (const key of ["pagesize", "page", "Geography", "StartDate", "EndDate", "TypeOfViolence", "Country"]) {
      const val = url.searchParams.get(key);
      if (val) params.set(key, val);
    }

    // Default pagesize if not specified
    if (!params.has("pagesize")) params.set("pagesize", "1000");

    const apiUrl = `${UCDP_API}?${params.toString()}`;
    const resp = await fetch(apiUrl, {
      headers: { "x-ucdp-access-token": UCDP_TOKEN },
    });

    if (!resp.ok) {
      return new Response(
        JSON.stringify({ error: `UCDP API returned ${resp.status}` }),
        { status: resp.status, headers: { ...CORS_HEADERS, "Content-Type": "application/json" } }
      );
    }

    const data = await resp.json();
    return new Response(JSON.stringify(data), {
      headers: { ...CORS_HEADERS, "Content-Type": "application/json" },
    });
  } catch (err) {
    return new Response(
      JSON.stringify({ error: err.message }),
      { status: 500, headers: { ...CORS_HEADERS, "Content-Type": "application/json" } }
    );
  }
});
