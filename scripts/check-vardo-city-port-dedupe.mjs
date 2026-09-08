#!/usr/bin/env node
/**
 * CI helper: Vardø city diacritic + port/airport densify (2026-09-08 GIS Quality Loop).
 *
 * Usage:
 *   node scripts/check-vardo-city-port-dedupe.mjs path/to/atlas.4326.geojson
 *   node scripts/check-vardo-city-port-dedupe.mjs --csv-cities cities.csv --csv-ports ports.csv --csv-airports arctic_airports.csv
 */
import fs from "node:fs";

const args = process.argv.slice(2);
const errors = [];

function fail(msg) {
  console.error(msg);
  process.exit(1);
}

function near(a, b, eps = 5e-4) {
  return Math.abs(a - b) < eps;
}

if (args.includes("--csv-cities")) {
  const ci = args.indexOf("--csv-cities");
  const pi = args.indexOf("--csv-ports");
  const ai = args.indexOf("--csv-airports");
  const citiesPath = args[ci + 1];
  const portsPath = pi >= 0 ? args[pi + 1] : null;
  const airportsPath = ai >= 0 ? args[ai + 1] : null;
  if (!citiesPath) fail("missing cities csv");
  const cities = fs.readFileSync(citiesPath, "utf8");
  const cityIds = [...cities.matchAll(/^ARC-CITY-\d+/gm)].map((m) => m[0]);
  if (cityIds.includes("ARC-CITY-042")) errors.push("cities.csv still has ARC-CITY-042 (ASCII Vardo dup)");
  if (!cityIds.includes("ARC-CITY-084")) errors.push("cities.csv missing ARC-CITY-084 (Vardø keeper)");
  if (portsPath) {
    const ports = fs.readFileSync(portsPath, "utf8");
    if (/^ARC-PORT-032,.*ARC-CITY-042/m.test(ports)) errors.push("ARC-PORT-032 still city_id ARC-CITY-042");
    const m94 = ports.match(/^ARC-PORT-094,[^\n]+/m);
    if (m94) {
      const floats = [...m94[0].matchAll(/(-?\d+\.\d+)/g)].map((x) => Number(x[1]));
      let lat, lon;
      for (let i = 0; i < floats.length - 1; i++) {
        if (floats[i] > 70 && floats[i] < 71 && floats[i + 1] > 31 && floats[i + 1] < 32) {
          lat = floats[i];
          lon = floats[i + 1];
          break;
        }
      }
      if (!(lat && near(lat, 70.3759328) && near(lon, 31.1072193))) {
        errors.push(`ARC-PORT-094 not on Kystverket fishing harbour band (got ${lat},${lon})`);
      }
    } else errors.push("ARC-PORT-094 missing");
    const m76 = ports.match(/^ARC-PORT-076,[^\n]+/m);
    if (m76) {
      const floats = [...m76[0].matchAll(/(-?\d+\.\d+)/g)].map((x) => Number(x[1]));
      let lat, lon;
      for (let i = 0; i < floats.length - 1; i++) {
        if (floats[i] > 69.7 && floats[i] < 69.8 && floats[i + 1] > 30 && floats[i + 1] < 30.1) {
          lat = floats[i];
          lon = floats[i + 1];
          break;
        }
      }
      if (!(lat && near(lat, 69.728621) && near(lon, 30.0417013))) {
        errors.push(`ARC-PORT-076 not on Sør-Varanger rådhus band (got ${lat},${lon})`);
      }
    }
  }
  if (airportsPath) {
    const air = fs.readFileSync(airportsPath, "utf8");
    const m = air.match(/^ARC-AIR-010,[^\n]+/m);
    if (m) {
      const floats = [...m[0].matchAll(/(-?\d+\.\d+)/g)].map((x) => Number(x[1]));
      let lat, lon;
      for (let i = 0; i < floats.length - 1; i++) {
        if (floats[i] > 64 && floats[i] < 65 && floats[i + 1] < -51 && floats[i + 1] > -52) {
          lat = floats[i];
          lon = floats[i + 1];
          break;
        }
      }
      if (!(lat && near(lat, 64.1906162) && near(lon, -51.6763924))) {
        errors.push(`ARC-AIR-010 not on OSM Mittarfik Nuuk band (got ${lat},${lon})`);
      }
    } else errors.push("ARC-AIR-010 missing");
  }
} else {
  const atlasPath = args[0];
  if (!atlasPath) fail("usage: check-vardo-city-port-dedupe.mjs <atlas.4326.geojson> | --csv-cities ...");
  const gj = JSON.parse(fs.readFileSync(atlasPath, "utf8"));
  const ids = new Set();
  let p094 = null, p076 = null, a010 = null;
  const city3 = new Map();
  for (const f of gj.features || []) {
    const p = f.properties || {};
    const id = String(f.id ?? p.id ?? "");
    ids.add(id);
    const c = (f.geometry || {}).coordinates;
    if (id === "ARC-PORT-094") p094 = c;
    if (id === "ARC-PORT-076") p076 = c;
    if (id === "ARC-AIR-010") a010 = c;
    if (p.layer === "cities" && (f.geometry || {}).type === "Point") {
      const [lon, lat] = c;
      const k = `${Math.round(lon * 1e3) / 1e3}|${Math.round(lat * 1e3) / 1e3}`;
      if (!city3.has(k)) city3.set(k, []);
      city3.get(k).push(id);
    }
  }
  if (ids.has("ARC-CITY-042")) errors.push("atlas still has ARC-CITY-042");
  if (!ids.has("ARC-CITY-084")) errors.push("atlas missing ARC-CITY-084");
  if (!p094 || !(near(p094[1], 70.3759328) && near(p094[0], 31.1072193))) {
    errors.push(`ARC-PORT-094 coords ${p094} off fishing harbour`);
  }
  if (!p076 || !(near(p076[1], 69.728621) && near(p076[0], 30.0417013))) {
    errors.push(`ARC-PORT-076 coords ${p076} off rådhus`);
  }
  if (!a010 || !(near(a010[1], 64.1906162) && near(a010[0], -51.6763924))) {
    errors.push(`ARC-AIR-010 coords ${a010} off Nuuk aerodrome`);
  }
  for (const [k, v] of city3) {
    if (v.length >= 2) errors.push(`city 3dp stack at ${k}: ${v.join(",")}`);
  }
}

if (errors.length) {
  console.error("vardo-city-port-dedupe FAIL:");
  for (const e of errors) console.error(" -", e);
  process.exit(1);
}
console.log("OK: Vardø ASCII city dup dropped; PORT-094 fishing harbour + PORT-076 rådhus + AIR-010 Nuuk aerodrome densified");
