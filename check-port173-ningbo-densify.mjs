#!/usr/bin/env node
/** CI lock: ARC-PORT-173 Ningbo-Zhoushan densified off soft 29.8700/121.5500 onto OSM way/172381552. */
import { existsSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const candidates = [
  join(here, 'ports.csv'),
  join(here, 'dataset', 'ports.csv'),
  join(here, '..', 'dataset', 'ports.csv'),
  join(here, '..', 'ports.csv'),
];
const path = candidates.find((p) => existsSync(p));
if (!path) { console.error('ports.csv not found'); process.exit(1); }
const csv = readFileSync(path, 'utf8');
const lines = csv.trim().split(/\r?\n/);
const header = lines[0].split(',');
const latIdx = header.indexOf('latitude');
const lonIdx = header.indexOf('longitude');
const idIdx = header.indexOf('port_id');
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

const row = find('ARC-PORT-173');
if (!row) { console.error('ARC-PORT-173 missing'); process.exit(1); }

const lat = Number(row[latIdx]);
const lon = Number(row[lonIdx]);
const src = row[srcIdx] || '';
const TARGET = { lat: 29.9392024, lon: 121.8373241 };
const eps = 1e-5;

if (Math.abs(lat - TARGET.lat) > eps || Math.abs(lon - TARGET.lon) > eps) {
  console.error('ARC-PORT-173 densify lock failed', { lat, lon, TARGET });
  process.exit(1);
}
if (Math.abs(lat - 29.87) < 0.001 && Math.abs(lon - 121.55) < 0.001) {
  console.error('ARC-PORT-173 still on soft pin');
  process.exit(1);
}
if (!src.includes('172381552') || !src.includes('gis-densify-1458')) {
  console.error('ARC-PORT-173 sources lock failed', src.slice(0, 240));
  process.exit(1);
}
console.log('check-port173-ningbo-densify: pass', { lat, lon, csv: path });
