#!/usr/bin/env node
/** Assert ARC-PORT-043 densified onto OSM harbour way/129101713 (gis-densify-1445). */
import { readFileSync } from 'node:fs';
const atlasPath = process.argv[2] || 'dataset/atlas.4326.geojson';
const g = JSON.parse(readFileSync(atlasPath, 'utf8'));
const want = { lon: -173.23049, lat: 64.421137 };
const bad = { lon: -173.3, lat: 64.3833 };
let found = false;
let failed = 0;
for (const f of g.features || []) {
  if ((f.properties || {}).id !== 'ARC-PORT-043') continue;
  found = true;
  const [lon, lat] = f.geometry?.coordinates || [];
  if (Math.abs(lon - bad.lon) < 1e-4 && Math.abs(lat - bad.lat) < 1e-4) {
    console.error('ARC-PORT-043 still on soft-stack', [lon, lat]);
    failed++;
  } else if (Math.abs(lon - want.lon) > 1e-5 || Math.abs(lat - want.lat) > 1e-5) {
    console.error('ARC-PORT-043 unexpected coords', [lon, lat], 'want', want);
    failed++;
  } else {
    console.log('ARC-PORT-043 ok', [lon, lat]);
  }
}
if (!found) { console.error('ARC-PORT-043 missing'); failed++; }
if (failed) process.exit(1);
console.log('check-port043-provideniya-harbour-densify: pass');
