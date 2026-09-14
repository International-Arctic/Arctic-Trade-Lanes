#!/usr/bin/env node
/** CI stub: ARC-PORT-063 densified off city centroid at 5dp (2026-09-14 ~16:37 MSK). */
import { readFileSync } from 'node:fs';

const EXPECTED = {
  // lat, lon
  'ARC-PORT-063': [70.4836789, -21.9625036],
};

const CITY = {
  'ARC-CITY-069': [70.4845, -21.9666],
};

const atlasPath = process.argv[2] || 'dataset/atlas.4326.geojson';
const g = JSON.parse(readFileSync(atlasPath, 'utf8'));
const byId = new Map();
for (const f of g.features || []) {
  const id = f.properties?.id;
  if (id && f.geometry?.type === 'Point') byId.set(id, f.geometry.coordinates);
}
let failed = 0;
for (const [id, [lat, lon]] of Object.entries(EXPECTED)) {
  const c = byId.get(id);
  if (!c) { console.error('MISSING', id); failed++; continue; }
  const [x, y] = c; // lon, lat
  if (Math.abs(y - lat) > 1e-4 || Math.abs(x - lon) > 1e-4) {
    console.error('MISMATCH', id, 'got', y, x, 'want', lat, lon);
    failed++;
  } else {
    console.log('OK', id, y, x);
  }
  const city = byId.get('ARC-CITY-069');
  if (city) {
    const [cx, cy] = city;
    if (y.toFixed(5) === cy.toFixed(5) && x.toFixed(5) === cx.toFixed(5)) {
      console.error('STILL_STACKED_5DP', id, 'with ARC-CITY-069');
      failed++;
    } else {
      console.log('UNSTACKED_5DP', id, 'vs ARC-CITY-069', cy, cx);
    }
  }
}
if (failed) process.exit(1);
console.log('check-port-city-centroid-densify-1637: pass');
