#!/usr/bin/env node
/** CI: ARC-FAC-335 / 337 / 342 densified off city centroids (2026-09-14 ~14:47 MSK). */
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
  const id = f.id || (f.properties || {}).id;
  if (id) byId.set(String(id), f);
}
const expect = {
  'ARC-FAC-335': { lat: 62.4238429, lon: -114.4226383, city: 'ARC-CITY-023' },
  'ARC-FAC-337': { lat: 67.2916525, lon: 14.4076229, city: 'ARC-CITY-020' },
  'ARC-FAC-342': { lat: 64.5325868, lon: 40.5171670, city: 'ARC-CITY-002' },
};
const cities = new Map();
for (const f of fc.features || []) {
  const p = f.properties || {};
  const id = f.id || p.id;
  if (p.layer === 'cities' && id) {
    const [lon, lat] = f.geometry.coordinates;
    cities.set(String(id), { lon, lat });
  }
}
let failed = 0;
for (const [id, exp] of Object.entries(expect)) {
  const f = byId.get(id);
  if (!f) { console.error('MISSING', id); failed++; continue; }
  const [lon, lat] = f.geometry.coordinates;
  if (Math.abs(lat - exp.lat) > 1e-4 || Math.abs(lon - exp.lon) > 1e-4) {
    console.error('BAD COORDS', id, lat, lon, 'expected', exp.lat, exp.lon);
    failed++;
  }
  const city = cities.get(exp.city);
  if (city && lat.toFixed(5) === city.lat.toFixed(5) && lon.toFixed(5) === city.lon.toFixed(5)) {
    console.error('STILL STACKED ON CITY', id, exp.city);
    failed++;
  }
}
if (failed) { console.error('FAIL', failed); process.exit(1); }
console.log('OK industry densify 1447 (FAC-335/337/342)');
