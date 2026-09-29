#!/usr/bin/env node
/** CI lock: ARC-PORT-127 Nuupiluk densified off soft 60.72/-46.15 onto 60.7658/-46.2170 (gis-densify-1347). */
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

const row = find('ARC-PORT-127');
if (!row) { console.error('ARC-PORT-127 missing'); process.exit(1); }

const lat = Number(row[latIdx]);
const lon = Number(row[lonIdx]);
const src = row[srcIdx] || '';
const TARGET = { lat: 60.7658, lon: -46.2170 };
const eps = 1e-4;

if (Math.abs(lat - TARGET.lat) > eps || Math.abs(lon - TARGET.lon) > eps) {
  console.error('ARC-PORT-127 densify lock failed', { lat, lon, TARGET });
  process.exit(1);
}
if (Math.abs(lat - 60.72) < 0.001 && Math.abs(lon - (-46.15)) < 0.001) {
  console.error('ARC-PORT-127 still on soft pin');
  process.exit(1);
}
if (!src.includes('gis-densify-1347') || !src.includes('sermitsiaq.ag')) {
  console.error('ARC-PORT-127 sources lock failed', src.slice(0, 240));
  process.exit(1);
}
console.log('check-port127-nuupiluk-densify: pass', { lat, lon, csv: path });
