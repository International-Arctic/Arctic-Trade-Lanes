#!/usr/bin/env node
/** GIS densify check: ARC-SHIP-020 Halifax Shipyard off soft pin onto OSM way/358578623 */
import { readFileSync } from 'fs';
import { parse } from 'csv-parse/sync';

const csv = readFileSync(new URL('./shipbuilding_facilities.csv', import.meta.url), 'utf8');
const rows = parse(csv, { columns: true, skip_empty_lines: true });
const row = rows.find((r) => r.shipyard_id === 'ARC-SHIP-020');
if (!row) {
  console.error('FAIL: ARC-SHIP-020 missing');
  process.exit(1);
}
const lat = Number(row.latitude);
const lon = Number(row.longitude);
const src = row.sources || '';
const expectLat = 44.6672758;
const expectLon = -63.5966057;
const softOld = { lat: 44.65, lon: -63.57 };
const ok =
  Math.abs(lat - expectLat) < 1e-6 &&
  Math.abs(lon - expectLon) < 1e-6 &&
  src.includes('way/358578623') &&
  src.includes('Q1442711') &&
  (Math.abs(lat - softOld.lat) > 0.01 || Math.abs(lon - softOld.lon) > 0.01);
console.log(JSON.stringify({ id: 'ARC-SHIP-020', lat, lon, expectLat, expectLon, ok, srcSnippet: src.slice(-220) }, null, 2));
process.exit(ok ? 0 : 1);
