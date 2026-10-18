import type { Context } from "hono";

/**
 * ATL load governor (2026-10-14, additive) — admission control for high load.
 *
 * Measured baseline before this module existed: one process answered ~29k req/s
 * of RAM-served documents while pinned at ~92% of a single core, and it had NO
 * ceiling of any kind. A flood of DISTINCT cold paths (every one a cache miss,
 * each miss a full `seoHtml` render plus a brotli AND a gzip pass) was accepted
 * unconditionally — 800 of them in 264 ms, every one of them rendered.
 *
 * The gates below are ordered cheapest-first, and — deliberately — the cold path
 * QUEUES before it sheds. Queueing is the difference between "slower" and "broken":
 * a burst of legitimate cold requests is served after a bounded wait, and only a
 * flood that exhausts the queue is refused.
 *
 *   1. Global in-flight ceiling  - one integer compare for the whole site. Last resort.
 *   2. Per-client token bucket   - coarse single-abuser guard, bounded LRU map.
 *   3. Render slots + bounded FIFO queue - the only work a flood can amplify.
 *   4. Single-flight coalescing  - N simultaneous misses on ONE path = 1 render.
 *
 * Nothing here changes which bytes a URL returns. Warm paths — vault hits and
 * cached renders — never enter the governor at all, so normal traffic is
 * untouched; only genuinely cold work is ever queued or shed.
 */

type Bucket = { tokens: number; last: number };

export type GovernorStats = {
  enabled: boolean;
  inFlight: number;
  maxInflight: number;
  renderActive: number;
  maxRenderInflight: number;
  renderQueued: number;
  maxRenderQueue: number;
  admitted: number;
  coalesced: number;
  shedGlobal: number;
  shedRender: number;
  shedClient: number;
  clientKeys: number;
  retiredClientKeys: number;
  clientRps: number;
  clientBurst: number;
  proxyRps: number;
  proxyBurst: number;
  socketIpsSeen: number;
};

export type Admission = { ok: true } | { ok: false; reason: "client" | "render"; retryAfter: number };

function positiveInt(value: string | undefined, fallback: number): number {
  const n = Number(value);
  return Number.isFinite(n) && n > 0 ? Math.floor(n) : fallback;
}

/**
 * Socket address of the peer, captured in the Bun entrypoint before Hono sees the
 * request. This is the one client signal that cannot be spoofed by a header, so
 * it is what per-client limiting falls back to when no proxy header is present.
 */
const socketIps = new WeakMap<Request, string>();

export function rememberSocketIp(req: Request, ip: string | undefined): void {
  if (ip) socketIps.set(req, ip);
}

/**
 * Best-effort client identity, in trust order.
 *
 * The origin sits behind Cloudflare/proxy hops, so prefer the forwarded client
 * headers; fall back to the real socket address. Returns "" only when neither
 * exists, and an unknown client is simply not rate limited — a single shared
 * bucket labelled "unknown" would let one misconfigured hop throttle every
 * visitor at once. It stays covered by the global and render ceilings.
 */
export type ClientId = { key: string; forwarded: boolean };

/**
 * Client identity plus HOW it was derived.
 *
 * `forwarded: true` means a proxy header named the real visitor, so the strict
 * per-visitor bucket applies. `forwarded: false` means the only signal was the
 * socket peer - and that is the edge/proxy address, shared by every visitor
 * arriving through it. Those two cases must not share one allowance: a strict
 * limit keyed on a shared edge address would throttle the entire internet as a
 * single client, which is a self-inflicted outage rather than protection.
 */
export function clientId(c: Context): ClientId {
  const h = (name: string) => c.req.header(name);
  const cf = h("cf-connecting-ip");
  if (cf) return { key: cf.trim(), forwarded: true };
  const real = h("x-real-ip");
  if (real) return { key: real.trim(), forwarded: true };
  const xff = h("x-forwarded-for");
  if (xff) {
    const first = xff.split(",")[0]?.trim();
    if (first) return { key: first, forwarded: true };
  }
  const zo = h("x-zo-client-ip") ?? h("x-client-ip");
  if (zo) return { key: zo.trim(), forwarded: true };
  return { key: socketIps.get(c.req.raw) ?? "", forwarded: false };
}

export function clientKey(c: Context): string {
  return clientId(c).key;
}

export class LoadGovernor {
  readonly enabled: boolean;
  readonly maxInflight: number;
  readonly maxRenderInflight: number;
  readonly maxRenderQueue: number;
  readonly clientRps: number;
  readonly clientBurst: number;
  /** Allowance for a shared proxy/edge address, which fronts many visitors. */
  readonly proxyRps: number;
  readonly proxyBurst: number;
  readonly maxClientKeys: number;

  private inFlight = 0;
  private renderActive = 0;
  private renderQueue: Array<() => void> = [];
  private clients = new Map<string, Bucket>();
  private flights = new Map<string, Promise<unknown>>();
  private admitted = 0;
  private coalesced = 0;
  private shedGlobal = 0;
  private shedRender = 0;
  private shedClient = 0;
  private retiredClientKeys = 0;

  constructor(env: Record<string, string | undefined> = process.env) {
    this.enabled = env.ATL_GOVERNOR !== "0";
    this.maxInflight = positiveInt(env.ATL_MAX_INFLIGHT, 4096);
    this.maxRenderInflight = positiveInt(env.ATL_MAX_RENDER_INFLIGHT, 16);
    this.maxRenderQueue = positiveInt(env.ATL_MAX_RENDER_QUEUE, 1024);
    this.clientRps = positiveInt(env.ATL_CLIENT_RPS, 600);
    this.clientBurst = positiveInt(env.ATL_CLIENT_BURST, this.clientRps * 2);
    this.proxyRps = positiveInt(env.ATL_PROXY_RPS, this.clientRps * 25);
    this.proxyBurst = positiveInt(env.ATL_PROXY_BURST, this.clientBurst * 25);
    this.maxClientKeys = positiveInt(env.ATL_MAX_CLIENT_KEYS, 16384);
  }

  /**
   * Gate for every request, before any work happens: one compare. A `true` must be
   * paired with `exit()` in a `finally`. Returns `false` only when the site is
   * already at its absolute in-flight ceiling — the last-resort shed.
   */
  enter(): boolean {
    if (!this.enabled) return true;
    if (this.inFlight >= this.maxInflight) {
      this.shedGlobal += 1;
      return false;
    }
    this.inFlight += 1;
    return true;
  }

  exit(): void {
    if (!this.enabled) return;
    if (this.inFlight > 0) this.inFlight -= 1;
  }

  /** Per-client token bucket check. Cheap Map math; runs before any queueing. */
  admitClient(c: Context): Admission {
    if (!this.enabled) return { ok: true };
    const id = clientId(c);
    const rps = id.forwarded ? this.clientRps : this.proxyRps;
    const burst = id.forwarded ? this.clientBurst : this.proxyBurst;
    if (!this.allowClient(id.key, Date.now(), rps, burst)) {
      return { ok: false, reason: "client", retryAfter: 1 };
    }
    return { ok: true };
  }

  /**
   * Acquire a render slot, waiting in a bounded FIFO queue if all slots are busy.
   *
   * Resolves with a release function, or `null` when the queue is already full —
   * that is the only case in which cold work is refused, and it means the box is
   * facing far more distinct cold paths than it can ever render.
   */
  async acquireRender(): Promise<(() => void) | null> {
    if (!this.enabled) return () => {};

    if (this.renderActive < this.maxRenderInflight) {
      this.renderActive += 1;
      this.admitted += 1;
      return () => this.releaseRender();
    }

    if (this.renderQueue.length >= this.maxRenderQueue) {
      this.shedRender += 1;
      return null;
    }

    await new Promise<void>((resolve) => this.renderQueue.push(resolve));
    this.admitted += 1;
    return () => this.releaseRender();
  }

  /**
   * Hand the slot to the next waiter if there is one, otherwise retire it.
   *
   * Transferring rather than decrementing is what keeps concurrency exactly at the
   * ceiling: the woken waiter takes over the slot that was just freed.
   */
  private releaseRender(): void {
    const next = this.renderQueue.shift();
    if (next) {
      next();
      return;
    }
    if (this.renderActive > 0) this.renderActive -= 1;
  }

  /**
   * Coalesce concurrent work for one key: a flood of simultaneous misses on the
   * same path costs one render instead of one per request.
   */
  singleFlight<T>(key: string, fn: () => T | Promise<T>): Promise<T> {
    const existing = this.flights.get(key);
    if (existing) {
      this.coalesced += 1;
      return existing as Promise<T>;
    }
    const flight = (async () => fn())();
    this.flights.set(key, flight);
    // A failed flight must also be released, or the key stays poisoned forever.
    flight.catch(() => {}).finally(() => this.flights.delete(key));
    return flight;
  }

  /** Token bucket with insertion-order LRU eviction and a hard size ceiling. */
  private allowClient(key: string, now: number, rps: number, burst: number): boolean {
    if (!key) return true;

    let bucket = this.clients.get(key);
    if (!bucket) {
      if (this.clients.size >= this.maxClientKeys) this.retireClients();
      bucket = { tokens: burst, last: now };
      this.clients.set(key, bucket);
    } else {
      const elapsed = (now - bucket.last) / 1000;
      if (elapsed > 0) bucket.tokens = Math.min(burst, bucket.tokens + elapsed * rps);
      bucket.last = now;
      this.clients.delete(key);
      this.clients.set(key, bucket);
    }

    if (bucket.tokens < 1) {
      this.shedClient += 1;
      return false;
    }
    bucket.tokens -= 1;
    return true;
  }

  /** Drop the coldest quarter of client buckets; keeps memory flat under churn. */
  private retireClients(): void {
    const drop = Math.max(1, Math.floor(this.maxClientKeys / 4));
    let removed = 0;
    for (const key of this.clients.keys()) {
      this.clients.delete(key);
      removed += 1;
      if (removed >= drop) break;
    }
    this.retiredClientKeys += removed;
  }

  stats(): GovernorStats {
    return {
      enabled: this.enabled,
      inFlight: this.inFlight,
      maxInflight: this.maxInflight,
      renderActive: this.renderActive,
      maxRenderInflight: this.maxRenderInflight,
      renderQueued: this.renderQueue.length,
      maxRenderQueue: this.maxRenderQueue,
      admitted: this.admitted,
      coalesced: this.coalesced,
      shedGlobal: this.shedGlobal,
      shedRender: this.shedRender,
      shedClient: this.shedClient,
      clientKeys: this.clients.size,
      retiredClientKeys: this.retiredClientKeys,
      clientRps: this.clientRps,
      clientBurst: this.clientBurst,
      proxyRps: this.proxyRps,
      proxyBurst: this.proxyBurst,
      socketIpsSeen: this.socketIpCount,
    };
  }

  private socketIpCount = 0;

  noteSocketIp(): void {
    this.socketIpCount += 1;
  }
}

/** Singleton: one governor per process, shared by every gate. */
let governorSingleton: LoadGovernor | null = null;

export function getGovernor(): LoadGovernor {
  if (!governorSingleton) governorSingleton = new LoadGovernor();
  return governorSingleton;
}

const SHED_HTML =
  '<!doctype html><meta charset="utf-8"><title>Busy — ArcticTradeLanes</title>' +
  '<meta name="robots" content="noindex">' +
  '<body style="font:16px system-ui;margin:4rem auto;max-width:34rem;padding:0 1rem;color:#1a1a1a">' +
  "<h1 style=\"font-size:1.25rem\">Temporarily at capacity</h1>" +
  "<p>ArcticTradeLanes is handling more traffic than usual and deferred this request to keep the rest fast. " +
  "It is a load-shed response, not an error in the page you asked for.</p>" +
  "<p>Retry in a second. Machine clients: honour <code>Retry-After</code> and back off.</p></body>";

const SHED_JSON = { ok: false, error: "busy", reason: "load_shed", retryAfter: 1 };

/**
 * The shed response. Pre-serialised constants so answering "no" is as close to
 * free as this box can make it — a shed path that itself costs a render would
 * defeat the purpose of shedding.
 */
export function shedResponse(c: Context, retryAfter = 1): Response {
  const headers = new Headers({
    "Retry-After": String(retryAfter),
    "Cache-Control": "no-store, no-transform",
    "X-ATL-Shed": "1",
  });
  if (c.req.path.startsWith("/api/")) {
    headers.set("Content-Type", "application/json; charset=UTF-8");
    headers.set("Access-Control-Allow-Origin", "*");
    return new Response(JSON.stringify(SHED_JSON), { status: 503, headers });
  }
  headers.set("Content-Type", "text/html; charset=UTF-8");
  return new Response(SHED_HTML, { status: 503, headers });
}

/**
 * Requests that must stay answerable even while the box is shedding: health and
 * diagnostics. If the governor could shed its own metrics, an operator would be
 * blind exactly when they need to look.
 */
const NEVER_SHED = new Set(["/api/perf", "/api/health", "/api/alpha/status"]);

export function governorMiddleware() {
  const governor = getGovernor();
  return async (c: Context, next: () => Promise<void>): Promise<void> => {
    if (!governor.enabled) return next();
    const method = c.req.method;
    if (method !== "GET" && method !== "HEAD" && method !== "POST") return next();
    // WebSocket upgrades are long-lived by design and must not occupy a slot.
    if (c.req.header("upgrade")) return next();
    if (NEVER_SHED.has(c.req.path)) return next();

    if (!governor.enter()) return void (c.res = shedResponse(c));
    try {
      await next();
    } finally {
      governor.exit();
    }
  };
}
