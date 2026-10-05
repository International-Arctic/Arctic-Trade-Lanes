#!/usr/bin/env node
// gis-aliassync-1313 (2026-10-05): every public atlas alias must serve the SAME generation and bytes.
// Caught live: root /atlas.* was gen 2026-10-05T09:49:53Z, /atlas/* was 08:59:34Z and /data/* was
// 2026-09-29T15:42:55Z, so crawlers and API users of /data/* missed six days of geo fixes.
// Usage: node scripts/check-atlas-alias-sync.mjs [https://arctictradelanes.com]
import { createHash } from 'node:crypto';
const base = (process.argv[2] || 'https://arctictradelanes.com').replace(/\/$/, '');
const prefixes = ['', '/data', '/atlas'];
const wgs = ['atlas.wgs84.geojson', 'atlas.4326.geojson', 'atlas.geojson'];
const md5 = (b) => createHash('md5').update(b).digest('hex');
async function get(path) {
  const r = await fetch(`${base}${path}?alias_check=${Date.now()}`, { headers: { 'user-agent': 'atl-alias-check/1.0' } });
  if (!r.ok) throw new Error(`${path} HTTP ${r.status}`);
  return Buffer.from(await r.arrayBuffer());
}
let bad = 0;
const ref = { gen: null, wgs: null, p3996: null };
for (const p of prefixes) {
  const man = JSON.parse((await get(`${p}/atlas.manifest.json`)).toString('utf8'));
  ref.gen ??= man.generated;
  if (man.generated !== ref.gen) { console.log(`STALE  ${p || '/'} manifest ${man.generated} != ${ref.gen}`); bad++; }
  for (const f of wgs) {
    const b = await get(`${p}/${f}`);
    if (b[0] === 0x3c) { console.log(`HTML   ${p}/${f} (SPA fallback, not GeoJSON)`); bad++; continue; }
    const h = md5(b); ref.wgs ??= h;
    if (h !== ref.wgs) { console.log(`DIFF   ${p}/${f} ${h.slice(0, 8)} != ${ref.wgs.slice(0, 8)}`); bad++; }
  }
  const h3 = md5(await get(`${p}/atlas.3996.geojson`)); ref.p3996 ??= h3;
  if (h3 !== ref.p3996) { console.log(`DIFF   ${p}/atlas.3996.geojson ${h3.slice(0, 8)} != ${ref.p3996.slice(0, 8)}`); bad++; }
}
console.log(`${bad ? 'FAIL' : 'OK'}  ${base} aliases ${prefixes.map((p) => p || '/').join(' ')} generation ${ref.gen} (problems: ${bad})`);
process.exit(bad ? 1 : 0);
