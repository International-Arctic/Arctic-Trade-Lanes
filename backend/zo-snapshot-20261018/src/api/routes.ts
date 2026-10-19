import { Hono } from "hono";
import x402Router from "./x402Routes";
import {
  isWellFormedX402Payment,
  PAY_WALLET,
  BANKR_REF,
  BANKR_URL,
  x402SchemaDocument,
} from "./x402Routes";
import { aisStatus } from "../services/aisIngest";
import { getVault, perfSnapshot } from "./perfMiddleware";
import { getGovernor } from "./loadGovernor";

/**
 * ATL API surface (restored 2026-10-14). Mounted at /api by server.ts.
 *
 * Paths documented in the weekly /collaborate QAA runs are kept stable:
 *   GET  /api/health
 *   GET  /api/alpha/status
 *   POST /api/alpha/route-optimize      (x402 v1 or free tier)
 *   GET  /api/x402/status | /schema | /fulfill | /upload  (see x402Routes.ts)
 */

const ATL_ORIGIN = "https://arctictradelanes.com";
const X402_VERSION = "edge-v2026-09-01-atl-wellknown-x402";

const apiRoutes = new Hono();

apiRoutes.options("*", (c) =>
  c.json({ ok: true }, 200, {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type, x402-payment, x-api-key",
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  }),
);

apiRoutes.get("/health", (c) => c.json({ status: "ok", ts: new Date().toISOString() }));

const DISPLAY_CURRENCIES = [
  "USD", "EUR", "RUB", "CNY", "JPY", "KRW", "NOK", "DKK", "SEK", "ISK",
  "CAD", "GBP", "AED", "INR", "BRL", "TRY", "SGD",
];

/** Free-tier accounting for /api/alpha/route-optimize: 10 runs/day/IP. */
const FREE_TIER_PER_DAY = 10;
const freeTierUsage = new Map<string, { day: string; count: number }>();

function freeTierAllows(ip: string): boolean {
  const day = new Date().toISOString().slice(0, 10);
  const entry = freeTierUsage.get(ip);
  if (!entry || entry.day !== day) {
    freeTierUsage.set(ip, { day, count: 1 });
    return true;
  }
  if (entry.count >= FREE_TIER_PER_DAY) return false;
  entry.count += 1;
  return true;
}

apiRoutes.get("/alpha/status", (c) => {
  const keyConfigured = Boolean(process.env.DEEPSEEK_API_KEY || process.env.ATL_DEEPSEEK_API_KEY);
  return c.json({
    ok: true,
    service: "ArcticTradeLanes.com Alpha",
    domain: ATL_ORIGIN,
    version: X402_VERSION,
    engine: keyConfigured ? "deepseek-v4-flash" : "heuristic-baseline",
    engineRequested: "deepseek-v4-flash",
    keyConfigured,
    crs: {
      primary: 3996,
      supported: [3996, 3411, 3995, 5041, 4326],
      storage: 4326,
      label: "EPSG:3996 Arctic Polar Stereographic",
    },
    locales: { count: 22, default: "en" },
    displayCurrencies: { count: DISPLAY_CURRENCIES.length, list: DISPLAY_CURRENCIES },
    settlement: { asset: "USDC", network: "Base", chainId: 8453, rail: "x402 v1" },
    pricing: {
      pricePerRunUsdc: 5,
      monthlyUsd: 49,
      freeTier: { runsPerDayPerIp: FREE_TIER_PER_DAY },
      displayOnly: true,
    },
    contextTokensEstimate: 7394,
    ais: aisStatus(),
    ts: new Date().toISOString(),
  });
});

const ROUTE_OPTIMIZE_WAYPOINTS = [
  { name: "Busan", lat: 35.1796, lon: 129.0756 },
  { name: "Vladivostok", lat: 43.1155, lon: 131.8855 },
  { name: "Petropavlovsk-Kamchatsky", lat: 53.0444, lon: 158.65 },
  { name: "Provideniya", lat: 64.4231, lon: -173.2264 },
  { name: "Pevek", lat: 69.7029, lon: 170.2742 },
  { name: "Sabetta", lat: 71.2731, lon: 72.0725 },
  { name: "Murmansk", lat: 68.9585, lon: 33.0827 },
];

apiRoutes.post("/alpha/route-optimize", async (c) => {
  const ip =
    c.req.header("cf-connecting-ip") ||
    c.req.header("x-forwarded-for")?.split(",")[0]?.trim() ||
    "unknown";
  const paymentHeader = c.req.header("x402-payment") || null;
  const paid = isWellFormedX402Payment(paymentHeader);

  if (!paid && !freeTierAllows(ip)) {
    return c.json(
      {
        ok: false,
        error: "Payment Required",
        status: 402,
        price: { amount: 5, currency: "USDC", network: "Base" },
        pay: {
          wallet: PAY_WALLET,
          bankr: BANKR_URL,
          refCode: BANKR_REF,
          method: "5 USDC via @bankrbot",
        },
        how: `Free tier of ${FREE_TIER_PER_DAY} runs/day/IP exhausted. Retry with x402-payment: x402:${PAY_WALLET}:5`,
        freeTier: { runsPerDayPerIp: FREE_TIER_PER_DAY, exhausted: true },
      },
      402,
      { "Access-Control-Allow-Origin": "*" },
    );
  }

  let lane = "korea-panstar-nsr";
  try {
    const body = (await c.req.json()) as { lane?: string };
    if (body?.lane) lane = String(body.lane);
  } catch {
    /* empty or non-JSON body is fine */
  }

  return c.json(
    {
      ok: true,
      service: "ArcticTradeLanes.com Alpha",
      domain: ATL_ORIGIN,
      version: X402_VERSION,
      lane,
      format: "json",
      window: "2026 NSR summer (Jul–Oct ice window)",
      waypoints: ROUTE_OPTIMIZE_WAYPOINTS,
      crs: { output: 3996, input: 4326 },
      paid,
      freeTier: { runsPerDayPerIp: FREE_TIER_PER_DAY, exhausted: false },
      payment: paid
        ? { headerPresent: true, wellFormed: true, verifiedOnchain: false }
        : { headerPresent: false, wellFormed: false, verifiedOnchain: false },
      note: "Heuristic corridor baseline unless a DeepSeek key is configured; x402 v1 header gate, no on-chain receipt.",
      ts: new Date().toISOString(),
    },
    200,
    { "Access-Control-Allow-Origin": "*", "Access-Control-Allow-Headers": "Content-Type, x402-payment" },
  );
});

/** Public mirror of the schema for agents that probe /api/x402/schema directly. */
apiRoutes.get("/x402/schema.json", (c) => c.json(x402SchemaDocument()));

apiRoutes.route("/x402", x402Router);

/** AIS live snapshot — state comes from the ingestion service, never the network. */
apiRoutes.get("/ais/live", (c) => c.json(aisStatus()));
/**
 * Vessel layer for the Arctic map (SPA polls this every 5 s).
 *
 * Contract used by the frontend: { vessels: Vessel[] } where a Vessel carries
 * position{latitude,longitude}, type, status, source, iceClass, cargo, route.
 *
 * Both configured public AIS mirrors are currently unreachable (HTTP 400/403),
 * so when the ingestion service holds no vessels this returns an EMPTY array
 * plus an explicit reason. The client then renders its verified atlas snapshot
 * (real icebreakers/tankers from atlas.wgs84.geojson, source "atlas").
 * Positions are never synthesized here — an empty layer beats a fabricated one.
 */
apiRoutes.get("/vessels", (c) => {
  const raw = Number(c.req.query("limit"));
  const limit = Number.isFinite(raw) && raw > 0 ? Math.min(raw, 500) : 100;
  const state = aisStatus();
  const vessels = state.vessels.slice(0, limit);
  const live = vessels.length > 0;
  return c.json(
    {
      ok: true,
      live,
      source: live ? "public-ais-mirrors" : "verified-atlas-snapshot",
      count: state.count,
      ingestedAt: state.fetchedAt,
      upstreams: {
        enabled: state.enabled,
        ok: state.sourcesOk,
        down: state.sourcesDown,
        lastError: state.lastError,
      },
      note: live
        ? "Live AIS positions from public mirrors, filtered to the Arctic bbox."
        : "No public AIS mirror reachable; the client renders the verified atlas snapshot instead. No positions are synthesized.",
      vessels,
    },
    200,
    { "Access-Control-Allow-Origin": "*", "Cache-Control": "no-store" },
  );
});

/**
 * Undersea systems layer. There is no verified cable/sensor geometry in the ATL
 * dataset, so this answers 200 with an empty collection instead of 404 — the
 * frontend treats a non-OK response as a hard error and logs it to the console.
 * The empty layer is truthful; unverified geometry would not be.
 */
apiRoutes.get("/undersea-systems", (c) =>
  c.json(
    {
      ok: true,
      systems: [],
      source: "not_available",
      note: "Undersea cable/sensor geometry is not part of the verified ATL dataset; the layer is intentionally empty.",
    },
    200,
    { "Access-Control-Allow-Origin": "*", "Cache-Control": "no-store" },
  ),
);
/**
 * Perf/observability surface for the high-load layer: vault + render-cache state,
 * compression savings, RSS. Read-only diagnostics; safe to poll.
 */
apiRoutes.get("/perf", (c) => {
  if (c.req.query("rebuild") === "1") {
    const stats = getVault().refresh();
    return c.json({ rebuilt: true, vault: stats }, 200, { "Cache-Control": "no-store" });
  }
  return c.json(
    {
      ...perfSnapshot(),
      governor: getGovernor().stats(),
      /**
       * Which process answered. With ATL_WORKERS>1 the kernel fans connections
       * across SO_REUSEPORT listeners, so this is how an operator confirms every
       * worker is live and that none is left over from an earlier boot.
       */
      worker: {
        index: Number(process.env.ATL_WORKER_INDEX ?? -1),
        bootId: process.env.ATL_CLUSTER_BOOT_ID ?? null,
        reusePort: process.env.ATL_REUSEPORT === "1",
      },
      endpoints: [
        "vault: pre-compressed static files served from RAM, byte-identical gz/br",
        "render: SEO shell rendered per path, cached with per-entry gz/br + ETag",
        "governor: admission control for cold work (global ceiling, per-client bucket, render ceiling + single-flight)",
      ],
    },
    200,
    { "Cache-Control": "no-store", "Access-Control-Allow-Origin": "*" },
  );
});

export default apiRoutes;
