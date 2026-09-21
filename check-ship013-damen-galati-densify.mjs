#!/usr/bin/env node
/** CI lock: ARC-SHIP-013 Damen Galati densified off soft 45.43/28.05 onto WD Q4686063 P625. */
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(fileURLToPath(import.meta.url));
const csv = readFileSync(join(root, 'shipbuilding_facilities.csv'), 'utf8');
const lines = csv.trim().split(/\r?\n/);
const header = lines[0].split(',');
const latIdx = header.indexOf('latitude');
const lonIdx = header.indexOf('longitude');
const idIdx = header.indexOf('shipyard_id');
const srcIdx = header.indexOf('sources');

function parseRow(line) {
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

function find(id) {
  for (const line of lines.slice(1)) {
    const cols = parseRow(line);
    if (cols[idIdx] === id) return cols;
  }
  return null;
}

const row = find('ARC-SHIP-013');
if (!row) { console.error('ARC-SHIP-013 missing'); process.exit(1); }

const lat = Number(row[latIdx]);
const lon = Number(row[lonIdx]);
const src = row[srcIdx] || '';
const TARGET = { lat: 45.44375, lon: 28.085805555555556 };
const eps = 1e-5;

if (Math.abs(lat - TARGET.lat) > eps || Math.abs(lon - TARGET.lon) > eps) {
  console.error('ARC-SHIP-013 densify lock failed', { lat, lon, TARGET });
  process.exit(1);
}
if (Math.abs(lat - 45.43) < 0.005 && Math.abs(lon - 28.05) < 0.005) {
  console.error('ARC-SHIP-013 still on soft pin');
  process.exit(1);
}
if (!src.includes('Q4686063') || !src.includes('gis-densify-1202') || !src.includes('888306100')) {
  console.error('ARC-SHIP-013 sources lock failed', src.slice(0, 240));
  process.exit(1);
}
console.log('check-ship013-damen-galati-densify: pass', { lat, lon });
