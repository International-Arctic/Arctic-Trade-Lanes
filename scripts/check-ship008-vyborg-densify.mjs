#!/usr/bin/env node
/** Assert ARC-SHIP-008 densified onto OSM Vyborg Shipyard relation/7738660 (gis-densify-1135). */
import { readFileSync } from 'node:fs';
const atlasPath = process.argv[2] || 'dataset/atlas.4326.geojson';
const g = JSON.parse(readFileSync(atlasPath, 'utf8'));
const want = { lon: 28.750973, lat: 60.696219 };
const bad = { lon: 28.7400, lat: 60.7100 };
let found = false;
let failed = 0;
for (const f of g.features || []) {
  if ((f.properties || {}).id !== 'ARC-SHIP-008') continue;
  found = true;
  const [lon, lat] = f.geometry?.coordinates || [];
  if (Math.abs(lon - bad.lon) < 1e-3 && Math.abs(lat - bad.lat) < 1e-3) {
    console.error('ARC-SHIP-008 still on Vyborg soft-pin', [lon, lat]);
    failed++;
  } else if (Math.abs(lon - want.lon) > 1e-4 || Math.abs(lat - want.lat) > 1e-4) {
    console.error('ARC-SHIP-008 unexpected coords', [lon, lat], 'want', want);
    failed++;
  } else {
    console.log('ARC-SHIP-008 ok', [lon, lat]);
  }
}
if (!found) { console.error('ARC-SHIP-008 missing'); failed++; }
if (failed) process.exit(1);
console.log('check-ship008-vyborg-densify: pass');
