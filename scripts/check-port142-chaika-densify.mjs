#!/usr/bin/env node
/** gis-densify-1621: ARC-PORT-142 Chaika Coal Terminal */
import { readFileSync } from 'node:fs';
const csv = readFileSync(new URL('./ports.csv', import.meta.url), 'utf8');
const row = csv.split(/\r?\n/).find((l) => l.startsWith('ARC-PORT-142,'));
if (!row) throw new Error('ARC-PORT-142 missing');
const parts = [];
let cur = '';
let inQ = false;
for (const ch of row) {
  if (ch === '"') { inQ = !inQ; cur += ch; continue; }
  if (ch === ',' && !inQ) { parts.push(cur); cur = ''; continue; }
  cur += ch;
}
parts.push(cur);
const latitude = parts[4];
const longitude = parts[5];
const expectLat = '73.3779684';
const expectLon = '80.5176146';
if (latitude !== expectLat || longitude !== expectLon) {
  console.error('FAIL ARC-PORT-142', { latitude, longitude, expectLat, expectLon });
  process.exit(1);
}
console.log('PASS ARC-PORT-142 Chaika densify', latitude, longitude, 'OSM way/1104012015');
