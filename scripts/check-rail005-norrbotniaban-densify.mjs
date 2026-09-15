#!/usr/bin/env node
/**
 * CI: ARC-RAIL-005 North Bothnia Line densified off ARC-CITY-056 Umeå city.
 * Anchor: OSM railway=construction Norrbotniabanan way/973282865 (Umeå–Dåva first segment).
 * Usage: node scripts/check-rail005-norrbotniaban-densify.mjs [atlas.4326.geojson]
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

const rail = pt('ARC-RAIL-005');
const city = pt('ARC-CITY-056');
const EXPECT = { lat: 63.871859, lon: 20.242932 };

if (rail) {
  if (Math.abs(rail.lat - EXPECT.lat) > 0.02 || Math.abs(rail.lon - EXPECT.lon) > 0.05) {
    errors.push(
      `ARC-RAIL-005 expected near Norrbotniabanan OSM ${EXPECT.lat},${EXPECT.lon} got ${rail.lat},${rail.lon}`,
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
      errors.push('ARC-RAIL-005 still soft-stacked on ARC-CITY-056 Umeå city centroid');
    }
  }
}

if (errors.length) {
  console.error('check-rail005-norrbotniaban-densify failed:\n' + errors.join('\n'));
  process.exit(1);
}
console.log(
  'check-rail005-norrbotniaban-densify: pass',
  rail && `${rail.lat},${rail.lon}`,
  '(off CITY-056)',
);
