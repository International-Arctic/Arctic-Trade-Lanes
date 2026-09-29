#!/usr/bin/env node
/** CI lock: ARC-FAC-321 ETFuels Ranua Näätäaapa densified off soft 65.9300/26.5100 onto WD Q24322521 P625 65.933333333333/26.2 (gis-densify-1657). */
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

const row = find('ARC-FAC-321');
if (!row) { console.error('ARC-FAC-321 missing'); process.exit(1); }

const lat = Number(row[latIdx]);
const lon = Number(row[lonIdx]);
const src = row[srcIdx] || '';
const TARGET = { lat: 65.933333333333, lon: 26.2 };
const eps = 1e-4;

if (Math.abs(lat - TARGET.lat) > eps || Math.abs(lon - TARGET.lon) > eps) {
  console.error('ARC-FAC-321 densify lock failed', { lat, lon, TARGET });
  process.exit(1);
}
if (Math.abs(lat - 65.93) < 1e-6 && Math.abs(lon - 26.51) < 1e-6) {
  console.error('ARC-FAC-321 still on soft pin');
  process.exit(1);
}
if (!src.includes('gis-densify-1657') || !src.includes('Q24322521')) {
  console.error('ARC-FAC-321 sources lock failed', src.slice(0, 240));
  process.exit(1);
}
console.log('check-fac321-naataaapa-wd-densify: pass', { lat, lon, csv: path });
