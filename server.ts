import { existsSync, readFileSync } from "node:fs";
import type { ViteDevServer } from "vite";
import { createServer as createViteServer } from "vite";
import { Hono } from "hono";
import apiRoutes from "./src/api/routes";
import { x402DiscoveryDocument } from "./src/api/x402Routes";
import { agentCardDocument } from "./src/api/discoveryRoutes";
import {
  atlCompress,
  countRequest,
  getRenderCache,
  getShell,
  getVault,
  isCacheablePath,
  renderedResponse,
  vaultResponse,
  type Rendered,
} from "./src/api/perfMiddleware";
import { startAisIngestion } from "./src/services/aisIngest";
import {
  getGovernor,
  governorMiddleware,
  rememberSocketIp,
  shedResponse,
} from "./src/api/loadGovernor";
import { factNotFound, factResponse, factStats } from "./src/api/factRoutes";
import { isKnownRoutePath, seoHtml } from "./src/api/seoMiddleware";
// ATL-HOME-EXTRAS-HOOK (2026-10-18): additive homepage sections + private intake queues.
import { injectHomeExtras } from "./src/home/homeExtras";
import atlIntakeRoutes from "./src/home/intakeRoutes";
import { webSocketServer, bunWebSocketHandler } from "./src/services/WebSocketServer";

type Mode = "development" | "production";
const app = new Hono();

/**
 * Unhandled route errors are logged instead of vanishing into a bare 500.
 * Cheap (only runs on failure) and leaves the response shape JSON for probes.
 */
app.onError((err, c) => {
  countRequest("errors");
  console.error(`[atl] ${c.req.method} ${c.req.path} -> ${err instanceof Error ? err.message : String(err)}`);
  return c.json({ error: "internal_error" }, 500);
});

const mode: Mode =
  process.env.NODE_ENV === "production" ? "production" : "development";

/**
 * High-load layer (2026-10-14): pre-compressed in-RAM static vault + render cache.
 * Built once per process, before any route is registered.
 *
 * `atlCompress()` is registered first so it wraps every dynamic response (API JSON,
 * fall-through HTML). Responses the vault already encoded carry Content-Encoding, so
 * the middleware skips them and never re-compresses.
 */
/**
 * Vault roots, in priority order. `./dist` is the built output and always wins;
 * `./public` is a fallback so paths the build does not emit (favicon, brand svgs,
 * og images, ad config) are served from RAM instead of 404ing.
 */
const VAULT_ROOTS = ["./dist", "./public"];
const vault = getVault(VAULT_ROOTS);
const renderCache = getRenderCache();

/**
 * Load governor, registered FIRST so it is the outermost gate.
 *
 * It is a single integer compare on the hot path. Warm responses (vault hits and
 * cached renders) pass straight through it; only cold work is ever deferred or
 * shed. Registered before atlCompress so a shed response costs no middleware work.
 */
const governor = getGovernor();
app.use("*", governorMiddleware());
app.use("*", atlCompress({ threshold: 1024 }));
/**
 * Never leak an unhandled throw as a bare 500: log the cause once and count it in
 * /api/perf. Under load this is the difference between "site is down" and
 * "one route is failing".
 */
app.onError((err, c) => {
  countRequest("errors");
  console.error(`[atl-500] ${c.req.method} ${c.req.path} - ${err?.message ?? err}`);
  return c.text("Internal Server Error", 500);
});

/**
 * Configure WebSocket routes
 */
webSocketServer.configureRoutes(app);

/**
 * x402 discovery (www / Zo-origin parity — Worker may not run on grey-cloud www)
 */
app.get("/.well-known/x402.json", (c) => c.json(x402DiscoveryDocument()));
app.get("/v1/.well-known/x402.json", (c) => c.json(x402DiscoveryDocument()));

/**
 * A2A agent card (parity with the mvp-static discovery files).
 */
app.get("/.well-known/agent-card.json", (c) => c.json(agentCardDocument()));
app.get("/.well-known/agent.json", (c) => c.json(agentCardDocument()));

/**
 * Mount API routes
 */
/**
 * Private intake queues (2026-10-18): POST /api/atl-interest, POST /api/contributions.
 * Registered before apiRoutes; only these two exact POST paths are matched.
 */
app.route("/", atlIntakeRoutes);
app.route("/api", apiRoutes);

startAisIngestion();

/**
 * Health check endpoint
 */
app.get("/api/health", (c) => c.json({ status: "ok" }));

if (mode === "production") {
  configureProduction(app);
} else {
  await configureDevelopment(app);
}

if (mode === "production") {
  const shell = getShell();
  const warm = renderCache.warm(shell);
  const stats = vault.statsSnapshot();
  console.log(
    `[atl-perf] vault ${stats.files} files / ${(stats.bytesOnDisk / 1048576).toFixed(1)} MB on disk -> ` +
      `${stats.sharedPayloads} shared payloads / ${(stats.bytesInRam / 1048576).toFixed(1)} MB in RAM ` +
      `(built ${stats.buildMs} ms) · rendered ${warm.rendered} route-locale docs in ${warm.ms} ms · pid ${process.pid}`,
  );
}

/**
 * Determine port based on mode.
 * In production, use port 3000 or environment variable.
 * In development, use environment variable PORT or default to 3000.
 */
const port = process.env.PORT ? parseInt(process.env.PORT, 10) : 3000;

/**
 * Cluster worker watchdog.
 *
 * When this process was started by cluster.ts it must not outlive its launcher. A
 * stray worker holding the port with SO_REUSEPORT enabled would answer a share of
 * requests from stale code with no error anywhere — the exact failure that made
 * reusePort opt-in in the first place. Reparenting is the signal that still works
 * when the launcher is SIGKILLed, where no shutdown handler of its own can run.
 */
if (process.env.ATL_CLUSTER_CHILD === "1") {
  const launcherPid = process.ppid;
  const bootId = process.env.ATL_CLUSTER_BOOT_ID ?? "?";
  console.log(
    `[atl] worker ${process.env.ATL_WORKER_INDEX ?? "?"} of cluster boot ${bootId} ` +
      `(launcher pid ${launcherPid}) listening on ${port}`,
  );
  /**
   * `process.ppid` is read once by this runtime and never refreshed, so it still
   * reported the dead launcher after reparenting. `/proc/self/status` is the only
   * reading that actually changes, and it is one small file read per tick.
   */
  const currentPpid = (): number => {
    try {
      const match = /^PPid:\s+(\d+)/m.exec(readFileSync("/proc/self/status", "utf8"));
      return match ? Number(match[1]) : process.ppid;
    } catch {
      return process.ppid;
    }
  };
  setInterval(() => {
    const ppid = currentPpid();
    if (ppid !== launcherPid) {
      console.error(`[atl] launcher ${launcherPid} is gone (ppid now ${ppid}); exiting to avoid a stale listener`);
      process.exit(0);
    }
  }, 1000);
}

export default {
  /**
   * The socket peer address is the one client signal a request cannot forge, so it
   * is captured here — before Hono runs, where `server.requestIP()` is still cheap —
   * and stashed on the Request for the governor's client key. Nothing is decided
   * here; the hot path stays a single Map lookup.
   */
  fetch(req: Request, server: Bun.Server<undefined>) {
    const ip = server.requestIP(req);
    rememberSocketIp(req, ip?.address);
    if (ip) getGovernor().noteSocketIp();
    return app.fetch(req, server);
  },
  port,
  idleTimeout: 255,
  /**
   * SO_REUSEPORT is OFF by default, and that is deliberate.
   *
   * With SO_REUSEPORT the kernel load-balances across EVERY process bound to the
   * port. A stale process left over from a restart then keeps serving stale code
   * on a share of requests - same URL, different body, no error anywhere. On
   * 2026-10-14 that produced an intermittent mixture of 200/404/500 on this origin.
   * Single supervised process = one listener = exactly one answer per URL.
   * Opt in with ATL_REUSEPORT=1 only when running intentional sibling workers.
   */
  reusePort: process.env.ATL_REUSEPORT === "1",
  websocket: bunWebSocketHandler,
};

/** Shared header set for the pre-generated Arctic-panel SSR pages. */
const SSR_HEADERS: Record<string, string> = {
  "Cache-Control": "public, max-age=300",
  "X-ATL-SSR": "arctic-panel",
};

/** Restored static pages (2026-10-18): /[lc/]funding and /[lc/]advertise. */
const ATL_PAGE_RE = /^\/(?:(ru|zh|ja|ko|el|de|nl|fr|es|it|pt|tr|ar|hi|vi|id|da|fi|sv|nb|is)\/)?(funding|advertise)\/?$/;
const PAGE_HEADERS: Record<string, string> = { "Cache-Control": "public, max-age=300" };

/** Neutral people pages + homepage extras (2026-10-18). */
const ATL_PEOPLE_RE = /^\/(?:(ru|zh|ja|ko|el|de|nl|fr|es|it|pt|tr|ar|hi|vi|id|da|fi|sv|nb|is)\/)?people(?:\/([a-z0-9-]+))?\/?$/;
const ATL_HOME_RE = /^\/(?:(ru|zh|ja|ko|el|de|nl|fr|es|it|pt|tr|ar|hi|vi|id|da|fi|sv|nb|is)\/?)?$/;
const HOME_X_HEADERS: Record<string, string> = { "X-ATL-Home": "extras" };

/**
 * Configure routing for production builds.
 */
function configureProduction(app: Hono) {
  app.get("/favicon.ico", (c) => {
    const svg = vaultResponse(vault, "/favicon.svg", c);
    return svg ?? new Response(null, { status: 404 });
  });
  // UM x ATL ARCTIC-PANEL SYNC (2026-09-28): verified, source-cited fat SSR pages generated by
  // scripts/ssr_arctic_panel/gen.py into ./ssr (6 people + 1 event x 22 locales). Additive: only
  // /[lc/]people|events/<slug> paths with an existing ./ssr file; everything else falls through.
  app.use(async (c, next) => {
    if (c.req.method !== "GET" && c.req.method !== "HEAD") return next();
    const p = c.req.path.replace(/\/+$/, "");
    if (!/^\/(?:[a-z]{2}\/)?(?:people|events)\/[a-z0-9-]+$/.test(p)) return next();
    // Cache probe first: a warm SSR page must not touch the disk at all. The
    // previous form read the file on EVERY request and threw the bytes away
    // whenever the entry was already cached.
    const key = `ssr:${p}`;
    const warm = renderCache.lookup(key);
    if (warm) return renderedResponse(warm, c, SSR_HEADERS);
    const file = `./ssr${p}.html`;
    if (!existsSync(file)) return next();
    /**
     * Was `renderedResponse(cached, c, SSR_HEADERS)` — `cached` was never assigned
     * anywhere in this file, so the branch could only ever throw a ReferenceError.
     * It stayed invisible because ./ssr is absent, and would have returned 500 for
     * every people/event page the moment the SSR generator was restored.
     */
    return renderedResponse(renderCache.cacheHtml(key, readFileSync(file, "utf8")), c, SSR_HEADERS);
  });
  // RESTORED STATIC PAGES (2026-10-18, owner-approved): /funding and /advertise (+ 21 locale
  // prefixes) served from ./pages/[<lc>/]<slug>.html, generated by site/static-pages/build_pages.py
  // (GitHub International-Arctic/Arctic-Trade-Lanes). Additive: only these two slugs are matched and
  // only when the file exists; every other path falls through to the vault/render/404 chain unchanged.
  app.use(async (c, next) => {
    if (c.req.method !== "GET" && c.req.method !== "HEAD") return next();
    const m = ATL_PAGE_RE.exec(c.req.path);
    if (!m) return next();
    const rel = `${m[1] ? m[1] + "/" : ""}${m[2]}`;
    const key = `page:${rel}`;
    const warm = renderCache.lookup(key);
    if (warm) return renderedResponse(warm, c, { ...PAGE_HEADERS, "X-ATL-Page": m[2] });
    const file = `./pages/${rel}.html`;
    if (!existsSync(file)) return next();
    return renderedResponse(renderCache.cacheHtml(key, readFileSync(file, "utf8")), c, { ...PAGE_HEADERS, "X-ATL-Page": m[2] });
  });
  // NEUTRAL PEOPLE PAGES (2026-10-18): /[lc/]people and /[lc/]people/<slug> from ./pages, generated by
  // site/people-pages/build_people_pages.py (templates only, no ads/payment/token). Plus /sitemap-people.xml.
  app.use(async (c, next) => {
    if (c.req.method !== "GET" && c.req.method !== "HEAD") return next();
    if (c.req.path === "/sitemap-people.xml") {
      if (!existsSync("./pages/sitemap-people.xml")) return next();
      return new Response(readFileSync("./pages/sitemap-people.xml"), { headers: { "Content-Type": "application/xml; charset=UTF-8", "Cache-Control": "public, max-age=3600" } });
    }
    const m = ATL_PEOPLE_RE.exec(c.req.path);
    if (!m) return next();
    const rel = `${m[1] ? m[1] + "/" : ""}people${m[2] ? "/" + m[2] : ""}`;
    const key = `page:${rel}`;
    const warm = renderCache.lookup(key);
    if (warm) return renderedResponse(warm, c, { ...PAGE_HEADERS, "X-ATL-Page": "people" });
    const file = `./pages/${rel}.html`;
    if (!existsSync(file)) return next();
    return renderedResponse(renderCache.cacheHtml(key, readFileSync(file, "utf8")), c, { ...PAGE_HEADERS, "X-ATL-Page": "people" });
  });
  // HOME EXTRAS (2026-10-18, owner order): the SAME seoHtml() shell the render chain serves for / and /<lc>,
  // plus server-rendered sections appended after <div id="root"></div> (src/home/homeExtras.ts). The SPA,
  // its JSON-LD, H1, og image and ad slots are untouched. Any error falls through to the original chain.
  // Kill switch: ATL_HOME_EXTRAS=0.
  app.use(async (c, next) => {
    if (process.env.ATL_HOME_EXTRAS === "0") return next();
    if (c.req.method !== "GET" && c.req.method !== "HEAD") return next();
    const m = ATL_HOME_RE.exec(c.req.path);
    if (!m) return next();
    const key = seoHtmlPath(c.req.path);
    const ck = `homex:${key}`;
    const warm = renderCache.lookup(ck);
    if (warm) return renderedResponse(warm, c, HOME_X_HEADERS);
    let entry: Rendered;
    try {
      entry = renderCache.cacheHtml(ck, injectHomeExtras(seoHtml(key, getShell()), m[1] || "en"));
    } catch (err) {
      console.error(`[atl-home-x] ${key} -> ${err instanceof Error ? err.message : String(err)}`);
      return next();
    }
    return renderedResponse(entry, c, HOME_X_HEADERS);
  });
  /**
   * Hot path — zero disk I/O for repeat traffic.
   *
   * Before: `Bun.file('./dist'+path).exists()` + `.stat()` per request, then up to nine
   * `existsSync` probes and a `readFileSync` inside seoHtml for the HTML fallback.
   * Now: one Map lookup in the vault; on a miss, one cached render keyed by path.
   */
  app.use(async (c, next) => {
    if (c.req.method !== "GET" && c.req.method !== "HEAD") return next();

    const path = c.req.path;
    if (
      path.startsWith("/api/") ||
      path.startsWith("/.well-known/") ||
      path.startsWith("/v1/.well-known/")
    ) {
      return next();
    }

    // 1. exact file from the pre-compressed vault (dist/, plus public/ in dev)
    countRequest("requests");
    const file = vaultResponse(vault, path, c);
    if (file) {
      countRequest("vaultHits");
      if (file.status === 304) countRequest("notModified");
      else if (file.headers.get("Content-Encoding")) countRequest("servedCompressed");
      return file;
    }

    // 2. generated fact pages + 221 sharded sitemaps (~29.3k static documents).
    //    Additive: only paths listed in factpages/.routes.json are served; anything
    //    else returns null and falls through exactly as it did before. Runs before
    //    the extension guard so /sitemaps/*.xml is reachable.
    const fact = factResponse(c);
    if (fact) return fact;

    // 3. rendered SEO shell, cached and pre-compressed per normalised path
    if (path.includes(".") && !/\.html?$/i.test(path)) return next();

    // 4. a dotless path that is not a route this origin publishes is a 404, not a
    //    copy of the homepage. Before this gate every unmatched path answered 200
    //    with the shell — an unbounded set of indexable duplicates.
    if (!isKnownRoutePath(path)) {
      countRequest("notFound");
      return factNotFound(c) ?? c.text("Not Found", 404);
    }

    const key = seoHtmlPath(path);
    const shell = getShell();

    // Warm path. One Map probe; a hit is answered without ever touching the
    // governor, so normal traffic cannot be throttled by the load ceiling.
    const warm = renderCache.lookup(key);
    if (warm) {
      countRequest("renderHits");
      return emitRendered(warm, c);
    }
    countRequest("renderMisses");

    // Cold path - the only work a flood can amplify.
    //
    // Order matters. The per-client bucket is checked first (cheap Map math), then
    // exactly ONE render slot is taken per distinct path: single-flight wraps the
    // slot acquisition, so a thousand requests racing onto one cold URL consume one
    // slot between them rather than a thousand, and the ones that merely wait are
    // answered from the leader's result the moment it lands.
    const admission = governor.admitClient(c);
    if (!admission.ok) {
      countRequest("shedLoad");
      return shedResponse(c, admission.retryAfter);
    }

    const entry = await governor.singleFlight<Rendered | null>(
      `render:${key}`,
      async (): Promise<Rendered | null> => {
        const release = await governor.acquireRender();
        // Queue full: more distinct cold paths are in flight than this box will
        // ever render. Refuse honestly instead of growing latency without bound.
        if (!release) return null;
        try {
          // A sibling flight may have produced this document while we queued.
          const raced = renderCache.lookup(key, Date.now(), false);
          if (raced) return raced;
          return isCacheablePath(key)
            ? renderCache.renderFresh(key, shell)
            : renderCache.renderUncached(key, shell);
        } finally {
          release();
        }
      },
    );

    if (!entry) {
      countRequest("shedLoad");
      return shedResponse(c, 1);
    }
    return emitRendered(entry, c);
  });
}

/**
 * Emit a rendered document and keep the byte-accounting counters identical to the
 * pre-governor hot path (304 for revalidations, `servedCompressed` for real bodies).
 */
function emitRendered(entry: Rendered, c: Parameters<typeof renderedResponse>[1]): Response {
  const rendered = renderedResponse(entry, c);
  if (rendered.status === 304) countRequest("notModified");
  else if (rendered.headers.get("Content-Encoding")) countRequest("servedCompressed");
  return rendered;
}

/** Mirror the normalisation seoHtml applies so cache keys match byte-for-byte. */
function seoHtmlPath(path: string): string {
  let p = (path || "/").split("?")[0].split("#")[0];
  if (!p.startsWith("/")) p = `/${p}`;
  if (p.length > 1) p = p.replace(/\/+$/, "");
  return p === "" ? "/" : p;
}

/**
 * Configure routing for development builds.
 */
async function configureDevelopment(app: Hono): Promise<ViteDevServer> {
  const vite = await createViteServer({
    server: { middlewareMode: true, hmr: false, ws: false },
    appType: "custom",
  });

  app.use("*", async (c, next) => {
    if (c.req.path.startsWith("/api/")) return next();
    if (c.req.path === "/favicon.ico") return c.redirect("/favicon.svg", 302);

    const url = c.req.path;

    const staticFile = vaultResponse(vault, c.req.path, c);
    if (staticFile) return staticFile;

    try {
      if (url === "/" || url === "/index.html") {
        let template = await Bun.file("./index.html").text();
        template = await vite.transformIndexHtml(url, template);
        return c.html(template);
      }

      const publicFile = Bun.file(`./public${url}`);
      if (await publicFile.exists()) {
        const stat = await publicFile.stat();
        if (stat && !stat.isDirectory()) {
          return new Response(publicFile, {
            headers: { "Cache-Control": "no-cache" },
          });
        }
      }

      let result;
      try {
        result = await vite.transformRequest(url);
      } catch {
        result = null;
      }

      if (result) {
        return new Response(result.code, {
          headers: {
            "Content-Type": "application/javascript",
            "Cache-Control": "no-cache",
          },
        });
      }

      let template = await Bun.file("./index.html").text();
      template = await vite.transformIndexHtml("/", template);
      return c.html(template);
    } catch (error) {
      vite.ssrFixStacktrace(error as Error);
      console.error(error);
      return c.text("Internal Server Error", 500);
    }
  });

  return vite;
}
