#!/usr/bin/env node
/** CI: remaining industry↔city 3dp stacks after 2026-09-14 16:00 densify should be 0. */
import fs from 'node:fs';
const atlasPath = process.argv[2] || 'dataset/atlas.4326.geojson';
const gj = JSON.parse(fs.readFileSync(atlasPath, 'utf8'));
const cities = new Map();
for (const ft of gj.features) {
  const p = ft.properties || {};
  if (p.layer !== 'cities' || ft.geometry?.type !== 'Point') continue;
  const [lon, lat] = ft.geometry.coordinates;
  cities.set(`${lon.toFixed(3)},${lat.toFixed(3)}`, p.id);
}
const densified = ['ARC-FAC-315','ARC-FAC-362','ARC-FAC-363','ARC-FAC-378'];
const stacks = [];
const coords = {};
for (const ft of gj.features) {
  const p = ft.properties || {};
  if (p.layer !== 'industry' || ft.geometry?.type !== 'Point') continue;
  const [lon, lat] = ft.geometry.coordinates;
  const key = `${lon.toFixed(3)},${lat.toFixed(3)}`;
  if (densified.includes(p.id)) coords[p.id] = [lon, lat];
  if (cities.has(key)) stacks.push({ id: p.id, city: cities.get(key), lon, lat, gq: p.geo_quality });
}
console.log(JSON.stringify({ industry_city_stacks: stacks.length, stacks, densified_coords: coords }, null, 2));
if (stacks.length !== 0) {
  console.error('FAIL: expected 0 industry↔city stacks');
  process.exit(1);
}
for (const id of densified) {
  if (!coords[id]) { console.error('FAIL missing', id); process.exit(1); }
}
console.log('PASS: industry densify 1600 — 0 stacks');
