import { createHash } from "node:crypto";
import { readdirSync, readFileSync, statSync } from "node:fs";
import { extname, join } from "node:path";
import { brotliCompressSync, constants as zlib, gzipSync } from "node:zlib";
import type { Context } from "hono";
import { LOCALES, knownRoutePaths, seoHtml } from "./seoMiddleware";
import { getGovernor } from "./loadGovernor";

/**
 * ATL high-load performance layer (2026-10-14, additive).
 *
 * The origin previously did, on EVERY request:
 *   - `Bun.file('./dist'+path).exists()` + `.stat()`  (2 syscalls on a 9p mount)
 *   - `readFileSync` of the page document + up to 9 `existsSync` probes (seoMiddleware)
 *   - an uncompressed 2.2 MB GeoJSON body (12 byte-identical copies on disk)
 *
 * This module removes all per-request disk I/O from the hot path:
 *
 *   1. StaticVault      - dist/ is walked once at boot; every compressible file is
 *                         pre-compressed (brotli + gzip) and byte-identical files are
 *                         de-duplicated by content hash (12 GeoJSON copies -> 2 payloads).
 *                         Data files keep a throttled mtime revalidation so the hourly
 *                         atlas rebuild is picked up without a restart.
 *   2. RenderCache      - fully rendered SEO HTML per normalised path, pre-compressed,
 *                         with a strong ETag so repeat hits answer 304 with no body.
 *   3. Cache-Control    - immutable for hashed assets, SWR for HTML and data.
 *
 * Nothing here changes which bytes a URL returns; it only changes how they are produced.
 */

const IDENTITY_MAX = 256 * 1024;
const COMPRESS_MIN = 1024;
const COMPRESS_MAX = 24 * 1024 * 1024;

const MIME: Record<string, string> = {
  ".html": "text/html; charset=UTF-8",
  ".htm": "text/html; charset=UTF-8",
  ".js": "text/javascript; charset=UTF-8",
  ".mjs": "text/javascript; charset=UTF-8",
  ".css": "text/css; charset=UTF-8",
  ".json": "application/json; charset=UTF-8",
  ".geojson": "application/geo+json; charset=UTF-8",
  ".csv": "text/csv; charset=UTF-8",
  ".txt": "text/plain; charset=UTF-8",
  ".md": "text/markdown; charset=UTF-8",
  ".xml": "application/xml; charset=UTF-8",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".webp": "image/webp",
  ".avif": "image/avif",
  ".gif": "image/gif",
  ".ico": "image/x-icon",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
  ".ttf": "font/ttf",
  ".otf": "font/otf",
  ".webmanifest": "application/manifest+json; charset=UTF-8",
  ".map": "application/json; charset=UTF-8",
  ".wasm": "application/wasm",
  ".pdf": "application/pdf",
};

const COMPRESSIBLE = new Set([
  ".html", ".htm", ".js", ".mjs", ".css", ".json", ".geojson", ".csv",
  ".txt", ".md", ".xml", ".svg", ".webmanifest", ".map",
]);

const HASHED_ASSET = /assets\/[A-Za-z0-9_/.-]*-[A-Za-z0-9_]{8,}\.[a-z0-9]+$/i;
const SYNC_EXT = new Set([".geojson", ".json", ".csv", ".xml", ".txt", ".md"]);

export function mimeFor(path: string): string {
  return MIME[extname(path).toLowerCase()] ?? "application/octet-stream";
}

function isCompressible(path: string): boolean {
  return COMPRESSIBLE.has(extname(path).toLowerCase());
}

function cacheControlFor(rel: string): string {
  const ext = extname(rel).toLowerCase();
  if (HASHED_ASSET.test(rel)) return "public, max-age=31536000, immutable";
  if (SYNC_EXT.has(ext)) return "public, max-age=300, stale-while-revalidate=3600";
  if (ext === ".html" || ext === ".htm") return "public, max-age=120, stale-while-revalidate=600";
  if (ext === ".svg" || ext === ".png" || ext === ".jpg" || ext === ".jpeg" ||
      ext === ".webp" || ext === ".avif" || ext === ".gif" || ext === ".ico" ||
      ext === ".woff" || ext === ".woff2" || ext === ".ttf" || ext === ".otf") {
    return "public, max-age=604800";
  }
  return "public, max-age=3600";
}

type Shared = { gz?: Uint8Array; br?: Uint8Array };

type VaultEntry = {
  rel: string;
  abs: string;
  root: string;
  mime: string;
  size: number;
  mtimeMs: number;
  etag: string;
  cacheControl: string;
  body?: Uint8Array;
  shared: Shared;
  sync: boolean;
  nextSync: number;
};

export type VaultStats = {
  files: number;
  bytesOnDisk: number;
  identityEntries: number;
  sharedPayloads: number;
  bytesInRam: number;
  buildMs: number;
};

function shortHash(buf: Uint8Array): string {
  return createHash("sha256").update(buf).digest("hex").slice(0, 32);
}

function compressPair(buf: Uint8Array, size: number): Shared {
  const quality = size > 1024 * 1024 ? 4 : 9;
  const out: Shared = {};
  try {
    out.gz = new Uint8Array(gzipSync(buf, { level: zlib.Z_BEST_COMPRESSION }));
  } catch {
    out.gz = undefined;
  }
  try {
    out.br = new Uint8Array(
      brotliCompressSync(buf, {
        params: {
          [zlib.BROTLI_PARAM_QUALITY]: quality,
          [zlib.BROTLI_PARAM_SIZE_HINT]: size,
        },
      }),
    );
  } catch {
    out.br = undefined;
  }
  return out;
}

/**
 * Files that exist on disk but must never be served: dataset backups, editor and
 * OS junk, half-written temp files. They are not linked from any page and each one
 * would otherwise cost RAM in the vault and widen the public surface.
 */
const NEVER_SERVED = /(?:\.bak(?:-|$)|~$|\.orig$|\.tmp$|\.swp$|\.log$|\.sqlite$|\.db$|\.DS_Store$)/i;

function walkFiles(root: string, rel = ""): string[] {
  const out: string[] = [];
  let entries: ReturnType<typeof readdirSync>;
  try {
    entries = readdirSync(join(root, rel), { withFileTypes: true });
  } catch {
    return out;
  }
  for (const entry of entries) {
    const next = rel ? `${rel}/${entry.name}` : entry.name;
    if (entry.isDirectory()) {
      out.push(...walkFiles(root, next));
    } else if (entry.isFile() && isServable(next)) {
      out.push(next);
    }
  }
  return out;
}

function isServable(rel: string): boolean {
  return !NEVER_SERVED.test(rel) && !rel.split("/").some((seg) => seg.startsWith("."));
}

export class StaticVault {
  private entries = new Map<string, VaultEntry>();
  private pool = new Map<string, Shared>();
  readonly roots: string[];
  private stats: VaultStats = {
    files: 0,
    bytesOnDisk: 0,
    identityEntries: 0,
    sharedPayloads: 0,
    bytesInRam: 0,
    buildMs: 0,
  };

  constructor(roots: string[]) {
    this.roots = roots;
  }

  build(): void {
    const started = Date.now();
    for (const root of this.roots) {
      for (const rel of walkFiles(root)) {
        // First root wins: ./dist is the built output, ./public is only a fallback for
        // paths the build does not emit (favicons, brand svgs, og images).
        if (this.entries.has(rel)) continue;
        this.load(root, rel, true);
      }
    }
    this.stats.buildMs = Date.now() - started;
    this.recount();
  }

  private load(root: string, rel: string, fresh: boolean): VaultEntry | null {
    const abs = join(root, rel);
    let st: ReturnType<typeof statSync>;
    try {
      st = statSync(abs);
    } catch {
      return null;
    }
    if (!st.isFile()) return null;

    const size = st.size;
    const mime = mimeFor(rel);
    const compressible = isCompressible(rel) && size >= COMPRESS_MIN && size <= COMPRESS_MAX;

    let buf: Uint8Array | undefined;
    let etag: string;
    let body: Uint8Array | undefined;
    let shared: Shared = {};

    if (compressible || size <= IDENTITY_MAX) {
      try {
        buf = new Uint8Array(readFileSync(abs));
      } catch {
        return null;
      }
    }

    if (buf) {
      const hash = shortHash(buf);
      etag = `"${hash}"`;
      if (size <= IDENTITY_MAX) body = buf;
      if (compressible) {
        const cached = this.pool.get(hash);
        if (cached) {
          shared = cached;
        } else {
          shared = compressPair(buf, size);
          this.pool.set(hash, shared);
        }
      }
    } else {
      etag = `"${size.toString(16)}-${Math.round(st.mtimeMs).toString(16)}"`;
    }

    const entry: VaultEntry = {
      rel,
      abs,
      root,
      mime,
      size,
      mtimeMs: st.mtimeMs,
      etag,
      cacheControl: cacheControlFor(rel),
      body,
      shared,
      sync: SYNC_EXT.has(extname(rel).toLowerCase()),
      nextSync: 0,
    };

    this.entries.set(rel, entry);
    if (!fresh) this.recount();
    return entry;
  }

  /** Throttled mtime revalidation so hourly atlas rebuilds land without a restart. */
  private maybeResync(entry: VaultEntry, now: number): VaultEntry {
    if (!entry.sync || now < entry.nextSync) return entry;
    entry.nextSync = now + 2000;
    let st: ReturnType<typeof statSync>;
    try {
      st = statSync(entry.abs);
    } catch {
      return entry;
    }
    if (st.size === entry.size && Math.round(st.mtimeMs) === Math.round(entry.mtimeMs)) {
      return entry;
    }
    const reloaded = this.load(entry.root, entry.rel, false);
    return reloaded ?? entry;
  }

  private recount(): void {
    let bytesInRam = 0;
    for (const entry of this.entries.values()) {
      if (entry.body) bytesInRam += entry.body.byteLength;
    }
    for (const shared of this.pool.values()) {
      bytesInRam += (shared.gz?.byteLength ?? 0) + (shared.br?.byteLength ?? 0);
    }
    let bytesOnDisk = 0;
    let identityEntries = 0;
    for (const entry of this.entries.values()) {
      bytesOnDisk += entry.size;
      if (entry.body) identityEntries += 1;
    }
    this.stats = {
      files: this.entries.size,
      bytesOnDisk,
      identityEntries,
      sharedPayloads: this.pool.size,
      bytesInRam,
      buildMs: this.stats.buildMs,
    };
  }

  get length(): number {
    return this.entries.size;
  }

  statsSnapshot(): VaultStats {
    this.recount();
    return { ...this.stats };
  }

  lookup(relPath: string): VaultEntry | null {
    const rel = relPath.replace(/^\/+/, "");
    if (!rel || rel.includes("..")) return null;
    const entry = this.entries.get(rel);
    if (!entry) return null;
    return this.maybeResync(entry, Date.now());
  }

  /** Force a full rebuild (used by /api/perf?rebuild=1 diagnostics). */
  refresh(): VaultStats {
    this.pool.clear();
    this.entries.clear();
    this.build();
    return this.statsSnapshot();
  }

  sharedBytes(): { gz: number; br: number } {
    let gz = 0;
    let br = 0;
    for (const shared of this.pool.values()) {
      gz += shared.gz?.byteLength ?? 0;
      br += shared.br?.byteLength ?? 0;
    }
    return { gz, br };
  }
}

function etagMatches(header: string, etag: string): boolean {
  if (header.trim() === "*") return true;
  const bare = etag.replace(/^W\//, "");
  for (const candidate of header.split(",")) {
    const c = candidate.trim();
    if (c === etag || c === bare || c.replace(/^W\//, "") === bare) return true;
  }
  return false;
}

type Encoding = "br" | "gzip" | "identity";

function pickEncoding(acceptEncoding: string | undefined, shared: Shared, hasIdentity: boolean): Encoding {
  const ae = (acceptEncoding ?? "").toLowerCase();
  if (shared.br && /\bbr\b/.test(ae)) return "br";
  if (shared.gz && /\bgzip\b/.test(ae)) return "gzip";
  if (hasIdentity || shared.br || shared.gz) return "identity";
  return "identity";
}

/** Serve a vault entry, or return null so the caller can fall through. */
export function vaultResponse(vault: StaticVault, urlPath: string, c: Context): Response | null {
  const entry = vault.lookup(urlPath);
  if (!entry) return null;

  const headers = new Headers({
    "Content-Type": entry.mime,
    "Cache-Control": entry.cacheControl,
    "ETag": entry.etag,
    "X-ATL-Vault": "hit",
  });

  if (etagMatches(c.req.header("if-none-match") ?? "", entry.etag)) {
    return new Response(null, { status: 304, headers });
  }

  const isHead = c.req.method === "HEAD";
  const encoding = isHead ? "identity" : pickEncoding(c.req.header("accept-encoding"), entry.shared, Boolean(entry.body));

  if (encoding === "br" && entry.shared.br) {
    headers.set("Content-Encoding", "br");
    headers.set("Vary", "Accept-Encoding");
    headers.set("Content-Length", String(entry.shared.br.byteLength));
    return new Response(isHead ? null : entry.shared.br, { status: 200, headers });
  }
  if (encoding === "gzip" && entry.shared.gz) {
    headers.set("Content-Encoding", "gzip");
    headers.set("Vary", "Accept-Encoding");
    headers.set("Content-Length", String(entry.shared.gz.byteLength));
    return new Response(isHead ? null : entry.shared.gz, { status: 200, headers });
  }
  if (entry.body) {
    headers.set("Content-Length", String(entry.body.byteLength));
    headers.set("Vary", "Accept-Encoding");
    return new Response(isHead ? null : entry.body, { status: 200, headers });
  }

  headers.set("Content-Length", String(entry.size));
  return new Response(isHead ? null : Bun.file(entry.abs), { status: 200, headers });
}

export type Rendered = {
  html: string;
  etag: string;
  gz: Uint8Array;
  br: Uint8Array;
  expires: number;
  hits: number;
};

export type RenderStats = {
  entries: number;
  bytesInRam: number;
  hits: number;
  misses: number;
  revalidations: number;
  hitRatio: number;
  ttlMs: number;
};

export class RenderCache {
  private map = new Map<string, Rendered>();
  readonly maxEntries: number;
  readonly ttlMs: number;
  private hits = 0;
  private misses = 0;

  constructor(maxEntries = 2048, ttlMs = Number(process.env.ATL_HTML_TTL_MS ?? 120_000)) {
    this.maxEntries = maxEntries;
    this.ttlMs = Number.isFinite(ttlMs) && ttlMs > 0 ? ttlMs : 120_000;
  }

  private evict(): void {
    while (this.map.size > this.maxEntries) {
      const oldest = this.map.keys().next();
      if (oldest.done) break;
      this.map.delete(oldest.value);
    }
  }

  private put(key: string, value: Rendered): void {
    this.map.delete(key);
    this.map.set(key, value);
    this.evict();
  }

  render(path: string, shell: string, now = Date.now()): Rendered {
    const hit = this.recall(path, now);
    if (hit) return hit;
    this.misses += 1;
    return this.store(path, seoHtml(path, shell), now);
  }

  /**
   * Cache an already-rendered document (SSR panels, pre-built pages) under an
   * explicit key. Same compression + ETag treatment as the SEO shell render.
   */
  renderDocument(key: string, html: string, now = Date.now()): Rendered {
    const hit = this.recall(key, now);
    if (hit) return hit;
    this.misses += 1;
    return this.store(key, html, now);
  }

  /**
   * Non-building read used by the load governor's hot path.
   *
   * Splitting lookup from build is what lets the server answer a warm path without
   * ever entering the governor (no admission decision, no promise), and lets the
   * single-flight leader re-check for a document a sibling flight just produced.
   * `count=false` keeps that re-check from double-counting a hit/miss.
   */
  lookup(key: string, now = Date.now(), count = true): Rendered | null {
    const existing = this.map.get(key);
    if (!existing || existing.expires <= now) {
      if (count) this.misses += 1;
      return null;
    }
    if (count) {
      existing.hits += 1;
      this.hits += 1;
    }
    this.map.delete(key);
    this.map.set(key, existing);
    return existing;
  }

  /**
   * Unconditional rebuild for a key, used only by a single-flight leader after a
   * miss.
   *
   * Deliberately does NOT count a miss: the caller's `lookup()` probe already
   * counted it. So one cold request = one miss no matter how many concurrent
   * requests were coalesced onto the same single-flight key.
   */
  renderFresh(key: string, shell: string, now = Date.now()): Rendered {
    return this.store(key, seoHtml(key, shell), now);
  }

  /**
   * Render without inserting into the cache.
   *
   * Used for URLs that are not a known route: a flood of random paths must not be
   * able to (a) grow the cache past its budget or (b) force thousands of
   * brotli/gzip compressions that would then be retained. Cost is one render and
   * the response is still correct, byte for byte.
   */
  renderUncached(key: string, html: string, now = Date.now()): Rendered {
    this.misses += 1;
    return this.build(key, html, now);
  }
  /**
   * Cache a document generated outside the shell pipeline — the pre-built Arctic-panel
   * SSR pages. Same ETag/encoding treatment as a rendered route, so the SSR branch costs
   * one disk read per TTL instead of one per request.
   */
  cacheHtml(key: string, html: string, now = Date.now()): Rendered {
    return this.store(key, html, now);
  }
  /**
   * Cache a document this process did not render itself — used by the Arctic-panel
   * SSR branch in server.ts, where the HTML already exists on disk and only needs
   * the ETag/gzip/brotli treatment. Prefer this over `renderFresh()`, which would
   * re-render the document from the shell and discard the file's own content.
   */
  cacheHtml(key: string, html: string, now = Date.now()): Rendered {
    return this.store(key, html, now);
  }
  /**
   * Retain a document produced outside the SEO pipeline — the pre-generated
   * Arctic-panel SSR pages — so every request after the first is an ordinary
   * cache hit instead of another disk read.
   */
  cacheHtml(key: string, html: string, now = Date.now()): Rendered {
    return this.store(key, html, now);
  }

  /**
   * Cache a document that was produced somewhere other than `seoHtml()`.
   *
   * The Arctic-panel SSR pages are pre-generated files on disk, not shells with
   * SEO injected, so they cannot go through `renderFresh()`. They still want the
   * same pre-compressed body + ETag treatment, which is exactly what `build()`
   * does. Adding this closes the `ReferenceError: cached is not defined` that
   * server.ts carried in its SSR branch - a latent 500 on every /people and
   * /events page, invisible only because ./ssr was not present.
   */
  cacheHtml(key: string, html: string, now = Date.now()): Rendered {
    return this.store(key, html, now);
  }

  private recall(key: string, now: number): Rendered | null {
    const existing = this.map.get(key);
    if (!existing || existing.expires <= now) return null;
    existing.hits += 1;
    this.hits += 1;
    this.map.delete(key);
    this.map.set(key, existing);
    return existing;
  }

  private store(key: string, html: string, now: number): Rendered {
    const entry = this.build(key, html, now);
    this.put(key, entry);
    return entry;
  }

  private build(key: string, html: string, now: number): Rendered {
    const bytes = Buffer.from(html, "utf8");
    return {
      html,
      etag: `"${shortHash(bytes)}"`,
      gz: new Uint8Array(gzipSync(bytes, { level: zlib.Z_DEFAULT_COMPRESSION })),
      br: new Uint8Array(brotliCompressSync(bytes, { params: { [zlib.BROTLI_PARAM_QUALITY]: 5 } })),
      expires: now + this.ttlMs,
      hits: 0,
    };
  }

  /** Warm the known route x locale matrix so the first real hit is already hot. */
  warm(shell: string): { rendered: number; ms: number } {
    const started = Date.now();
    let rendered = 0;
    for (const route of knownRoutePaths()) {
      const base = route === "/" ? "" : route;
      for (const locale of LOCALES) {
        const path = locale === "en" ? `/${base.replace(/^\//, "")}` : `/${locale}${base}`;
        const normalised = path === "/" ? "/" : path.replace(/\/+$/, "");
        this.render(normalised || "/", shell);
        rendered += 1;
      }
    }
    return { rendered, ms: Date.now() - started };
  }

  invalidate(): void {
    this.map.clear();
  }
  /** O(1) read of the hit/miss counters — used by the hot path for metrics. */
  get counters(): { hits: number; misses: number } {
    return { hits: this.hits, misses: this.misses };
  }

  stats(): RenderStats {
    let bytesInRam = 0;
    for (const entry of this.map.values()) {
      bytesInRam += entry.gz.byteLength + entry.br.byteLength + entry.html.length;
    }
    const total = this.hits + this.misses;
    return {
      entries: this.map.size,
      bytesInRam,
      hits: this.hits,
      misses: this.misses,
      revalidations: this.hits,
      hitRatio: total === 0 ? 0 : Number((this.hits / total).toFixed(3)),
      ttlMs: this.ttlMs,
    };
  }
}

/** Emit a cached HTML document with encoding negotiation and 304 support. */
export function renderedResponse(entry: Rendered, c: Context, extra: Record<string, string> = {}): Response {
  const headers = new Headers({
    "Content-Type": "text/html; charset=UTF-8",
    "Cache-Control": "public, max-age=120, stale-while-revalidate=600",
    "ETag": entry.etag,
    "X-ATL-Vault": "render",
    ...extra,
  });

  if (etagMatches(c.req.header("if-none-match") ?? "", entry.etag)) {
    return new Response(null, { status: 304, headers });
  }

  if (c.req.method === "HEAD") {
    headers.set("Content-Length", String(Buffer.byteLength(entry.html, "utf8")));
    return new Response(null, { status: 200, headers });
  }

  const ae = (c.req.header("accept-encoding") ?? "").toLowerCase();
  if (/\bbr\b/.test(ae)) {
    headers.set("Content-Encoding", "br");
    headers.set("Vary", "Accept-Encoding");
    headers.set("Content-Length", String(entry.br.byteLength));
    return new Response(entry.br, { status: 200, headers });
  }
  if (/\bgzip\b/.test(ae)) {
    headers.set("Content-Encoding", "gzip");
    headers.set("Vary", "Accept-Encoding");
    headers.set("Content-Length", String(entry.gz.byteLength));
    return new Response(entry.gz, { status: 200, headers });
  }
  headers.set("Vary", "Accept-Encoding");
  headers.set("Content-Length", String(Buffer.byteLength(entry.html, "utf8")));
  return new Response(entry.html, { status: 200, headers });
}

let vaultSingleton: StaticVault | null = null;
let renderSingleton: RenderCache | null = null;
/**
 * True when the URL maps to a route this origin actually ships, so the rendered
 * document is worth keeping. Anything else is rendered but not retained.
 */
export function isCacheablePath(urlPath: string): boolean {
  let p = (urlPath || "/").split("?")[0].split("#")[0];
  if (!p.startsWith("/")) p = `/${p}`;
  if (p.length > 1) p = p.replace(/\/+$/, "");
  if (p === "" || p === "/") return true;
  const segments = p.split("/").filter(Boolean);
  const rest =
    segments.length > 0 && (LOCALES as readonly string[]).includes(segments[0])
      ? `/${segments.slice(1).join("/")}`
      : p;
  if (rest === "/" || rest === "") return true;
  return knownRoutePaths().includes(rest);
}

function appendVary(current: string | null, value: string): string {
  if (!current) return value;
  if (current === "*") return current;
  const parts = current.split(",").map((s) => s.trim().toLowerCase());
  return parts.includes(value.toLowerCase()) ? current : `${current}, ${value}`;
}

type CompressOptions = { threshold?: number; maxBytes?: number; quality?: number };

const COMPRESSIBLE_TYPE = /^(?:text\/|application\/(?:json|xml|javascript|x-ndjson|ld\+json)|image\/svg)/i;

/**
 * Drop-in replacement for `hono/compress`, which this Bun runtime cannot run:
 * it needs a global `CompressionStream` and throws `ReferenceError` on every
 * response it touches, turning each request that carries an `Accept-Encoding`
 * header into a 500. This version compresses synchronously with node:zlib and
 * can never fail a request - any error leaves the original response in place.
 *
 * Responses that already carry a Content-Encoding (the pre-compressed vault and
 * render cache) are passed through untouched, so the hot path stays allocation-free.
 */
export function atlCompress(options: CompressOptions = {}) {
  const threshold = options.threshold ?? 1024;
  const maxBytes = options.maxBytes ?? 4 * 1024 * 1024;
  const quality = options.quality ?? 5;

  return async (c: Context, next: () => Promise<void>): Promise<void> => {
    await next();

    try {
      const res = c.res;
      if (process.env.ATL_DEBUG_COMPRESS === "1" && res && res.status >= 500) {
        console.error("[atl-compress] upstream 5xx", c.req.method, c.req.path, res.status);
      }
      if (!res || !res.body) return;
      if (res.status === 204 || res.status === 304) return;
      if (c.req.method === "HEAD") return;
      // Already encoded by the vault/render cache: pass straight through.
      if (res.headers.get("Content-Encoding")) return;
      if (/\bno-transform\b/i.test(res.headers.get("Cache-Control") ?? "")) return;
      if (!COMPRESSIBLE_TYPE.test(res.headers.get("Content-Type") ?? "")) return;

      const declared = Number(res.headers.get("Content-Length") ?? "0");
      // Nothing to gain on a body we already know is small: do not even read it.
      if (declared > 0 && declared < threshold) return;
      if (declared > maxBytes) return;

      const accept = (c.req.header("accept-encoding") ?? "").toLowerCase();
      const wantsBr = /\bbr\b/.test(accept);
      const wantsGzip = /\bgzip\b/.test(accept);
      if (!wantsBr && !wantsGzip) return;

      // Reading the body consumes it, so from here on the response is ALWAYS
      // rebuilt - compressed when we win, verbatim when we do not. Returning
      // early after this point would ship a consumed body (Bun answers 500).
      const raw = new Uint8Array(await res.arrayBuffer());
      let body = raw;
      let encoding: string | null = null;
      if (raw.byteLength >= threshold && raw.byteLength <= maxBytes) {
        try {
          if (wantsBr) {
            const packed = new Uint8Array(
              brotliCompressSync(raw, { params: { [zlib.BROTLI_PARAM_QUALITY]: quality } }),
            );
            if (packed.byteLength < raw.byteLength) {
              body = packed;
              encoding = "br";
            }
          }
          if (!encoding && wantsGzip) {
            const packed = new Uint8Array(gzipSync(raw));
            if (packed.byteLength < raw.byteLength) {
              body = packed;
              encoding = "gzip";
            }
          }
        } catch {
          body = raw;
          encoding = null;
        }
      }

      const headers = new Headers(res.headers);
      headers.delete("Content-Encoding");
      if (encoding) {
        headers.set("Content-Encoding", encoding);
        headers.set("Vary", appendVary(headers.get("Vary"), "Accept-Encoding"));
      }
      headers.set("Content-Length", String(body.byteLength));

      c.res = new Response(body, {
        status: res.status,
        statusText: res.statusText,
        headers,
      });
    } catch {
      /* never let compression break a response */
    }
  };
}

/** Built once per process; safe to call from both boot paths. */
export function getVault(roots: string[] = ["./dist"]): StaticVault {
  if (!vaultSingleton) {
    vaultSingleton = new StaticVault(roots);
    vaultSingleton.build();
  }
  return vaultSingleton;
}

export function getRenderCache(): RenderCache {
  if (!renderSingleton) renderSingleton = new RenderCache();
  return renderSingleton;
}
let shellSingleton: string | null = null;

/** dist/index.html is the SEO shell: read once, then served from RAM forever. */
export function getShell(path = "./dist/index.html"): string {
  if (shellSingleton === null) shellSingleton = readFileSync(path, "utf8");
  return shellSingleton;
}

export type PerfSnapshot = {
  errors: number;
  vault: VaultStats;
  render: RenderStats;
  uptimeS: number;
  rssMB: number;
  heapUsedMB: number;
  pid: number;
  ttlMs: number;
  bytesSavedByCompression: number;
  requests: number;
  shed: { load: number; admitted: number; coalesced: number };
};

const counters = { requests: 0, servedCompressed: 0, notModified: 0, vaultHits: 0, renderHits: 0, renderMisses: 0, errors: 0, shedLoad: 0 };

export function countRequest(kind: keyof typeof counters): void {
  counters[kind] += 1;
}

export function perfSnapshot(): PerfSnapshot {
  const mem = process.memoryUsage();
  const vault = getVault();
  const render = getRenderCache();
  const vaultStats = vault.statsSnapshot();
  const shared = vault.sharedBytes();
  const governorStats = getGovernor().stats();
  return {
    errors: counters.errors,
    vault: vaultStats,
    render: render.stats(),
    uptimeS: Math.round(process.uptime()),
    rssMB: Number((mem.rss / 1048576).toFixed(1)),
    heapUsedMB: Number((mem.heapUsed / 1048576).toFixed(1)),
    pid: process.pid,
    ttlMs: render.ttlMs,
    bytesSavedByCompression: vaultStats.bytesOnDisk - (shared.gz + shared.br),
    requests: counters.requests,
    shed: { load: counters.shedLoad, admitted: governorStats.admitted, coalesced: governorStats.coalesced },
  };
}
