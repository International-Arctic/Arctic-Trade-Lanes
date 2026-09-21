#!/usr/bin/env node
/** GIS densify check: ARC-SHIP-043 Fosen Yard off soft pin onto Wikidata Q1439358 P159/P625 */
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const root = dirname(fileURLToPath(import.meta.url));
const csvPath = join(root, 'shipbuilding_facilities.csv');
const expectLat = 63.5649722;
const expectLon = 9.8986944;
const softOld = { lat: 64.25, lon: 10.45 };

const text = readFileSync(csvPath, 'utf8');
const line = text.split(/\r?\n/).find((l) => l.startsWith('ARC-SHIP-043,'));
if (!line) { console.error('FAIL: ARC-SHIP-043 missing'); process.exit(1); }
const fields = [];
let cur = '', inQ = false;
for (let i = 0; i < line.length; i++) {
  const ch = line[i];
  if (ch === '"') { inQ = !inQ; continue; }
  if (ch === ',' && !inQ) { fields.push(cur); cur = ''; continue; }
  cur += ch;
}
fields.push(cur);
const lat = Number(fields[4]);
const lon = Number(fields[5]);
const src = fields[13] || '';
const ok =
  Math.abs(lat - expectLat) < 1e-7 &&
  Math.abs(lon - expectLon) < 1e-7 &&
  src.includes('Q1439358') &&
  src.includes('gis-densify-0940') &&
  (Math.abs(lat - softOld.lat) > 0.01 || Math.abs(lon - softOld.lon) > 0.01);
console.log(JSON.stringify({ id: 'ARC-SHIP-043', lat, lon, expectLat, expectLon, ok, srcSnippet: src.slice(-220) }, null, 2));
process.exit(ok ? 0 : 1);
