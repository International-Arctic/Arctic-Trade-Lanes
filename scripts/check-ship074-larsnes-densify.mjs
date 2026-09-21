#!/usr/bin/env node
/** CI lock: ARC-SHIP-074 Larsnes Mek densified off soft 62.45/6.09 onto WD Q52502362 P625. */
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const csv = readFileSync(join(root, 'shipbuilding_facilities.csv'), 'utf8');
const lines = csv.trim().split(/\r?\n/);
const header = lines[0].split(',');
const latIdx = header.indexOf('latitude');
const lonIdx = header.indexOf('longitude');
const idIdx = header.indexOf('shipyard_id');

function parseRow(line) {
  // naive CSV split respecting quotes
  const cols = [];
  let cur = '', inQ = false;
  for (let i = 0; i < line.length; i++) {
    const c = line[i];
    if (c === '"') { inQ = !inQ; continue; }
    if (c === ',' && !inQ) { cols.push(cur); cur = ''; continue; }
    cur += c;
  }
  cols.push(cur);
  return cols;
}

let row = null;
for (const line of lines.slice(1)) {
  const cols = parseRow(line);
  if (cols[idIdx] === 'ARC-SHIP-074') { row = cols; break; }
}
if (!row) {
  console.error('ARC-SHIP-074 missing');
  process.exit(1);
}
const lat = Number(row[latIdx]);
const lon = Number(row[lonIdx]);
const TARGET = { lat: 62.203405, lon: 5.572472 };
const eps = 1e-5;
if (Math.abs(lat - TARGET.lat) > eps || Math.abs(lon - TARGET.lon) > eps) {
  console.error('ARC-SHIP-074 densify lock failed', { lat, lon, TARGET });
  process.exit(1);
}
if (Math.abs(lat - 62.45) < 0.01 && Math.abs(lon - 6.09) < 0.01) {
  console.error('ARC-SHIP-074 still on soft pin');
  process.exit(1);
}
console.log('check-ship074-larsnes-densify: pass', { lat, lon });
