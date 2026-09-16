#!/usr/bin/env node
/** GIS densify check: ARC-SHIP-011 Rauma Marine Constructions off soft-pin onto OSM way/294240416 */
import { readFileSync } from 'fs';
import { parse } from 'csv-parse/sync';

const csv = readFileSync(new URL('./shipbuilding_facilities.csv', import.meta.url), 'utf8');
const rows = parse(csv, { columns: true, skip_empty_lines: true });
const row = rows.find((r) => r.shipyard_id === 'ARC-SHIP-011');
if (!row) {
  console.error('FAIL: ARC-SHIP-011 missing');
  process.exit(1);
}
const lat = Number(row.latitude);
const lon = Number(row.longitude);
const src = row.sources || '';
const expectLat = 61.1221867;
const expectLon = 21.4603935;
const softOld = { lat: 61.13, lon: 21.51 };
const ok =
  Math.abs(lat - expectLat) < 1e-6 &&
  Math.abs(lon - expectLon) < 1e-6 &&
  src.includes('way/294240416') &&
  src.includes('Q17334709') &&
  (Math.abs(lat - softOld.lat) > 0.005 || Math.abs(lon - softOld.lon) > 0.005);
console.log(JSON.stringify({ id: 'ARC-SHIP-011', lat, lon, expectLat, expectLon, ok, srcSnippet: src.slice(-200) }, null, 2));
process.exit(ok ? 0 : 1);
