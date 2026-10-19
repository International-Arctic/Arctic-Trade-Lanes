/**
 * Private intake queues for the homepage extras (2026-10-18).
 *   POST /api/atl-interest   -> $ATL early-interest list (email OR wallet)
 *   POST /api/contributions  -> moderated contribution queue (status "pending"; never auto-published)
 *
 * Storage: NDJSON files OUTSIDE the app repo (default /home/workspace/ArcticTradeLanes.com/_private-intake,
 * override ATL_INTAKE_DIR), mode 0600. IPs are stored only as salted SHA-256 prefixes.
 * Abuse controls: honeypot field "website", per-IP rate limit, body size cap, strict validation,
 * file size ceiling. Accepts JSON (fetch) or form posts (no-JS: 303 back to the homepage anchor).
 */
import { Hono, type Context } from "hono";
import { appendFileSync, chmodSync, existsSync, mkdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { createHash, randomBytes, randomUUID } from "node:crypto";

const DIR = process.env.ATL_INTAKE_DIR || "/home/workspace/ArcticTradeLanes.com/_private-intake";
const FILES = { interest: `${DIR}/atl-interest.ndjson`, contribution: `${DIR}/contributions.ndjson` } as const;
const MAX_BODY = 16 * 1024;
const MAX_FILE = 25 * 1024 * 1024;
const WINDOW_MS = 10 * 60 * 1000;
const PER_IP = 5;
const LOCALES = new Set(["en", "ru", "zh", "ja", "ko", "el", "de", "nl", "fr", "es", "it", "pt", "tr", "ar", "hi", "vi", "id", "da", "fi", "sv", "nb", "is"]);

let salt = "";
function ensureStore(): void {
  if (salt) return;
  if (!existsSync(DIR)) mkdirSync(DIR, { recursive: true, mode: 0o700 });
  const saltFile = `${DIR}/.salt`;
  if (!existsSync(saltFile)) writeFileSync(saltFile, randomBytes(24).toString("hex"), { mode: 0o600 });
  salt = readFileSync(saltFile, "utf8").trim();
}

const hits = new Map<string, number[]>();
function limited(key: string, now = Date.now()): boolean {
  const arr = (hits.get(key) || []).filter((t) => now - t < WINDOW_MS);
  if (arr.length >= PER_IP) { hits.set(key, arr); return true; }
  arr.push(now); hits.set(key, arr);
  if (hits.size > 50_000) hits.clear();
  return false;
}

function clientIp(c: Context): string {
  return (c.req.header("cf-connecting-ip") || c.req.header("x-real-ip") || (c.req.header("x-forwarded-for") || "").split(",")[0] || "unknown").trim();
}
const clean = (v: unknown, max: number) => (typeof v === "string" ? v.replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, "").trim().slice(0, max) : "");
const EMAIL = /^[^\s@<>"]{1,64}@[^\s@<>"]{1,190}\.[A-Za-z]{2,24}$/;
const WALLET = [/^0x[a-fA-F0-9]{40}$/, /^[1-9A-HJ-NP-Za-km-z]{32,44}$/, /^[a-z0-9-]{1,63}(\.[a-z0-9-]{1,63})*\.eth$/i];
const URL_RE = /^https?:\/\/[^\s<>"]{3,490}$/i;
const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;

async function readBody(c: Context): Promise<{ data: Record<string, unknown>; form: boolean } | null> {
  const len = Number(c.req.header("content-length") || "0");
  if (len > MAX_BODY) return null;
  const ct = (c.req.header("content-type") || "").toLowerCase();
  try {
    if (ct.includes("application/json")) {
      const raw = await c.req.text();
      if (raw.length > MAX_BODY) return null;
      const j = JSON.parse(raw);
      return j && typeof j === "object" && !Array.isArray(j) ? { data: j, form: false } : null;
    }
    if (ct.includes("application/x-www-form-urlencoded") || ct.includes("multipart/form-data")) {
      const b = await c.req.parseBody();
      const data: Record<string, unknown> = {};
      for (const [k, v] of Object.entries(b)) if (typeof v === "string") data[k] = v;
      return { data, form: true };
    }
  } catch { /* fallthrough */ }
  return null;
}

function reply(c: Context, form: boolean, lang: string, status: number, anchor: string, body: Record<string, unknown>) {
  if (form) {
    const pre = lang && lang !== "en" ? `/${lang}` : "/";
    return c.redirect(`${pre}?atlx=${status === 200 ? "ok" : "err"}#${anchor}`, 303);
  }
  return c.json(body, status as 200);
}

function store(kind: keyof typeof FILES, rec: Record<string, unknown>): boolean {
  ensureStore();
  const f = FILES[kind];
  try { if (existsSync(f) && statSync(f).size > MAX_FILE) return false; } catch { /* ignore */ }
  appendFileSync(f, JSON.stringify(rec) + "\n", { mode: 0o600 });
  try { chmodSync(f, 0o600); } catch { /* ignore */ }
  return true;
}

function meta(c: Context, kind: string, data: Record<string, unknown>) {
  ensureStore();
  const ip = clientIp(c);
  return {
    id: randomUUID(),
    ts: new Date().toISOString(),
    kind,
    status: "pending",
    test: data.test === "1" || data.test === true || undefined,
    lang: LOCALES.has(String(data.lang)) ? String(data.lang) : "en",
    ipHash: createHash("sha256").update(salt + ip).digest("hex").slice(0, 16),
    ua: clean(c.req.header("user-agent"), 200),
  };
}

const intake = new Hono();

intake.post("/api/atl-interest", async (c) => {
  const parsed = await readBody(c);
  if (!parsed) return c.json({ ok: false, error: "bad_request" }, 400);
  const { data, form } = parsed;
  const lang = LOCALES.has(String(data.lang)) ? String(data.lang) : "en";
  if (clean(data.website, 200)) return reply(c, form, lang, 422, "atlx-token", { ok: false, error: "rejected" });
  ensureStore();
  if (limited(`i:${clientIp(c)}`)) return reply(c, form, lang, 429, "atlx-token", { ok: false, error: "rate_limited" });
  const email = clean(data.email, 254).toLowerCase();
  const wallet = clean(data.wallet, 128);
  const emailOk = !!email && EMAIL.test(email);
  const walletOk = !!wallet && WALLET.some((r) => r.test(wallet));
  const consent = data.consent === "1" || data.consent === "on" || data.consent === true;
  if ((!emailOk && !walletOk) || (email && !emailOk) || (wallet && !walletOk) || !consent) {
    return reply(c, form, lang, 400, "atlx-token", { ok: false, error: "invalid" });
  }
  const role = ["supporter", "builder", "media", "business"].includes(String(data.role)) ? String(data.role) : "supporter";
  const ok = store("interest", { ...meta(c, "atl-interest", data), email: emailOk ? email : undefined, wallet: walletOk ? wallet : undefined, role, consent: true });
  if (!ok) return reply(c, form, lang, 503, "atlx-token", { ok: false, error: "unavailable" });
  return reply(c, form, lang, 200, "atlx-token", { ok: true });
});

intake.post("/api/contributions", async (c) => {
  const parsed = await readBody(c);
  if (!parsed) return c.json({ ok: false, error: "bad_request" }, 400);
  const { data, form } = parsed;
  const lang = LOCALES.has(String(data.lang)) ? String(data.lang) : "en";
  if (clean(data.website, 200)) return reply(c, form, lang, 422, "atlx-contribute", { ok: false, error: "rejected" });
  ensureStore();
  if (limited(`c:${clientIp(c)}`)) return reply(c, form, lang, 429, "atlx-contribute", { ok: false, error: "rate_limited" });
  const type = String(data.type);
  const name = clean(data.name, 160);
  const details = clean(data.details, 2000);
  const url = clean(data.url, 500);
  const location = clean(data.location, 160);
  const date = clean(data.date, 10);
  const contact = clean(data.contact, 254).toLowerCase();
  const consent = data.consent === "1" || data.consent === "on" || data.consent === true;
  const bad =
    !["business", "event", "port", "correction"].includes(type) ||
    name.length < 2 || details.length < 10 || !consent ||
    (url && !URL_RE.test(url)) || (date && !DATE_RE.test(date)) || (contact && !EMAIL.test(contact));
  if (bad) return reply(c, form, lang, 400, "atlx-contribute", { ok: false, error: "invalid" });
  const ok = store("contribution", { ...meta(c, "contribution", data), type, name, details, url: url || undefined, location: location || undefined, date: date || undefined, contact: contact || undefined });
  if (!ok) return reply(c, form, lang, 503, "atlx-contribute", { ok: false, error: "unavailable" });
  return reply(c, form, lang, 200, "atlx-contribute", { ok: true });
});

export default intake;
