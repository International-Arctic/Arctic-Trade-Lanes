#!/usr/bin/env node
/**
 * QA: ship/icebreaker country props + schematic stack size.
 * Usage: node scripts/check-ship-fleet.mjs [path-or-url-to-atlas.4326.geojson]
 */
import { readFileSync } from 'node:fs';

const src = process.argv[2] || 'https://arctictradelanes.com/atlas.4326.geojson';
const MAX_STACK = Number(process.env.MAX_SHIP_STACK || 24);

async function load(path) {
  if (/^https?:/i.test(path)) {
    const res = await fetch(path, { headers: { 'user-agent': 'ATL-GIS-QA/1.0' } });
    if (!res.ok) throw new Error(`HTTP ${res.status} for ${path}`);
    return res.json();
  }
  return JSON.parse(readFileSync(path, 'utf8'));
}

const fc = await load(src);
const ships = (fc.features || []).filter((f) =>
  ['tankers', 'icebreakers'].includes(f?.properties?.layer)
);
let missingCountry = 0;
let maxStack = 0;
for (const f of ships) {
  const p = f.properties || {};
  if (!String(p.country || '').trim()) missingCountry += 1;
  maxStack = Math.max(maxStack, Number(p.position_stack_size) || 1);
}
const ok = missingCountry === 0 && maxStack <= MAX_STACK;
console.log(JSON.stringify({ src, ships: ships.length, missingCountry, maxStack, MAX_STACK, ok }, null, 2));
if (!ok) process.exit(1);
