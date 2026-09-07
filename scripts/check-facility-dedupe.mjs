#!/usr/bin/env node
import fs from 'node:fs';

function normName(s) {
  return String(s || '').trim().toLowerCase().replace(/\s+/g, ' ');
}
function round4(n) {
  return Math.round(Number(n) * 1e4) / 1e4;
}

const atlasPath = process.argv[2];
if (!atlasPath) {
  console.error('Usage: node scripts/check-facility-dedupe.mjs path/to/atlas.4326.geojson');
  process.exit(2);
}
const gj = JSON.parse(fs.readFileSync(atlasPath, 'utf8'));
const problems = [];
const shipIds = new Map();
const progKeys = new Map();
for (const f of gj.features || []) {
  const p = f.properties || {};
  const layer = p.layer;
  const id = p.id || f.id;
  if (layer === 'shipyards' && id) {
    if (shipIds.has(id)) problems.push(`duplicate shipyard id ${id}`);
    else shipIds.set(id, true);
  }
  if (layer === 'programs') {
    const c = (f.geometry || {}).coordinates;
    if (!c || c.length < 2) continue;
    const key = `${normName(p.name)}|${round4(c[0])}|${round4(c[1])}`;
    if (normName(p.name) && progKeys.has(key)) {
      problems.push(`duplicate program name+coord ${id} ~ ${progKeys.get(key)}`);
    } else if (normName(p.name)) {
      progKeys.set(key, id);
    }
  }
}
if (problems.length) {
  console.error('facility-dedupe FAIL:');
  for (const p of problems) console.error(' -', p);
  process.exit(1);
}
console.log('facility-dedupe OK');
