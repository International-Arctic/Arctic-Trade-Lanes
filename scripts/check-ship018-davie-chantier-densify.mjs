#!/usr/bin/env node
/** GIS densify check: ARC-SHIP-018 Davie Shipbuilding / Chantier Davie off soft Lévis pin onto OSM way/169057674 */
import { readFileSync } from 'fs';
import { parse } from 'csv-parse/sync';

const csv = readFileSync(new URL('./shipbuilding_facilities.csv', import.meta.url), 'utf8');
const rows = parse(csv, { columns: true, skip_empty_lines: true });
const row = rows.find((r) => r.shipyard_id === 'ARC-SHIP-018');
if (!row) {
  console.error('FAIL: ARC-SHIP-018 missing');
  process.exit(1);
}
const lat = Number(row.latitude);
const lon = Number(row.longitude);
const src = row.sources || '';
const expectLat = 46.8300382;
const expectLon = -71.1603630;
const softOld = { lat: 46.8, lon: -71.18 };
const ok =
  Math.abs(lat - expectLat) < 1e-6 &&
  Math.abs(lon - expectLon) < 1e-6 &&
  src.includes('way/169057674') &&
  src.includes('Q2956389') &&
  (Math.abs(lat - softOld.lat) > 0.01 || Math.abs(lon - softOld.lon) > 0.01);
console.log(JSON.stringify({ id: 'ARC-SHIP-018', lat, lon, expectLat, expectLon, ok, srcSnippet: src.slice(-220) }, null, 2));
process.exit(ok ? 0 : 1);
