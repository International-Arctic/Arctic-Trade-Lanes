#!/usr/bin/env node
/** Assert three densified ports are off city-centroid stacks (GIS Quality Loop 2026-09-14 09:14 MSK). */
import fs from 'node:fs';

const EXPECTED = {
  'ARC-PORT-004': { lat: 71.2804697, lon: 72.061166 },
  'ARC-PORT-007': { lat: 73.5043654, lon: 80.5151725 },
  'ARC-PORT-008': { lat: 71.9841653, lon: 102.4753286 },
};

const path = process.argv[2] || 'dataset/atlas.4326.geojson';
const fc = JSON.parse(fs.readFileSync(path, 'utf8'));
const byId = new Map();
for (const f of fc.features || []) {
  const p = f.properties || {};
  const id = p.id || p.program_id;
  if (id && f.geometry?.type === 'Point') byId.set(id, f.geometry.coordinates);
}

let failed = 0;
for (const [id, exp] of Object.entries(EXPECTED)) {
  const c = byId.get(id);
  if (!c) {
    console.error('MISSING', id);
    failed++;
    continue;
  }
  const [lon, lat] = c;
  const ok = Math.abs(lat - exp.lat) < 1e-4 && Math.abs(lon - exp.lon) < 1e-4;
  if (!ok) {
    console.error('MISMATCH', id, { got: [lat, lon], exp });
    failed++;
  } else {
    console.log('OK', id, lat, lon);
  }
}

if (failed) process.exit(1);
console.log('port-city-centroid-densify-0914: pass');
