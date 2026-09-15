#!/usr/bin/env node
/**
 * CI: ARC-FAC-387 Nordgold Lenotap GOK densified off ARC-PORT-042 Egvekinot harbour.
 * Anchor: OSM waterway Ленотап way/649821635 (Nominatim); Iultin locality way/649821750 cross-check.
 * Usage: node scripts/check-fac387-lenotap-densify.mjs [atlas.4326.geojson]
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

const fac = pt('ARC-FAC-387');
const port = pt('ARC-PORT-042');

// Expected densify band: Lenotap river / Iultin mining district (~67.88–67.94N, ~178.7–178.95W)
const EXPECT = { lat: 67.938146, lon: -178.93125 };
if (fac) {
  if (Math.abs(fac.lat - EXPECT.lat) > 0.05 || Math.abs(fac.lon - EXPECT.lon) > 0.25) {
    errors.push(
      `ARC-FAC-387 expected near Lenotap OSM ${EXPECT.lat},${EXPECT.lon} got ${fac.lat},${fac.lon}`,
    );
  }
  // Must not remain on Egvekinot harbour soft-stack
  if (port) {
    const same6 =
      Math.round(fac.lon * 1e6) === Math.round(port.lon * 1e6) &&
      Math.round(fac.lat * 1e6) === Math.round(port.lat * 1e6);
    const same3 =
      Math.round(fac.lon * 1e3) === Math.round(port.lon * 1e3) &&
      Math.round(fac.lat * 1e3) === Math.round(port.lat * 1e3);
    if (same6 || same3) {
      errors.push('ARC-FAC-387 still soft-stacked on ARC-PORT-042 Egvekinot harbour');
    }
  }
  // Must be well north of Egvekinot town/harbour (~66.3N)
  if (fac.lat < 67.5) {
    errors.push(`ARC-FAC-387 still south of Iultin/Lenotap mining band (${fac.lat})`);
  }
}

if (errors.length) {
  console.error('check-fac387-lenotap-densify failed:\n' + errors.join('\n'));
  process.exit(1);
}
console.log(
  'check-fac387-lenotap-densify: pass',
  fac && `${fac.lat},${fac.lon}`,
  '(off PORT-042)',
);
