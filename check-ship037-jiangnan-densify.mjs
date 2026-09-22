#!/usr/bin/env node
/** CI lock: ARC-SHIP-037 Jiangnan densified off soft 31.3533/121.6917 onto OSM way/145733398 Changxing. */
import { existsSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const candidates = [
  join(here, 'shipbuilding_facilities.csv'),
  join(here, 'dataset', 'shipbuilding_facilities.csv'),
  join(here, '..', 'dataset', 'shipbuilding_facilities.csv'),
  join(here, '..', 'shipbuilding_facilities.csv'),
];
const path = candidates.find((p) => existsSync(p));
if (!path) { console.error('shipbuilding_facilities.csv not found'); process.exit(1); }
const csv = readFileSync(path, 'utf8');
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

const row = find('ARC-SHIP-037');
if (!row) { console.error('ARC-SHIP-037 missing'); process.exit(1); }

const lat = Number(row[latIdx]);
const lon = Number(row[lonIdx]);
const src = row[srcIdx] || '';
const TARGET = { lat: 31.3557037, lon: 121.7415905 };
const eps = 1e-5;

if (Math.abs(lat - TARGET.lat) > eps || Math.abs(lon - TARGET.lon) > eps) {
  console.error('ARC-SHIP-037 densify lock failed', { lat, lon, TARGET });
  process.exit(1);
}
if (Math.abs(lat - 31.3533) < 0.001 && Math.abs(lon - 121.6917) < 0.001) {
  console.error('ARC-SHIP-037 still on soft pin');
  process.exit(1);
}
if (!src.includes('145733398') || !src.includes('gis-densify-0920') || !src.includes('Jiangnan')) {
  console.error('ARC-SHIP-037 sources lock failed', src.slice(0, 240));
  process.exit(1);
}
console.log('check-ship037-jiangnan-densify: pass', { lat, lon, csv: path });
