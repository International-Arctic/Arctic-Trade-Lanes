#!/usr/bin/env node
/** CI stub: ARC-PORT-024 densified off city centroid at 5dp (2026-09-14 ~17:45 MSK). */
import { readFileSync } from 'node:fs';

const EXPECTED = {
  'ARC-PORT-024': [70.335833333333, -148.36222222222],
};

const atlasPath = process.argv[2] || 'dataset/atlas.4326.geojson';
const g = JSON.parse(readFileSync(atlasPath, 'utf8'));
const byId = new Map();
for (const f of g.features || []) {
  const id = f.properties?.id;
  if (id && f.geometry?.type === 'Point') byId.set(id, { c: f.geometry.coordinates, gq: f.properties?.geo_quality });
}
let failed = 0;
for (const [id, [lat, lon]] of Object.entries(EXPECTED)) {
  const hit = byId.get(id);
  if (!hit) { console.error('MISSING', id); failed++; continue; }
  const [x, y] = hit.c;
  if (Math.abs(y - lat) > 1e-4 || Math.abs(x - lon) > 1e-4) {
    console.error('MISMATCH', id, 'got', y, x, 'want', lat, lon);
    failed++;
  } else {
    console.log('OK', id, y, x);
  }
  if (hit.gq === 'centroid_clone') {
    console.error('STILL_STAMPED_centroid_clone', id);
    failed++;
  }
  const city = byId.get('ARC-CITY-029');
  if (city) {
    const [cx, cy] = city.c;
    if (y.toFixed(5) === cy.toFixed(5) && x.toFixed(5) === cx.toFixed(5)) {
      console.error('STILL_STACKED_5DP', id, 'with ARC-CITY-029');
      failed++;
    } else {
      console.log('UNSTACKED_5DP', id, 'vs ARC-CITY-029', cy, cx);
    }
  }
}
if (failed) process.exit(1);
console.log('check-port-city-centroid-densify-1745: pass');
