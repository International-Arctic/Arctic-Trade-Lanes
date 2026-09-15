#!/usr/bin/env node
/**
 * CI: ARC-RAIL-006 Rail Nordica densified off ARC-CITY-036 Kemi city.
 * Anchor: OSM railway=station Kemi node/251738389 (Haparanda/Tornio-Kemi-Oulu corridor hub).
 * Usage: node scripts/check-rail006-kemi-densify.mjs [atlas.4326.geojson]
 */
import { readFileSync } from 'node:fs';

const atlasPath = process.argv[2] || 'dataset/atlas.4326.geojson';
const g = JSON.parse(readFileSync(atlasPath, 'utf8'));
const byId = new Map();
for (const f of g.features || []) {
  const id = f.id || (f.properties || {}).id;
  if (id) byId.set(id, f);
}

const errors = [];
function pt(id) {
  const f = byId.get(id);
  if (!f || f.geometry?.type !== 'Point') {
    errors.push(`missing point ${id}`);
    return null;
  }
  const [lon, lat] = f.geometry.coordinates;
  return { lon, lat };
}

const rail = pt('ARC-RAIL-006');
const city = pt('ARC-CITY-036');
const EXPECT = { lat: 65.736726, lon: 24.574302 };

if (rail) {
  if (Math.abs(rail.lat - EXPECT.lat) > 0.01 || Math.abs(rail.lon - EXPECT.lon) > 0.02) {
    errors.push(
      `ARC-RAIL-006 expected near Kemi station OSM ${EXPECT.lat},${EXPECT.lon} got ${rail.lat},${rail.lon}`,
    );
  }
  if (city) {
    const same6 =
      Math.round(rail.lon * 1e6) === Math.round(city.lon * 1e6) &&
      Math.round(rail.lat * 1e6) === Math.round(city.lat * 1e6);
    const same3 =
      Math.round(rail.lon * 1e3) === Math.round(city.lon * 1e3) &&
      Math.round(rail.lat * 1e3) === Math.round(city.lat * 1e3);
    if (same6 || same3) {
      errors.push('ARC-RAIL-006 still soft-stacked on ARC-CITY-036 Kemi city centroid');
    }
  }
}

if (errors.length) {
  console.error('check-rail006-kemi-densify failed:\n' + errors.join('\n'));
  process.exit(1);
}
console.log(
  'check-rail006-kemi-densify: pass',
  rail && `${rail.lat},${rail.lon}`,
  '(off CITY-036)',
);
