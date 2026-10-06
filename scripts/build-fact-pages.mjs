#!/usr/bin/env node
// ATL programmatic fact pages (spec §11). Templates only: zero per-page generated prose.
// No network calls. Reads the atlas GeoJSON + manifest, public/data/slugs.json and i18n/labels.{lang}.json,
// writes static HTML + sharded sitemaps into ./factpages (served by an additive route in server.ts).
// Usage: node scripts/build-fact-pages.mjs [--layers ports,programs] [--out factpages] [--no-validate]
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { lintText, lintFile, listFiles } from './lint-neutral.mjs';

const args = Object.fromEntries(process.argv.slice(2).map((a, i, all) => a.startsWith('--') ? [a.slice(2), (all[i + 1] && !all[i + 1].startsWith('--')) ? all[i + 1] : true] : null).filter(Boolean));
const ROOT = process.cwd();
const ORIGIN = 'https://arctictradelanes.com';
const ATLAS = path.resolve(ROOT, args.atlas || 'public/data/atlas.4326.geojson');
const MANIFEST = path.resolve(ROOT, args.manifest || 'public/data/atlas.manifest.json');
const SLUGS = path.resolve(ROOT, args.slugs || 'public/data/slugs.json');
const I18N = path.resolve(ROOT, args.i18n || 'i18n');
const OUT = path.resolve(ROOT, args.out || 'factpages');
const LANGS = ['en','ru','zh','ja','ko','el','de','nl','fr','es','it','pt','tr','ar','hi','vi','id','da','fi','sv','nb','is'];
const HREFLANG = { zh: 'zh-CN', nb: 'no' };           // match the live sitemap.xml codes
const INTL = { zh: 'zh-CN', nb: 'nb' };
const RTL = new Set(['ar']);
const hl = (l) => HREFLANG[l] || l;
const ALL_LAYERS = ['ports','programs','cities','shipyards','industry','airports','rail','lanes','tankers','icebreakers','rescue'];
const LAYERS = String(args.layers || process.env.ATL_FACT_LAYERS || ALL_LAYERS.join(',')).split(',').map((s) => s.trim()).filter((l) => ALL_LAYERS.includes(l));
// Skip the (slow) rebuild when nothing that feeds the pages changed; --force rebuilds anyway.
const INPUT_HASH = (() => {
  const h = crypto.createHash('sha256');
  const files = [ATLAS, MANIFEST, new URL(import.meta.url).pathname, path.join(path.dirname(new URL(import.meta.url).pathname), 'lint-neutral.mjs'), path.join(path.dirname(new URL(import.meta.url).pathname), 'neutral-terms.sha256.json')];
  if (fs.existsSync(I18N)) for (const f of fs.readdirSync(I18N).sort()) if (f.endsWith('.json')) files.push(path.join(I18N, f));
  for (const f of files) { h.update(f.split('/').pop() + '\0'); if (fs.existsSync(f)) h.update(fs.readFileSync(f)); }
  h.update(LAYERS.join(','));
  return h.digest('hex');
})();
if (!args.force && fs.existsSync(path.join(OUT, '.inputs.sha256')) && fs.readFileSync(path.join(OUT, '.inputs.sha256'), 'utf8').trim() === INPUT_HASH) {
  console.log(`[fact-pages] inputs unchanged (${INPUT_HASH.slice(0, 12)}); keeping ${path.relative(ROOT, OUT)} (use --force to rebuild)`);
  process.exit(0);
}
const PREFIX = { ports:'port', programs:'program', cities:'city', shipyards:'shipyard', industry:'industry', airports:'airport', rail:'rail', lanes:'lane', tankers:'vessel', icebreakers:'vessel', rescue:'rescue' };
const INDEX = { ports:'ports', programs:'programs', cities:'cities', shipyards:'shipyards', industry:'industry', airports:'airports', rail:'rail', lanes:'lanes', tankers:'tankers', icebreakers:'icebreakers', rescue:'rescue' };
const PROJ = ['programs','industry','airports','rail','rescue'];
// structured facts per layer (rendered in the facts <dl>, counted by the thin-content gate)
const FACTS = {
  ports: ['country','coordinates','operator','unlocode','max_depth_m','berths','ice_class_support','cargo_capacity_t','annual_vessel_calls'],
  cities: ['country','region','coordinates','population','gdp_usd'],
  shipyards: ['country','location','coordinates','specialization','arctic_capable'],
  lanes: ['operators','typical_distance_nm','transit_days','ice_conditions','difficulty','icebreaker_required','transit_fee_usd','volume_teu_per_year'],
  tankers: ['country','operator','ice_class','dwt','cargo','route','year_built'],
  icebreakers: ['country','operator','ice_class','power_kw','route','year_built'],
};
for (const l of PROJ) FACTS[l] = ['country','city','coordinates','type','operator','status','confidence','verified','url'];
const DETAILS = Object.fromEntries(PROJ.map((l) => [l, ['benefits','eligibility','sources']]));
const NO_COORD = new Set(['lanes','tankers','icebreakers']);   // schematic positions: no coordinates claimed
const THIN_MIN = 5;

// ---------- helpers ----------
const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const fill = (t, o) => String(t).replace(/\{(\w+)\}/g, (_, k) => (o[k] ?? ''));
const ldjson = (o) => JSON.stringify(o).replace(/</g, '\\u003c');
const empty = (v) => v == null || (typeof v === 'string' && /^\s*(|-|–|n\/?a|null|none|unknown|tbd|\?)\s*$/i.test(v)) || (Array.isArray(v) && !v.length);
const clean = (v) => !empty(v) && lintText(String(v)).length === 0;
const labels = Object.fromEntries(LANGS.map((l) => [l, JSON.parse(fs.readFileSync(path.join(I18N, `labels.${l}.json`), 'utf8'))]));
const T = (lang, k) => labels[lang][k] ?? labels.en[k] ?? k;
const pfx = (lang) => (lang === 'en' ? '' : `/${lang}`);
const homeUrl = (lang) => (lang === 'en' ? '/' : `/${lang}`);
const regionNames = Object.fromEntries(LANGS.map((l) => [l, new Intl.DisplayNames([INTL[l] || l], { type: 'region' })]));
const nf = Object.fromEntries(LANGS.map((l) => [l, new Intl.NumberFormat(INTL[l] || l, { maximumFractionDigits: 2 })]));
const df = Object.fromEntries(LANGS.map((l) => [l, new Intl.DateTimeFormat(INTL[l] || l, { dateStyle: 'long', timeZone: 'UTC' })]));
function countryName(lang, o) {
  const iso = String(o.iso2 || '').toUpperCase();
  if (/^[A-Z]{2}$/.test(iso) && !/[\/,]/.test(o.country || '')) { try { const n = regionNames[lang].of(iso); if (n && n !== iso) return n; } catch {} }
  return o.country || iso;
}
const isNum = (v) => typeof v === 'number' || (typeof v === 'string' && /^\s*-?\d+(\.\d+)?\s*$/.test(v));
const num = (lang, v) => (isNum(v) ? nf[lang].format(Number(v)) : String(v));
const isoDate = (v) => (typeof v === 'string' && /^\d{4}-\d{2}-\d{2}/.test(v) ? v.slice(0, 10) : null);
function hav(a, b) {
  const R = 6371.0088, r = Math.PI / 180;
  const dLat = (b[1] - a[1]) * r, dLon = (b[0] - a[0]) * r;
  const x = Math.sin(dLat / 2) ** 2 + Math.cos(a[1] * r) * Math.cos(b[1] * r) * Math.sin(dLon / 2) ** 2;
  return 2 * R * Math.asin(Math.min(1, Math.sqrt(x)));
}
const CYR = { а:'a',б:'b',в:'v',г:'g',д:'d',е:'e',ё:'e',ж:'zh',з:'z',и:'i',й:'y',к:'k',л:'l',м:'m',н:'n',о:'o',п:'p',р:'r',с:'s',т:'t',у:'u',ф:'f',х:'kh',ц:'ts',ч:'ch',ш:'sh',щ:'shch',ъ:'',ы:'y',ь:'',э:'e',ю:'yu',я:'ya' };
const SPECIAL = { ø:'o', æ:'ae', œ:'oe', ß:'ss', ł:'l', đ:'d', ð:'d', þ:'th', ı:'i', '&':' and ' };
export function slugify(name) {
  let s = String(name).replace(/\s*\([^)]*\)\s*/g, ' ').toLowerCase();
  s = [...s].map((c) => CYR[c] ?? SPECIAL[c] ?? c).join('');
  s = s.normalize('NFKD').replace(/\p{M}+/gu, '').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
  if (s.length > 60) { s = s.slice(0, 61); s = s.includes('-') ? s.slice(0, s.lastIndexOf('-')) : s.slice(0, 60); }
  return s.replace(/-+$/g, '');
}

// ---------- load data ----------
const atlas = JSON.parse(fs.readFileSync(ATLAS, 'utf8'));
const manifest = fs.existsSync(MANIFEST) ? JSON.parse(fs.readFileSync(MANIFEST, 'utf8')) : {};
const ATLAS_DATE = isoDate(manifest.generated || atlas.generated) || new Date().toISOString().slice(0, 10);
const objs = [];
for (const f of atlas.features || []) {
  const p = f.properties || {}; const id = p.id || f.id;
  if (!id || !ALL_LAYERS.includes(p.layer)) continue;
  const g = f.geometry || {};
  let pt = null;
  if (Array.isArray(p.position_anchor) && p.position_anchor.length === 2) pt = p.position_anchor.map(Number);
  else if (g.type === 'Point') pt = g.coordinates;
  else if (g.type === 'LineString' && g.coordinates?.length) pt = g.coordinates[Math.floor(g.coordinates.length / 2)];
  objs.push({ id, layer: p.layer, p, pt, geom: g });
}
objs.sort((a, b) => a.id.localeCompare(b.id, 'en', { numeric: true }));

// ---------- slugs (stable: existing entries never change) ----------
const slugs = fs.existsSync(SLUGS) ? JSON.parse(fs.readFileSync(SLUGS, 'utf8')) : {};
const taken = {};
for (const [id, s] of Object.entries(slugs)) { const o = objs.find((x) => x.id === id); const k = o ? PREFIX[o.layer] : '?'; (taken[k] ||= new Set()).add(s); }
let added = 0;
for (const o of objs) {
  if (slugs[o.id]) continue;
  const k = PREFIX[o.layer]; const used = (taken[k] ||= new Set());
  let base = slugify(o.p.name) || o.id.toLowerCase(); let s = base;
  if (used.has(s) && o.p.iso2) s = `${base}-${String(o.p.iso2).toLowerCase()}`;
  for (let n = 2; used.has(s); n++) s = `${base}-${n}`;
  used.add(s); slugs[o.id] = s; added++;
}
const sortedSlugs = Object.fromEntries(Object.entries(slugs).sort(([a], [b]) => a.localeCompare(b, 'en', { numeric: true })));
fs.mkdirSync(path.dirname(SLUGS), { recursive: true });
fs.writeFileSync(SLUGS, JSON.stringify(sortedSlugs, null, 1) + '\n');

const pages = objs.filter((o) => LAYERS.includes(o.layer));
const byId = new Map(objs.map((o) => [o.id, o]));
const pagePath = (lang, o) => `${pfx(lang)}/${PREFIX[o.layer]}/${slugs[o.id]}`;
const indexPath = (lang, layer) => `${pfx(lang)}/${INDEX[layer]}`;
const mapLink = (lang, o) => `${homeUrl(lang)}${lang === 'en' ? '' : ''}?focus=${encodeURIComponent(o.id)}&layer=${encodeURIComponent(o.layer)}#z=6`;

// ---------- facts ----------
function factValue(lang, o, k) {
  const p = o.p;
  if (k === 'country') return clean(p.country) || clean(p.iso2) ? esc(countryName(lang, p)) : null;
  if (k === 'coordinates') {
    if (NO_COORD.has(o.layer) || !o.pt || !isFinite(o.pt[0]) || !isFinite(o.pt[1])) return null;
    return `${o.pt[1].toFixed(4)}, ${o.pt[0].toFixed(4)}`;
  }
  const v = p[k];
  if (!clean(v)) return null;
  if (k === 'url') return /^https?:\/\//i.test(v) ? `<a href="${esc(v)}" rel="nofollow noopener" target="_blank">${esc(v.replace(/^https?:\/\/(www\.)?/i, '').replace(/\/$/, '').slice(0, 60))}</a>` : null;
  if (k === 'verified') { const d = isoDate(v); return d ? `<time datetime="${d}">${esc(df[lang].format(new Date(d + 'T00:00:00Z')))}</time>` : esc(v); }
  if (k === 'max_depth_m') return isNum(v) ? `${num(lang, v)} ${esc(T(lang, 'unit_m'))}` : esc(v);
  if (k === 'cargo_capacity_t') return isNum(v) ? `${num(lang, v)} ${esc(T(lang, 'unit_t_yr'))}` : esc(v);
  if (k === 'dwt') return isNum(v) ? `${num(lang, v)} t` : esc(v);
  if (k === 'power_kw') return isNum(v) ? `${num(lang, v)} kW` : esc(v);
  if (k === 'typical_distance_nm') return isNum(v) ? `${num(lang, v)} NM` : esc(v);
  if (k === 'transit_days') return `${esc(v)} ${esc(T(lang, 'unit_days'))}`;
  if (k === 'transit_fee_usd') return `${isNum(v) ? num(lang, v) : esc(v)} USD`;
  if (k === 'volume_teu_per_year') return isNum(v) ? `${num(lang, v)} TEU` : esc(v);
  if (k === 'gdp_usd') return isNum(v) ? `${num(lang, v)} USD` : esc(v);
  if (k === 'year_built' || k === 'unlocode') return esc(v);
  if (isNum(v)) return num(lang, v);
  return esc(v);
}
const structuredCount = (o) => (FACTS[o.layer] || []).filter((k) => factValue('en', o, k) != null).length;

// ---------- nearby (8 nearest by great-circle distance, among generated pages) ----------
const located = pages.filter((o) => o.pt && isFinite(o.pt[0]) && isFinite(o.pt[1]));
const nearby = new Map();
for (const o of located) {
  const d = [];
  for (const q of located) if (q !== o) d.push([hav(o.pt, q.pt), q]);
  d.sort((a, b) => a[0] - b[0] || a[1].id.localeCompare(b[1].id));
  nearby.set(o.id, d.slice(0, 8));
}

// ---------- page rendering ----------
const CSS = `:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;font:16px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;background:#07121f;color:#e6eef7}a{color:#7cc8ff}header,main,footer{max-width:960px;margin:0 auto;padding:12px 18px}header{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:center;border-bottom:1px solid #18324d}header .brand{font-weight:700;color:#e6eef7;text-decoration:none}nav.bc ol{list-style:none;display:flex;flex-wrap:wrap;gap:6px;margin:0;padding:0;font-size:14px}nav.bc li+li:before{content:"›";margin-right:6px;color:#6b8aa8}h1{font-size:clamp(22px,3.4vw,32px);line-height:1.25;margin:18px 0 8px}h2{font-size:19px;margin:26px 0 8px;color:#bfe3ff}.intro{color:#c9d8e6}.btn{display:inline-block;padding:9px 14px;border-radius:8px;background:#0f6fb5;color:#fff;text-decoration:none;font-weight:600}.btn.alt{background:#173550}dl{display:grid;grid-template-columns:minmax(140px,32%) 1fr;gap:6px 16px;margin:0}dt{color:#8fb0cc}dd{margin:0;overflow-wrap:anywhere}ul.list{columns:2 260px;padding-left:18px}ul.list li{break-inside:avoid;margin:2px 0}.muted{color:#8fa6bb;font-size:14px}.layer-tag{font-size:12px;color:#8fb0cc;margin-left:6px}footer{border-top:1px solid #18324d;margin-top:28px;font-size:13px;color:#8fa6bb}footer .langs a{margin-right:8px;display:inline-block}`;

function alternates(pathFor) {
  const tags = LANGS.map((l) => `<link rel="alternate" hreflang="${hl(l)}" href="${ORIGIN}${pathFor(l)}">`);
  tags.push(`<link rel="alternate" hreflang="x-default" href="${ORIGIN}${pathFor('en')}">`);
  return tags.join('');
}
function langLinks(pathFor, cur) {
  return LANGS.map((l) => (l === cur ? `<strong>${l}</strong>` : `<a href="${pathFor(l)}" hreflang="${hl(l)}" lang="${hl(l)}">${l}</a>`)).join(' ');
}
function shell({ lang, title, desc, canonicalPath, pathFor, robots, ld, body }) {
  return `<!doctype html><html lang="${hl(lang)}"${RTL.has(lang) ? ' dir="rtl"' : ''}><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">`
    + `<title>${esc(title)}</title><meta name="description" content="${esc(desc)}"><meta name="robots" content="${robots}">`
    + `<link rel="canonical" href="${ORIGIN}${canonicalPath}">${alternates(pathFor)}`
    + `<meta property="og:type" content="website"><meta property="og:site_name" content="ArcticTradeLanes"><meta property="og:title" content="${esc(title)}"><meta property="og:description" content="${esc(desc)}"><meta property="og:url" content="${ORIGIN}${canonicalPath}"><meta property="og:locale" content="${hl(lang).replace('-', '_')}">`
    + `<link rel="icon" href="/favicon.svg" type="image/svg+xml"><style>${CSS}</style>`
    + `<script type="application/ld+json">${ldjson(ld)}</script></head><body>`
    + body
    + `<footer><p class="langs" aria-label="${esc(T(lang, 'languages'))}">${esc(T(lang, 'languages'))}: ${langLinks(pathFor, lang)}</p><p>© ArcticTradeLanes.com · <a href="${homeUrl(lang)}">${esc(T(lang, 'site'))}</a> · <a href="https://github.com/International-Arctic/ArcticTradeLanes-Dataset" rel="noopener">${esc(T(lang, 'source_repo'))}</a></p></footer></body></html>\n`;
}
function bbox(layer) {
  const pts = objs.filter((o) => o.layer === layer && o.pt).map((o) => o.pt);
  if (!pts.length) return null;
  const la = pts.map((p) => p[1]), lo = pts.map((p) => p[0]);
  const r = (x) => Math.round(x * 100) / 100;
  return `${r(Math.min(...la))} ${r(Math.min(...lo))} ${r(Math.max(...la))} ${r(Math.max(...lo))}`;
}
const BBOX = Object.fromEntries(ALL_LAYERS.map((l) => [l, bbox(l)]));
const layerCount = Object.fromEntries(ALL_LAYERS.map((l) => [l, objs.filter((o) => o.layer === l).length]));
function datasetNode(lang, layer) {
  const n = { '@type': 'Dataset', '@id': `${ORIGIN}${indexPath(lang, layer)}#dataset`, name: fill(T(lang, 'dataset_name'), { layer: T(lang, `layers.${layer}`) }),
    description: fill(T(lang, 'index_intro'), { count: layerCount[layer], layer: T(lang, `layers.${layer}`) }),
    url: `${ORIGIN}${indexPath(lang, layer)}`, inLanguage: hl(lang), dateModified: ATLAS_DATE,
    license: 'https://www.apache.org/licenses/LICENSE-2.0',
    creator: { '@type': 'Organization', name: 'ArcticTradeLanes.com', url: ORIGIN },
    isAccessibleForFree: true,
    distribution: [{ '@type': 'DataDownload', encodingFormat: 'application/geo+json', contentUrl: `${ORIGIN}/atlas.4326.geojson` }] };
  if (BBOX[layer]) n.spatialCoverage = { '@type': 'Place', geo: { '@type': 'GeoShape', box: BBOX[layer] } };
  return n;
}
function lastMod(o) { return isoDate(o.p.verified) || ATLAS_DATE; }

function renderObject(lang, o, indexable) {
  const p = o.p; const name = String(p.name); const url = pagePath(lang, o); const full = ORIGIN + url;
  const layerS = T(lang, `layer.${o.layer}`), layerP = T(lang, `layers.${o.layer}`);
  const cname = (clean(p.country) || clean(p.iso2)) ? countryName(lang, p) : '';
  const hasCoord = !NO_COORD.has(o.layer) && o.pt;
  const lat = hasCoord ? o.pt[1].toFixed(4) : '', lon = hasCoord ? o.pt[0].toFixed(4) : '';
  const introKey = o.layer === 'lanes' || !cname ? 'intro_lane' : hasCoord ? 'intro' : 'intro_nocoord';
  const intro = fill(T(lang, introKey), { name, type: layerS, country: cname, lat, lon });
  const desc = fill(T(lang, 'meta_desc'), { name: name.slice(0, 90), type: layerS, country: cname || 'Arctic' });
  const rows = (FACTS[o.layer] || []).map((k) => [k, factValue(lang, o, k)]).filter(([, v]) => v != null);
  rows.push(['atlas_id', esc(o.id)]);
  const det = (DETAILS[o.layer] || []).filter((k) => clean(p[k])).map((k) => [k, esc(p[k])]);
  const coSite = (Array.isArray(p.co_site_ids) ? p.co_site_ids : []).map((id) => byId.get(id)).filter((q) => q && LAYERS.includes(q.layer));
  const near = nearby.get(o.id) || [];
  const isoUp = String(p.iso2 || '').toUpperCase();
  // JSON-LD @graph (§11.5); empty fields omitted
  const main = { '@id': `${full}#${PROJ.includes(o.layer) && o.layer === 'programs' ? 'project' : 'place'}`, name, url: full, identifier: o.id, description: intro, hasMap: ORIGIN + mapLink('en', o) };
  const geo = hasCoord ? { '@type': 'GeoCoordinates', latitude: +lat, longitude: +lon } : null;
  const addr = /^[A-Z]{2}$/.test(isoUp) ? { '@type': 'PostalAddress', addressCountry: isoUp, ...(clean(p.city) && String(p.city).length < 80 ? { addressLocality: String(p.city) } : {}) } : null;
  if (o.layer === 'programs') {
    main['@type'] = 'Project';
    const loc = { '@type': 'Place' }; if (geo) loc.geo = geo; if (addr) loc.address = addr; if (clean(p.city) && String(p.city).length < 80) loc.name = String(p.city);
    if (Object.keys(loc).length > 1) main.location = loc;
    if (clean(p.url) && /^https?:/.test(p.url)) main.sameAs = [p.url];
  } else {
    main['@type'] = o.layer === 'ports' ? ['Place', 'CivicStructure'] : o.layer === 'cities' ? 'City' : o.layer === 'airports' ? 'Airport' : (o.layer === 'tankers' || o.layer === 'icebreakers') ? 'Vehicle' : 'Place';
    if (o.layer === 'ports') main.additionalType = 'https://www.wikidata.org/wiki/Q44782';
    if (main['@type'] === 'Vehicle') { delete main.hasMap; if (clean(p.year_built)) main.productionDate = String(p.year_built); }
    else { if (geo) main.geo = geo; if (addr) main.address = addr; }
    if (o.layer === 'lanes' && o.geom?.type === 'LineString') {
      const c = o.geom.coordinates; const step = Math.max(1, Math.ceil(c.length / 24)); const s = [];
      for (let i = 0; i < c.length; i += step) s.push(c[i]); if (s[s.length - 1] !== c[c.length - 1]) s.push(c[c.length - 1]);
      main.geo = { '@type': 'GeoShape', line: s.map((q) => `${q[1].toFixed(3)} ${q[0].toFixed(3)}`).join(' ') };
    }
    if (clean(p.url) && /^https?:/.test(p.url)) main.sameAs = [p.url];
  }
  const graph = [main];
  if (clean(p.operator) && o.layer !== 'lanes') {
    const org = { '@type': 'Organization', '@id': `${full}#operator`, name: String(p.operator) };
    graph.push(org);
    if (main['@type'] === 'Project') main.parentOrganization = { '@id': org['@id'] };
  }
  graph.push(datasetNode(lang, o.layer));
  graph.push({ '@type': 'BreadcrumbList', itemListElement: [
    { '@type': 'ListItem', position: 1, name: T(lang, 'atlas'), item: ORIGIN + homeUrl(lang) },
    { '@type': 'ListItem', position: 2, name: layerP, item: ORIGIN + indexPath(lang, o.layer) },
    { '@type': 'ListItem', position: 3, name } ] });
  const ld = { '@context': 'https://schema.org', '@graph': graph };
  const lm = lastMod(o);
  const body = `<header><a class="brand" href="${homeUrl(lang)}">ArcticTradeLanes</a><nav class="bc" aria-label="${esc(T(lang, 'breadcrumb'))}"><ol><li><a href="${homeUrl(lang)}">${esc(T(lang, 'atlas'))}</a></li><li><a href="${indexPath(lang, o.layer)}">${esc(layerP)}</a></li><li aria-current="page">${esc(name.length > 60 ? name.slice(0, 57) + '…' : name)}</li></ol></nav></header>`
    + `<main><h1>${esc(name)}</h1><p class="intro">${esc(intro)}</p>`
    + `<p><a class="btn" href="${esc(mapLink(lang, o))}" data-atl-focus="${esc(o.id)}">${esc(T(lang, 'open_map'))}</a></p>`
    + `<section><h2>${esc(T(lang, 'facts'))}</h2><dl><dt>${esc(T(lang, 'layer'))}</dt><dd><a href="${indexPath(lang, o.layer)}">${esc(layerP)}</a></dd>${rows.map(([k, v]) => `<dt>${esc(T(lang, k))}</dt><dd>${v}</dd>`).join('')}</dl></section>`
    + (det.length ? `<section><h2>${esc(T(lang, 'details'))}</h2><dl>${det.map(([k, v]) => `<dt>${esc(T(lang, k))}</dt><dd>${v}</dd>`).join('')}</dl></section>` : '')
    + (coSite.length ? `<section><h2>${esc(T(lang, 'co_site'))}</h2><ul class="list">${coSite.map((q) => `<li><a href="${pagePath(lang, q)}">${esc(q.p.name)}</a><span class="layer-tag">${esc(T(lang, `layer.${q.layer}`))}</span></li>`).join('')}</ul></section>` : '')
    + (near.length ? `<section><h2>${esc(T(lang, 'nearby'))}</h2><ul class="list">${near.map(([d, q]) => `<li><a href="${pagePath(lang, q)}">${esc(String(q.p.name).length > 80 ? String(q.p.name).slice(0, 77) + '…' : q.p.name)}</a><span class="layer-tag">${esc(T(lang, `layer.${q.layer}`))} · ${num(lang, Math.round(d))} ${esc(T(lang, 'unit_km'))}</span></li>`).join('')}</ul></section>` : '')
    + `<section><h2>${esc(T(lang, 'sources'))}</h2><ul>`
    + (clean(p.url) && /^https?:/.test(p.url) ? `<li>${esc(T(lang, 'official_site'))}: <a href="${esc(p.url)}" rel="nofollow noopener" target="_blank">${esc(String(p.url).replace(/^https?:\/\/(www\.)?/, '').slice(0, 60))}</a></li>` : '')
    + `<li><a href="/atlas.4326.geojson">${esc(T(lang, 'source_data'))}</a></li><li><a href="https://github.com/International-Arctic/ArcticTradeLanes-Dataset" rel="noopener">${esc(T(lang, 'source_repo'))}</a></li></ul></section>`
    + `<p class="muted">${esc(T(lang, 'last_updated'))}: <time datetime="${lm}">${esc(df[lang].format(new Date(lm + 'T00:00:00Z')))}</time></p>`
    + `<p><a class="btn alt" href="${indexPath(lang, o.layer)}">${esc(fill(T(lang, 'all_layer'), { layer: layerP }))}</a>`
    + (/^[A-Z]{2}$/.test(isoUp) && cname ? ` <a class="btn alt" href="${indexPath(lang, o.layer)}#c-${isoUp}">${esc(fill(T(lang, 'more_in_country'), { layer: layerP, country: cname }))}</a>` : '')
    + `</p></main>`;
  const title = `${name.length > 64 ? name.slice(0, 61) + '…' : name} · ${layerS} · ArcticTradeLanes`;
  return shell({ lang, title, desc, canonicalPath: url, pathFor: (l) => pagePath(l, o), robots: indexable ? 'index,follow' : 'noindex,follow', ld, body });
}

function renderIndex(lang, layer, members) {
  const layerP = T(lang, `layers.${layer}`); const url = indexPath(lang, layer);
  const groups = new Map();
  for (const o of members) { const k = String(o.p.iso2 || '').toUpperCase() || 'ZZ'; if (!groups.has(k)) groups.set(k, []); groups.get(k).push(o); }
  const keys = [...groups.keys()].sort((a, b) => countryName(lang, groups.get(a)[0].p).localeCompare(countryName(lang, groups.get(b)[0].p), INTL[lang] || lang));
  const title = `${fill(T(lang, 'index_title'), { layer: layerP })} · ArcticTradeLanes`;
  const intro = fill(T(lang, 'index_intro'), { count: members.length, layer: layerP });
  const ld = { '@context': 'https://schema.org', '@graph': [ { ...datasetNode(lang, layer) },
    { '@type': 'BreadcrumbList', itemListElement: [ { '@type': 'ListItem', position: 1, name: T(lang, 'atlas'), item: ORIGIN + homeUrl(lang) }, { '@type': 'ListItem', position: 2, name: layerP } ] } ] };
  const body = `<header><a class="brand" href="${homeUrl(lang)}">ArcticTradeLanes</a><nav class="bc" aria-label="${esc(T(lang, 'breadcrumb'))}"><ol><li><a href="${homeUrl(lang)}">${esc(T(lang, 'atlas'))}</a></li><li aria-current="page">${esc(layerP)}</li></ol></nav></header>`
    + `<main><h1>${esc(fill(T(lang, 'index_title'), { layer: layerP }))}</h1><p class="intro">${esc(intro)}</p>`
    + `<p><a class="btn" href="${homeUrl(lang)}?layer=${encodeURIComponent(layer)}#z=3">${esc(T(lang, 'view_layer_map'))}</a></p>`
    + `<h2>${esc(T(lang, 'by_country'))}</h2><p class="muted">${keys.map((k) => `<a href="#c-${k}">${esc(countryName(lang, groups.get(k)[0].p))}</a> (${groups.get(k).length})`).join(' · ')}</p>`
    + keys.map((k) => `<section><h2 id="c-${k}">${esc(countryName(lang, groups.get(k)[0].p))}</h2><ul class="list">${groups.get(k).sort((a, b) => String(a.p.name).localeCompare(String(b.p.name))).map((o) => `<li><a href="${pagePath(lang, o)}">${esc(o.p.name)}</a></li>`).join('')}</ul></section>`).join('')
    + `<p class="muted"><a href="/atlas.4326.geojson">${esc(T(lang, 'source_data'))}</a> · ${esc(T(lang, 'last_updated'))}: <time datetime="${ATLAS_DATE}">${esc(df[lang].format(new Date(ATLAS_DATE + 'T00:00:00Z')))}</time></p></main>`;
  return shell({ lang, title, desc: intro, canonicalPath: url, pathFor: (l) => indexPath(l, layer), robots: 'index,follow', ld, body });
}
function render404(lang) {
  const body = `<header><a class="brand" href="${homeUrl(lang)}">ArcticTradeLanes</a></header><main><h1>${esc(T(lang, 'not_found_title'))}</h1><p class="intro">${esc(T(lang, 'not_found_text'))}</p><ul>${LAYERS.filter((l, i, a) => a.findIndex((x) => INDEX[x] === INDEX[l]) === i).map((l) => `<li><a href="${indexPath(lang, l)}">${esc(T(lang, `layers.${l}`))}</a></li>`).join('')}</ul><p><a class="btn" href="${homeUrl(lang)}">${esc(T(lang, 'back_atlas'))}</a></p></main>`;
  return `<!doctype html><html lang="${hl(lang)}"${RTL.has(lang) ? ' dir="rtl"' : ''}><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(T(lang, 'not_found_title'))} · ArcticTradeLanes</title><meta name="robots" content="noindex,follow"><style>${CSS}</style></head><body>${body}</body></html>\n`;
}

// ---------- write ----------
const t0 = Date.now();
const TMP = OUT + '.tmp';
fs.rmSync(TMP, { recursive: true, force: true });
fs.mkdirSync(TMP, { recursive: true });
const write = (rel, s) => { const f = path.join(TMP, rel); fs.mkdirSync(path.dirname(f), { recursive: true }); fs.writeFileSync(f, s); };
const stats = {}; const sitemapUrls = {}; const objectMap = {};
const indexable = new Map(pages.map((o) => [o.id, structuredCount(o) >= THIN_MIN]));
for (const o of pages) objectMap[o.id] = pagePath('en', o);
const xmlAlt = (pathFor) => LANGS.map((l) => `<xhtml:link rel="alternate" hreflang="${hl(l)}" href="${ORIGIN}${pathFor(l)}"/>`).join('') + `<xhtml:link rel="alternate" hreflang="x-default" href="${ORIGIN}${pathFor('en')}"/>`;
for (const lang of LANGS) {
  for (const o of pages) {
    const idx = indexable.get(o.id);
    write(`${lang}/${PREFIX[o.layer]}/${slugs[o.id]}.html`, renderObject(lang, o, idx));
    const st = (stats[o.layer] ||= {}); const s = (st[lang] ||= { indexable: 0, noindex: 0 }); idx ? s.indexable++ : s.noindex++;
    if (idx) ((sitemapUrls[`${PREFIX[o.layer]}-${lang}`] ||= [])).push(`<url><loc>${ORIGIN}${pagePath(lang, o)}</loc><lastmod>${lastMod(o)}</lastmod>${xmlAlt((l) => pagePath(l, o))}</url>`);
  }
  for (const layer of LAYERS) {
    const members = pages.filter((o) => o.layer === layer);
    write(`${lang}/_index/${INDEX[layer]}.html`, renderIndex(lang, layer, members));
    ((sitemapUrls[`${PREFIX[layer]}-${lang}`] ||= [])).push(`<url><loc>${ORIGIN}${indexPath(lang, layer)}</loc><lastmod>${ATLAS_DATE}</lastmod>${xmlAlt((l) => indexPath(l, layer))}</url>`);
  }
  write(`${lang}/404.html`, render404(lang));
}
let sitemapCount = 0; const shards = [];
for (const [name, urls] of Object.entries(sitemapUrls)) {
  sitemapCount += urls.length; shards.push(name);
  write(`sitemaps/${name}.xml`, `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n${urls.join('\n')}\n</urlset>\n`);
}
write('sitemaps/index.xml', `<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${shards.map((n) => `<sitemap><loc>${ORIGIN}/sitemaps/${n}.xml</loc><lastmod>${ATLAS_DATE}</lastmod></sitemap>`).join('\n')}\n</sitemapindex>\n`);
write('object-map.json', JSON.stringify(objectMap) + '\n');
const indexPagesCount = LANGS.length * LAYERS.length;
const totalIndexable = Object.values(stats).reduce((a, st) => a + Object.values(st).reduce((b, s) => b + s.indexable, 0), 0) + indexPagesCount;
const report = { generated_from: { atlas_generated: ATLAS_DATE, objects: objs.length }, layers: LAYERS, langs: LANGS.length, slugs_added: added, pages: stats, index_pages: indexPagesCount, indexable_pages_total: totalIndexable, sitemap_urls: sitemapCount, shards: shards.length };
write('build-report.json', JSON.stringify(report, null, 1) + '\n');
write('.inputs.sha256', INPUT_HASH + '\n');
console.log(`[fact-pages] rendered ${pages.length} objects x ${LANGS.length} langs (+${indexPagesCount} index pages) in ${((Date.now() - t0) / 1000).toFixed(1)}s; sitemap URLs ${sitemapCount}; slugs added ${added}`);

// ---------- gates: neutral lint (0 hits), JSON-LD parse, hreflang reciprocity, page count == sitemap count ----------
let fail = 0;
const hits = []; let nfiles = 0;
for (const f of listFiles(TMP)) { if (f.endsWith('.json')) continue; nfiles++; hits.push(...lintFile(f)); }
if (hits.length) { fail++; for (const h of hits.slice(0, 50)) console.error(`HIT ${path.relative(TMP, h.file)} :: ${h.where} :: term#${h.term}`); }
console.log(`[fact-pages] neutral lint: ${nfiles} files, ${hits.length} hits`);
if (sitemapCount !== totalIndexable) { fail++; console.error(`[fact-pages] page count ${totalIndexable} != sitemap URL count ${sitemapCount}`); }
if (!args['no-validate']) {
  let ldBad = 0, hrefBad = 0, checked = 0;
  const altsOf = new Map();
  const files = [...listFiles(TMP)].filter((f) => f.endsWith('.html') && !f.endsWith('404.html'));
  for (const f of files) {
    const h = fs.readFileSync(f, 'utf8');
    const m = h.match(/<script type="application\/ld\+json">(.*?)<\/script>/s);
    try { const j = JSON.parse(m[1]); if (!Array.isArray(j['@graph']) || !j['@graph'].some((n) => n['@type'] === 'BreadcrumbList') || !j['@graph'].some((n) => n['@type'] === 'Dataset')) throw 0; } catch { ldBad++; }
    const canon = (h.match(/<link rel="canonical" href="([^"]+)"/) || [])[1];
    const alts = [...h.matchAll(/<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">/g)].map((x) => [x[1], x[2]]);
    if (alts.length !== LANGS.length + 1) hrefBad++;
    altsOf.set(canon, new Set(alts.filter(([k]) => k !== 'x-default').map(([, u]) => u)));
    checked++;
  }
  for (const [canon, set] of altsOf) {
    if (!set.has(canon)) { hrefBad++; continue; }
    for (const u of set) { const back = altsOf.get(u); if (!back || !back.has(canon)) { hrefBad++; break; } }
  }
  console.log(`[fact-pages] validated ${checked} pages: JSON-LD invalid ${ldBad}, hreflang non-reciprocal ${hrefBad}`);
  if (ldBad || hrefBad) fail++;
}
if (fail) { console.error('[fact-pages] FAILED gates; keeping previous ./factpages output'); fs.rmSync(TMP, { recursive: true, force: true }); process.exit(1); }
fs.rmSync(OUT + '.old', { recursive: true, force: true });
if (fs.existsSync(OUT)) fs.renameSync(OUT, OUT + '.old');
fs.renameSync(TMP, OUT);
fs.rmSync(OUT + '.old', { recursive: true, force: true });
console.log(`[fact-pages] OK -> ${path.relative(ROOT, OUT)} (${JSON.stringify(Object.fromEntries(Object.entries(stats).map(([l, st]) => [l, st.en])))} per lang)`);
