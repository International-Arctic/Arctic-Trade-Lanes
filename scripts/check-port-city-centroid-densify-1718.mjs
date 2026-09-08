#!/usr/bin/env node
/** Assert six densified ports are off city-centroid stacks (GIS Quality Loop 2026-09-08 17:18 MSK). */
import fs from 'node:fs';

const EXPECTED = {
  'ARC-PORT-070': { lat: 65.411542, lon: -52.8992878 },
  'ARC-PORT-071': { lat: 71.0374618, lon: 27.842285 },
  'ARC-PORT-072': { lat: 70.237943, lon: 22.3496727 },
  'ARC-PORT-095': { lat: 70.9479126, lon: 27.3353868 },
  'ARC-PORT-098': { lat: 60.1189282, lon: -149.4278488 },
  'ARC-PORT-162': { lat: 62.2410997, lon: -6.8188386 },
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
console.log('port-city-centroid-densify-1718: pass');
