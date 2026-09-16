#!/usr/bin/env node
/** Assert ARC-SHIP-012 densified onto OSM Pernon telakka way/32198547 (gis-densify-1215). */
import { readFileSync } from 'node:fs';
const atlasPath = process.argv[2] || 'dataset/atlas.4326.geojson';
const g = JSON.parse(readFileSync(atlasPath, 'utf8'));
const want = { lon: 22.130376, lat: 60.456311 };
const bad = { lon: 22.2700, lat: 60.4500 };
let found = false;
let failed = 0;
for (const f of g.features || []) {
  if ((f.properties || {}).id !== 'ARC-SHIP-012') continue;
  found = true;
  const [lon, lat] = f.geometry?.coordinates || [];
  if (Math.abs(lon - bad.lon) < 1e-3 && Math.abs(lat - bad.lat) < 1e-3) {
    console.error('ARC-SHIP-012 still on Turku soft-pin', [lon, lat]);
    failed++;
  } else if (Math.abs(lon - want.lon) > 1e-4 || Math.abs(lat - want.lat) > 1e-4) {
    console.error('ARC-SHIP-012 unexpected coords', [lon, lat], 'want', want);
    failed++;
  } else {
    console.log('ARC-SHIP-012 ok', [lon, lat]);
  }
}
if (!found) { console.error('ARC-SHIP-012 missing'); failed++; }
if (failed) process.exit(1);
console.log('check-ship012-turku-perno-densify: pass');
