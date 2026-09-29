#!/usr/bin/env node
/** CI lock: ARC-PORT-128 Indiga densified off soft 67.6/49.0 onto Cape Bolshoy Rumyanichny 67.5497/47.8522 (gis-densify-1320). */
import { existsSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const candidates = [
  join(here, 'ports.csv'),
  join(here, 'dataset', 'ports.csv'),
  join(here, '..', 'dataset', 'ports.csv'),
  join(here, '..', 'ports.csv'),
  join(here, 'data', 'ports.csv'),
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

const row = find('ARC-PORT-128');
if (!row) { console.error('ARC-PORT-128 missing'); process.exit(1); }

const lat = Number(row[latIdx]);
const lon = Number(row[lonIdx]);
const src = row[srcIdx] || '';
const TARGET = { lat: 67.5497, lon: 47.8522 };
const eps = 1e-4;

if (Math.abs(lat - TARGET.lat) > eps || Math.abs(lon - TARGET.lon) > eps) {
  console.error('ARC-PORT-128 densify lock failed', { lat, lon, TARGET });
  process.exit(1);
}
if (Math.abs(lat - 67.6) < 0.001 && Math.abs(lon - 49.0) < 0.001) {
  console.error('ARC-PORT-128 still on soft pin');
  process.exit(1);
}
if (!src.includes('gis-densify-1320') || !src.includes('ru.wikipedia.org/wiki')) {
  console.error('ARC-PORT-128 sources lock failed', src.slice(0, 240));
  process.exit(1);
}
console.log('check-port128-indiga-densify: pass', { lat, lon, csv: path });
