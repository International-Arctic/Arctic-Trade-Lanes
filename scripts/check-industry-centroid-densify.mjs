#!/usr/bin/env node
/**
 * CI helper: industry facilities densified off shared town centroids.
 * Cycle A (2026-09-08 morning): NGA Bjerkvik, AWA Gruve 3, Hotellneset, Kirkenes unstack
 * Cycle B (2026-09-08 ~09:38 MSK): Murmansk ×4, Bakki/Húsavík, Stegra/Boden, Arkhangelsk rail
 * Cycle C (2026-09-08 ~11:23 MSK): Utqiaġvik ASRC/UIC Agvik Street densify
 * Cycle D (2026-09-08 ~12:10 MSK): Hammerfest Markoppneset vs Rypefjorden
 * Usage: node scripts/check-industry-centroid-densify.mjs [atlas.4326.geojson]
 */
import fs from "node:fs";

const path = process.argv[2] || "atlas.4326.geojson";
const data = JSON.parse(fs.readFileSync(path, "utf8"));
const byId = new Map();
for (const f of data.features || []) {
  const id = f.id || (f.properties || {}).id;
  if (id) byId.set(id, f);
}
const errors = [];
function pt(id) {
  const f = byId.get(id);
  if (!f || f.geometry?.type !== "Point") {
    errors.push(`missing point ${id}`);
    return null;
  }
  const [lon, lat] = f.geometry.coordinates;
  return { lon, lat, p: f.properties || {} };
}
const round4 = (n) => Math.round(n * 1e4) / 1e4;
const key4 = (p) => `${round4(p.lon)}|${round4(p.lat)}`;

const nga = pt("ARC-FAC-366");
const narvikPort = { lat: 68.4386, lon: 17.4279 };
if (nga) {
  if (Math.abs(nga.lat - narvikPort.lat) < 1e-3 && Math.abs(nga.lon - narvikPort.lon) < 1e-3) {
    errors.push("ARC-FAC-366 still on Narvik port centroid");
  }
  if (!(nga.lat > 68.52 && nga.lat < 68.58 && nga.lon > 17.5 && nga.lon < 17.62)) {
    errors.push(`ARC-FAC-366 unexpected Bjerkvik band ${nga.lat},${nga.lon}`);
  }
}

const awa = pt("ARC-FAC-309");
const lyb = { lat: 78.2232, lon: 15.6267 };
if (awa) {
  if (Math.abs(awa.lat - lyb.lat) < 1e-3 && Math.abs(awa.lon - lyb.lon) < 1e-3) {
    errors.push("ARC-FAC-309 still on Longyearbyen centroid");
  }
  if (!(awa.lat > 78.23 && awa.lat < 78.25 && awa.lon > 15.42 && awa.lon < 15.48)) {
    errors.push(`ARC-FAC-309 unexpected Gruve 3 region ${awa.lat},${awa.lon}`);
  }
}

const hot = pt("ARC-FAC-367");
if (hot) {
  if (Math.abs(hot.lat - lyb.lat) < 1e-3 && Math.abs(hot.lon - lyb.lon) < 1e-3) {
    errors.push("ARC-FAC-367 still on Longyearbyen centroid");
  }
  if (!(hot.lat > 78.24 && hot.lat < 78.26 && hot.lon > 15.46 && hot.lon < 15.52)) {
    errors.push(`ARC-FAC-367 unexpected Hotellneset region ${hot.lat},${hot.lon}`);
  }
}

const kIds = ["ARC-FAC-312", "ARC-FAC-313", "ARC-FAC-360", "ARC-FAC-361"];
const kPts = kIds.map(pt).filter(Boolean);
if (kPts.length === 4) {
  const keys = new Set(kPts.map(key4));
  if (keys.size < 4) {
    errors.push(`Kirkenes industry pins still share exact coords (${keys.size} unique of 4)`);
  }
}

// Cycle B — Murmansk / Bakki / Boden / Arkhangelsk
const murIds = ["ARC-FAC-316", "ARC-FAC-336", "ARC-FAC-346", "ARC-FAC-386"];
const murPts = murIds.map(pt).filter(Boolean);
if (murPts.length === 4) {
  const keys = new Set(murPts.map(key4));
  if (keys.size < 4) {
    errors.push(`Murmansk industry pins still share exact coords (${keys.size} unique of 4)`);
  }
  const city = { lat: 68.9585, lon: 33.0827 };
  for (const p of murPts) {
    if (Math.abs(p.lat - city.lat) < 1e-3 && Math.abs(p.lon - city.lon) < 1e-3) {
      errors.push("a Murmansk industry pin still on city centroid 68.9585,33.0827");
    }
  }
}

const hus = { lat: 66.0446, lon: -17.3383 };
const bak332 = pt("ARC-FAC-332");
const bak334 = pt("ARC-FAC-334");
for (const [id, p] of [
  ["ARC-FAC-332", bak332],
  ["ARC-FAC-334", bak334],
]) {
  if (!p) continue;
  if (Math.abs(p.lat - hus.lat) < 1e-3 && Math.abs(p.lon - hus.lon) < 1e-3) {
    errors.push(`${id} still on Húsavík town pin`);
  }
  // Bakki industrial band ~2 km N of Húsavík
  if (!(p.lat > 66.05 && p.lat < 66.09 && p.lon > -17.36 && p.lon < -17.31)) {
    errors.push(`${id} unexpected Bakki band ${p.lat},${p.lon}`);
  }
}
if (bak332 && bak334 && key4(bak332) === key4(bak334)) {
  errors.push("Bakki FAC-332/334 still share exact coords");
}

const stegra = pt("ARC-FAC-319");
const bodenTown = { lat: 65.8252, lon: 21.6893 };
if (stegra) {
  if (Math.abs(stegra.lat - bodenTown.lat) < 1e-3 && Math.abs(stegra.lon - bodenTown.lon) < 1e-3) {
    errors.push("ARC-FAC-319 still on Boden municipal centroid");
  }
  // Södra Svartbyn Stegra construction site band
  if (!(stegra.lat > 65.79 && stegra.lat < 65.83 && stegra.lon > 21.75 && stegra.lon < 21.85)) {
    errors.push(`ARC-FAC-319 unexpected Stegra plant band ${stegra.lat},${stegra.lon}`);
  }
}

const ark342 = pt("ARC-FAC-342");
const ark385 = pt("ARC-FAC-385");
if (ark342 && ark385 && key4(ark342) === key4(ark385)) {
  errors.push("Arkhangelsk FAC-342/385 still share exact coords");
}

// Cycle C — Utqiagvik ASRC / UIC off shared town centroid
const utqTown = { lat: 71.2906, lon: -156.7887 };
const asrc = pt("ARC-FAC-011");
const uic = pt("ARC-FAC-013");
for (const [id, p] of [
  ["ARC-FAC-011", asrc],
  ["ARC-FAC-013", uic],
]) {
  if (!p) continue;
  if (Math.abs(p.lat - utqTown.lat) < 1e-3 && Math.abs(p.lon - utqTown.lon) < 1e-3) {
    errors.push(`${id} still on Utqiagvik town centroid`);
  }
  // Browerville Agvik St band (OSM Nominatim 1230 / 1250 Agvik)
  if (!(p.lat > 71.291 && p.lat < 71.2935 && p.lon > -156.7865 && p.lon < -156.7825)) {
    errors.push(`${id} unexpected Agvik St band ${p.lat},${p.lon}`);
  }
}
if (asrc && uic && key4(asrc) === key4(uic)) {
  errors.push("Utqiagvik FAC-011/013 still share exact coords");
}

// Cycle D — Hammerfest Barents Blue (Markoppneset) vs GreenH (Rypefjorden)
const hmfTown = { lat: 70.6633, lon: 23.6822 };
const fac344 = pt("ARC-FAC-344");
const fac358 = pt("ARC-FAC-358");
if (fac344) {
  if (Math.abs(fac344.lat - hmfTown.lat) < 1e-3 && Math.abs(fac344.lon - hmfTown.lon) < 1e-3) {
    errors.push("ARC-FAC-344 still on Hammerfest town centroid");
  }
  // Markoppneset / Repparfjord-Kvalsund side (~30 km SE of Hammerfest)
  if (!(fac344.lat > 70.45 && fac344.lat < 70.50 && fac344.lon > 24.22 && fac344.lon < 24.30)) {
    errors.push(`ARC-FAC-344 unexpected Markoppneset band ${fac344.lat},${fac344.lon}`);
  }
}
if (fac358) {
  if (Math.abs(fac358.lat - hmfTown.lat) < 1e-3 && Math.abs(fac358.lon - hmfTown.lon) < 1e-3) {
    errors.push("ARC-FAC-358 still on Hammerfest town centroid");
  }
  // Rypefjorden / Indrefjord harbour approach
  if (!(fac358.lat > 70.62 && fac358.lat < 70.65 && fac358.lon > 23.64 && fac358.lon < 23.70)) {
    errors.push(`ARC-FAC-358 unexpected Rypefjorden band ${fac358.lat},${fac358.lon}`);
  }
}
if (fac344 && fac358 && key4(fac344) === key4(fac358)) {
  errors.push("Hammerfest FAC-344/358 still share exact coords");
}

if (errors.length) {
  console.error("industry centroid densify QA failed:\\n" + errors.join("\\n"));
  process.exit(1);
}
console.log(
  "OK: industry centroid densify checks passed (… + Utqiagvik ASRC/UIC + Hammerfest Markoppneset/Rypefjorden)",
);
