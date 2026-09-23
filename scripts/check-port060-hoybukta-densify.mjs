#!/usr/bin/env node
/** Assert ARC-PORT-060 densified onto OSM hamlet node/9880257803 Høybukta (gis-densify-1254). */
import { readFileSync } from 'node:fs';
const atlasPath = process.argv[2] || 'dataset/atlas.4326.geojson';
const g = JSON.parse(readFileSync(atlasPath, 'utf8'));
const want = { lon: 29.876194, lat: 69.728857 };
const soft = { lon: 29.95, lat: 69.73 };
let found = false;
let failed = 0;
for (const f of g.features || []) {
  if ((f.properties || {}).id !== 'ARC-PORT-060') continue;
  found = true;
  const [lon, lat] = f.geometry?.coordinates || [];
  if (Math.abs(lon - soft.lon) < 1e-3 && Math.abs(lat - soft.lat) < 1e-3) {
    console.error('ARC-PORT-060 still on soft pin', [lon, lat]);
    failed++;
  } else if (Math.abs(lon - want.lon) > 1e-5 || Math.abs(lat - want.lat) > 1e-5) {
    console.error('ARC-PORT-060 unexpected coords', [lon, lat], 'want', want);
    failed++;
  } else {
    console.log('ARC-PORT-060 ok', [lon, lat]);
  }
}
if (!found) { console.error('ARC-PORT-060 missing'); failed++; }
if (failed) process.exit(1);
console.log('check-port060-hoybukta-densify: pass');
