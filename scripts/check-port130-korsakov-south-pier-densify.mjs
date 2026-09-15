#!/usr/bin/env node
/** Assert ARC-PORT-130 densified onto OSM pier way/104497425 (gis-densify-1551). */
import { readFileSync } from 'node:fs';
const atlasPath = process.argv[2] || 'dataset/atlas.4326.geojson';
const g = JSON.parse(readFileSync(atlasPath, 'utf8'));
const want = { lon: 142.759969, lat: 46.620285 };
const bad = { lon: 142.774, lat: 46.6347 };
let found = false;
let failed = 0;
for (const f of g.features || []) {
  if ((f.properties || {}).id !== 'ARC-PORT-130') continue;
  found = true;
  const [lon, lat] = f.geometry?.coordinates || [];
  if (Math.abs(lon - bad.lon) < 1e-4 && Math.abs(lat - bad.lat) < 1e-4) {
    console.error('ARC-PORT-130 still on soft-stack', [lon, lat]);
    failed++;
  } else if (Math.abs(lon - want.lon) > 1e-5 || Math.abs(lat - want.lat) > 1e-5) {
    console.error('ARC-PORT-130 unexpected coords', [lon, lat], 'want', want);
    failed++;
  } else {
    console.log('ARC-PORT-130 ok', [lon, lat]);
  }
}
if (!found) { console.error('ARC-PORT-130 missing'); failed++; }
if (failed) process.exit(1);
console.log('check-port130-korsakov-south-pier-densify: pass');
