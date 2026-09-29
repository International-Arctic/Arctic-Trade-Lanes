#!/usr/bin/env node
/** CI lock: ARC-FAC-349 Longkou Nanshan LNG densified off soft 37.655/120.325 onto GEM exact 37.680774/120.220284 (gis-densify-1901). */
import { existsSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const candidates = [
  join(here, 'arctic_industrial_facilities.csv'),
  join(here, 'dataset', 'arctic_industrial_facilities.csv'),
  join(here, '..', 'dataset', 'arctic_industrial_facilities.csv'),
  join(here, '..', 'arctic_industrial_facilities.csv'),
  join(here, '..', 'ArcticTradeLanes-Dataset', 'arctic_industrial_facilities.csv'),
  join(here, '..', 'ArcticTradeLanes-Dataset', 'data', 'arctic_industrial_facilities.csv'),
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

const row = find('ARC-FAC-349');
if (!row) { console.error('ARC-FAC-349 missing'); process.exit(1); }

const lat = Number(row[latIdx]);
const lon = Number(row[lonIdx]);
const src = row[srcIdx] || '';
const TARGET = { lat: 37.680774, lon: 120.220284 };
const eps = 1e-4;

if (Math.abs(lat - TARGET.lat) > eps || Math.abs(lon - TARGET.lon) > eps) {
  console.error('ARC-FAC-349 densify lock failed', { lat, lon, TARGET });
  process.exit(1);
}
if (Math.abs(lat - 37.655) < 1e-6 && Math.abs(lon - 120.325) < 1e-6) {
  console.error('ARC-FAC-349 still on soft pin');
  process.exit(1);
}
if (!src.includes('gis-densify-1901') || !src.includes('37.680774')) {
  console.error('ARC-FAC-349 sources lock failed', src.slice(0, 240));
  process.exit(1);
}
console.log('check-fac349-longkou-nanshan-gem-densify: pass', { lat, lon, csv: path });
