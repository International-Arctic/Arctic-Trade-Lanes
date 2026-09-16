#!/usr/bin/env node
/** Assert ARC-SHIP-003 densified onto OSM Severnaya Verf relation/1411836 (gis-densify-1011). */
import { readFileSync } from 'node:fs';
const atlasPath = process.argv[2] || 'dataset/atlas.4326.geojson';
const g = JSON.parse(readFileSync(atlasPath, 'utf8'));
const want = { lon: 30.233195, lat: 59.875194 };
const bad = { lon: 30.2600, lat: 59.9420 };
let found = false;
let failed = 0;
for (const f of g.features || []) {
  if ((f.properties || {}).id !== 'ARC-SHIP-003') continue;
  found = true;
  const [lon, lat] = f.geometry?.coordinates || [];
  if (Math.abs(lon - bad.lon) < 1e-3 && Math.abs(lat - bad.lat) < 1e-3) {
    console.error('ARC-SHIP-003 still on St. Petersburg soft-pin', [lon, lat]);
    failed++;
  } else if (Math.abs(lon - want.lon) > 1e-4 || Math.abs(lat - want.lat) > 1e-4) {
    console.error('ARC-SHIP-003 unexpected coords', [lon, lat], 'want', want);
    failed++;
  } else {
    console.log('ARC-SHIP-003 ok', [lon, lat]);
  }
}
if (!found) { console.error('ARC-SHIP-003 missing'); failed++; }
if (failed) process.exit(1);
console.log('check-ship003-severnaya-verft-densify: pass');
