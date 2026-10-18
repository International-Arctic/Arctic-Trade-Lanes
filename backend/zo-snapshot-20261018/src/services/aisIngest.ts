/**
 * AIS vessel ingestion (restored 2026-10-14).
 *
 * The original module polled public AIS mirrors on a timer. Those upstreams are
 * unauthenticated and frequently down, so this restoration is deliberately
 * defensive:
 *   - OFF by default. Set ATL_AIS_INGEST=1 to enable the poll loop.
 *   - Every fetch is timeout-bounded and wrapped; a failure never throws into
 *     the server boot path and never rejects an interval callback.
 *   - Status lives in memory only and is exposed through /api/alpha/status and
 *     /api/ais/live, so the server never writes into public/.
 */

export type AisStatus = {
  enabled: boolean;
  fetchedAt: number | null;
  sourcesOk: string[];
  sourcesDown: string[];
  count: number;
  vessels: unknown[];
  lastError: string | null;
};

const SOURCES: { name: string; url: string }[] = [
  { name: "arcgis-shippositions", url: "https://services9.arcgis.com/6Hv9AANartyT7fJW/arcgis/rest/services/ShipPositions/FeatureServer/0/query?where=1%3D1&outFields=*&f=geojson&resultRecordCount=200" },
  { name: "geoscience-au-2020", url: "https://services.ga.gov.au/gis/rest/services/Australian_Ship_Traffic/MapServer/0/query?where=1%3D1&outFields=*&f=geojson&resultRecordCount=200" },
];

const INTERVAL_MS = 15 * 60 * 1000;
const TIMEOUT_MS = 10_000;

const state: AisStatus = {
  enabled: false,
  fetchedAt: null,
  sourcesOk: [],
  sourcesDown: [],
  count: 0,
  vessels: [],
  lastError: null,
};

let timer: ReturnType<typeof setInterval> | null = null;
let inFlight = false;

function isInsideArctic(lat: number, lon: number): boolean {
  return lat >= 58 || (lat >= 50 && lon >= -170 && lon <= 180 && lat >= 50 && lat < 58);
}

async function fetchSource(source: { name: string; url: string }) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    const response = await fetch(source.url, {
      signal: controller.signal,
      headers: { accept: "application/json" },
    });
    if (!response.ok) return { ok: false as const, reason: `HTTP ${response.status}` };
    const body = (await response.json()) as { features?: any[] };
    const features = Array.isArray(body?.features) ? body.features : [];
    return { ok: true as const, features };
  } catch (error) {
    return { ok: false as const, reason: error instanceof Error ? error.message : String(error) };
  } finally {
    clearTimeout(timeout);
  }
}

export async function refreshAis(): Promise<AisStatus> {
  if (inFlight) return { ...state };
  inFlight = true;
  const ok: string[] = [];
  const down: string[] = [];
  const vessels: unknown[] = [];
  try {
    const results = await Promise.all(
      SOURCES.map(async (source) => ({ source, result: await fetchSource(source) })),
    );
    for (const { source, result } of results) {
      if (!result.ok) {
        down.push(source.name);
        continue;
      }
      ok.push(source.name);
      for (const feature of result.features) {
        const geometry = feature?.geometry;
        const props = feature?.properties ?? {};
        const coords = Array.isArray(geometry?.coordinates) ? geometry.coordinates : null;
        if (!coords) continue;
        const lon = Number(coords[0]);
        const lat = Number(coords[1]);
        if (!Number.isFinite(lat) || !Number.isFinite(lon)) continue;
        if (!isInsideArctic(lat, lon)) continue;
        vessels.push({
          id: props.mmsi ?? props.MMSI ?? feature.id ?? null,
          name: props.name ?? props.NAME ?? props.vesselname ?? null,
          lat,
          lon,
          speed: props.speed ?? props.SOG ?? null,
          course: props.course ?? props.COG ?? null,
          source: source.name,
        });
        if (vessels.length >= 500) break;
      }
    }
    state.sourcesOk = ok;
    state.sourcesDown = down;
    state.count = vessels.length;
    state.vessels = vessels;
    state.fetchedAt = Date.now();
    state.lastError = null;
  } catch (error) {
    state.lastError = error instanceof Error ? error.message : String(error);
    state.fetchedAt = Date.now();
  } finally {
    inFlight = false;
  }
  return { ...state };
}

/**
 * Called once at boot by server.ts. Must never throw and must never block boot.
 */
export function startAisIngestion(): void {
  const enabled = process.env.ATL_AIS_INGEST === "1";
  state.enabled = enabled;
  if (!enabled) return;
  if (timer) return;

  state.fetchedAt = Date.now();
  void refreshAis().catch(() => undefined);

  timer = setInterval(() => {
    void refreshAis().catch(() => undefined);
  }, INTERVAL_MS);
  if (typeof timer.unref === "function") timer.unref();
}

export function aisStatus(): AisStatus {
  return { ...state, vessels: [...state.vessels] };
}

export function stopAisIngestion(): void {
  if (timer) {
    clearInterval(timer);
    timer = null;
  }
}
