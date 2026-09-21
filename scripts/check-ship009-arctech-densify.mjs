#!/usr/bin/env node
/** GIS densify check: ARC-SHIP-009 Arctech onto Wikidata Q4117007 P625; ≠ ARC-SHIP-010 exact centroid */
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const root = dirname(fileURLToPath(import.meta.url));
const csvPath = join(root, '..', 'dataset', 'shipbuilding_facilities.csv');
const expectLat = 60.158;
const expectLon = 24.929;
const softOld = { lat: 60.17, lon: 24.94 };

function parseRow(line) {
  const fields = [];
  let cur = '', inQ = false;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (ch === '"') { inQ = !inQ; continue; }
    if (ch === ',' && !inQ) { fields.push(cur); cur = ''; continue; }
    cur += ch;
  }
  fields.push(cur);
  return fields;
}

const text = readFileSync(csvPath, 'utf8');
const lines = text.split(/\r?\n/);
const row009 = lines.find((l) => l.startsWith('ARC-SHIP-009,'));
const row010 = lines.find((l) => l.startsWith('ARC-SHIP-010,'));
if (!row009) { console.error('FAIL: ARC-SHIP-009 missing'); process.exit(1); }
if (!row010) { console.error('FAIL: ARC-SHIP-010 missing'); process.exit(1); }
const f = parseRow(row009);
const g = parseRow(row010);
const lat = Number(f[4]);
const lon = Number(f[5]);
const src = f[13] || '';
const hLat = Number(g[4]);
const hLon = Number(g[5]);
const ok =
  Math.abs(lat - expectLat) < 1e-6 &&
  Math.abs(lon - expectLon) < 1e-6 &&
  src.includes('Q4117007') &&
  src.includes('gis-densify-1135') &&
  (Math.abs(lat - softOld.lat) > 0.001 || Math.abs(lon - softOld.lon) > 0.001) &&
  !(Math.abs(lat - hLat) < 1e-4 && Math.abs(lon - hLon) < 1e-4);
console.log(JSON.stringify({ id: 'ARC-SHIP-009', lat, lon, expectLat, expectLon, ship010: { hLat, hLon }, ok, srcSnippet: src.slice(0, 220) }, null, 2));
process.exit(ok ? 0 : 1);
