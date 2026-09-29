#!/usr/bin/env node
/** CI lock: ARC-FAC-390 Pavlovskoye densified off soft 72.12/53.42 onto WD Q4341836 P625 72.8521/53.7067 (gis-densify-1119). */
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

const row = find('ARC-FAC-390');
if (!row) { console.error('ARC-FAC-390 missing'); process.exit(1); }

const lat = Number(row[latIdx]);
const lon = Number(row[lonIdx]);
const src = row[srcIdx] || '';
const TARGET = { lat: 72.8521, lon: 53.7067 };
const eps = 1e-4;

if (Math.abs(lat - TARGET.lat) > eps || Math.abs(lon - TARGET.lon) > eps) {
  console.error('ARC-FAC-390 densify lock failed', { lat, lon, TARGET });
  process.exit(1);
}
if (Math.abs(lat - 72.12) < 0.001 && Math.abs(lon - 53.42) < 0.001) {
  console.error('ARC-FAC-390 still on soft pin');
  process.exit(1);
}
if (!src.includes('gis-densify-1119') || !src.includes('Q4341836')) {
  console.error('ARC-FAC-390 sources lock failed', src.slice(0, 240));
  process.exit(1);
}
console.log('check-fac390-pavlovskoye-densify: pass', { lat, lon, csv: path });
