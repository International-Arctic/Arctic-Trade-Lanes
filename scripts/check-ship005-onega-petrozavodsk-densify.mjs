#!/usr/bin/env node
/** Assert ARC-SHIP-005 densified onto OSM Onego Shipyard way/41865465 (gis-densify-0916). */
import { readFileSync } from 'node:fs';
const atlasPath = process.argv[2] || 'dataset/atlas.4326.geojson';
const g = JSON.parse(readFileSync(atlasPath, 'utf8'));
const want = { lon: 34.40231, lat: 61.782944 };
const bad = { lon: 40.52, lat: 64.54 };
let found = false;
let failed = 0;
for (const f of g.features || []) {
  if ((f.properties || {}).id !== 'ARC-SHIP-005') continue;
  found = true;
  const [lon, lat] = f.geometry?.coordinates || [];
  if (Math.abs(lon - bad.lon) < 1e-3 && Math.abs(lat - bad.lat) < 1e-3) {
    console.error('ARC-SHIP-005 still on Arkhangelsk soft-pin', [lon, lat]);
    failed++;
  } else if (Math.abs(lon - want.lon) > 1e-5 || Math.abs(lat - want.lat) > 1e-5) {
    console.error('ARC-SHIP-005 unexpected coords', [lon, lat], 'want', want);
    failed++;
  } else {
    console.log('ARC-SHIP-005 ok', [lon, lat]);
  }
}
if (!found) { console.error('ARC-SHIP-005 missing'); failed++; }
if (failed) process.exit(1);
console.log('check-ship005-onega-petrozavodsk-densify: pass');
