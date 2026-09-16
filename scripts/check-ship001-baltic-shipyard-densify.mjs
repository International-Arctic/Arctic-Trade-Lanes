#!/usr/bin/env node
/** Assert ARC-SHIP-001 densified onto OSM Baltic Shipyard relation/8702900 (gis-densify-0940). */
import { readFileSync } from 'node:fs';
const atlasPath = process.argv[2] || 'dataset/atlas.4326.geojson';
const g = JSON.parse(readFileSync(atlasPath, 'utf8'));
const want = { lon: 30.25709, lat: 59.925065 };
const bad = { lon: 30.262, lat: 59.943 };
let found = false;
let failed = 0;
for (const f of g.features || []) {
  if ((f.properties || {}).id !== 'ARC-SHIP-001') continue;
  found = true;
  const [lon, lat] = f.geometry?.coordinates || [];
  if (Math.abs(lon - bad.lon) < 1e-3 && Math.abs(lat - bad.lat) < 1e-3) {
    console.error('ARC-SHIP-001 still on St. Petersburg soft-pin', [lon, lat]);
    failed++;
  } else if (Math.abs(lon - want.lon) > 1e-4 || Math.abs(lat - want.lat) > 1e-4) {
    console.error('ARC-SHIP-001 unexpected coords', [lon, lat], 'want', want);
    failed++;
  } else {
    console.log('ARC-SHIP-001 ok', [lon, lat]);
  }
}
if (!found) { console.error('ARC-SHIP-001 missing'); failed++; }
if (failed) process.exit(1);
console.log('check-ship001-baltic-shipyard-densify: pass');
