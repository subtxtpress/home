// ACLED credentials stored as Supabase secrets (never exposed to browser)
const ACLED_EMAIL = Deno.env.get("ACLED_EMAIL") || "";
const ACLED_PASSWORD = Deno.env.get("ACLED_PASSWORD") || "";
const ACLED_BASE = "https://acleddata.com";
const ACLED_API = `${ACLED_BASE}/api/acled/read`;
const ACLED_TOKEN_URL = `${ACLED_BASE}/oauth/token`;

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
};

// In-memory token cache (persists across warm invocations)
let cachedAccessToken: string | null = null;
let cachedRefreshToken: string | null = null;
let tokenExpiresAt = 0; // Unix ms

/**
 * Authenticate with ACLED OAuth and get access + refresh tokens.
 * Uses refresh_token if available and not expired, otherwise full login.
 */
async function getAccessToken(): Promise<string> {
  const now = Date.now();

  // If cached token is still valid (with 5-min buffer), reuse it
  if (cachedAccessToken && now < tokenExpiresAt - 300_000) {
    return cachedAccessToken;
  }

  // Try refresh token first (avoids sending credentials again)
  if (cachedRefreshToken) {
    try {
      const refreshResp = await fetch(ACLED_TOKEN_URL, {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: new URLSearchParams({
          refresh_token: cachedRefreshToken,
          grant_type: "refresh_token",
          client_id: "acled",
        }),
      });

      if (refreshResp.ok) {
        const data = await refreshResp.json();
        cachedAccessToken = data.access_token;
        cachedRefreshToken = data.refresh_token;
        tokenExpiresAt = now + (data.expires_in * 1000);
        console.log("[ACLED] Token refreshed successfully");
        return cachedAccessToken!;
      }
      console.warn("[ACLED] Refresh failed, falling back to full login");
    } catch (e) {
      console.warn("[ACLED] Refresh error:", e);
    }
  }

  // Full login with credentials
  if (!ACLED_EMAIL || !ACLED_PASSWORD) {
    throw new Error("ACLED_EMAIL and ACLED_PASSWORD secrets are not configured");
  }

  const loginResp = await fetch(ACLED_TOKEN_URL, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      username: ACLED_EMAIL,
      password: ACLED_PASSWORD,
      grant_type: "password",
      client_id: "acled",
    }),
  });

  if (!loginResp.ok) {
    const errText = await loginResp.text();
    throw new Error(`ACLED auth failed (${loginResp.status}): ${errText}`);
  }

  const data = await loginResp.json();
  cachedAccessToken = data.access_token;
  cachedRefreshToken = data.refresh_token;
  tokenExpiresAt = now + (data.expires_in * 1000);
  console.log("[ACLED] Full login successful");
  return cachedAccessToken!;
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { status: 204, headers: CORS_HEADERS });
  }

  try {
    // Get a valid access token (cached / refreshed / fresh login)
    const token = await getAccessToken();

    // Build ACLED API query from allowed params
    const url = new URL(req.url);
    const params = new URLSearchParams();

    const ALLOWED_PARAMS = [
      "limit", "page",
      "event_date", "event_date_where",
      "event_type", "sub_event_type",
      "country", "region",
      "admin1", "admin2", "admin3",
      "latitude", "longitude",
      "geo_precision",
      "fatalities", "fatalities_where",
      "disorder_type",
      "actor1", "actor2",
      "inter1", "inter2", "interaction",
      "source",
      "fields",          // select specific fields
      "acled_id",        // specific event lookup
      "acled_id_where",
      "timestamp",       // for incremental updates
      "timestamp_where",
    ];

    for (const key of ALLOWED_PARAMS) {
      const val = url.searchParams.get(key);
      if (val) params.set(key, val);
    }

    // Default limit if not specified
    if (!params.has("limit")) params.set("limit", "5000");

    const apiUrl = `${ACLED_API}?${params.toString()}`;

    const resp = await fetch(apiUrl, {
      headers: {
        "Authorization": `Bearer ${token}`,
        "Accept": "application/json",
      },
    });

    if (!resp.ok) {
      // If 401/403, clear cached tokens so next request re-authenticates
      if (resp.status === 401 || resp.status === 403) {
        cachedAccessToken = null;
        cachedRefreshToken = null;
        tokenExpiresAt = 0;
      }
      const errText = await resp.text();
      return new Response(
        JSON.stringify({ error: `ACLED API returned ${resp.status}`, detail: errText }),
        { status: resp.status, headers: { ...CORS_HEADERS, "Content-Type": "application/json" } }
      );
    }

    const data = await resp.json();
    return new Response(JSON.stringify(data), {
      headers: {
        ...CORS_HEADERS,
        "Content-Type": "application/json",
        "Cache-Control": "public, max-age=300", // Cache 5 min
      },
    });
  } catch (err) {
    return new Response(
      JSON.stringify({ error: err.message }),
      { status: 500, headers: { ...CORS_HEADERS, "Content-Type": "application/json" } }
    );
  }
});
