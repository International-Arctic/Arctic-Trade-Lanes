#!/usr/bin/env node
/**
 * CI helper: city diacritic / airport near-dup densify (2026-09-08 GIS Quality Loop).
 *
 * Usage:
 *   node scripts/check-city-airport-dedupe.mjs path/to/atlas.4326.geojson
 *   node scripts/check-city-airport-dedupe.mjs --csv-cities path/to/cities.csv --csv-airports path/to/arctic_airports.csv
 */
import fs from "node:fs";

const args = process.argv.slice(2);
const errors = [];

function fail(msg) {
  console.error(msg);
  process.exit(1);
}

function loadCsv(path) {
  const text = fs.readFileSync(path, "utf8").replace(/^\uFEFF/, "");
  const lines = text.trim().split(/\r?\n/);
  const headers = lines[0].split(",");
  // naive for id presence checks only
  return { headers, lines: lines.slice(1), raw: text };
}

if (args[0] === "--csv-cities" || args.includes("--csv-cities")) {
  const ci = args.indexOf("--csv-cities");
  const ai = args.indexOf("--csv-airports");
  const citiesPath = args[ci + 1];
  const airportsPath = ai >= 0 ? args[ai + 1] : null;
  if (!citiesPath) fail("missing cities csv");
  const cities = fs.readFileSync(citiesPath, "utf8");
  const cityIds = [...cities.matchAll(/^ARC-CITY-\d+/gm)].map((m) => m[0]);
  if (cityIds.includes("ARC-CITY-043")) errors.push("cities.csv still has ARC-CITY-043 (ASCII Honningsvag dup)");
  if (!cityIds.includes("ARC-CITY-086")) errors.push("cities.csv missing ARC-CITY-086 (Honningsvåg keeper)");
  if (airportsPath) {
    const air = fs.readFileSync(airportsPath, "utf8");
    const airIds = [...air.matchAll(/^ARC-AIR-\d+/gm)].map((m) => m[0]);
    if (airIds.includes("ARC-AIR-011")) errors.push("arctic_airports.csv still has ARC-AIR-011 (Inuvik AIF near-dup)");
    if (!airIds.includes("ARC-AIR-005")) errors.push("arctic_airports.csv missing ARC-AIR-005");
    // densify band: OSM aerodrome ~68.3060612,-133.4822581 (id-column row only)
    const m = air.match(/^ARC-AIR-005,[^\n]+/m);
    if (m) {
      // program_name may contain commas inside quotes — pull lat/lon via CSV-ish floats near Canada,Inuvik
      const floats = [...m[0].matchAll(/(-?\d+\.\d+)/g)].map((x) => Number(x[1]));
      // expect ... lat, lon ... after city field; take the pair near 68/-133
      let lat, lon;
      for (let i = 0; i < floats.length - 1; i++) {
        if (floats[i] > 60 && floats[i] < 80 && floats[i + 1] < -100 && floats[i + 1] > -180) {
          lat = floats[i]; lon = floats[i + 1]; break;
        }
      }
      if (!(lat && Math.abs(lat - 68.3060612) < 5e-4 && Math.abs(lon - -133.4822581) < 5e-4)) {
        errors.push(`ARC-AIR-005 not on OSM CYEV aerodrome band (got ${lat},${lon})`);
      }
    }
  }
} else {
  const atlasPath = args[0];
  if (!atlasPath) fail("usage: check-city-airport-dedupe.mjs <atlas.4326.geojson> | --csv-cities <cities.csv> [--csv-airports <arctic_airports.csv>]");
  const gj = JSON.parse(fs.readFileSync(atlasPath, "utf8"));
  const ids = new Set();
  let air005 = null;
  const city3 = new Map();
  for (const f of gj.features || []) {
    const p = f.properties || {};
    const id = String(f.id ?? p.id ?? "");
    ids.add(id);
    if (id === "ARC-AIR-005") air005 = (f.geometry || {}).coordinates;
    if (p.layer === "cities" && (f.geometry || {}).type === "Point") {
      const [lon, lat] = f.geometry.coordinates;
      const k = `${Math.round(lon * 1e3) / 1e3}|${Math.round(lat * 1e3) / 1e3}`;
      if (!city3.has(k)) city3.set(k, []);
      city3.get(k).push(id);
    }
  }
  if (ids.has("ARC-CITY-043")) errors.push("atlas still has ARC-CITY-043");
  if (!ids.has("ARC-CITY-086")) errors.push("atlas missing ARC-CITY-086");
  if (ids.has("ARC-AIR-011")) errors.push("atlas still has ARC-AIR-011");
  if (!ids.has("ARC-AIR-005")) errors.push("atlas missing ARC-AIR-005");
  if (air005) {
    const [lon, lat] = air005;
    if (!(Math.abs(lat - 68.3060612) < 5e-4 && Math.abs(lon - -133.4822581) < 5e-4)) {
      errors.push(`ARC-AIR-005 coords ${lon},${lat} off OSM CYEV aerodrome`);
    }
  }
  for (const [k, v] of city3) {
    if (v.length >= 2) errors.push(`city 3dp stack at ${k}: ${v.join(",")}`);
  }
}

if (errors.length) {
  console.error("city-airport-dedupe FAIL:");
  for (const e of errors) console.error(" -", e);
  process.exit(1);
}
console.log("OK: Honningsvåg city diacritic dup dropped; Inuvik AIF airport near-dup dropped; AIR-005 on OSM CYEV");
