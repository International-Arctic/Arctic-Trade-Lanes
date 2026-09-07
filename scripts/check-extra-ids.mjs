#!/usr/bin/env node
/**
 * Fail when program_id / Feature.id repeats inside a CSV or GeoJSON layer.
 * Usage:
 *   node scripts/check-extra-ids.mjs path/to/arctic_airports.csv
 *   node scripts/check-extra-ids.mjs --geojson path/to/atlas.4326.geojson --layer airports
 */
import fs from 'node:fs';

const args = process.argv.slice(2);
const geoIdx = args.indexOf('--geojson');
const layerIdx = args.indexOf('--layer');

function fail(msg) {
  console.error(msg);
  process.exit(1);
}

if (geoIdx >= 0) {
  const path = args[geoIdx + 1];
  const layer = layerIdx >= 0 ? args[layerIdx + 1] : 'airports';
  if (!path) fail('missing --geojson path');
  const fc = JSON.parse(fs.readFileSync(path, 'utf8'));
  const seen = new Map();
  const dups = [];
  for (const f of fc.features || []) {
    const p = f.properties || {};
    if ((p.layer || p.type) !== layer) continue;
    const id = String(f.id ?? p.id ?? '');
    if (!id) continue;
    if (seen.has(id)) dups.push(id);
    else seen.set(id, true);
  }
  if (dups.length) fail(`duplicate ${layer} ids: ${[...new Set(dups)].join(', ')}`);
  console.log(`ok: ${seen.size} unique ${layer} ids in ${path}`);
  process.exit(0);
}

const path = args[0];
if (!path) fail('usage: check-extra-ids.mjs <csv> | --geojson <fc> [--layer airports]');
const text = fs.readFileSync(path, 'utf8').replace(/^\uFEFF/, '');
const lines = text.trim().split(/\r?\n/);
const headers = lines[0].split(',');
const idCol = headers.findIndex((h) => h.trim() === 'program_id' || h.trim() === 'port_id' || h.trim() === 'id');
if (idCol < 0) fail('no program_id/port_id/id column');
const seen = new Map();
const dups = [];
for (let i = 1; i < lines.length; i++) {
  // naive CSV split is fine for these id-only checks (ids have no commas)
  const cols = lines[i].split(',');
  const id = (cols[idCol] || '').trim();
  if (!id) continue;
  if (seen.has(id)) dups.push(id);
  else seen.set(id, true);
}
if (dups.length) fail(`duplicate ids in ${path}: ${[...new Set(dups)].join(', ')}`);
console.log(`ok: ${seen.size} unique ids in ${path}`);
