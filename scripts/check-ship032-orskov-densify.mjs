#!/usr/bin/env node
/** GIS densify check: ARC-SHIP-032 Orskov Yard off soft Frederikshavn pin onto OSM way/1252850980 + way/1252850979 centroid */
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const csvPath = join(root, 'dataset/shipbuilding_facilities.csv');
const atlasPath = process.argv[2] || join(root, 'dataset/atlas.4326.geojson');

const expectLat = 57.4368155;
const expectLon = 10.5474498;
const softOld = { lat: 57.44, lon: 10.54 };

function parseCsvRow(id) {
  const text = readFileSync(csvPath, 'utf8');
  const lines = text.split(/\r?\n/);
  const header = lines[0].split(',');
  const idIdx = header.indexOf('shipyard_id');
  const latIdx = header.indexOf('latitude');
  const lonIdx = header.indexOf('longitude');
  const srcIdx = header.indexOf('sources');
  for (const line of lines.slice(1)) {
    if (!line.startsWith(id + ',')) continue;
    // naive field extract via regex for quoted CSV — use JSON from atlas primarily; for sources scan line
    const latM = line.match(new RegExp(`^${id},(?:[^,]|,"[^"]*")*?,([^,]+),([^,]+),`));
    // Better: walk CSV properly for this single known-simple row structure after id
    // Row has many quoted fields; extract lat/lon as 5th/6th columns via csv-ish split
    const fields = [];
    let cur = '';
    let q = false;
    for (let i = 0; i < line.length; i++) {
      const c = line[i];
      if (c === '"') {
        if (q && line[i + 1] === '"') {
          cur += '"';
          i++;
        } else q = !q;
      } else if (c === ',' && !q) {
        fields.push(cur);
        cur = '';
      } else cur += c;
    }
    fields.push(cur);
    return {
      shipyard_id: fields[idIdx],
      latitude: fields[latIdx],
      longitude: fields[lonIdx],
      sources: fields[srcIdx] || '',
    };
  }
  return null;
}

const row = parseCsvRow('ARC-SHIP-032');
if (!row) {
  console.error('FAIL: ARC-SHIP-032 missing in CSV');
  process.exit(1);
}
const lat = Number(row.latitude);
const lon = Number(row.longitude);
const src = row.sources || '';
const csvOk =
  Math.abs(lat - expectLat) < 1e-6 &&
  Math.abs(lon - expectLon) < 1e-6 &&
  src.includes('way/1252850980') &&
  src.includes('way/1252850979') &&
  src.includes('Q19827622') &&
  (Math.abs(lat - softOld.lat) > 0.001 || Math.abs(lon - softOld.lon) > 0.001);

const atlas = JSON.parse(readFileSync(atlasPath, 'utf8'));
const feat = (atlas.features || []).find((f) => (f.properties || {}).id === 'ARC-SHIP-032');
let atlasOk = false;
if (!feat) {
  console.error('FAIL: ARC-SHIP-032 missing in atlas');
} else {
  const [alon, alat] = feat.geometry?.coordinates || [];
  atlasOk = Math.abs(alon - expectLon) < 1e-6 && Math.abs(alat - expectLat) < 1e-6;
  if (!atlasOk) console.error('FAIL: atlas coords', [alon, alat]);
}

const typoGone = !(atlas.features || []).some((f) => (f.properties || {}).id === 'ARC-SSHIP-024');
const ship024 = (atlas.features || []).some((f) => (f.properties || {}).id === 'ARC-SHIP-024');

const ok = csvOk && atlasOk && typoGone && ship024;
console.log(
  JSON.stringify(
    {
      id: 'ARC-SHIP-032',
      lat,
      lon,
      expectLat,
      expectLon,
      csvOk,
      atlasOk,
      typoGone,
      ship024,
      ok,
      srcSnippet: src.slice(-240),
    },
    null,
    2
  )
);
process.exit(ok ? 0 : 1);
