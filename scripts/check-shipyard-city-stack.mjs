#!/usr/bin/env node
/**
 * Lock exact shipyard↔city stacks to the known centroid_clone remainder.
 * Sevgiprorybflot (ARC-SHIP-069) has no named OSM facility in Murmansk —
 * do not invent a yard pin. Fail if a new unstamped stack appears or if
 * SHIP-069 loses its stamp / leaves the Murmansk city pin without updating
 * EXPECTED_STACKS.
 *
 * Usage: node scripts/check-shipyard-city-stack.mjs [atlas.4326.geojson]
 */
import { readFileSync } from 'node:fs';

/** Allowed exact stacks: shipyard id → city id (must be geo_quality=centroid_clone). */
const EXPECTED_STACKS = new Map([
  ['ARC-SHIP-069', 'ARC-CITY-001'], // Bergen Group Sevgiprorybflot ↔ Murmansk
]);

const atlasPath = process.argv[2] || 'dataset/atlas.4326.geojson';
const g = JSON.parse(readFileSync(atlasPath, 'utf8'));

function coordKey(f, digits = 6) {
  const c = f?.geometry?.coordinates;
  if (!Array.isArray(c) || c.length < 2) return null;
  const lon = Number(c[0]);
  const lat = Number(c[1]);
  if (!Number.isFinite(lon) || !Number.isFinite(lat)) return null;
  return `${lon.toFixed(digits)},${lat.toFixed(digits)}`;
}

const citiesByKey = new Map();
for (const f of g.features || []) {
  if ((f.properties || {}).layer !== 'cities') continue;
  const k = coordKey(f);
  if (!k) continue;
  if (!citiesByKey.has(k)) citiesByKey.set(k, []);
  citiesByKey.get(k).push(f);
}

const found = []; // { shipId, cityId, key, gq }
for (const f of g.features || []) {
  const p = f.properties || {};
  if (p.layer !== 'shipyards') continue;
  const k = coordKey(f);
  if (!k || !citiesByKey.has(k)) continue;
  for (const city of citiesByKey.get(k)) {
    found.push({
      shipId: p.id,
      cityId: (city.properties || {}).id,
      key: k,
      gq: String(p.geo_quality || '').toLowerCase(),
      name: p.name,
    });
  }
}

const errors = [];
const foundKeys = new Set(found.map((s) => `${s.shipId}|${s.cityId}`));
const expectedKeys = new Set([...EXPECTED_STACKS.entries()].map(([s, c]) => `${s}|${c}`));

for (const stack of found) {
  const wantCity = EXPECTED_STACKS.get(stack.shipId);
  if (!wantCity) {
    errors.push(
      `unexpected shipyard↔city exact stack: ${stack.shipId} (${stack.name}) ↔ ${stack.cityId} @ ${stack.key} — densify or stamp+update EXPECTED_STACKS`,
    );
    continue;
  }
  if (wantCity !== stack.cityId) {
    errors.push(
      `${stack.shipId} stacked on ${stack.cityId}, expected ${wantCity}`,
    );
  }
  if (stack.gq !== 'centroid_clone') {
    errors.push(
      `${stack.shipId} exact city stack missing geo_quality=centroid_clone (got ${stack.gq || 'none'})`,
    );
  }
}

for (const [shipId, cityId] of EXPECTED_STACKS) {
  if (!foundKeys.has(`${shipId}|${cityId}`)) {
    errors.push(
      `missing expected stack ${shipId}↔${cityId} — if densified onto verifiable OSM, remove from EXPECTED_STACKS`,
    );
  }
}

if (errors.length) {
  console.error('check-shipyard-city-stack failed:');
  for (const e of errors) console.error(' -', e);
  process.exit(1);
}

console.log(
  'check-shipyard-city-stack: pass',
  [...expectedKeys].sort().join(', '),
  `(${found.length} exact stack(s))`,
);
