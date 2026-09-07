#!/usr/bin/env node
/**
 * check-program-iso2.mjs — fail if programs/industry point layers lack iso2.
 * Usage: node scripts/check-program-iso2.mjs [atlas.4326.geojson]
 */
import { readFileSync } from 'node:fs';

const path = process.argv[2] || 'atlas.4326.geojson';
const gj = JSON.parse(readFileSync(path, 'utf8'));
const layers = new Set(['programs', 'industry', 'ports', 'cities', 'tankers', 'icebreakers', 'shipyards', 'airports', 'rescue', 'rail']);
const miss = [];
const counts = {};
for (const f of gj.features || []) {
  const p = f.properties || {};
  const layer = p.layer;
  if (!layers.has(layer)) continue;
  counts[layer] = (counts[layer] || 0) + 1;
  if (!p.iso2) miss.push({ layer, name: p.name, country: p.country, city: p.city });
}
console.log('layer counts', counts);
if (miss.length) {
  console.error('MISSING iso2:', miss.length);
  for (const m of miss.slice(0, 25)) console.error(m);
  process.exit(1);
}
console.log('OK: all checked point layers have iso2');
