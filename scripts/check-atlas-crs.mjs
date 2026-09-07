#!/usr/bin/env node
/** Spot-check ATL atlas CRS stamps. Usage: node scripts/check-atlas-crs.mjs [baseUrl] */
const base = (process.argv[2] || 'https://arctictradelanes.com').replace(/\/$/, '');
const expect = {
  'atlas.3996.geojson': 3996,
  'atlas.4326.geojson': 4326,
  'atlas.wgs84.geojson': 4326,
  'data/atlas.3996.geojson': 3996,
  'data/atlas.4326.geojson': 4326,
};
let failed = 0;
for (const [path, epsg] of Object.entries(expect)) {
  const url = `${base}/${path}`;
  const res = await fetch(url, { headers: { 'user-agent': 'ATL-GIS-CRS-check/1.0' } });
  if (!res.ok) { console.error('FAIL', res.status, url); failed++; continue; }
  const j = await res.json();
  const got = j?.projection?.epsg;
  const pt = (j.features || []).find(f => f?.geometry?.type === 'Point')?.geometry?.coordinates;
  const looksWgs = pt && Math.abs(pt[0]) <= 180 && Math.abs(pt[1]) <= 90;
  const okMeta = got === epsg;
  const okCoords = epsg === 4326 ? looksWgs : !looksWgs;
  if (okMeta && okCoords) console.log('OK', path, 'epsg', got, 'sample', pt?.slice?.(0, 2));
  else { console.error('FAIL', path, { got, expect: epsg, sample: pt, looksWgs }); failed++; }
}
process.exit(failed ? 1 : 0);
