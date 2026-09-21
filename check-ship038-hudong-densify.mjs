#!/usr/bin/env node
/** CI lock: ARC-SHIP-038 Hudong densified off soft 31.27/121.54 onto OSM way/165711825 Pudong Zhujiamen. */
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

const row = find('ARC-SHIP-038');
if (!row) { console.error('ARC-SHIP-038 missing'); process.exit(1); }

const lat = Number(row[latIdx]);
const lon = Number(row[lonIdx]);
const src = row[srcIdx] || '';
const TARGET = { lat: 31.2797045, lon: 121.5698527 };
const eps = 1e-5;

if (Math.abs(lat - TARGET.lat) > eps || Math.abs(lon - TARGET.lon) > eps) {
  console.error('ARC-SHIP-038 densify lock failed', { lat, lon, TARGET });
  process.exit(1);
}
if (Math.abs(lat - 31.27) < 0.005 && Math.abs(lon - 121.54) < 0.005) {
  console.error('ARC-SHIP-038 still on soft pin');
  process.exit(1);
}
if (!src.includes('165711825') || !src.includes('gis-densify-1754') || !src.includes('Hudong')) {
  console.error('ARC-SHIP-038 sources lock failed', src.slice(0, 240));
  process.exit(1);
}
console.log('check-ship038-hudong-densify: pass', { lat, lon, csv: path });
