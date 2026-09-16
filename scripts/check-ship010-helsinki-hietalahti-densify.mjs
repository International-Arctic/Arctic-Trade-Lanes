#!/usr/bin/env node
/** Assert ARC-SHIP-010 densified onto OSM Helsinki Shipyard way/4260855 (gis-densify-0916). */
import { readFileSync } from 'node:fs';
const atlasPath = process.argv[2] || 'dataset/atlas.4326.geojson';
const g = JSON.parse(readFileSync(atlasPath, 'utf8'));
const want = { lon: 24.927293, lat: 60.156499 };
const bad = { lon: 24.95, lat: 60.18 };
let found = false;
let failed = 0;
for (const f of g.features || []) {
  if ((f.properties || {}).id !== 'ARC-SHIP-010') continue;
  found = true;
  const [lon, lat] = f.geometry?.coordinates || [];
  if (Math.abs(lon - bad.lon) < 1e-3 && Math.abs(lat - bad.lat) < 1e-3) {
    console.error('ARC-SHIP-010 still on coarse Helsinki centroid', [lon, lat]);
    failed++;
  } else if (Math.abs(lon - want.lon) > 1e-5 || Math.abs(lat - want.lat) > 1e-5) {
    console.error('ARC-SHIP-010 unexpected coords', [lon, lat], 'want', want);
    failed++;
  } else {
    console.log('ARC-SHIP-010 ok', [lon, lat]);
  }
}
if (!found) { console.error('ARC-SHIP-010 missing'); failed++; }
if (failed) process.exit(1);
console.log('check-ship010-helsinki-hietalahti-densify: pass');
