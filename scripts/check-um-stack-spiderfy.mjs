#!/usr/bin/env bun
/**
 * geo-filter 0.1.8 smoke: spiderfy-on-click + approximate-location flag (display-only, true coords kept).
 *
 * 1) Offline fixture asserts (CI-safe).
 * 2) `--live`: fetches https://unicornsmap.com/api/radar/geo.json, prints stack metrics and checks the
 *    spider layout of every live stack at zoom 4..18 (min neighbour spacing, coords untouched).
 *    `--file path.json` reads a saved geo.json instead. Live drift never fails CI; layout bugs do.
 *
 * Usage: bun scripts/check-um-stack-spiderfy.mjs [--live | --file geo.json]
 */
import { groupSharedPoints, flagApproximateLocations, spiderfyOffsetsPx, spiderfyLegs, spiderfyStackGeoJson } from '../packages/geo-filter/src/spiderfyStack.ts';

let failed = 0;
const fail = (...a) => { console.error('FAIL', ...a); failed++; };
const minGap = (pts) => {
  let m = Infinity;
  for (let i = 0; i < pts.length; i++) for (let j = i + 1; j < pts.length; j++) m = Math.min(m, Math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1]));
  return m;
};

// --- fixture: 5 on NYC centroid, 2 at one office, 1 singleton, 1 null ---------------------------
const P = (slug, lng, lat) => ({ slug, name: slug, lng, lat });
const pins = [
  P('e', -74.006, 40.7128), P('a', -74.006, 40.7128), P('c', -74.006, 40.7128), P('b', -74.006, 40.7128), P('d', -74.006, 40.7128),
  P('office-1', 8.5155, 47.1662), P('office-2', 8.5155, 47.1662),
  P('solo', 30.31, 59.94),
  { slug: 'nogeo', name: 'nogeo' },
];
const before = JSON.stringify(pins);
const stacks = groupSharedPoints(pins);
if (stacks.length !== 2 || stacks[0].size !== 5 || stacks[1].size !== 2) fail('stacks want [5,2] got', stacks.map((s) => s.size));
if (stacks[0].members.map((i) => pins[i].slug).join() !== 'a,b,c,d,e') fail('stack order not by slug');
const fl = flagApproximateLocations(pins);
if (fl.stats.flagged !== 5) fail('flagged want 5 got', fl.stats.flagged);
if (fl.pins[5].approximate_location !== false || fl.pins[5].shared_point_size !== 2) fail('2-person office must not be approximate');
if (fl.pins[7].location_precision !== 'point') fail('singleton must be point');
if ('location_precision' in fl.pins[8]) fail('no-geo pin must pass through untouched');
if (fl.pins.some((p, i) => p.lat !== pins[i].lat || p.lng !== pins[i].lng)) fail('coordinates rewritten');
if (JSON.stringify(pins) !== before) fail('input mutated');
// GeoJSON feature input
const F = (slug, lng, lat) => ({ type: 'Feature', geometry: { type: 'Point', coordinates: [lng, lat] }, properties: { slug } });
const fc = [F('x', 1, 1), F('y', 1, 1), F('z', 1, 1)];
const ff = flagApproximateLocations(fc);
if (!ff.pins.every((f) => f.properties.approximate_location === true && f.geometry.coordinates[0] === 1)) fail('feature flag/coords');
// layout
for (const n of [2, 3, 9, 10, 34, 74]) {
  const o = spiderfyOffsetsPx(n);
  if (o.length !== n) fail('offsets length', n);
  const g = minGap(o);
  if (g < 28 * 0.85) fail(`n=${n} min neighbour gap ${g.toFixed(1)} px < 23.8`);
  if (JSON.stringify(o) !== JSON.stringify(spiderfyOffsetsPx(n))) fail('non-deterministic', n);
}
const legs = spiderfyLegs([-74.006, 40.7128], 5, { zoom: 14 });
if (legs.some(([x, y]) => Math.abs(x + 74.006) > 0.01 || Math.abs(y - 40.7128) > 0.01)) fail('z14 legs drift > 0.01 deg');
const gj = spiderfyStackGeoJson(pins, stacks[0], { zoom: 12 });
if (gj.features.length !== 10 || gj.features.filter((f) => f.properties.spider_role === 'leg_end').length !== 5) fail('stack geojson');
console.log(failed ? `fixtures: ${failed} FAIL` : 'fixtures: OK');

// --- live -----------------------------------------------------------------------------------
const argv = process.argv.slice(2);
const fileIx = argv.indexOf('--file');
let live = null;
if (fileIx >= 0) live = JSON.parse(await Bun.file(argv[fileIx + 1]).text());
else if (argv.includes('--live')) {
  try { live = await (await fetch('https://unicornsmap.com/api/radar/geo.json', { headers: { 'user-agent': 'ATL-geo-filter-smoke/0.1.8' } })).json(); }
  catch (e) { console.log('live: fetch failed (not a CI failure):', String(e)); }
}
if (live) {
  const lp = live.pins || live.features || [];
  const s = groupSharedPoints(lp);
  const f = flagApproximateLocations(lp);
  const stacked = s.reduce((a, b) => a + b.size, 0);
  console.log(`live: ${lp.length} pins | ${s.length} shared points holding ${stacked} pins | approximate (stack>=3): ${f.stats.flagged} pins on ${f.stats.stacksAtOrAboveMin} points`);
  console.log('live top stacks:', s.slice(0, 6).map((x) => `${x.anchor.join(',')}×${x.size}`).join('  '));
  let worst = Infinity;
  for (const st of s) for (let z = 4; z <= 18; z += 2) {
    const L = spiderfyLegs(st.anchor, st.size, { zoom: z });
    const scale = 512 * 2 ** z;
    const px = L.map(([lng, lat]) => { const sn = Math.sin(lat * Math.PI / 180); return [((lng + 180) / 360) * scale, (0.5 - Math.log((1 + sn) / (1 - sn)) / (4 * Math.PI)) * scale]; });
    worst = Math.min(worst, minGap(px));
  }
  if (s.length && worst < 28 * 0.85) fail('live min leg gap', worst);
  if (f.pins.some((p, i) => JSON.stringify(p.geometry ?? [p.lat, p.lng]) !== JSON.stringify(lp[i].geometry ?? [lp[i].lat, lp[i].lng]))) fail('live coordinates rewritten');
  console.log(`live layout: min neighbour leg gap across all stacks, zoom 4..18 = ${worst.toFixed(1)} px`);
}
if (failed) process.exit(1);
