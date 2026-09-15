#!/usr/bin/env node
/**
 * Assert atlas centroid_clone quarantine set stays the known help-wanted remainder.
 * Usage: node scripts/check-centroid-clone-remaining.mjs [atlas.4326.geojson]
 */
import { readFileSync } from 'node:fs';

const EXPECTED = new Set([
  'ARC-PORT-034', // Obskaya LNG — semantic/rail vs marine LNG mismatch; leave for owner
  'ARC-PORT-069', // Chevak planned barge landing — no pier/harbour OSM
  'ARC-SHIP-069', // Sevgiprorybflot Murmansk HQ still on city centroid
]);

const atlasPath = process.argv[2] || 'dataset/atlas.4326.geojson';
const g = JSON.parse(readFileSync(atlasPath, 'utf8'));
const found = new Set();
for (const f of g.features || []) {
  const p = f.properties || {};
  if (String(p.geo_quality || '').toLowerCase() === 'centroid_clone') {
    found.add(p.id);
  }
}

const missing = [...EXPECTED].filter((id) => !found.has(id));
const extra = [...found].filter((id) => !EXPECTED.has(id));
let failed = 0;
if (missing.length) {
  console.error('MISSING expected centroid_clone:', missing.join(', '));
  failed++;
}
if (extra.length) {
  console.error('UNEXPECTED centroid_clone (densify or update EXPECTED):', extra.join(', '));
  failed++;
}
if (found.size !== EXPECTED.size) {
  console.error('count mismatch', found.size, 'vs', EXPECTED.size);
  failed++;
}
if (failed) process.exit(1);
console.log('check-centroid-clone-remaining: pass', [...found].sort().join(', '));
