#!/usr/bin/env node
/** CI lock: ARC-PORT-148 Ura Guba densified off soft 69.16/33.42 onto Saam FSU AIS 69.3375/32.9273 (gis-densify-1048). */
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

const row = find('ARC-PORT-148');
if (!row) { console.error('ARC-PORT-148 missing'); process.exit(1); }

const lat = Number(row[latIdx]);
const lon = Number(row[lonIdx]);
const src = row[srcIdx] || '';
const TARGET = { lat: 69.3375, lon: 32.9273 };
const eps = 1e-5;

if (Math.abs(lat - TARGET.lat) > eps || Math.abs(lon - TARGET.lon) > eps) {
  console.error('ARC-PORT-148 densify lock failed', { lat, lon, TARGET });
  process.exit(1);
}
if (Math.abs(lat - 69.16) < 0.001 && Math.abs(lon - 33.42) < 0.001) {
  console.error('ARC-PORT-148 still on soft pin');
  process.exit(1);
}
if (!src.includes('gis-densify-1048') || !src.includes('9915090')) {
  console.error('ARC-PORT-148 sources lock failed', src.slice(0, 240));
  process.exit(1);
}
console.log('check-port148-ura-guba-densify: pass', { lat, lon, csv: path });
