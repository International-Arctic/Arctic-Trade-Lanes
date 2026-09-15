#!/usr/bin/env node
/** Assert ARC-PORT-001 densified onto OSM MMTP way/85150513 (gis-densify-1638). */
import { readFileSync } from 'node:fs';
const atlasPath = process.argv[2] || 'dataset/atlas.4326.geojson';
const g = JSON.parse(readFileSync(atlasPath, 'utf8'));
const want = { lon: 33.063447, lat: 68.98092 };
const bad = { lon: 33.061, lat: 68.9841 };
let found = false;
let failed = 0;
for (const f of g.features || []) {
  if ((f.properties || {}).id !== 'ARC-PORT-001') continue;
  found = true;
  const [lon, lat] = f.geometry?.coordinates || [];
  if (Math.abs(lon - bad.lon) < 1e-4 && Math.abs(lat - bad.lat) < 1e-4) {
    console.error('ARC-PORT-001 still on soft-stack', [lon, lat]);
    failed++;
  } else if (Math.abs(lon - want.lon) > 1e-5 || Math.abs(lat - want.lat) > 1e-5) {
    console.error('ARC-PORT-001 unexpected coords', [lon, lat], 'want', want);
    failed++;
  } else {
    console.log('ARC-PORT-001 ok', [lon, lat]);
  }
}
if (!found) { console.error('ARC-PORT-001 missing'); failed++; }
if (failed) process.exit(1);
console.log('check-port001-murmansk-mmtp-densify: pass');
