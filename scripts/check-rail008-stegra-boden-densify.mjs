#!/usr/bin/env node
/**
 * CI: ARC-RAIL-008 Stegra–Boden Industrial Park rail densified off ARC-FAC-368 soft-stack.
 * Anchor: OSM landuse=construction STEGRA stålverk Boden way/1388001960.
 * Usage: node scripts/check-rail008-stegra-boden-densify.mjs [atlas.4326.geojson]
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

const rail = pt('ARC-RAIL-008');
const fac = pt('ARC-FAC-368');
const EXPECT = { lat: 65.805032, lon: 21.793665 };

if (rail) {
  if (Math.abs(rail.lat - EXPECT.lat) > 0.01 || Math.abs(rail.lon - EXPECT.lon) > 0.02) {
    errors.push(
      `ARC-RAIL-008 expected near Stegra OSM ${EXPECT.lat},${EXPECT.lon} got ${rail.lat},${rail.lon}`,
    );
  }
  if (fac) {
    const same6 =
      Math.round(rail.lon * 1e6) === Math.round(fac.lon * 1e6) &&
      Math.round(rail.lat * 1e6) === Math.round(fac.lat * 1e6);
    const same3 =
      Math.round(rail.lon * 1e3) === Math.round(fac.lon * 1e3) &&
      Math.round(rail.lat * 1e3) === Math.round(fac.lat * 1e3);
    if (same6 || same3) {
      errors.push('ARC-RAIL-008 still soft-stacked on ARC-FAC-368 Boden Industrial Park centroid');
    }
  }
}

if (errors.length) {
  console.error('check-rail008-stegra-boden-densify failed:\n' + errors.join('\n'));
  process.exit(1);
}
console.log(
  'check-rail008-stegra-boden-densify: pass',
  rail && `${rail.lat},${rail.lon}`,
  '(off FAC-368)',
);
