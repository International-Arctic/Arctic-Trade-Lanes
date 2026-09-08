#!/usr/bin/env node
/**
 * CI helper: port↔city centroid densify (2026-09-08 GIS Quality Loop).
 *
 * Usage:
 *   node scripts/check-port-city-centroid-densify.mjs path/to/atlas.4326.geojson
 *   node scripts/check-port-city-centroid-densify.mjs --csv path/to/ports.csv
 */
import fs from "node:fs";

const args = process.argv.slice(2);
const errors = [];

function near(a, b, eps = 5e-4) {
  return Math.abs(a - b) < eps;
}

const expect = {
  "ARC-PORT-012": { lat: 64.1564348, lon: -21.8666787 },
  "ARC-PORT-014": { lat: 69.6507379, lon: 18.9649587 },
  "ARC-PORT-015": { lat: 69.7278875, lon: 30.0717814 },
  "ARC-PORT-016": { lat: 70.6869236, lon: 23.5981352 },
  "ARC-PORT-017": { lat: 78.2292987, lon: 15.601367 },
  "ARC-PORT-018": { lat: 67.285142, lon: 14.3805101 },
  "ARC-PORT-019": { lat: 68.4294644, lon: 17.4239955 },
  "ARC-PORT-028": { lat: 64.9959866, lon: 25.4052871 },
  "ARC-PORT-029": { lat: 65.5806088, lon: 22.1534831 },
};

const cityBanned = {
  "ARC-PORT-012": { lat: 64.1466, lon: -21.9426 },
  "ARC-PORT-014": { lat: 69.6492, lon: 18.9553 },
  "ARC-PORT-015": { lat: 69.7269, lon: 30.0456 },
  "ARC-PORT-016": { lat: 70.6634, lon: 23.6821 },
  "ARC-PORT-017": { lat: 78.2232, lon: 15.6267 },
  "ARC-PORT-018": { lat: 67.2804, lon: 14.4049 },
  "ARC-PORT-019": { lat: 68.4385, lon: 17.4273 },
  "ARC-PORT-028": { lat: 65.0121, lon: 25.4651 },
  "ARC-PORT-029": { lat: 65.5848, lon: 22.1567 },
};

function parseCsv(text) {
  const lines = text.trimEnd().split(/\r?\n/);
  const headers = lines[0].split(",");
  const latI = headers.indexOf("latitude");
  const lonI = headers.indexOf("longitude");
  const idI = headers.indexOf("port_id");
  const rows = new Map();
  for (const line of lines.slice(1)) {
    // naive split is ok for these densify id rows (lat/lon are plain floats, early columns)
    const cols = line.split(",");
    const id = cols[idI];
    if (!expect[id]) continue;
    rows.set(id, { lat: Number(cols[latI]), lon: Number(cols[lonI]) });
  }
  return rows;
}

if (args[0] === "--csv") {
  const csvPath = args[1];
  if (!csvPath) {
    console.error("missing ports csv");
    process.exit(1);
  }
  const rows = parseCsv(fs.readFileSync(csvPath, "utf8"));
  for (const [id, exp] of Object.entries(expect)) {
    const p = rows.get(id);
    if (!p) {
      errors.push(`${id} missing from csv`);
      continue;
    }
    if (!near(p.lat, exp.lat, 5e-3) || !near(p.lon, exp.lon, 5e-3)) {
      errors.push(`${id} expected ~${exp.lat},${exp.lon} got ${p.lat},${p.lon}`);
    }
    const ban = cityBanned[id];
    if (near(p.lat, ban.lat, 5e-4) && near(p.lon, ban.lon, 5e-4)) {
      errors.push(`${id} still on city centroid`);
    }
  }
} else {
  const path = args[0] || "atlas.4326.geojson";
  const data = JSON.parse(fs.readFileSync(path, "utf8"));
  const byId = new Map();
  for (const f of data.features || []) {
    const id = f.id || (f.properties || {}).id;
    if (id) byId.set(id, f);
  }
  for (const [id, exp] of Object.entries(expect)) {
    const f = byId.get(id);
    if (!f || f.geometry?.type !== "Point") {
      errors.push(`missing point ${id}`);
      continue;
    }
    const [lon, lat] = f.geometry.coordinates;
    if (!near(lat, exp.lat, 5e-3) || !near(lon, exp.lon, 5e-3)) {
      errors.push(`${id} expected ~${exp.lat},${exp.lon} got ${lat},${lon}`);
    }
    const ban = cityBanned[id];
    if (near(lat, ban.lat, 5e-4) && near(lon, ban.lon, 5e-4)) {
      errors.push(`${id} still on city centroid`);
    }
  }
}

if (errors.length) {
  for (const e of errors) console.error(e);
  process.exit(1);
}
console.log("ok: port-city-centroid densify");
