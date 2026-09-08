#!/usr/bin/env node
/** Assert six densified ports are off city-centroid stacks (GIS Quality Loop 2026-09-08 16:09). */
import fs from 'node:fs';

const EXPECTED = {
  'ARC-PORT-010': { lat: 66.9400725, lon: -53.6749927 },
  'ARC-PORT-013': { lat: 65.6851709, lon: -18.0790671 },
  'ARC-PORT-020': { lat: 58.7759414, lon: -94.1944813 },
  'ARC-PORT-023': { lat: 61.0831733, lon: -146.381728 },
  'ARC-PORT-027': { lat: 65.6747392, lon: 24.5852607 },
  'ARC-PORT-054': { lat: 64.6585543, lon: 24.4178846 },
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

// PORT-146 must remain on Kemin satama (not collide with densified 027)
const p146 = byId.get('ARC-PORT-146');
if (p146) {
  const [lon, lat] = p146;
  const sameAs027 = Math.abs(lat - EXPECTED['ARC-PORT-027'].lat) < 1e-4 && Math.abs(lon - EXPECTED['ARC-PORT-027'].lon) < 1e-4;
  if (sameAs027) {
    console.error('COLLISION ARC-PORT-146 stacked on densified ARC-PORT-027');
    failed++;
  } else {
    console.log('OK ARC-PORT-146 distinct from 027', lat, lon);
  }
}

if (failed) process.exit(1);
console.log('port-city-centroid-densify-1609: pass');
