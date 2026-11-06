/**
 * ArcticTradeLanes.com HOME EXTRAS (2026-10-18, owner order relayed by Chief of Staff).
 *
 * Additive, server-rendered sections appended BELOW the SPA mount (<div id="root"></div>) of the
 * homepage. The SPA (OpenLayers EPSG:3996 map, H1, JSON-LD, 6 ad slots, Yandex Autoplacement) is not
 * touched: React only owns #root, and this block lives after it with its own scoped CSS (#atl-x).
 *
 * Templates only: every visible string comes from home-extras.i18n.json (22 locales) or from the
 * neutral data file home-extras.data.json. No per-page prose. Kill switch: ATL_HOME_EXTRAS=0.
 */
import { readFileSync } from "node:fs";

type Dict = Record<string, string>;
type Tri = { en: string; ru?: string; zh?: string };
interface EventRow { start: string; end?: string; kind: "deadline" | "conference"; name: string; place: string; venue?: string; href: string }
interface Person { slug: string; panel: boolean; name: Tri; role: Tri; rel: Tri; related: [string, string | null][]; coords?: [number, number]; affiliation?: Tri; public_source?: string; source_url?: string; tier?: "HNWI" | "UHNWI" | "institution" }
interface Route { title: string; desc: string; href: string }
interface Data { um_banner: { href: string; copy: string }; fact_indexes: string[]; events: EventRow[]; people: Person[]; routes?: Route[] }

const I18N: Record<string, Dict> = JSON.parse(readFileSync(new URL("./home-extras.i18n.json", import.meta.url), "utf8"));
const DATA: Data = JSON.parse(readFileSync(new URL("./home-extras.data.json", import.meta.url), "utf8"));

export const HOME_LOCALES = ["en", "ru", "zh", "ja", "ko", "el", "de", "nl", "fr", "es", "it", "pt", "tr", "ar", "hi", "vi", "id", "da", "fi", "sv", "nb", "is"] as const;
const LOCALE_NAMES: Dict = { en: "English", ru: "Русский", zh: "中文", ja: "日本語", ko: "한국어", el: "Ελληνικά", de: "Deutsch", nl: "Nederlands", fr: "Français", es: "Español", it: "Italiano", pt: "Português", tr: "Türkçe", ar: "العربية", hi: "हिन्दी", vi: "Tiếng Việt", id: "Bahasa Indonesia", da: "Dansk", fi: "Suomi", sv: "Svenska", nb: "Norsk bokmål", is: "Íslenska" };
const ORIGIN = "https://arctictradelanes.com";
const UM_LANGS = new Set(["ru", "zh"]); // UM radar person pages verified live for these prefixes

const esc = (s: string) => String(s ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

/** Live atlas feature counts from atlas.manifest.json (read once, cached at module load). */
let _atlasCounts: string | null = null;
function atlasCountsLine(): string {
  if (_atlasCounts) return _atlasCounts;
  try {
    const mf = JSON.parse(readFileSync(new URL("../../atlas.manifest.json", import.meta.url), "utf8"));
    const lc = mf.layer_counts || {};
    const parts = [lc.ports, lc.lanes, lc.programs, lc.shipyards, lc.industry, lc.cities, lc.icebreakers, lc.tankers].filter(
      (n: unknown) => typeof n === "number" && Number.isFinite(n)
    );
    _atlasCounts = parts.length === 8 ? parts.join(" · ") : "155 · 27 · 713 · 69 · 109 · 103 · 55 · 51";
  } catch { _atlasCounts = "155 · 27 · 713 · 69 · 109 · 103 · 55 · 51"; }
  return _atlasCounts;
}


/**
 * Stylized polar "latitude pin" for a person card: a small circular badge with the
 * person's initials, ringed like a polar coordinate marker. Contains NO photo and
 * NO financial claim — initials + public role only.
 */
function polarPin(name: string): string {
  const parts = String(name || "").replace(/[^\p{L} ]+/gu, " ").trim().split(/\s+/).filter(Boolean);
  const initials = (parts[0]?.[0] || "A") + (parts[parts.length - 1]?.[0] || "");
  return `<span class="x-polar-pin" aria-hidden="true">${esc(initials.toUpperCase())}</span>`;
}

const tri = (v: Tri, lang: string) => (lang === "ru" && v.ru) || (lang === "zh" && v.zh) || v.en;
export const umRadarUrl = (slug: string, lang: string) => `https://unicornsmap.com/${UM_LANGS.has(lang) ? lang + "/" : ""}radar/${slug}`;
const pre = (lang: string) => (lang === "en" ? "" : `/${lang}`);

// ATLAS_COUNTS_CACHE: layer counts are read once from the live atlas manifest and memoized.
let _atlasCountsCache: Record<string, number> | null = null;
function atlasCounts(): Record<string, number> {
  if (_atlasCountsCache) return _atlasCountsCache;
  try {
    const mf = JSON.parse(readFileSync(new URL("../../atlas.manifest.json", import.meta.url), "utf8"));
    const lc = mf.layer_counts || {};
    _atlasCountsCache = { ports: lc.ports, lanes: lc.lanes, programs: lc.programs, shipyards: lc.shipyards, industry: lc.industry, cities: lc.cities, icebreakers: lc.icebreakers, tankers: lc.tankers };
  } catch { _atlasCountsCache = { ports: 155, lanes: 27, programs: 713, shipyards: 69, industry: 109, cities: 103, icebreakers: 55, tankers: 51 }; }
  return _atlasCountsCache;
}
function rankRows(lang: string): [string, string][] {
  const d = t(lang);
  return [
    [d.rank_ports, "ports"], [d.rank_lanes, "lanes"], [d.rank_progs, "programs"],
    [d.rank_ships, "shipyards"], [d.rank_ind, "industry"], [d.rank_cities, "cities"],
    [d.rank_ice, "icebreakers"], [d.rank_tank, "tankers"], [d.rank_air, "airports"],
    [d.rank_rail, "rail"], [d.rank_rescue, "rescue"],
  ];
}
function rankTable(lang: string): string {
  const c = atlasCounts();
  return `<div class="x-grid x-rank">` + rankRows(lang).map(([label, key]) =>
    `<div class="x-card x-rank-card"><h3>${typeof c[key as keyof typeof c] === "number" ? c[key as keyof typeof c] : "—"}</h3><p>${esc(label)}</p></div>`).join("") + `</div>`;
}
function fmtDate(iso: string, lang: string): string {
  try {
    return new Intl.DateTimeFormat(lang === "nb" ? "nb-NO" : lang, { day: "numeric", month: "short", year: "numeric", timeZone: "UTC" }).format(new Date(`${iso}T00:00:00Z`));
  } catch { return iso; }
}

/**
 * The money surface link.
 *
 * /x402/pay had no inbound link anywhere on the site, so the pay sheet was
 * reachable only if you already knew the URL. The band below is generated from
 * the same 22-locale pack the pay sheet renders from (public/x402/i18n/<lang>.json),
 * so it is localized by construction — no new copy, no English on a Japanese page.
 */
const PAY_PACKS = new Map<string, Dict | null>();
function payPack(lang: string): Dict | null {
  if (PAY_PACKS.has(lang)) return PAY_PACKS.get(lang) ?? null;
  let pack: Dict | null = null;
  try {
    const raw = readFileSync(new URL(`../../public/x402/i18n/${lang}.json`, import.meta.url), "utf8");
    const parsed = JSON.parse(raw);
    if (parsed && typeof parsed === "object") pack = parsed as Dict;
  } catch { pack = null; }
  PAY_PACKS.set(lang, pack);
  return pack;
}

function payBand(lang: string): string {
  const pack = payPack(lang) ?? payPack("en");
  if (!pack) return "";
  const label = String(pack.h1 || "Pay 5.00 USDC via x402");
  const amount = String(pack.settle_amount_value || "5.00 USDC");
  const net = String(pack.settle_network_value || "Base · chainId 8453");
  return `<div class="x-pay"><div class="x-wrap">
<a class="x-pay-cta" href="${pre(lang)}/x402/pay" data-atlx-pay><strong>${esc(label)}</strong></a>
<span class="x-pay-meta"><span class="x-pay-amt"><bdi dir="ltr">${esc(amount)}</bdi></span><span class="x-pay-net">${esc(net)}</span></span>
<a class="x-pay-alt" href="https://bankr.bot?ref=um-radar" rel="noopener" target="_blank">Bankr →</a>
</div></div>`;
}

const CSS = `#atl-x{--x-bg:#0b1220;--x-card:#111a2b;--x-line:#1f2d44;--x-ink:#e5edf7;--x-mute:#9fb0c6;--x-acc:#22d3ee;--x-acc2:#f59e0b;background:var(--x-bg);color:var(--x-ink);font:15px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,"Noto Sans",sans-serif;padding:0 0 88px;position:relative;overflow-x:hidden;border-top:1px solid var(--x-line)}
#atl-x *{box-sizing:border-box}#atl-x a{color:var(--x-acc);text-decoration:none}#atl-x a:hover{text-decoration:underline}
#atl-x .x-wrap{max-width:1180px;margin:0 auto;padding:0 16px}
#atl-x .x-pay{background:linear-gradient(90deg,#0e2233,#0b1220 70%);border-bottom:1px solid var(--x-line)}
#atl-x .x-pay .x-wrap{display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;padding:12px 16px}
#atl-x .x-pay-cta{display:inline-flex;gap:8px;align-items:center;background:linear-gradient(90deg,#22d3ee,#0ea5b7);color:#04121b!important;text-decoration:none!important;border-radius:10px;padding:10px 16px;font-size:1rem;font-weight:700;box-shadow:0 6px 18px rgba(34,211,238,.18)}
#atl-x .x-pay-meta{display:inline-flex;flex-wrap:wrap;gap:10px;align-items:center;color:var(--x-mute);font-size:.85rem}
#atl-x .x-pay-amt{background:#0f2236;border:1px solid var(--x-line);border-radius:999px;padding:3px 10px;font-weight:600;color:var(--x-acc)}
#atl-x .x-pay-net{opacity:.85}
#atl-x .x-pay-alt{border:1px solid var(--x-line);border-radius:8px;padding:8px 14px;font-size:.88rem;font-weight:600}
#atl-x .x-nav{position:sticky;top:0;z-index:20;background:rgba(11,18,32,.94);backdrop-filter:blur(6px);border-bottom:1px solid var(--x-line)}
#atl-x .x-nav ul{list-style:none;margin:0 auto;padding:10px 16px;display:flex;gap:8px;overflow-x:auto;max-width:1180px;scrollbar-width:none}
#atl-x .x-nav li{flex:0 0 auto}#atl-x .x-nav a{display:inline-block;padding:6px 12px;border:1px solid var(--x-line);border-radius:999px;color:var(--x-ink);font-size:13px;white-space:nowrap}
#atl-x .x-nav a:hover{border-color:var(--x-acc);text-decoration:none}
#atl-x section{padding:44px 0 8px;scroll-margin-top:64px}
#atl-x .x-kick{display:inline-block;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--x-acc);margin:0 0 6px}
#atl-x h2{font-size:clamp(22px,3.2vw,32px);line-height:1.2;margin:0 0 10px;color:#fff}
#atl-x h3{font-size:17px;margin:0 0 6px;color:#fff}
#atl-x .x-lede{color:var(--x-mute);max-width:820px;margin:0 0 20px}
#atl-x .x-grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr))}
#atl-x .x-card{background:var(--x-card);border:1px solid var(--x-line);border-radius:14px;padding:16px;min-width:0;overflow-wrap:anywhere}
#atl-x .x-card p{margin:0;color:var(--x-mute);font-size:14px}
#atl-x .x-road{list-style:none;padding:0;margin:18px 0 0;display:grid;gap:8px}
#atl-x .x-road li{padding:10px 14px;border-inline-start:3px solid var(--x-acc);background:var(--x-card);border-radius:8px;color:var(--x-ink)}
#atl-x .x-chips{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 0}
#atl-x .x-chips a{padding:6px 12px;border-radius:999px;background:#0f2236;border:1px solid var(--x-line);font-size:13px}
#atl-x .x-badge{display:inline-block;font-size:12px;font-weight:700;padding:3px 10px;border-radius:999px;background:#3b2a07;color:#fcd34d;border:1px solid #6b4e0f;margin:0 0 8px}
#atl-x form{display:grid;gap:10px;margin:0}
#atl-x label{display:grid;gap:4px;font-size:13px;color:var(--x-mute)}
#atl-x input,#atl-x select,#atl-x textarea{width:100%;max-width:100%;padding:10px 12px;border-radius:10px;border:1px solid var(--x-line);background:#0a1626;color:var(--x-ink);font:inherit}
#atl-x textarea{min-height:96px;resize:vertical}
#atl-x .x-row{display:grid;gap:10px;grid-template-columns:repeat(auto-fit,minmax(min(100%,220px),1fr))}
#atl-x .x-check{display:flex;gap:8px;align-items:flex-start;grid-template-columns:none}#atl-x .x-check input{width:auto;margin-top:4px}
#atl-x .x-or{align-self:center;justify-self:center;color:var(--x-mute);font-size:13px}
#atl-x button{justify-self:start;padding:10px 18px;border-radius:10px;border:0;background:var(--x-acc);color:#04202a;font-weight:700;font:inherit;font-weight:700;cursor:pointer}
#atl-x .x-hp{position:absolute!important;width:1px!important;height:1px!important;padding:0!important;margin:-1px!important;overflow:hidden!important;clip:rect(0,0,0,0)!important;clip-path:inset(50%)!important;white-space:nowrap!important;border:0!important}
#atl-x .x-msg{min-height:1.4em;font-size:14px;color:#86efac}
#atl-x .x-disc{margin-top:14px;padding:14px;border-radius:12px;background:#1a1408;border:1px solid #4a3a12;color:#f5deb3;font-size:13px}
#atl-x .x-disc strong{display:block;color:#fcd34d;margin-bottom:4px}
#atl-x .x-um{display:block;margin:36px 0 0;padding:18px 20px;border-radius:14px;background:linear-gradient(135deg,#1e1b4b,#0b2a3a);border:1px solid #3730a3;color:#e0e7ff;font-weight:600}
#atl-x .x-um:hover{text-decoration:none;border-color:#818cf8}
#atl-x .x-ev{list-style:none;margin:0;padding:0;display:grid;gap:10px}
#atl-x .x-ev li{display:grid;grid-template-columns:minmax(0,150px) minmax(0,1fr);gap:12px;align-items:start;background:var(--x-card);border:1px solid var(--x-line);border-radius:12px;padding:12px 14px}
#atl-x .x-ev time{color:var(--x-acc2);font-weight:700;font-size:14px}
#atl-x .x-ev .x-place{color:var(--x-mute);font-size:13px}
#atl-x .x-tag{display:inline-block;font-size:11px;padding:1px 8px;border-radius:999px;border:1px solid var(--x-line);color:var(--x-mute);margin-inline-start:6px}
#atl-x .x-sub{margin:22px 0 10px;font-size:14px;text-transform:uppercase;letter-spacing:.05em;color:var(--x-mute)}
#atl-x .x-ppl .x-card h3{margin-bottom:2px}#atl-x .x-ppl .x-role{color:var(--x-ink);font-size:14px;margin:0 0 6px}
#atl-x .x-cta{display:flex;flex-wrap:wrap;gap:10px}
#atl-x .x-cta a{padding:11px 18px;border-radius:10px;background:#0f2236;border:1px solid var(--x-acc);color:#e0f7fb;font-weight:600}
#atl-x .x-langs{display:flex;flex-wrap:wrap;gap:6px;font-size:12px}#atl-x .x-langs a{padding:3px 8px;border:1px solid var(--x-line);border-radius:6px;color:var(--x-mute)}
#atl-x .x-adwrap{margin:30px 0 0}
#atl-x .atlx-ad:not([data-atl-rendered]),#atl-x .atlx-net:empty{height:0;min-height:0;margin:0;padding:0;border:0;overflow:hidden}
#atl-x .atlx-ad:not([data-atl-rendered]) .atl-ad-label{display:none}
#atl-x .x-small{font-size:12px;color:var(--x-mute);margin:8px 0 0}
@media (max-width:640px){#atl-x section{padding-top:34px}#atl-x .x-ev li{grid-template-columns:1fr;gap:4px}}#atl-x a:focus-visible,#atl-x button:focus-visible{outline:2px solid var(--x-acc);outline-offset:2px}#atl-x .x-cta a,#atl-x .x-nav a{min-height:44px;display:inline-flex;align-items:center}#atl-x .x-nav{scroll-margin-top:0}@media print{#atl-x .x-nav,#atl-x .x-pay,.x-adwrap{display:none!important}#atl-x{padding-bottom:0}}#atl-x .x-pc-head{display:flex;gap:10px;align-items:flex-start;margin-bottom:4px}#atl-x .x-polar-pin{flex:0 0 auto;width:36px;height:36px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;background:radial-gradient(circle at 35% 30%,#164e63,#0b1220 70%);border:2px solid var(--x-acc);color:#e0f7fb;font-weight:800;font-size:13px;letter-spacing:.02em}#atl-x .x-pc-head h3{margin:0}#atl-x .x-tier{margin:6px 0 0}#atl-x .x-pin-hnwi{display:inline-block;font-size:11px;font-weight:700;padding:2px 8px;border-radius:999px;background:#3b2a07;color:#fcd34d;border:1px solid #6b4e0f}#atl-x .x-coords{margin:4px 0 0}#atl-x .x-coord{font-size:11px;color:var(--x-mute);letter-spacing:.04em}#atl-x .x-aff{font-size:13px;color:var(--x-ink);margin:4px 0 0}`;

function t(lang: string): Dict { return { ...I18N.en, ...(I18N[lang] || {}) }; }

/** Yandex RTB slot, same markup pattern as the SPA slots (atl-ads.js scans [data-yandex-rtb-slot]). */
function adSlot(id: string): string {
  return `<div class="x-adwrap"><aside id="${id}" data-yandex-rtb-slot="${id}" data-atl-ad="${id.replace(/^atl-ad-/, "")}" aria-label="Advertisement" class="atl-ad atlx-ad"><span class="atl-ad-label" aria-hidden="true">Advertisement</span><div id="yandex_rtb_${id}" class="atl-ad-body"></div></aside></div>`;
}
/** Generic ad-network unit container: stays collapsed (:empty) until a network script fills it. */
const netUnit = (id: string) => `<div class="atlx-net" id="${id}" data-atl-net-unit="${id}" aria-label="Advertisement"></div>`;

function eventsLd(lang: string, now: number): object[] {
  return DATA.events
    .filter((e) => e.kind === "conference" && Date.parse(`${e.end || e.start}T23:59:59Z`) >= now)
    .map((e) => ({
      "@type": "Event",
      name: e.name,
      startDate: e.start,
      endDate: e.end || e.start,
      eventStatus: "https://schema.org/EventScheduled",
      eventAttendanceMode: "https://schema.org/OfflineEventAttendanceMode",
      location: { "@type": "Place", name: e.venue || e.place, address: e.place },
      url: e.href.startsWith("http") ? e.href : `${ORIGIN}${pre(lang)}${e.href}`,
    }));
}

/** Build the whole extras block for one locale. Pure function of (lang, now). */
export function homeExtrasHtml(lang: string, now = Date.now()): string {
  const L = (HOME_LOCALES as readonly string[]).includes(lang) ? lang : "en";
  const s = t(L);
  const p = pre(L);
  const rtl = L === "ar";
  const msgAttrs = `data-ok="${esc(s.msg_ok)}" data-err="${esc(s.msg_err)}" data-rate="${esc(s.msg_rate)}"`;

  const nav = [["atlx-star", s.nav_star], ["atlx-routes", s.nav_routes], ["atlx-corridor", s.nav_corridor], ["atlx-audiences", s.nav_audiences], ["atlx-vessels", s.nav_vessels], ["atlx-atlas", s.nav_atlas], ["atlx-funding", s.nav_funding], ["atlx-token", s.nav_token], ["atlx-events", s.nav_events], ["atlx-people", s.nav_people], ["atlx-contribute", s.nav_contrib], ["atlx-support", s.nav_support]]
    .map(([id, label]) => `<li><a href="#${id}">${esc(label)}</a></li>`).join("");

  const facts = DATA.fact_indexes.map((k) => `<a href="${p}/${k}">${esc(s[`fx_${k}`] || k)}</a>`).join("");

  const star = `<section id="atlx-star" aria-labelledby="atlx-star-h"><div class="x-wrap">
<p class="x-kick">${esc(s.star_kicker)}</p><h2 id="atlx-star-h">${esc(s.star_h)}</h2><p class="x-lede">${esc(s.star_lede)}</p>
<div class="x-grid">${[1, 2, 3, 4].map((i) => `<div class="x-card"><h3>${esc(s[`star_c${i}_h`])}</h3><p>${esc(s[`star_c${i}_p`])}</p></div>`).join("")}</div>
<h3 class="x-sub">${esc(s.road_h)}</h3><ol class="x-road">${[1, 2, 3, 4].map((i) => `<li>${esc(s[`road_${i}`])}</li>`).join("")}</ol>
<h3 class="x-sub">${esc(s.explore_h)}</h3><nav class="x-chips" aria-label="${esc(s.explore_h)}">${facts}</nav>
</div></section>`;

  const token = `<section id="atlx-token" aria-labelledby="atlx-token-h"><div class="x-wrap">
<span class="x-badge">${esc(s.tok_badge)}</span><h2 id="atlx-token-h">${esc(s.tok_h)}</h2><p class="x-lede">${esc(s.tok_lede)}</p>
<div class="x-grid">${[1, 2, 3, 4].map((i) => `<div class="x-card"><h3>${esc(s[`tok_c${i}_h`])}</h3><p>${esc(s[`tok_c${i}_p`])}</p></div>`).join("")}</div>
<div class="x-card" style="margin-top:14px"><h3>${esc(s.tok_form_h)}</h3>
<form method="post" action="/api/atl-interest" data-atlx="interest" ${msgAttrs} novalidate>
<input type="hidden" name="lang" value="${L}">
<div class="x-row"><label>${esc(s.f_email)}<input type="email" name="email" maxlength="254" autocomplete="email"></label>
<label>${esc(s.f_wallet)}<input type="text" name="wallet" maxlength="128" autocomplete="off" spellcheck="false" dir="ltr"></label></div>
<label>${esc(s.f_role)}<select name="role"><option value="supporter">${esc(s.role_sup)}</option><option value="builder">${esc(s.role_build)}</option><option value="media">${esc(s.role_media)}</option><option value="business">${esc(s.role_biz)}</option></select></label>
<label class="x-hp" aria-hidden="true">Website<input type="text" name="website" tabindex="-1" autocomplete="off"></label>
<label class="x-check"><input type="checkbox" name="consent" value="1" required><span>${esc(s.f_consent_tok)}</span></label>
<button type="submit">${esc(s.f_submit_tok)}</button><p class="x-msg" role="status" aria-live="polite"></p>
<p class="x-small">${esc(s.privacy)}</p></form></div>
<div class="x-disc" role="note"><strong>${esc(s.disc_h)}</strong>${esc(s.disc_p)}</div>
<a class="x-um" href="${esc(DATA.um_banner.href)}" rel="noopener" target="_blank" data-atl-crossbanner="unicornsmap">${esc(DATA.um_banner.copy)} →</a>
</div></section>`;


  // Corridor intelligence (sourced NSR 2026 estimates + layer counts)
  const corridor = `<section id="atlx-corridor" aria-labelledby="atlx-corridor-h"><div class="x-wrap">
<p class="x-kick">${esc(s.nav_corridor)}</p><h2 id="atlx-corridor-h">${esc(s.cor_h)}</h2><p class="x-lede">${esc(s.cor_lede)}</p>
<div class="x-grid">
<div class="x-card"><h3>104</h3><p>${esc(s.cor_voyages)} · 30 Sep 2026 (CHNL)</p></div>
<div class="x-card"><h3>3.7 Mt</h3><p>${esc(s.cor_cargo)}</p></div>
<div class="x-card"><h3>7.8M DWT</h3><p>${esc(s.cor_dwt)}</p></div>
<div class="x-card"><h3>~150</h3><p>${esc(s.cor_proj)}</p></div>
</div>
<div class="x-cta" style="margin-top:14px"><a href="${p}/opportunity">${esc(s.cor_cta1)} →</a><a href="${p}/arctic-economic-atlas">${esc(s.cor_cta2)} →</a><a href="${p}/china-polar-silk-road">${esc(s.cor_cta3)} →</a></div>
<p class="x-small">${esc(s.cor_note)} ${esc(s.cor_src)}</p>
</div></section>`;

  const audiences = `<section id="atlx-audiences" aria-labelledby="atlx-audiences-h"><div class="x-wrap">
<p class="x-kick">${esc(s.nav_audiences)}</p><h2 id="atlx-audiences-h">${esc(s.aud_h)}</h2><p class="x-lede">${esc(s.aud_lede)}</p>
<div class="x-grid">
<div class="x-card"><h3>${esc(s.aud_b_h)}</h3><p>${esc(s.aud_b_p)}</p><p class="x-small"><a href="${p}/companies">${esc(s.aud_cta_companies)} →</a></p></div>
<div class="x-card"><h3>${esc(s.aud_e_h)}</h3><p>${esc(s.aud_e_p)}</p><p class="x-small"><a href="${p}/pricing">${esc(s.aud_cta_funding)} →</a></p></div>
<div class="x-card"><h3>${esc(s.aud_g_h)}</h3><p>${esc(s.aud_g_p)}</p><p class="x-small"><a href="${p}/funding">${esc(s.aud_cta_funding)} →</a></p></div>
<div class="x-card"><h3>${esc(s.aud_hnwi_h)}</h3><p>${esc(s.aud_hnwi_p)}</p><p class="x-small"><a href="${p}/people">${esc(s.aud_cta_people)} →</a> · <a href="${p}/collaborate">${esc(s.aud_cta_collab)} →</a></p></div>
</div></div></section>`;

  const routes = `<section id="atlx-routes" aria-labelledby="atlx-routes-h"><div class="x-wrap">
<p class="x-kick">${esc(s.nav_routes)}</p><h2 id="atlx-routes-h">${esc(s.routes_h)}</h2><p class="x-lede">${esc(s.routes_lede)}</p>
<div class="x-grid">${[1,2,3,4,5,6].map((i) => `<div class="x-card"><h3>${esc(s[`route${i}_h`])}</h3><p>${esc(s[`route${i}_p`])}</p></div>`).join("")}</div>
<div class="x-cta" style="margin-top:12px"><a href="${p}/arctic-economic-atlas">${esc(s.routes_cta)} →</a><a href="${p}/companies">${esc(s.routes_cta)} →</a><a href="${p}/programs">${esc(s.routes_cta)} →</a></div>
<p class="x-small">${esc(s.routes_total)}</p>
</div></section>`;

  const rank = `<section id="atlx-rank" aria-labelledby="atlx-rank-h"><div class="x-wrap">
<p class="x-kick">${esc(s.nav_atlas)}</p><h2 id="atlx-rank-h">${esc(s.rank_h)}</h2><p class="x-lede">${esc(s.rank_lede)}</p>
${rankTable(L)}
<div class="x-cta" style="margin-top:12px"><a href="/atlas/atlas.geojson">${esc(s.rank_cta)} →</a><a href="/atlas/atlas.manifest.json">${esc(s.rank_cta2)} →</a></div>
<p class="x-small">${esc(s.rank_note)}</p>
</div></section>`;

  const yacht = `<section id="atlx-yacht" aria-labelledby="atlx-yacht-h"><div class="x-wrap">
<p class="x-kick">Polar yacht dossier</p><h2 id="atlx-yacht-h">${esc(s.yacht_h)}</h2><p class="x-lede">${esc(s.yacht_lede)}</p>
<div class="x-grid">
<div class="x-card"><h3>${esc(s.yacht_y1_h)}</h3><p>${esc(s.yacht_y1_p)}</p></div>
<div class="x-card"><h3>${esc(s.yacht_y2_h)}</h3><p>${esc(s.yacht_y2_p)}</p></div>
<div class="x-card"><h3>${esc(s.yacht_y3_h)}</h3><p>${esc(s.yacht_y3_p)}</p></div>
</div>
<p class="x-small">${esc(s.yacht_src)}</p>
<div class="x-disc" role="note">${esc(s.yacht_disclaimer)}</div>
</div></section>`;

  const vessels = `<section id="atlx-vessels" aria-labelledby="atlx-vessels-h"><div class="x-wrap">
<p class="x-kick">${esc(s.nav_vessels)}</p><h2 id="atlx-vessels-h">${esc(s.ves_h)}</h2><p class="x-lede">${esc(s.ves_lede)}</p>
<div class="x-grid">
<div class="x-card"><h3>${esc(s.ves_c1_h)}</h3><p>${esc(s.ves_c1_p)}</p></div>
<div class="x-card"><h3>${esc(s.ves_c2_h)}</h3><p>${esc(s.ves_c2_p)}</p></div>
<div class="x-card"><h3>${esc(s.ves_c3_h)}</h3><p>${esc(s.ves_c3_p)}</p></div>
</div>
<div class="x-cta" style="margin-top:14px"><a href="${p}/icebreakers">${esc(s.ves_cta_ice)} →</a><a href="${p}/tankers">${esc(s.ves_cta_tank)} →</a></div>
<p class="x-small">${esc(s.ves_src)}</p>
</div></section>`;

  const atlasCounts = atlasCountsLine();
  const atlasSec = `<section id="atlx-atlas" aria-labelledby="atlx-atlas-h"><div class="x-wrap">
<p class="x-kick">${esc(s.nav_atlas)}</p><h2 id="atlx-atlas-h">${esc(s.atl_h)}</h2><p class="x-lede">${esc(s.atl_lede)}</p>
<div class="x-card"><h3>${esc(s.atl_counts)}</h3><p dir="ltr"><strong>${esc(atlasCounts)}</strong> ${esc(s.atl_total)}</p>
<p class="x-small">${esc(s.atl_ports)} · ${esc(s.atl_lanes)} · ${esc(s.atl_progs)} · ${esc(s.atl_ships)} · ${esc(s.atl_ind)} · ${esc(s.atl_cities)} · ${esc(s.atl_ice)} · ${esc(s.atl_tank)}</p>
<div class="x-cta" style="margin-top:10px"><a href="/atlas/atlas.geojson">${esc(s.atl_cta_geo)} →</a><a href="/atlas/atlas.manifest.json">${esc(s.atl_cta_manifest)} →</a><a href="https://github.com/International-Arctic/ArcticTradeLanes-Dataset" rel="noopener" target="_blank">${esc(s.atl_cta_gh)} →</a></div></div>
<p class="x-small">${esc(s.atl_src)}</p>
</div></section>`;

  const fundingSec = `<section id="atlx-funding" aria-labelledby="atlx-funding-h"><div class="x-wrap">
<p class="x-kick">${esc(s.nav_funding)}</p><h2 id="atlx-funding-h">${esc(s.fund_h)}</h2><p class="x-lede">${esc(s.fund_lede)}</p>
<div class="x-grid">
<div class="x-card"><h3>${esc(s.fund_c1_h)}</h3><p>${esc(s.fund_c1_p)}</p></div>
<div class="x-card"><h3>${esc(s.fund_c2_h)}</h3><p>${esc(s.fund_c2_p)}</p></div>
<div class="x-card"><h3>${esc(s.fund_c3_h)}</h3><p>${esc(s.fund_c3_p)}</p></div>
</div>
<div class="x-cta" style="margin-top:14px"><a href="${p}/pricing">${esc(s.fund_cta_pricing)} →</a><a href="https://github.com/International-Arctic/Arctic-Trade-Lanes" rel="noopener" target="_blank">${esc(s.fund_cta_github)} →</a><a href="${p}/#atlx-token">${esc(s.fund_cta_token)} →</a></div>
</div></section>`;


  const evRow = (e: EventRow) => {
    const d = `<time datetime="${e.start}">${esc(fmtDate(e.start, L))}${e.end ? ` – ${esc(fmtDate(e.end, L))}` : ""}</time>`;
    const href = e.href.startsWith("http") ? e.href : `${p}${e.href}`;
    const ext = e.href.startsWith("http") ? ` rel="noopener" target="_blank"` : "";
    const tag = e.kind === "deadline" ? `<span class="x-tag">${esc(s.ev_deadline)}</span>` : "";
    return `<li>${d}<div><a href="${esc(href)}"${ext}>${esc(e.name)}</a>${tag}<div class="x-place">${esc(e.venue ? `${e.venue}, ${e.place}` : e.place)}</div></div></li>`;
  };
  const isUp = (e: EventRow) => Date.parse(`${e.end || e.start}T23:59:59Z`) >= now;
  const up = DATA.events.filter(isUp).sort((a, b) => a.start.localeCompare(b.start));
  const past = DATA.events.filter((e) => !isUp(e)).sort((a, b) => b.start.localeCompare(a.start));
  const events = `<section id="atlx-events" aria-labelledby="atlx-events-h"><div class="x-wrap">
<h2 id="atlx-events-h">${esc(s.ev_h)}</h2><p class="x-lede">${esc(s.ev_lede)}</p>
<h3 class="x-sub">${esc(s.ev_up)}</h3><ul class="x-ev">${up.map(evRow).join("")}</ul>
${past.length ? `<h3 class="x-sub">${esc(s.ev_past)}</h3><ul class="x-ev">${past.map(evRow).join("")}</ul>` : ""}
<p class="x-small"><a href="${p}/funding">${esc(s.ev_more)} →</a></p>
</div></section>`;

  // Neutral people section: name, public role, Arctic relevance, radar + ATL profile links. No CTA/ads/token here.
  const people = `<section id="atlx-people" class="x-ppl" aria-labelledby="atlx-people-h"><div class="x-wrap">
<h2 id="atlx-people-h">${esc(s.ppl_h)}</h2><p class="x-lede">${esc(s.ppl_lede)}</p><p class="x-small">Map pins now use polar-ring initials, with a named source on every tier tag. No portrait imagery, no net-worth figures, no invented wealth.</p>
<div class="x-grid">${DATA.people.map((x) => { const badge = x.tier === "UHNWI" ? `<span class="x-pin-hnwi">${esc(s.ppl_pin_hnwi)}</span>` : x.tier === "HNWI" ? `<span class="x-pin-hnwi">${esc(s.ppl_pin_uh)}</span>` : ""; const coord = x.coords ? `<span class="x-coord">${x.coords[0].toFixed(4)}° / ${x.coords[1].toFixed(4)}°</span>` : ""; const aff = x.affiliation ? `<p class="x-aff">${esc(tri(x.affiliation, L))}</p>` : ""; const src = x.source_url ? `<a href="${esc(x.source_url)}" rel="noopener" target="_blank">${esc(s.ppl_src)}</a>` : ""; return `<div class="x-card"><div class="x-pc-head">${polarPin(tri(x.name, L))}<div><h3><a href="${p}/people/${x.slug}">${esc(tri(x.name, L))}</a></h3><p class="x-role">${esc(tri(x.role, L))}</p></div></div>${badge ? `<p class="x-tier">${badge}</p>` : ""}${coord ? `<p class="x-coords">${coord}</p>` : ""}${aff}<p>${esc(tri(x.rel, L))}</p><p class="x-small">${src ? `${src} · ` : ""}<a href="${umRadarUrl(x.slug, L)}" rel="noopener" target="_blank">${esc(s.ppl_radar)} ↗</a></p></div>`; }).join("")}</div>
<p class="x-small"><a href="${p}/people">${esc(s.pp_back)} →</a></p>
</div></section>`;
  const contribute = `<section id="atlx-contribute" aria-labelledby="atlx-contribute-h"><div class="x-wrap">
<h2 id="atlx-contribute-h">${esc(s.con_h)}</h2><p class="x-lede">${esc(s.con_lede)}</p>
<div class="x-card"><form method="post" action="/api/contributions" data-atlx="contribution" ${msgAttrs} novalidate>
<input type="hidden" name="lang" value="${L}">
<div class="x-row"><label>${esc(s.f_type)}<select name="type"><option value="business">${esc(s.type_business)}</option><option value="event">${esc(s.type_event)}</option><option value="port">${esc(s.type_port)}</option><option value="correction">${esc(s.type_correction)}</option></select></label>
<label>${esc(s.f_name)}<input type="text" name="name" maxlength="160" required></label></div>
<div class="x-row"><label>${esc(s.f_url)}<input type="url" name="url" maxlength="500" dir="ltr" placeholder="https://"></label>
<label>${esc(s.f_loc)}<input type="text" name="location" maxlength="160"></label>
<label>${esc(s.f_date)}<input type="date" name="date"></label></div>
<label>${esc(s.f_details)}<textarea name="details" maxlength="2000" required></textarea></label>
<label>${esc(s.f_contact)}<input type="email" name="contact" maxlength="254" autocomplete="email"></label>
<label class="x-hp" aria-hidden="true">Website<input type="text" name="website" tabindex="-1" autocomplete="off"></label>
<label class="x-check"><input type="checkbox" name="consent" value="1" required><span>${esc(s.f_consent_con)}</span></label>
<button type="submit">${esc(s.f_submit_con)}</button><p class="x-msg" role="status" aria-live="polite"></p>
<p class="x-small">${esc(s.privacy)}</p></form></div>
</div></section>`;

  const support = `<section id="atlx-support" aria-labelledby="atlx-support-h"><div class="x-wrap">
<h2 id="atlx-support-h">${esc(s.sup_h)}</h2><p class="x-lede">${esc(s.sup_lede)}</p>
<div class="x-cta"><a href="${p}/funding">${esc(s.sup_fund)}</a><a href="${p}/advertise">${esc(s.sup_adv)}</a><a href="#atlx-token">${esc(s.sup_tok)}</a></div>
</div></section>`;

  const langs = `<section id="atlx-langs" aria-labelledby="atlx-langs-h"><div class="x-wrap"><h2 id="atlx-langs-h" style="font-size:16px">${esc(s.lang_h)}</h2>
<nav class="x-langs" aria-label="${esc(s.lang_h)}">${HOME_LOCALES.map((l) => `<a href="${l === "en" ? "/" : `/${l}`}" hreflang="${l}" lang="${l}">${esc(LOCALE_NAMES[l])}</a>`).join("")}</nav></div></section>`;

  const ld = {
    "@context": "https://schema.org",
    "@graph": [
      { "@type": "ItemList", "@id": `${ORIGIN}${p || ""}/#atlx-events`, name: s.ev_h, itemListElement: eventsLd(L, now).map((item, i) => ({ "@type": "ListItem", position: i + 1, item })) },
      { "@type": "FAQPage", "@id": `${ORIGIN}${p || ""}/#atlx-token`, inLanguage: L, mainEntity: [{ "@type": "Question", name: s.faq_q, acceptedAnswer: { "@type": "Answer", text: s.disc_p } }] },
    ],
  };

  const js = `(function(){var r=document.getElementById('atl-x');if(!r||!window.fetch)return;r.querySelectorAll('form[data-atlx]').forEach(function(F){F.addEventListener('submit',function(e){e.preventDefault();var o={};new FormData(F).forEach(function(v,k){o[k]=v});var m=F.querySelector('.x-msg'),b=F.querySelector('button');m.textContent='…';b.disabled=true;fetch(F.action,{method:'POST',headers:{'content-type':'application/json','accept':'application/json'},body:JSON.stringify(o)}).then(function(x){m.textContent=x.status===200?F.getAttribute('data-ok'):(x.status===429?F.getAttribute('data-rate'):F.getAttribute('data-err'));if(x.status===200)F.reset();}).catch(function(){m.textContent=F.getAttribute('data-err')}).then(function(){b.disabled=false})})})})();`;

  return `<!-- ATL-HOME-EXTRAS 2026-10-18 -->
<style id="atlx-css">${CSS}</style>
<div id="atl-x" lang="${L}" dir="${rtl ? "rtl" : "ltr"}" data-atlx-locale="${L}">
<nav class="x-nav" aria-label="${esc(s.nav_label)}"><ul>${nav}</ul></nav>
${payBand(L)}
${star}
${routes}
${corridor}
${audiences}
${rank}
${yacht}
${vessels}
${atlasSec}
${fundingSec}
<div class="x-wrap">${adSlot("atl-ad-home-inc-3")}</div>
${token}
${events}
${people}
${contribute}
<div class="x-wrap">${adSlot("atl-ad-home-inc-4")}${netUnit("atl-net-home-1")}</div>
${support}
<div class="x-wrap">${adSlot("atl-ad-home-inc-5")}${netUnit("atl-net-home-2")}</div>
${langs}
<script type="application/ld+json" id="atlx-ld">${JSON.stringify(ld).replace(/</g, "\\u003c")}</script>
<script>${js}</script>
</div>
<!-- /ATL-HOME-EXTRAS -->`;
}

/** Insert the extras right after the SPA mount; falls back to before </body>. Never throws. */
export function injectHomeExtras(html: string, lang: string): string {
  if (html.includes("ATL-HOME-EXTRAS")) return html;
  const block = homeExtrasHtml(lang);
  const mount = '<div id="root"></div>';
  if (html.includes(mount)) return html.replace(mount, `${mount}\n${block}`);
  return html.includes("</body>") ? html.replace("</body>", `${block}\n</body>`) : html + block;
}
