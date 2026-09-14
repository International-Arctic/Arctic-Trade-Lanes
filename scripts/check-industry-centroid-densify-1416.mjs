#!/usr/bin/env node
/** CI: ARC-FAC-012 / ARC-FAC-351 densified off city centroids (2026-09-14 14:16). */
import { readFileSync, existsSync } from 'node:fs';
import { resolve } from 'node:path';

const root = resolve(new URL('..', import.meta.url).pathname);
const atlasCandidates = [
  resolve(root, 'dataset/atlas.4326.geojson'),
  resolve(root, '../ArcticTradeLanes-Dataset/atlas.4326.geojson'),
];
const atlasPath = atlasCandidates.find((p) => existsSync(p));
if (!atlasPath) {
  console.error('SKIP: no atlas.4326.geojson (ok if dataset not vendored)');
  process.exit(0);
}
const fc = JSON.parse(readFileSync(atlasPath, 'utf8'));
const byId = new Map();
for (const f of fc.features || []) {
  if (f.id) byId.set(String(f.id), f);
}
const cities = new Map();
for (const f of fc.features || []) {
  if ((f.properties || {}).layer === 'cities' && f.id) {
    const [lon, lat] = f.geometry.coordinates;
    cities.set(String(f.id), { lon, lat });
  }
}
const expect = {
  'ARC-FAC-012': { lat: 64.4976121, lon: -165.40514, city: 'ARC-CITY-034' },
  'ARC-FAC-351': { lat: 51.8692789, lon: -176.6701699, city: 'ARC-CITY-090' },
};
let failed = 0;
for (const [id, exp] of Object.entries(expect)) {
  const f = byId.get(id);
  if (!f) {
    console.error('MISSING', id);
    failed++;
    continue;
  }
  const [lon, lat] = f.geometry.coordinates;
  if (Math.abs(lat - exp.lat) > 1e-5 || Math.abs(lon - exp.lon) > 1e-5) {
    console.error('BAD COORDS', id, lat, lon, 'expected', exp.lat, exp.lon);
    failed++;
  }
  const city = cities.get(exp.city);
  if (city && lat.toFixed(5) === city.lat.toFixed(5) && lon.toFixed(5) === city.lon.toFixed(5)) {
    console.error('STILL STACKED ON CITY', id, exp.city);
    failed++;
  }
}
// stamped clones should include shipyard 069
const ship = byId.get('ARC-SHIP-069');
if (ship && (ship.properties || {}).geo_quality !== 'centroid_clone') {
  console.error('ARC-SHIP-069 missing centroid_clone stamp');
  failed++;
}
if (failed) {
  console.error('FAIL', failed);
  process.exit(1);
}
console.log('OK industry densify 1416 + SHIP-069 stamp');
