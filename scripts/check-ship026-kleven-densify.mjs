#!/usr/bin/env node
/** GIS densify check: ARC-SHIP-026 Kleven Verft off soft pin onto Wikidata Q1774285 P159/P625; ≠ ARC-SHIP-072 */
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const root = dirname(fileURLToPath(import.meta.url));
const csvPath = join(root, '..', 'dataset', 'shipbuilding_facilities.csv');
const expectLat = 62.32329874;
const expectLon = 5.84101439;
const softOld = { lat: 62.35, lon: 6.15 };

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
const row026 = lines.find((l) => l.startsWith('ARC-SHIP-026,'));
const row072 = lines.find((l) => l.startsWith('ARC-SHIP-072,'));
if (!row026) { console.error('FAIL: ARC-SHIP-026 missing'); process.exit(1); }
if (!row072) { console.error('FAIL: ARC-SHIP-072 missing'); process.exit(1); }
const f = parseRow(row026);
const g = parseRow(row072);
const lat = Number(f[4]);
const lon = Number(f[5]);
const src = f[13] || '';
const gyLat = Number(g[4]);
const gyLon = Number(g[5]);
const ok =
  Math.abs(lat - expectLat) < 1e-7 &&
  Math.abs(lon - expectLon) < 1e-7 &&
  src.includes('Q1774285') &&
  src.includes('gis-densify-1113') &&
  (Math.abs(lat - softOld.lat) > 0.001 || Math.abs(lon - softOld.lon) > 0.001) &&
  !(Math.abs(lat - gyLat) < 1e-4 && Math.abs(lon - gyLon) < 1e-4);
console.log(JSON.stringify({ id: 'ARC-SHIP-026', lat, lon, expectLat, expectLon, gyLat, gyLon, ok, srcSnippet: src.slice(-220) }, null, 2));
process.exit(ok ? 0 : 1);
