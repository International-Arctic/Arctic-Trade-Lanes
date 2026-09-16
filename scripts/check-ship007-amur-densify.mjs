#!/usr/bin/env node
/** Assert ARC-SHIP-007 densified onto OSM Amur Shipbuilding Plant relation/3482541 (gis-densify-1135). */
import { readFileSync } from 'node:fs';
const atlasPath = process.argv[2] || 'dataset/atlas.4326.geojson';
const g = JSON.parse(readFileSync(atlasPath, 'utf8'));
const want = { lon: 137.046019, lat: 50.544 };
const bad = { lon: 137.0200, lat: 50.5500 };
let found = false;
let failed = 0;
for (const f of g.features || []) {
  if ((f.properties || {}).id !== 'ARC-SHIP-007') continue;
  found = true;
  const [lon, lat] = f.geometry?.coordinates || [];
  if (Math.abs(lon - bad.lon) < 1e-3 && Math.abs(lat - bad.lat) < 1e-3) {
    console.error('ARC-SHIP-007 still on Komsomolsk soft-pin', [lon, lat]);
    failed++;
  } else if (Math.abs(lon - want.lon) > 1e-4 || Math.abs(lat - want.lat) > 1e-4) {
    console.error('ARC-SHIP-007 unexpected coords', [lon, lat], 'want', want);
    failed++;
  } else {
    console.log('ARC-SHIP-007 ok', [lon, lat]);
  }
}
if (!found) { console.error('ARC-SHIP-007 missing'); failed++; }
if (failed) process.exit(1);
console.log('check-ship007-amur-densify: pass');
