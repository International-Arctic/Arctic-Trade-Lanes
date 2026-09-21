#!/usr/bin/env node
/** GIS densify check: ARC-SHIP-044 Havyard off soft pin onto Wikidata Q55947781 P625 */
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const csvPath = join(root, 'dataset/shipbuilding_facilities.csv');
const atlasPath = process.argv[2] || join(root, 'dataset/atlas.4326.geojson');
const expectLat = 61.1245683;
const expectLon = 5.3234446;
const softOld = { lat: 61.18, lon: 6.08 };

function parseCsv() {
  const text = readFileSync(csvPath, 'utf8');
  const line = text.split(/\r?\n/).find((l) => l.startsWith('ARC-SHIP-044,'));
  if (!line) throw new Error('ARC-SHIP-044 missing from CSV');
  const fields = [];
  let cur = '', inQ = false;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (ch === '"') { inQ = !inQ; continue; }
    if (ch === ',' && !inQ) { fields.push(cur); cur = ''; continue; }
    cur += ch;
  }
  fields.push(cur);
  return { lat: Number(fields[4]), lon: Number(fields[5]), src: fields[13] || '' };
}

const row = parseCsv();
const atlas = JSON.parse(readFileSync(atlasPath, 'utf8'));
const feat = atlas.features.find((f) => (f.properties || {}).id === 'ARC-SHIP-044');
if (!feat) { console.error('FAIL: ARC-SHIP-044 missing from atlas'); process.exit(1); }
const [alon, alat] = feat.geometry.coordinates;
const ok =
  Math.abs(row.lat - expectLat) < 1e-7 &&
  Math.abs(row.lon - expectLon) < 1e-7 &&
  Math.abs(alat - expectLat) < 1e-5 &&
  Math.abs(alon - expectLon) < 1e-5 &&
  row.src.includes('Q55947781') &&
  (Math.abs(row.lat - softOld.lat) > 0.01 || Math.abs(row.lon - softOld.lon) > 0.01);
console.log(JSON.stringify({ id: 'ARC-SHIP-044', csv: row, atlas: [alon, alat], expectLat, expectLon, ok }, null, 2));
process.exit(ok ? 0 : 1);
