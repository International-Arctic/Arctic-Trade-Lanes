import { createHash } from "node:crypto";
import { readFileSync, existsSync } from "node:fs";
import { join } from "node:path";
import { brotliCompressSync, gzipSync, constants as zlib } from "node:zlib";
import type { Context } from "hono";
import { LOCALES } from "./seoMiddleware";

/**
 * ATL fact-page layer (2026-10-14, additive).
 *
 * `scripts/build-fact-pages.mjs` generates ~29k static, source-cited object/index pages
 * plus 221 sharded sitemaps into ./factpages. Until now nothing served them: the paths
 * fell through to the SEO shell and returned the homepage copy with HTTP 200, which is
 * the worst of both worlds for a crawler (indexable duplicate, no content).
 *
 * This module is the missing reader. Shape matches the rest of the high-load layer:
 *
 *   1. A boot-cheap URL -> file manifest (`factpages/.routes.json`). One JSON read
 *      instead of a 29k-file directory walk in every cluster worker.
 *   2. A bounded LRU of pre-compressed bodies (brotli + gzip). Fact pages are cold,
 *      long-tail URLs, so the working set that repeats is small; the cache holds the
 *      head of that distribution and lets the tail go to disk.
 *   3. Strong ETags, so a recrawler revalidates to 304 with no body, and
 *      Accept-Encoding is honoured with `Vary` set.
 *
 * Everything is opt-in on the presence of the directory: if ./factpages is absent the
 * module reports "disabled", `factResponse` returns null for every path, and the origin
 * behaves exactly as it did before. That keeps the change reversible by deleting a
 * directory — no code rollback needed.
 */

const DIR = "./factpages";
const MANIFEST = join(DIR, ".routes.json");
const MAX_ENTRIES = Number(process.env.ATL_FACT_CACHE ?? 1500);
const ENABLED = process.env.ATL_FACT_PAGES !== "0";

type Entry = {
  br?: Uint8Array;
  gz?: Uint8Array;
  etag: string;
  type: string;
  cache: string;
};

type Stats = {
  enabled: boolean;
  mounted: boolean;
  routes: number;
  cached: number;
  hits: number;
  misses: number;
  notFound: number;
  served: number;
  bytesInRam: number;
  loadMs: number;
};

const stats: Stats = {
  enabled: ENABLED,
  mounted: false,
  routes: 0,
  cached: 0,
  hits: 0,
  misses: 0,
  notFound: 0,
  served: 0,
  bytesInRam: 0,
  loadMs: 0,
};

/** URL path -> path relative to ./factpages. Populated once, on the first request. */
let routes: Map<string, string> | null = null;
/** Insertion order doubles as LRU order: a hit is deleted and re-set to move it to the tail. */
const cache = new Map<string, Entry>();
/** 404 bodies per locale — 22 tiny documents, read once. */
const notFoundBodies = new Map<string, string>();

function load(): Map<string, string> | null {
  if (routes) return routes;
  if (!ENABLED || !existsSync(MANIFEST)) {
    routes = new Map();
    stats.mounted = false;
    return routes;
  }
  const t0 = Date.now();
  try {
    const payload = JSON.parse(readFileSync(MANIFEST, "utf8")) as { routes: Record<string, string> };
    routes = new Map(Object.entries(payload.routes));
    stats.routes = routes.size;
    stats.mounted = true;
  } catch (error) {
    console.error(`[atl-fact] manifest unreadable, fact pages disabled: ${error instanceof Error ? error.message : error}`);
    routes = new Map();
    stats.mounted = false;
  }
  stats.loadMs = Date.now() - t0;
  return routes;
}

/** Mirror of server.ts/seoHtml path normalisation so cache keys and lookups agree. */
function normalise(path: string): string {
  let p = (path || "/").split("?")[0].split("#")[0];
  if (!p.startsWith("/")) p = `/${p}`;
  if (p.length > 1) p = p.replace(/\/+$/, "");
  return p === "" ? "/" : p;
}

function typeFor(rel: string): string {
  return rel.endsWith(".xml") ? "application/xml; charset=UTF-8" : "text/html; charset=UTF-8";
}

/**
 * Fact pages change only when the atlas is rebuilt, so they follow the data cadence
 * (5 min, SWR 1 h) rather than the HTML cadence — a crawler that refetches a fact page
 * gets a 304 in the common case and fresh content within the hour after a rebuild.
 */
function cacheFor(rel: string): string {
  return rel.endsWith(".xml")
    ? "public, max-age=300, stale-while-revalidate=3600"
    : "public, max-age=300, stale-while-revalidate=3600";
}

function compress(raw: Buffer, type: string): Entry {
  const etag = `"${createHash("sha256").update(raw).digest("hex").slice(0, 32)}"`;
  const out: Entry = { etag, type, cache: "" };
  const size = raw.byteLength;
  const quality = size > 1024 * 1024 ? 4 : 9;
  try {
    out.gz = new Uint8Array(gzipSync(raw, { level: zlib.Z_BEST_COMPRESSION }));
  } catch {
    out.gz = undefined;
  }
  try {
    out.br = new Uint8Array(
      brotliCompressSync(raw, {
        params: { [zlib.BROTLI_PARAM_QUALITY]: quality, [zlib.BROTLI_PARAM_SIZE_HINT]: size },
      }),
    );
  } catch {
    out.br = undefined;
  }
  return out;
}

function store(rel: string, entry: Entry): void {
  cache.set(rel, entry);
  if (cache.size > MAX_ENTRIES) {
    const oldest = cache.keys().next().value as string | undefined;
    if (oldest !== undefined) cache.delete(oldest);
  }
}

function lookup(rel: string): Entry | null {
  const hit = cache.get(rel);
  if (!hit) {
    stats.misses++;
    return null;
  }
  cache.delete(rel);
  cache.set(rel, hit);
  stats.hits++;
  return hit;
}

function entryFor(rel: string): Entry | null {
  const warm = lookup(rel);
  if (warm) return warm;
  const abs = join(DIR, rel);
  if (!existsSync(abs)) return null;
  try {
    const entry = compress(readFileSync(abs), typeFor(rel));
    entry.cache = cacheFor(rel);
    store(rel, entry);
    return entry;
  } catch {
    return null;
  }
}

function etagMatches(header: string | undefined, etag: string): boolean {
  if (!header) return false;
  if (header.trim() === "*") return true;
  return header.split(",").some((part) => part.trim().replace(/^W\//, "") === etag);
}

function emit(entry: Entry, c: Context, status = 200): Response {
  const headers: Record<string, string> = {
    "Content-Type": entry.type,
    ETag: entry.etag,
    "Cache-Control": entry.cache,
    Vary: "Accept-Encoding",
    "X-ATL-Fact": "1",
  };
  if (status === 404) {
    headers["Cache-Control"] = "public, max-age=60";
    headers["X-Robots-Tag"] = "noindex, follow";
  }

  if (etagMatches(c.req.header("if-none-match"), entry.etag)) {
    return new Response(null, { status: 304, headers });
  }

  const accept = c.req.header("accept-encoding") ?? "";
  let body: Uint8Array | null = null;
  if (entry.br && /\bbr\b/.test(accept)) {
    body = entry.br;
    headers["Content-Encoding"] = "br";
  } else if (entry.gz && /\bgzip\b/.test(accept)) {
    body = entry.gz;
    headers["Content-Encoding"] = "gzip";
  }

  if (!body) {
    return new Response(null, { status: 304, headers: { ...headers, ETag: entry.etag } });
  }

  headers["Content-Length"] = String(body.byteLength);
  if (c.req.method === "HEAD") return new Response(null, { status, headers });
  return new Response(body, { status, headers });
}

/**
 * Serve a generated fact page or a sharded sitemap. Returns null when the path is not a
 * generated document, which is the signal for the caller to keep falling through.
 */
export function factResponse(c: Context): Response | null {
  const table = load();
  if (!stats.mounted) return null;

  const path = normalise(c.req.path);
  const rel = table.get(path);
  if (!rel) return null;

  const entry = entryFor(rel);
  if (!entry) return null;
  stats.served++;
  return emit(entry, c);
}

/** Locale of a normalised path, for the localised 404 document. */
function localeOf(path: string): string {
  const first = path.split("/").filter(Boolean)[0];
  return first && (LOCALES as readonly string[]).includes(first) ? first : "en";
}

/**
 * Real 404 for a path the origin does not publish.
 *
 * Before this, every unmatched dotless path returned the homepage copy with HTTP 200:
 * an unbounded set of indexable duplicates, and no way for a crawler to learn that a URL
 * is not a page. The body is the generated, localised 404 document.
 */
export function factNotFound(c: Context): Response | null {
  const path = normalise(c.req.path);
  const lang = localeOf(path);
  stats.notFound++;

  let body = notFoundBodies.get(lang);
  if (body === undefined) {
    const rel = `${lang}/404.html`;
    const abs = join(DIR, rel);
    body = existsSync(abs) ? readFileSync(abs, "utf8") : "";
    notFoundBodies.set(lang, body);
  }

  if (!body) {
    return new Response("Not Found", { status: 404, headers: { "Content-Type": "text/plain; charset=UTF-8" } });
  }

  const headers: Record<string, string> = {
    "Content-Type": "text/html; charset=UTF-8",
    "Cache-Control": "public, max-age=60",
    "X-Robots-Tag": "noindex, follow",
    "X-ATL-404": "1",
  };

  return new Response(c.req.method === "HEAD" ? null : body, { status: 404, headers });
}

/** Snapshot for /api/perf. Cheap: counters plus the live cache size. */
export function factStats(): Stats {
  let bytes = 0;
  for (const entry of cache.values()) bytes += (entry.br?.byteLength ?? 0) + (entry.gz?.byteLength ?? 0);
  stats.cached = cache.size;
  stats.bytesInRam = bytes;
  return { ...stats };
}
