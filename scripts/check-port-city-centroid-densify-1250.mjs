#!/usr/bin/env node
/** CI stub: densified ports must not share city centroid at 5dp (2026-09-14 ~12:50). */
import { readFileSync } from 'node:fs';

const EXPECTED = {
  'ARC-PORT-002': [64.5325868, 40.517167],
  'ARC-PORT-003': [69.4220612, 86.1447027],
  'ARC-PORT-005': [69.7052842, 170.2556335],
  'ARC-PORT-038': [69.1138158, -105.0597084],
  'ARC-PORT-059': [59.4509629, -135.3232692],
  'ARC-PORT-067': [59.6424035, -151.5194138],
  'ARC-PORT-092': [69.7938584, 20.9379571],
  'ARC-PORT-108': [53.9071465, -166.5097581],
  'ARC-PORT-170': [60.5433947, -145.765308],
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
}
if (failed) process.exit(1);
console.log('check-port-city-centroid-densify-1250: pass');
