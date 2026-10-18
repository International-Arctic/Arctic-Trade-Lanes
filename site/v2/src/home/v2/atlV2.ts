/**
 * ATL v2 additive layer (2026-10-18): hero band, flag strip, logo wall and 2026–2036 sprint story
 * injected into the home-extras block (BELOW the SPA map, never over it); country hubs, the open
 * companies registry pages, per-language sitemaps + a sitemap index, an /advertise section and
 * config-driven search verification meta. Templates only; data from data/arctic-brands (Wikidata +
 * ATL atlas), src/home/v2/hubs.json (atlas) and public/atl-hero/credits.json. Kill switch: ATL_V2=0.
 */
import { existsSync, readFileSync } from "node:fs";

type Dict = Record<string, string>;
const ROOT = new URL("../../../", import.meta.url);
const rd = (rel: string) => readFileSync(new URL(rel, ROOT), "utf8");
const I18N: Record<string, Dict> = JSON.parse(readFileSync(new URL("./v2.i18n.json", import.meta.url), "utf8"));
const HUBDATA: { order: string[]; hubs: Record<string, Hub> } = JSON.parse(readFileSync(new URL("./hubs.json", import.meta.url), "utf8"));

export const V2_LOCALES = ["en", "ru", "zh", "ja", "ko", "el", "de", "nl", "fr", "es", "it", "pt", "tr", "ar", "hi", "vi", "id", "da", "fi", "sv", "nb", "is"];
const LC = V2_LOCALES.filter((l) => l !== "en").join("|");
const RTL = new Set(["ar"]);
const SITE = "https://arctictradelanes.com";
const GH = "https://github.com/International-Arctic/Arctic-Trade-Lanes/blob/main";
const BUILD_DATE = "2026-10-18";

interface Item { n: string; h: string }
interface Hub { iso: string; group: "council" | "observer" | "partner"; currency: string; layers: Record<string, Item[]>; programs: Item[]; brands: string[]; brand_count: number }
interface Fact { kind: string; value: string; fact: string; source_url: string; date: string; qid?: string; qids?: string[]; href?: string }
interface Brand { id: string; slug: string; name: string; names: Dict; logo_url: string; logo_license: string; logo_source: string; country: string; sector: string; hq_lat: number | null; hq_lon: number | null; arctic_geo_lat: number | null; arctic_geo_lon: number | null; website: string; facts: Fact[]; currency: string; source: string; wikidata: string; sitelinks: number }
interface Credit { file: string; theme: string; title: string; source: string; author: string; license: string; license_url: string }

let BRANDS: Brand[] | null = null;
let BY_SLUG: Map<string, Brand> | null = null;
let LABELS: Record<string, Dict> = {};
function brands(): Brand[] {
  if (BRANDS) return BRANDS;
  try {
    BRANDS = JSON.parse(rd("data/arctic-brands/brands.json")) as Brand[];
    LABELS = JSON.parse(rd("data/arctic-brands/labels.json"));
  } catch (err) {
    console.error(`[atl-v2] brands load failed: ${err instanceof Error ? err.message : String(err)}`);
    BRANDS = [];
  }
  BY_SLUG = new Map(BRANDS.map((b) => [b.slug, b]));
  return BRANDS;
}
let CREDITS: Credit[] | null = null;
function credits(): Credit[] {
  if (CREDITS) return CREDITS;
  try { CREDITS = JSON.parse(rd("public/atl-hero/credits.json")); } catch { CREDITS = []; }
  return CREDITS!;
}
let VERIFY: Dict | null = null;
function verifyMeta(): string {
  if (!VERIFY) { try { VERIFY = JSON.parse(rd("config/atl-site-verification.json")); } catch { VERIFY = {}; } }
  const names: Dict = { google: "google-site-verification", yandex: "yandex-verification", bing: "msvalidate.01", baidu: "baidu-site-verification", naver: "naver-site-verification" };
  let out = "";
  for (const [k, n] of Object.entries(names)) {
    const v = String(VERIFY![k] || "").trim();
    if (v && /^[A-Za-z0-9_\-.:=]{4,200}$/.test(v)) out += `<meta name="${n}" content="${esc(v)}">\n`;
  }
  return out;
}

const esc = (s: unknown) => String(s ?? "").replace(/[&<>"']/g, (ch) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[ch]!));
const pre = (lang: string) => (lang === "en" ? "" : `/${lang}`);
const tr = (lang: string): Dict => ({ ...I18N.en, ...(I18N[lang] || {}) });
const fill = (s: string, v: Dict) => s.replace(/\{(\w+)\}/g, (_, k) => (k in v ? v[k] : `{${k}}`));
const flag = (iso: string) => iso.toUpperCase().replace(/./g, (ch) => String.fromCodePoint(127397 + ch.charCodeAt(0)));
const dnCache = new Map<string, Intl.DisplayNames | null>();
function dn(lang: string, type: "region" | "currency"): Intl.DisplayNames | null {
  const k = `${lang}:${type}`;
  if (!dnCache.has(k)) { try { dnCache.set(k, new Intl.DisplayNames([lang === "nb" ? "nb" : lang, "en"], { type })); } catch { dnCache.set(k, null); } }
  return dnCache.get(k)!;
}
export const countryName = (iso: string, lang: string) => dn(lang, "region")?.of(iso.toUpperCase()) || iso.toUpperCase();
const currencyName = (code: string, lang: string) => dn(lang, "currency")?.of(code) || code;
const brandName = (b: Brand, lang: string) => b.names?.[lang] || b.name;
const qlabel = (q: string, lang: string) => LABELS[q]?.[lang] || LABELS[q]?.en || "";
const ALIAS: Dict = { FO: "dk", SJ: "no" };
const hubOf = (iso2: string) => ALIAS[iso2] || iso2.toLowerCase();

function hreflangs(path: string): string {
  const rest = path === "/" ? "" : path;
  let s = V2_LOCALES.map((l) => `<link rel="alternate" hreflang="${l}" href="${SITE}${pre(l)}${rest || (l === "en" ? "/" : "")}">`).join("\n");
  s += `\n<link rel="alternate" hreflang="x-default" href="${SITE}${rest || "/"}">`;
  return s;
}

/* ---------------------------------------------------------------- shared CSS */
const PAGE_CSS = `:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#0b1220;color:#e5edf7;font:15px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,"Noto Sans",sans-serif}
a{color:#22d3ee;text-decoration:none}a:hover{text-decoration:underline}.w{max-width:1180px;margin:0 auto;padding:0 16px}
header.v2h{border-bottom:1px solid #1f2d44;background:#0d1626}header.v2h .w{display:flex;gap:16px;align-items:center;justify-content:space-between;padding:12px 16px;flex-wrap:wrap}
header.v2h b{font-size:16px}nav.bc{font-size:13px;color:#9fb0c6;margin:14px 0}h1{font-size:clamp(24px,4vw,34px);line-height:1.2;margin:8px 0 6px}
h2{font-size:19px;margin:28px 0 10px;border-bottom:1px solid #1f2d44;padding-bottom:6px}.mute{color:#9fb0c6}.card{background:#111a2b;border:1px solid #1f2d44;border-radius:12px;padding:14px 16px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:6px 18px;padding:0;margin:0;list-style:none}.grid li{overflow-wrap:anywhere}
dl.kv{display:grid;grid-template-columns:max-content 1fr;gap:6px 16px;margin:0}dl.kv dt{color:#9fb0c6}dl.kv dd{margin:0;overflow-wrap:anywhere}
.pill{display:inline-block;border:1px solid #1f2d44;border-radius:999px;padding:2px 10px;font-size:13px;margin:2px 4px 2px 0}
.v2flags{display:flex;flex-wrap:wrap;gap:6px;padding:0;margin:0;list-style:none}.v2flags a{display:inline-flex;gap:6px;align-items:center;border:1px solid #1f2d44;border-radius:999px;padding:4px 10px;font-size:13px;color:#e5edf7;white-space:nowrap}
.v2flags a[aria-current]{border-color:#22d3ee}.fl{font-size:18px;line-height:1}.wm{display:inline-flex;align-items:center;justify-content:center;min-width:120px;height:48px;padding:0 12px;border:1px solid #1f2d44;border-radius:8px;font-weight:700;letter-spacing:.02em;color:#e5edf7;background:#0f1a2c}
.logo{max-width:200px;max-height:80px;background:#fff;border-radius:8px;padding:8px}footer.v2f{border-top:1px solid #1f2d44;margin-top:40px;padding:20px 0 40px;font-size:13px;color:#9fb0c6}
.facts li{margin:4px 0}.src{font-size:12px;color:#9fb0c6}[dir=rtl] dl.kv{direction:rtl}`;

function flagStrip(lang: string, current = ""): string {
  const t = tr(lang);
  const li = (iso: string) => `<li><a href="${pre(lang)}/country/${iso}" hreflang="${lang}"${iso === current ? ' aria-current="page"' : ""}><span class="fl" aria-hidden="true">${flag(iso === "gl" ? "gl" : iso)}</span><span>${esc(countryName(iso, lang))}</span></a></li>`;
  const council = HUBDATA.order.filter((i) => HUBDATA.hubs[i].group === "council");
  const rest = HUBDATA.order.filter((i) => HUBDATA.hubs[i].group !== "council");
  return `<div class="v2fl"><p class="v2flt">${esc(t.flags_council)}</p><ul class="v2flags">${council.map(li).join("")}</ul>
<p class="v2flt">${esc(t.flags_observers)}</p><ul class="v2flags">${rest.map(li).join("")}</ul></div>`;
}

function shell(lang: string, o: { title: string; desc: string; path: string; body: string; ld: unknown[]; noindex?: boolean }): string {
  const t = tr(lang);
  const dir = RTL.has(lang) ? "rtl" : "ltr";
  const canonical = `${SITE}${pre(lang)}${o.path}`;
  return `<!doctype html><html lang="${lang}" dir="${dir}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(o.title)}</title><meta name="description" content="${esc(o.desc)}">
${o.noindex ? '<meta name="robots" content="noindex,follow">' : '<meta name="robots" content="index,follow,max-image-preview:large">'}
<link rel="canonical" href="${canonical}">
${hreflangs(o.path)}
<meta property="og:type" content="website"><meta property="og:site_name" content="Arctic Trade Lanes"><meta property="og:title" content="${esc(o.title)}"><meta property="og:description" content="${esc(o.desc)}"><meta property="og:url" content="${canonical}"><meta property="og:image" content="${SITE}/atl-hero/shipping.webp">
${verifyMeta()}<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<style>${PAGE_CSS}</style>
<script type="application/ld+json">${JSON.stringify(o.ld.length === 1 ? o.ld[0] : { "@context": "https://schema.org", "@graph": o.ld }).replace(/</g, "\\u003c")}</script>
</head><body>
<header class="v2h"><div class="w"><a href="${pre(lang) || "/"}"><b>Arctic Trade Lanes</b></a><span><a href="${pre(lang)}/companies">${esc(t.co_index_title)}</a> · <a href="${pre(lang)}/funding">${esc(t.hub_funding_all)}</a></span></div></header>
<main class="w">${o.body}</main>
<footer class="v2f"><div class="w"><p>${esc(t.flags_title)}</p>${flagStrip(lang)}<p style="margin-top:16px">${esc(t.co_note)} <a href="${GH}/data/arctic-brands/README.md" rel="noopener">GitHub</a></p></div></footer>
</body></html>`;
}

/* ---------------------------------------------------------------- country hub */
const LAYER_ORDER = ["ports", "shipyards", "icebreakers", "tankers", "industry", "cities", "airports", "rail", "rescue"];
function hubWeight(h: Hub): number {
  return Object.values(h.layers).reduce((a, v) => a + v.length, 0) + h.programs.length + h.brand_count;
}
function renderHub(lang: string, iso: string): string | null {
  const h = HUBDATA.hubs[iso];
  if (!h) return null;
  brands();
  const t = tr(lang);
  const cn = countryName(iso, lang);
  const p = pre(lang);
  const groupLabel = h.group === "council" ? t.hub_member : h.group === "observer" ? t.hub_observer : t.hub_partner;
  const list = (items: Item[], cap: number) => {
    const shown = items.slice(0, cap).map((i) => `<li><a href="${p}${i.h}">${esc(i.n)}</a></li>`).join("");
    const more = items.length > cap ? `<li class="mute">${esc(fill(t.hub_more, { n: String(items.length - cap) }))}</li>` : "";
    return `<ul class="grid">${shown}${more}</ul>`;
  };
  let body = `<nav class="bc"><a href="${p || "/"}">${esc(t.nav_home)}</a> › <a href="${p}/country/${iso}">${esc(cn)}</a></nav>
<h1><span aria-hidden="true">${flag(iso)}</span> ${esc(fill(t.hub_title, { country: cn }))}</h1>
<p class="mute">${esc(groupLabel)}</p>
<div class="card"><dl class="kv"><dt>${esc(t.hub_currency)}</dt><dd><b>${esc(h.currency)}</b> · ${esc(currencyName(h.currency, lang))}</dd>
<dt>${esc(t.hub_ports)}</dt><dd>${(h.layers.ports || []).length}</dd><dt>${esc(t.hub_brands)}</dt><dd>${h.brand_count}</dd><dt>${esc(t.hub_programs)}</dt><dd>${h.programs.length}</dd></dl></div>`;
  body += `<h2>${esc(t.hub_ports)}</h2>${(h.layers.ports || []).length ? list(h.layers.ports, 200) : `<p class="mute">${esc(t.hub_none)}</p>`}`;
  const ent = LAYER_ORDER.filter((l) => l !== "ports" && (h.layers[l] || []).length);
  body += `<h2>${esc(t.hub_entities)}</h2>`;
  body += ent.length ? ent.map((l) => `<h3 style="font-size:15px;margin:14px 0 6px">${esc(t["ly_" + l] || l)} <span class="mute">(${h.layers[l].length})</span></h3>${list(h.layers[l], 24)}`).join("") : `<p class="mute">${esc(t.hub_none)}</p>`;
  const bl = h.brands.map((s) => BY_SLUG!.get(s)).filter(Boolean) as Brand[];
  body += `<h2>${esc(t.hub_brands)} <span class="mute">(${h.brand_count})</span></h2>`;
  body += bl.length ? `<ul class="grid">${bl.map((b) => `<li><a href="${p}/company/${b.slug}">${esc(brandName(b, lang))}</a> <span class="mute">· ${esc(t["se_" + b.sector] || "")}</span></li>`).join("")}</ul>${h.brand_count > bl.length ? `<p><a href="${p}/companies#c-${iso}">${esc(t.co_back)} →</a></p>` : ""}` : `<p class="mute">${esc(t.hub_none)}</p>`;
  body += `<h2>${esc(t.hub_programs)} <span class="mute">(${h.programs.length})</span></h2>`;
  body += h.programs.length ? list(h.programs, 60) : `<p class="mute">${esc(t.hub_none)}</p>`;
  body += `<p><a href="${p}/funding">${esc(t.hub_funding_all)} →</a> · <a href="${p || "/"}">${esc(t.hub_map)} →</a></p>`;
  const ld = [
    { "@context": "https://schema.org", "@type": "Country", name: cn, identifier: iso.toUpperCase(), url: `${SITE}${p}/country/${iso}`, containsPlace: (h.layers.ports || []).slice(0, 25).map((i) => ({ "@type": "Place", name: i.n, url: `${SITE}${p}${i.h}` })) },
    { "@context": "https://schema.org", "@type": "BreadcrumbList", itemListElement: [{ "@type": "ListItem", position: 1, name: "Arctic Trade Lanes", item: `${SITE}${p || "/"}` }, { "@type": "ListItem", position: 2, name: cn, item: `${SITE}${p}/country/${iso}` }] },
  ];
  return shell(lang, { title: `${fill(t.hub_title, { country: cn })} | Arctic Trade Lanes`, desc: fill(t.hub_desc, { country: cn }), path: `/country/${iso}`, body, ld, noindex: hubWeight(h) < 3 });
}

/* ---------------------------------------------------------------- companies */
function renderCompanies(lang: string): string {
  const all = brands();
  const t = tr(lang);
  const p = pre(lang);
  const groups = new Map<string, Brand[]>();
  for (const b of all) { const k = hubOf(b.country); if (!groups.has(k)) groups.set(k, []); groups.get(k)!.push(b); }
  const order = [...HUBDATA.order.filter((i) => groups.has(i)), ...[...groups.keys()].filter((k) => !HUBDATA.hubs[k])];
  let body = `<nav class="bc"><a href="${p || "/"}">${esc(t.nav_home)}</a> › ${esc(t.co_index_title)}</nav>
<h1>${esc(t.co_index_title)}</h1><p class="mute">${esc(fill(t.co_index_desc, { n: String(all.length) }))}</p>
<p>${esc(t.co_contrib)} <a href="${p}/#atlx-contribute">→</a> · <a href="${GH}/data/arctic-brands/CONTRIBUTING.md" rel="noopener">GitHub</a> · <a href="${GH}/data/arctic-brands/brands.csv" rel="noopener">CSV</a> · <a href="${GH}/data/arctic-brands/brands.json" rel="noopener">JSON</a></p>
<p>${order.map((k) => `<a class="pill" href="#c-${k}">${HUBDATA.hubs[k] ? flag(k) + " " : ""}${esc(countryName(k, lang))} (${groups.get(k)!.length})</a>`).join("")}</p>`;
  for (const k of order) {
    const list = groups.get(k)!.slice().sort((a, b) => brandName(a, lang).localeCompare(brandName(b, lang), lang));
    body += `<h2 id="c-${k}">${HUBDATA.hubs[k] ? `<a href="${p}/country/${k}">${flag(k)} ${esc(countryName(k, lang))}</a>` : esc(countryName(k, lang))} <span class="mute">(${list.length})</span></h2><ul class="grid">${list.map((b) => `<li><a href="${p}/company/${b.slug}">${esc(brandName(b, lang))}</a></li>`).join("")}</ul>`;
  }
  const ld = [{
    "@context": "https://schema.org", "@type": "Dataset", name: "ATL arctic-brands registry", description: fill(I18N.en.co_index_desc, { n: String(all.length) }),
    url: `${SITE}${p}/companies`, license: "https://creativecommons.org/publicdomain/zero/1.0/", isAccessibleForFree: true, dateModified: BUILD_DATE,
    creator: { "@type": "Organization", name: "Arctic Trade Lanes", url: SITE }, isBasedOn: "https://www.wikidata.org/",
    spatialCoverage: { "@type": "Place", name: "Arctic and sub-Arctic (north of 60°N)" },
    distribution: [{ "@type": "DataDownload", encodingFormat: "text/csv", contentUrl: `${GH}/data/arctic-brands/brands.csv` }, { "@type": "DataDownload", encodingFormat: "application/json", contentUrl: `${GH}/data/arctic-brands/brands.json` }],
  }];
  return shell(lang, { title: `${t.co_index_title} | Arctic Trade Lanes`, desc: fill(t.co_index_desc, { n: String(all.length) }), path: "/companies", body, ld });
}

function renderCompany(lang: string, slug: string): string | null {
  brands();
  const b = BY_SLUG!.get(slug);
  if (!b) return null;
  const t = tr(lang);
  const p = pre(lang);
  const name = brandName(b, lang);
  const hub = hubOf(b.country);
  const cn = countryName(b.country, lang);
  const fv = (f: Fact) => {
    if (f.kind === "hq" && f.qid) return qlabel(f.qid, lang) || f.value;
    if ((f.kind === "industry" || f.kind === "exchange") && f.qids) return f.qids.map((q) => qlabel(q, lang)).filter(Boolean).join(", ") || f.value;
    return f.value;
  };
  const kindLabel: Dict = { founded: t.co_founded, hq: t.co_hq, industry: t.co_industry, exchange: t.co_exchange, operates: t.co_operates };
  const logo = b.logo_url
    ? `<p><img class="logo" src="${esc(b.logo_url)}" alt="${esc(name)} logo" loading="lazy" decoding="async" referrerpolicy="no-referrer"></p><p class="src">${esc(t.co_logo)}: ${esc(b.logo_license)} · <a href="${esc(b.logo_source)}" rel="noopener">Wikimedia Commons</a></p>`
    : `<p><span class="wm">${esc(name)}</span></p>`;
  const geo = b.arctic_geo_lat != null ? `${b.arctic_geo_lat.toFixed(3)}, ${b.arctic_geo_lon!.toFixed(3)}` : "";
  let body = `<nav class="bc"><a href="${p || "/"}">${esc(t.nav_home)}</a> › <a href="${p}/companies">${esc(t.co_index_title)}</a> › ${HUBDATA.hubs[hub] ? `<a href="${p}/country/${hub}">${esc(countryName(hub, lang))}</a> › ` : ""}${esc(name)}</nav>
<h1>${esc(name)}</h1>${logo}
<div class="card"><dl class="kv">
<dt>${esc(t.co_country)}</dt><dd>${HUBDATA.hubs[hub] ? `<a href="${p}/country/${hub}">${flag(b.country)} ${esc(cn)}</a>` : esc(cn)}</dd>
<dt>${esc(t.co_sector)}</dt><dd>${esc(t["se_" + b.sector] || t.se_other)}</dd>
<dt>${esc(t.co_currency)}</dt><dd><b>${esc(b.currency)}</b> · ${esc(currencyName(b.currency, lang))}</dd>
${geo ? `<dt>${esc(t.co_geo)}</dt><dd><bdi dir="ltr">${geo}</bdi></dd>` : ""}
${b.website ? `<dt>${esc(t.co_website)}</dt><dd><a href="${esc(b.website)}" rel="nofollow noopener" target="_blank"><bdi dir="ltr">${esc(b.website.replace(/^https?:\/\//, "").replace(/\/$/, ""))}</bdi></a></dd>` : ""}
</dl></div>
<h2>${esc(t.co_facts)}</h2><ul class="facts">${b.facts.map((f) => `<li><b>${esc(kindLabel[f.kind] || f.kind)}:</b> ${f.href ? `<a href="${p}${esc(f.href)}">${esc(fv(f))}</a>` : esc(fv(f))} <span class="src">— ${esc(t.co_source)}: <a href="${esc(f.source_url)}" rel="noopener">${esc(f.source_url.replace(/^https?:\/\//, ""))}</a>, ${esc(t.co_retrieved)} ${esc(f.date)}</span></li>`).join("")}</ul>
<p><a href="${p}/#atlx-contribute">${esc(t.co_correct)}</a> · <a href="${p}/companies">${esc(t.co_back)}</a>${HUBDATA.hubs[hub] ? ` · <a href="${p}/country/${hub}">${esc(t.co_hub)}</a>` : ""}</p>`;
  const org: Record<string, unknown> = { "@context": "https://schema.org", "@type": "Organization", name: b.name, url: `${SITE}${p}/company/${b.slug}`, address: { "@type": "PostalAddress", addressCountry: b.country } };
  if (b.website) org.sameAs = [b.website];
  if (b.wikidata) org.sameAs = [...((org.sameAs as string[]) || []), b.wikidata];
  if (b.logo_url) org.logo = b.logo_url;
  const founded = b.facts.find((f) => f.kind === "founded");
  if (founded) org.foundingDate = founded.value;
  if (b.arctic_geo_lat != null) org.location = { "@type": "Place", geo: { "@type": "GeoCoordinates", latitude: b.arctic_geo_lat, longitude: b.arctic_geo_lon } };
  return shell(lang, { title: `${fill(t.co_title, { name })} | Arctic Trade Lanes`, desc: fill(t.co_desc, { name, country: cn }), path: `/company/${b.slug}`, body, ld: [org] });
}

/* ---------------------------------------------------------------- sitemaps */
let FACT_SHARDS: string[] | null = null;
function factShards(): string[] {
  if (FACT_SHARDS) return FACT_SHARDS;
  try {
    const r = JSON.parse(rd("factpages/.routes.json"));
    const keys: string[] = Array.isArray(r) ? r : Array.isArray(r.routes) ? r.routes : Object.keys(r.routes || r);
    FACT_SHARDS = keys.filter((k) => /^\/sitemaps\/.+\.xml$/.test(k)).sort();
  } catch { FACT_SHARDS = []; }
  return FACT_SHARDS;
}
function sitemapLang(lang: string): string {
  const p = pre(lang);
  const urls: string[] = [];
  for (const iso of HUBDATA.order) if (hubWeight(HUBDATA.hubs[iso]) >= 3) urls.push(`${SITE}${p}/country/${iso}`);
  urls.push(`${SITE}${p}/companies`);
  for (const b of brands()) urls.push(`${SITE}${p}/company/${b.slug}`);
  return `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.map((u) => `<url><loc>${u}</loc><lastmod>${BUILD_DATE}</lastmod></url>`).join("\n")}\n</urlset>\n`;
}
function sitemapIndex(): string {
  const maps = ["/sitemap.xml", "/sitemap-people.xml", ...factShards(), ...V2_LOCALES.map((l) => `/sitemaps/atl-v2-${l}.xml`)];
  return `<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${maps.map((m) => `<sitemap><loc>${SITE}${m}</loc><lastmod>${BUILD_DATE}</lastmod></sitemap>`).join("\n")}\n</sitemapindex>\n`;
}

/* ---------------------------------------------------------------- router */
const RE_HUB = new RegExp(`^/(?:(${LC})/)?country/([a-z]{2})/?$`);
const RE_COS = new RegExp(`^/(?:(${LC})/)?companies/?$`);
const RE_CO = new RegExp(`^/(?:(${LC})/)?company/([a-z0-9-]+)/?$`);
const RE_SM = new RegExp(`^/sitemaps/atl-v2-(en|${LC})\\.xml$`);
const RE_HERO = /^\/atl-hero\/(atlas|shipping|aurora|business)\.webp$/;

export interface V2Hit { kind: "html" | "xml" | "webp" | "json"; key: string; body: () => string | Uint8Array | null }
export function v2Match(path: string): V2Hit | null {
  if (process.env.ATL_V2 === "0") return null;
  let m: RegExpExecArray | null;
  if ((m = RE_HUB.exec(path))) { const [, l, iso] = m; return { kind: "html", key: `v2:hub:${l || "en"}:${iso}`, body: () => renderHub(l || "en", iso) }; }
  if ((m = RE_COS.exec(path))) { const l = m[1] || "en"; return { kind: "html", key: `v2:cos:${l}`, body: () => renderCompanies(l) }; }
  if ((m = RE_CO.exec(path))) { const [, l, s] = m; return { kind: "html", key: `v2:co:${l || "en"}:${s}`, body: () => renderCompany(l || "en", s) }; }
  if ((m = RE_SM.exec(path))) { const l = m[1]; return { kind: "xml", key: `v2:sm:${l}`, body: () => sitemapLang(l) }; }
  if (path === "/sitemap-index.xml") return { kind: "xml", key: "v2:smi", body: () => sitemapIndex() };
  if ((m = RE_HERO.exec(path))) { const f = `public/atl-hero/${m[1]}.webp`; return { kind: "webp", key: `v2:hero:${m[1]}`, body: () => (existsSync(new URL(f, ROOT)) ? new Uint8Array(readFileSync(new URL(f, ROOT))) : null) }; }
  if (path === "/atl-hero/credits.json") return { kind: "json", key: "v2:credits", body: () => JSON.stringify(credits(), null, 1) };
  return null;
}

/* ---------------------------------------------------------------- homepage blocks */
const HOME_CSS = `#atl-x .v2-hero{position:relative;width:100%;aspect-ratio:1280/500;max-height:440px;overflow:hidden;background:#0b1220;contain:paint}
#atl-x .v2-hero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;animation:v2fade 40s linear infinite both}
#atl-x .v2-hero img:nth-child(1){opacity:1;animation-delay:0s}#atl-x .v2-hero img:nth-child(2){animation-delay:10s}#atl-x .v2-hero img:nth-child(3){animation-delay:20s}#atl-x .v2-hero img:nth-child(4){animation-delay:30s}
@keyframes v2fade{0%{opacity:0}3%{opacity:1}25%{opacity:1}28%{opacity:0}100%{opacity:0}}
#atl-x .v2-hero figcaption{position:absolute;inset:auto 0 0 0;padding:28px 16px 12px;background:linear-gradient(transparent,rgba(11,18,32,.92));font-weight:700;font-size:clamp(15px,2.4vw,22px)}
#atl-x .v2-hero figcaption span{display:block;max-width:1180px;margin:0 auto}
#atl-x .v2fl{padding:10px 0 4px}#atl-x .v2flt{margin:10px 0 6px;color:var(--x-mute);font-size:13px}#atl-x .v2flags{display:flex;flex-wrap:wrap;gap:6px;padding:0;margin:0;list-style:none}
#atl-x .v2flags a{display:inline-flex;gap:6px;align-items:center;border:1px solid var(--x-line);border-radius:999px;padding:4px 10px;font-size:13px;color:var(--x-ink);white-space:nowrap}#atl-x .fl{font-size:18px;line-height:1}
#atl-x .v2-logos{overflow:hidden;position:relative;margin:8px 0 4px;-webkit-mask:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent);mask:linear-gradient(90deg,transparent,#000 6%,#000 94%,transparent)}
#atl-x .v2-track{display:flex;gap:14px;width:max-content;animation:v2scroll 90s linear infinite;padding:6px 0}#atl-x .v2-logos:hover .v2-track{animation-play-state:paused}
@keyframes v2scroll{from{transform:translateX(0)}to{transform:translateX(-50%)}}
#atl-x .v2-lg{display:inline-flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;width:150px;height:84px;background:#f8fafc;border-radius:10px;padding:8px;color:#0b1220;text-decoration:none!important}
#atl-x .v2-lg img{max-width:128px;max-height:46px;width:auto;height:auto}#atl-x .v2-lg span{font-size:11px;line-height:1.2;text-align:center;color:#334155;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:134px}
#atl-x .v2-lg.wmo{background:#111a2b;border:1px solid var(--x-line)}#atl-x .v2-lg.wmo span{font-size:14px;font-weight:700;color:var(--x-ink);white-space:normal}
#atl-x .v2-sp{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:14px;margin-top:12px}#atl-x .v2-sp article{background:var(--x-card);border:1px solid var(--x-line);border-radius:12px;padding:14px 16px}
#atl-x .v2-sp h3{margin:0 0 6px;font-size:16px}#atl-x .v2-sp .n{color:var(--x-acc2);font-size:12px;font-weight:700;letter-spacing:.08em}#atl-x .v2-amt{list-style:none;padding:0;margin:8px 0 0}#atl-x .v2-amt li{margin:6px 0;font-size:14px}
#atl-x .v2-amt data{display:block;color:var(--x-acc);font-weight:600}#atl-x .v2-cur{display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin:10px 0}#atl-x .v2-cur select{background:#0f1a2c;color:var(--x-ink);border:1px solid var(--x-line);border-radius:8px;padding:6px 10px;font:inherit}
#atl-x .v2-fxnote{font-size:12px;color:var(--x-mute)}#atl-x .v2-cred{font-size:12px;color:var(--x-mute);margin-top:18px}#atl-x .v2-cred a{color:var(--x-mute);text-decoration:underline}
@media (prefers-reduced-motion:reduce){#atl-x .v2-hero img{animation:none}#atl-x .v2-hero img:not(:first-child){display:none}#atl-x .v2-track{animation:none}#atl-x .v2-logos{overflow-x:auto;-webkit-mask:none;mask:none}}`;

const SPRINT_AMOUNTS = [
  { name: "UArctic Entrepreneurship Fund", lo: 2000, hi: 5000, cur: "USD", src: "https://www.uarctic.org/activities/awards-grants/entrepreneurship-fund/apply-now/" },
  { name: "Business Finland Sprint Grant", lo: 75000, hi: 100000, cur: "EUR", src: "https://www.businessfinland.fi/en/services/funding/calls/2026/ongoing-sprint-grant-funding/" },
  { name: "Innovasjon Norge Startup Grant 2", lo: 0, hi: 1000000, cur: "NOK", upto: true, src: "https://www.innovasjonnorge.no/en/tjeneste/oppstartstilskudd-2" },
  { name: "Arctic Business Incubator", lo: 400000, hi: 400000, cur: "SEK", src: "https://abi.se/services/incubator/" },
];
const SW_CUR = ["EUR", "USD", "RUB", "NOK", "SEK", "DKK", "ISK", "CAD", "CNY", "JPY", "KRW", "INR", "GBP", "CHF", "PLN", "SGD", "AED", "TRY", "IDR"];
const DEF_CUR: Dict = { en: "USD", ru: "RUB", zh: "CNY", ja: "JPY", ko: "KRW", el: "EUR", de: "EUR", nl: "EUR", fr: "EUR", es: "EUR", it: "EUR", pt: "EUR", tr: "TRY", ar: "AED", hi: "INR", vi: "USD", id: "IDR", da: "DKK", fi: "EUR", sv: "SEK", nb: "NOK", is: "ISK" };

function heroBlock(lang: string): string {
  const t = tr(lang);
  const imgs = (["atlas", "shipping", "aurora", "business"] as const).map((k) => `<img src="/atl-hero/${k}.webp" width="1280" height="500" loading="lazy" decoding="async" alt="${esc(t["hero_alt_" + k])}">`).join("");
  return `<figure class="v2-hero" aria-label="${esc(t.hero_caption)}" style="margin:0">${imgs}<figcaption><span>${esc(t.hero_caption)}</span></figcaption></figure>
<div class="x-wrap"><nav aria-label="${esc(t.flags_title)}">${flagStrip(lang)}</nav></div>`;
}
function logoWall(lang: string): string {
  const t = tr(lang);
  const p = pre(lang);
  const pick = brands().filter((b) => b.country !== "RU" && b.source === "wikidata").slice(0, 160);
  const withLogo = pick.filter((b) => b.logo_url).slice(0, 30);
  const wordmarks = pick.filter((b) => !b.logo_url).slice(0, 10);
  const items = [...withLogo, ...wordmarks];
  if (!items.length) return "";
  const cell = (b: Brand, dup: boolean) => b.logo_url
    ? `<a class="v2-lg" href="${p}/company/${b.slug}"${dup ? ' tabindex="-1" aria-hidden="true"' : ""} title="${esc(brandName(b, lang))} · ${esc(t.co_logo)}: ${esc(b.logo_license)}, Wikimedia Commons"><img src="${esc(b.logo_url)}" alt="${dup ? "" : esc(brandName(b, lang))}" width="128" height="46" loading="lazy" decoding="async" referrerpolicy="no-referrer" onerror="this.remove()"><span>${esc(brandName(b, lang))}</span></a>`
    : `<a class="v2-lg wmo" href="${p}/company/${b.slug}"${dup ? ' tabindex="-1" aria-hidden="true"' : ""}><span>${esc(brandName(b, lang))}</span></a>`;
  return `<section id="atlx-logos"><div class="x-wrap"><h2>${esc(t.logos_title)}</h2><p class="x-lede" style="margin:0">${esc(t.logos_note)}</p></div>
<div class="v2-logos" dir="ltr"><div class="v2-track">${items.map((b) => cell(b, false)).join("")}${items.map((b) => cell(b, true)).join("")}</div></div>
<div class="x-wrap"><p><a href="${p}/companies">${esc(t.logos_all)} (${brands().length}) →</a></p></div></section>`;
}
function sprintBlock(lang: string): string {
  const t = tr(lang);
  const p = pre(lang);
  const def = DEF_CUR[lang] || "USD";
  const opts = SW_CUR.map((c) => `<option value="${c}"${c === def ? " selected" : ""}>${c} · ${esc(currencyName(c, lang))}</option>`).join("");
  const nf = (v: number, c: string) => { try { return new Intl.NumberFormat(lang, { style: "currency", currency: c, maximumFractionDigits: 0 }).format(v); } catch { return `${v} ${c}`; } };
  const amounts = SPRINT_AMOUNTS.map((a) => `<li><a href="${esc(a.src)}" rel="noopener">${esc(a.name)}</a>: <bdi>${a.upto ? "≤ " + nf(a.hi, a.cur) : a.lo === a.hi ? nf(a.hi, a.cur) : nf(a.lo, a.cur) + " – " + nf(a.hi, a.cur)}</bdi><data data-amt="${a.lo}|${a.hi}|${a.cur}|${a.upto ? 1 : ""}" value="${a.hi}"></data></li>`).join("");
  const card = (n: number, title: string, body: string) => `<article><div class="n">${String(n).padStart(2, "0")}</div><h3>${esc(title)}</h3>${body}</article>`;
  return `<section id="atlx-sprint" data-lang="${lang}" data-note="${esc(t.sp_fx_note)}" data-na="${esc(t.sp_fx_na)}"><div class="x-wrap">
<h2>${esc(t.sp_title)}</h2><p class="x-lede">${esc(t.sp_intro)}</p>
<div class="v2-cur"><label for="atlx-cur">${esc(t.sp_cur)}</label><select id="atlx-cur">${opts}</select><span class="v2-fxnote" aria-live="polite">${esc(t.sp_fx_loading)}</span></div>
<div class="v2-sp">
${card(1, t.sp_s1_t, `<p>${esc(t.sp_s1_b)}</p>`)}
${card(2, t.sp_s2_t, `<p>${esc(t.sp_s2_b)}</p>`)}
${card(3, t.sp_s3_t, `<p>${esc(t.sp_s3_b)}</p><ul class="v2-amt">${amounts}</ul><p class="v2-fxnote">${esc(t.sp_src)}: ${esc(t.sp_asof)} <a href="${p}/funding">/funding</a>, ${BUILD_DATE}</p><p><a href="${p}/funding">${esc(t.sp_s3_link)} →</a></p>`)}
${card(4, t.sp_s4_t, `<p>${esc(t.sp_s4_b)}</p><p><a href="${p}/companies">${esc(t.co_index_title)} →</a></p>`)}
${card(5, t.sp_s5_t, `<p>${esc(t.sp_s5_b)}</p><p><strong>${esc(t.sp_concept)}</strong></p><p><a href="${GH}/docs/atl-token-concept.md" rel="noopener">${esc(t.sp_s5_link)} →</a></p>`)}
${card(6, t.sp_s6_t, `<p>${esc(t.sp_s6_b)}</p><p><a href="${p || "/"}">${esc(t.hub_map)} →</a></p>`)}
</div></div></section>
<script>(function(){var s=document.getElementById("atlx-sprint");if(!s)return;var sel=s.querySelector("#atlx-cur"),note=s.querySelector(".v2-cur .v2-fxnote"),L=s.dataset.lang,fx=null,ld=0;
try{var sv=localStorage.getItem("atlx-cur");if(sv&&sel.querySelector('option[value="'+sv+'"]'))sel.value=sv}catch(e){}
function f(v,c){try{return new Intl.NumberFormat(L,{style:"currency",currency:c,maximumFractionDigits:0}).format(v)}catch(e){return Math.round(v)+" "+c}}
function cv(v,a,b){var r=fx.rates,x=a==="EUR"?1:r[a],y=b==="EUR"?1:r[b];return x&&y?v/x*y:null}
function paint(){if(!fx)return;var to=sel.value,miss=0,cbr=to==="RUB"||to==="AED";s.querySelectorAll("data[data-amt]").forEach(function(el){var q=el.dataset.amt.split("|"),lo=+q[0],hi=+q[1],c=q[2];if(c==="RUB"||c==="AED")cbr=1;var y=cv(hi,c,to),x=cv(lo,c,to);if(y==null){el.textContent="";miss=1;return}el.textContent=c===to?"":"≈ "+(q[3]?"≤ "+f(y,to):lo===hi?f(y,to):f(x,to)+" – "+f(y,to))});
var src="ECB",d=fx.sources.ECB.date;if(cbr&&fx.sources.CBR){src="ECB / CBR";d=d+" / "+fx.sources.CBR.date}note.textContent=miss?s.dataset.na:s.dataset.note.replace("{source}",src).replace("{date}",d)}
function load(){if(ld)return;ld=1;fetch("/api/atl-fx").then(function(r){return r.ok?r.json():null}).then(function(j){if(j&&j.rates){fx=j;paint()}else note.textContent=s.dataset.na}).catch(function(){note.textContent=s.dataset.na})}
sel.addEventListener("change",function(){try{localStorage.setItem("atlx-cur",sel.value)}catch(e){}paint()});
if("IntersectionObserver"in window){var io=new IntersectionObserver(function(e){if(e.some(function(x){return x.isIntersecting})){io.disconnect();load()}},{rootMargin:"400px"});io.observe(s)}else load()})();</script>`;
}
function netPlaceholders(): string {
  // Hidden containers for networks planned in docs/ad-network-plan.md. No IDs until accounts exist.
  const nets = ["adsense", "baidu-union", "yahoo-japan", "microsoft", "vk", "naver", "seznam"];
  return `<div class="atl-net-placeholders" hidden aria-hidden="true">${nets.map((n) => `<div data-atl-network="${n}" data-atl-slot=""></div>`).join("")}</div>`;
}
function creditLine(lang: string): string {
  const t = tr(lang);
  const c = credits();
  if (!c.length) return "";
  return `<div class="x-wrap"><p class="v2-cred">${esc(t.credits)}: ${c.map((x) => `<a href="${esc(x.source)}" rel="noopener">${esc(x.author || x.title)}</a> (${x.license_url ? `<a href="${esc(x.license_url)}" rel="noopener license">${esc(x.license)}</a>` : esc(x.license)})`).join(" · ")} · <a href="/atl-hero/credits.json">credits.json</a></p></div>`;
}

/** Adds v2 blocks to the home-extras HTML. Returns the input unchanged on any problem. */
export function v2HomeInject(html: string, lang: string): string {
  if (process.env.ATL_V2 === "0" || html.includes("ATL-V2-HOME")) return html;
  try {
    const L = V2_LOCALES.includes(lang) ? lang : "en";
    let out = html;
    const vm = verifyMeta();
    if (vm && !/name="(?:google-site-verification|yandex-verification|msvalidate\.01|baidu-site-verification|naver-site-verification)"/.test(out)) out = out.replace("</head>", `${vm}</head>`);
    const top = `<!-- ATL-V2-HOME 2026-10-18 --><style id="atlv2-css">${HOME_CSS}</style>${heroBlock(L)}${logoWall(L)}`;
    if (out.includes('<section id="atlx-star"')) out = out.replace('<section id="atlx-star"', `${top}<section id="atlx-star"`);
    if (out.includes('<section id="atlx-events"')) out = out.replace('<section id="atlx-events"', `${sprintBlock(L)}<section id="atlx-events"`);
    if (out.includes('<section id="atlx-support"')) out = out.replace('<section id="atlx-support"', `${netPlaceholders()}<section id="atlx-support"`);
    if (out.includes("<!-- /ATL-HOME-EXTRAS -->")) out = out.replace("<!-- /ATL-HOME-EXTRAS -->", `${creditLine(L)}<!-- /ATL-HOME-EXTRAS -->`);
    return out;
  } catch (err) {
    console.error(`[atl-v2] home inject: ${err instanceof Error ? err.message : String(err)}`);
    return html;
  }
}

/** /advertise: appends the cross-platform brand campaigns section. */
export function v2PageInject(html: string, lang: string, slug: string): string {
  if (process.env.ATL_V2 === "0" || slug !== "advertise" || html.includes("atlv2-adv")) return html;
  try {
    const t = tr(V2_LOCALES.includes(lang) ? lang : "en");
    const sec = `<section id="atlv2-adv" style="margin:28px 0;padding:16px 18px;border:1px solid #1f2d44;border-radius:12px"><h2>${esc(t.adv_title)}</h2><p>${esc(t.adv_b)}</p><p>${esc(t.adv_list)}</p><p><a href="${lang === "en" ? "" : "/" + lang}/collaborate">${esc(t.adv_cta)} →</a></p></section>`;
    return html.includes("</main>") ? html.replace("</main>", `${sec}</main>`) : html.replace("</body>", `${sec}</body>`);
  } catch { return html; }
}
