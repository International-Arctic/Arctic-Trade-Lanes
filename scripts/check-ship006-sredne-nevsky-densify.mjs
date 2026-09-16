#!/usr/bin/env node
/** Assert ARC-SHIP-006 densified onto OSM Sredne-Nevsky relation/2830545 (gis-densify-1036). */
import { readFileSync } from 'node:fs';
const atlasPath = process.argv[2] || 'dataset/atlas.4326.geojson';
const g = JSON.parse(readFileSync(atlasPath, 'utf8'));
const want = { lon: 30.629452, lat: 59.788468 };
const bad = { lon: 30.2000, lat: 59.8750 };
const severnaya = { lon: 30.233195, lat: 59.875194 };
let found = false;
let failed = 0;
for (const f of g.features || []) {
  if ((f.properties || {}).id !== 'ARC-SHIP-006') continue;
  found = true;
  const [lon, lat] = f.geometry?.coordinates || [];
  if (Math.abs(lon - bad.lon) < 1e-3 && Math.abs(lat - bad.lat) < 1e-3) {
    console.error('ARC-SHIP-006 still on St. Petersburg soft-pin', [lon, lat]);
    failed++;
  } else if (Math.abs(lon - severnaya.lon) < 1e-3 && Math.abs(lat - severnaya.lat) < 1e-3) {
    console.error('ARC-SHIP-006 conflated with ARC-SHIP-003 Severnaya', [lon, lat]);
    failed++;
  } else if (Math.abs(lon - want.lon) > 1e-4 || Math.abs(lat - want.lat) > 1e-4) {
    console.error('ARC-SHIP-006 unexpected coords', [lon, lat], 'want', want);
    failed++;
  } else {
    console.log('ARC-SHIP-006 ok', [lon, lat]);
  }
}
if (!found) { console.error('ARC-SHIP-006 missing'); failed++; }
if (failed) process.exit(1);
console.log('check-ship006-sredne-nevsky-densify: pass');
