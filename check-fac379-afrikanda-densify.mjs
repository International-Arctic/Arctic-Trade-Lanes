#!/usr/bin/env node
/** CI lock: ARC-FAC-379 Afrikanda densified off soft 67.2500/33.5200 onto OSM node/303015821 / WD Q1987760 67.4416890/32.7769090 (gis-densify-1147). */
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

const row = find('ARC-FAC-379');
if (!row) { console.error('ARC-FAC-379 missing'); process.exit(1); }

const lat = Number(row[latIdx]);
const lon = Number(row[lonIdx]);
const src = row[srcIdx] || '';
const TARGET = { lat: 67.4416890, lon: 32.7769090 };
const eps = 1e-4;

if (Math.abs(lat - TARGET.lat) > eps || Math.abs(lon - TARGET.lon) > eps) {
  console.error('ARC-FAC-379 densify lock failed', { lat, lon, TARGET });
  process.exit(1);
}
if (Math.abs(lat - 67.25) < 0.001 && Math.abs(lon - 33.52) < 0.001) {
  console.error('ARC-FAC-379 still on soft pin');
  process.exit(1);
}
if (!src.includes('gis-densify-1147') || !src.includes('Q1987760') || !src.includes('node/303015821')) {
  console.error('ARC-FAC-379 sources lock failed', src.slice(0, 240));
  process.exit(1);
}
console.log('check-fac379-afrikanda-densify: pass', { lat, lon, csv: path });
