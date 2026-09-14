#!/usr/bin/env node
/** Assert Tiksi + Ny-Ålesund densified off city centroids (GIS Quality Loop 2026-09-14 09:36 MSK). */
import fs from 'node:fs';

const EXPECTED = {
  'ARC-PORT-006': { lat: 71.6453769, lon: 128.8907265 },
  'ARC-PORT-144': { lat: 78.9280349, lon: 11.9358348 },
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
console.log('port-city-centroid-densify-0936: pass');
