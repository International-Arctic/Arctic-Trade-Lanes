#!/usr/bin/env node
/**
 * good first issue helper: fail if known-bad shipyard pins reappear,
 * or if any shipyard Feature has blank/null coords while claiming a Point,
 * or if banned duplicate ids are present.
 *
 * Usage: node scripts/check-shipyard-pins.mjs path/to/atlas.4326.geojson
 */
import fs from 'node:fs';

const path = process.argv[2];
if (!path) {
  console.error('usage: node scripts/check-shipyard-pins.mjs <atlas.4326.geojson>');
  process.exit(2);
}

const bannedIds = new Set(['ARC-SHIP-028', 'ARC-SHIP-059']);
const atlas = JSON.parse(fs.readFileSync(path, 'utf8'));
const ships = (atlas.features || []).filter(
  (f) => (f.properties || {}).layer === 'shipyards'
);

const errors = [];
for (const f of ships) {
  const id = (f.properties || {}).id;
  if (bannedIds.has(id)) errors.push(`banned duplicate id present: ${id}`);
  if (id === 'ARC-SHIP-075') errors.push('ARC-SHIP-075 must not be in atlas until site coords are verified');
  const g = f.geometry || {};
  if (g.type === 'Point') {
    const [lon, lat] = g.coordinates || [];
    if (!Number.isFinite(lon) || !Number.isFinite(lat)) errors.push(`${id}: non-finite coords`);
  }
}

 // Aker Arctic should not share Arctech Helsinki centroid
const byCoord = new Map();
for (const f of ships) {
  const [lon, lat] = (f.geometry && f.geometry.coordinates) || [];
  if (!Number.isFinite(lon)) continue;
  const key = `${lon.toFixed(4)},${lat.toFixed(4)}`;
  if (!byCoord.has(key)) byCoord.set(key, []);
  byCoord.get(key).push((f.properties || {}).id);
}
const arctech = ships.find((f) => (f.properties || {}).id === 'ARC-SHIP-009');
const aker = ships.find((f) => (f.properties || {}).id === 'ARC-SHIP-014');
if (arctech && aker) {
  const a = arctech.geometry.coordinates;
  const b = aker.geometry.coordinates;
  if (a[0].toFixed(4) === b[0].toFixed(4) && a[1].toFixed(4) === b[1].toFixed(4)) {
    errors.push('ARC-SHIP-014 still stacked on ARC-SHIP-009 Helsinki centroid');
  }
}

if (errors.length) {
  console.error('shipyard pin QA failed:');
  for (const e of errors) console.error(' -', e);
  process.exit(1);
}
console.log(`ok: ${ships.length} shipyards, no banned dups / TBD ghost pins`);
