#!/usr/bin/env node
/** Assert nine densified ports are off city-centroid stacks (GIS Quality Loop 2026-09-09 09:09 MSK). */
import fs from 'node:fs';

const EXPECTED = {
  'ARC-PORT-009': { lat: 64.17278, lon: -51.7225536 },
  'ARC-PORT-011': { lat: 69.2241501, lon: -51.0988283 },
  'ARC-PORT-021': { lat: 63.7230185, lon: -68.5226163 },
  'ARC-PORT-026': { lat: 64.4960224, lon: -165.4376724 },
  'ARC-PORT-057': { lat: 62.0084594, lon: -6.7674851 },
  'ARC-PORT-062': { lat: 68.7088992, lon: -52.8732373 },
  'ARC-PORT-077': { lat: 66.0708207, lon: -23.1241308 },
  'ARC-PORT-163': { lat: 62.2530714, lon: -6.5815773 },
  'ARC-PORT-172': { lat: 58.1436937, lon: 7.9883855 },
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
console.log('port-city-centroid-densify-0909: pass');
