/**
 * GET /api/atl-fx (2026-10-18): dated public reference rates for the homepage currency switcher.
 * ECB euro foreign exchange reference rates (daily XML) + Bank of Russia daily XML for RUB and AED,
 * which the ECB does not publish. Fetched server-side, cached in memory and on disk for 6 h, every
 * source dated. No invented values: a currency without a published rate is simply absent.
 */
import { Hono } from "hono";
import { existsSync, readFileSync, writeFileSync, renameSync } from "node:fs";

const ECB_URL = "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml";
const CBR_URL = "https://www.cbr.ru/scripts/XML_daily.asp";
const CACHE_FILE = process.env.ATL_FX_CACHE || "/tmp/atl-fx-cache.json";
const TTL = 6 * 3600 * 1000;

interface Fx { base: "EUR"; rates: Record<string, number>; sources: Record<string, { name: string; url: string; date: string; currencies?: string[] }>; fetched_at: string }
let mem: { at: number; data: Fx } | null = null;
let inflight: Promise<Fx | null> | null = null;

async function get(url: string): Promise<string | null> {
  try {
    const r = await fetch(url, { signal: AbortSignal.timeout(6000), headers: { "User-Agent": "ArcticTradeLanes-fx/1.0 (+https://arctictradelanes.com)" } });
    if (!r.ok) return null;
    return new TextDecoder("latin1").decode(await r.arrayBuffer());
  } catch { return null; }
}

async function build(): Promise<Fx | null> {
  const [ecb, cbr] = await Promise.all([get(ECB_URL), get(CBR_URL)]);
  if (!ecb) return null;
  const date = /time=['"](\d{4}-\d{2}-\d{2})['"]/.exec(ecb)?.[1];
  if (!date) return null;
  const rates: Record<string, number> = {};
  for (const m of ecb.matchAll(/currency=['"]([A-Z]{3})['"]\s+rate=['"]([\d.]+)['"]/g)) rates[m[1]] = Number(m[2]);
  const fx: Fx = { base: "EUR", rates, sources: { ECB: { name: "European Central Bank euro reference rates", url: ECB_URL, date } }, fetched_at: new Date().toISOString() };
  if (cbr) {
    const d = /ValCurs[^>]*Date="(\d{2})\.(\d{2})\.(\d{4})"/.exec(cbr);
    const val = (code: string) => {
      const m = new RegExp(`<CharCode>${code}</CharCode>\\s*<Nominal>(\\d+)</Nominal>[\\s\\S]*?<Value>([\\d,]+)</Value>`).exec(cbr);
      return m ? Number(m[2].replace(",", ".")) / Number(m[1]) : null;
    };
    const eurRub = val("EUR");
    const aedRub = val("AED");
    if (d && eurRub) {
      rates.RUB = Number(eurRub.toFixed(4));
      const cur = ["RUB"];
      if (aedRub) { rates.AED = Number((eurRub / aedRub).toFixed(4)); cur.push("AED"); }
      fx.sources.CBR = { name: "Bank of Russia official rates", url: CBR_URL, date: `${d[3]}-${d[2]}-${d[1]}`, currencies: cur };
    }
  }
  return fx;
}

export async function loadFx(): Promise<Fx | null> {
  const now = Date.now();
  if (mem && now - mem.at < TTL) return mem.data;
  try {
    if (existsSync(CACHE_FILE)) {
      const disk = JSON.parse(readFileSync(CACHE_FILE, "utf8"));
      if (disk?.at && now - disk.at < TTL && disk.data?.rates) { mem = disk; return disk.data; }
    }
  } catch { /* ignore */ }
  inflight ??= build().finally(() => { inflight = null; });
  const data = await inflight;
  if (data) {
    mem = { at: now, data };
    try { const tmp = `${CACHE_FILE}.${process.pid}`; writeFileSync(tmp, JSON.stringify(mem)); renameSync(tmp, CACHE_FILE); } catch { /* ignore */ }
    return data;
  }
  return mem?.data ?? null;
}

const v2Routes = new Hono();
v2Routes.get("/api/atl-fx", async (c) => {
  const fx = await loadFx();
  if (!fx) return c.json({ error: "reference rates unavailable" }, 503, { "Cache-Control": "no-store" });
  return c.json(fx, 200, { "Cache-Control": "public, max-age=1800, s-maxage=3600, stale-while-revalidate=3600" });
});
export default v2Routes;
