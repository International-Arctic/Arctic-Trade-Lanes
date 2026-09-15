#!/usr/bin/env node
/**
 * CI: ARC-PORT-153 Steensby Inlet densified off ARC-CITY-100 city clone.
 * Anchor: OSM relation/13745622 Steensby Inlet (natural=bay) center 70.3851175,-79.0793288.
 * Usage: node scripts/check-port153-steensby-densify.mjs [atlas.4326.geojson]
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
  return { lon, lat, gq: f.properties?.geo_quality };
}

const port = pt('ARC-PORT-153');
const city = pt('ARC-CITY-100');
const EXPECT = { lat: 70.3851175, lon: -79.0793288 };

if (port) {
  if (Math.abs(port.lat - EXPECT.lat) > 1e-4 || Math.abs(port.lon - EXPECT.lon) > 1e-4) {
    errors.push(
      `ARC-PORT-153 expected OSM R13745622 ${EXPECT.lat},${EXPECT.lon} got ${port.lat},${port.lon}`,
    );
  }
  if (port.gq === 'centroid_clone') {
    errors.push('ARC-PORT-153 still stamped geo_quality=centroid_clone');
  }
  if (city) {
    const same5 =
      port.lat.toFixed(5) === city.lat.toFixed(5) && port.lon.toFixed(5) === city.lon.toFixed(5);
    if (same5) {
      errors.push('ARC-PORT-153 still soft-stacked on ARC-CITY-100 at 5dp');
    }
  }
}

if (errors.length) {
  console.error('check-port153-steensby-densify failed:\n' + errors.join('\n'));
  process.exit(1);
}
console.log(
  'check-port153-steensby-densify: pass',
  port && `${port.lat},${port.lon}`,
  '(off CITY-100)',
);
