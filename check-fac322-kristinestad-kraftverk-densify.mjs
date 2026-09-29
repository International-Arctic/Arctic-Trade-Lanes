#!/usr/bin/env node
/** CI lock: ARC-FAC-322 Kristinestad densified off soft 62.2700/21.4400 onto OSM way/40644756 62.2570713/21.3234120 (gis-densify-1528). */
import { existsSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const candidates = [
  join(here, 'arctic_industrial_facilities.csv'),
  join(here, 'dataset', 'arctic_industrial_facilities.csv'),
  join(here, '..', 'dataset', 'arctic_industrial_facilities.csv'),
  join(here, '..', 'arctic_industrial_facilities.csv'),
];
const path = candidates.find((p) => existsSync(p));
if (!path) { console.error('arctic_industrial_facilities.csv not found'); process.exit(1); }
const csv = readFileSync(path, 'utf8');
const lines = csv.trim().split(/\r?\n/);
const header = lines[0].split(',');
const latIdx = header.indexOf('latitude');
const lonIdx = header.indexOf('longitude');
const idIdx = header.indexOf('program_id');
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

const row = find('ARC-FAC-322');
if (!row) { console.error('ARC-FAC-322 missing'); process.exit(1); }

const lat = Number(row[latIdx]);
const lon = Number(row[lonIdx]);
const src = row[srcIdx] || '';
const TARGET = { lat: 62.2570713, lon: 21.3234120 };
const eps = 1e-4;

if (Math.abs(lat - TARGET.lat) > eps || Math.abs(lon - TARGET.lon) > eps) {
  console.error('ARC-FAC-322 densify lock failed', { lat, lon, TARGET });
  process.exit(1);
}
if (Math.abs(lat - 62.27) < 1e-6 && Math.abs(lon - 21.44) < 1e-6) {
  console.error('ARC-FAC-322 still on soft pin');
  process.exit(1);
}
if (!src.includes('gis-densify-1528') || !src.includes('40644756')) {
  console.error('ARC-FAC-322 sources lock failed', src.slice(0, 240));
  process.exit(1);
}
console.log('check-fac322-kristinestad-kraftverk-densify: pass', { lat, lon, csv: path });
