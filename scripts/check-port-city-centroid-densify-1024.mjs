#!/usr/bin/env node
/** Assert Barentsburg / Salekhard / Utrenniy / Vopnafjörður densified off city centroids (GIS Quality Loop 2026-09-14 10:24 MSK). */
import fs from 'node:fs';

const EXPECTED = {
  'ARC-PORT-149': { lat: 78.0621120, lon: 14.2026026 }, // Barentsburg coal berth OSM way/741977198
  'ARC-PORT-033': { lat: 66.5228621, lon: 66.6011381 }, // Salekhard ferry terminal OSM node/8611184008
  'ARC-PORT-137': { lat: 71.0093732, lon: 73.7891686 }, // Utrenniy Arctic LNG 2 pier OSM way/651001100
  'ARC-PORT-155': { lat: 65.7555718, lon: -14.8223849 }, // Vopnafjörður Löndunarbryggja OSM way/220753596
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
console.log('port-city-centroid-densify-1024: pass');
