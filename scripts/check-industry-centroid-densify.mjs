#!/usr/bin/env node
/**
 * CI helper: industry facilities densified off shared town centroids.
 * - ARC-FAC-366 Narvik Green Ammonia at Bjerkvik/Lailasletta (not Narvik port)
 * - ARC-FAC-309 AWA at Gruve 3 (not Longyearbyen centroid)
 * - ARC-FAC-367 Hotellneset plant near OSM Hotellneset
 * - Kirkenes innovation/cluster pins no longer share one exact centroid
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

const nga = pt("ARC-FAC-366");
const narvikPort = { lat: 68.4386, lon: 17.4279 };
if (nga) {
  if (Math.abs(nga.lat - narvikPort.lat) < 1e-3 && Math.abs(nga.lon - narvikPort.lon) < 1e-3) {
    errors.push("ARC-FAC-366 still on Narvik port centroid");
  }
  // Bjerkvik / Lailasletta band
  if (!(nga.lat > 68.52 && nga.lat < 68.58 && nga.lon > 17.50 && nga.lon < 17.62)) {
    errors.push(`ARC-FAC-366 unexpected Bjerkvik band ${nga.lat},${nga.lon}`);
  }
}

const awa = pt("ARC-FAC-309");
const lyb = { lat: 78.2232, lon: 15.6267 };
if (awa) {
  if (Math.abs(awa.lat - lyb.lat) < 1e-3 && Math.abs(awa.lon - lyb.lon) < 1e-3) {
    errors.push("ARC-FAC-309 still on Longyearbyen centroid");
  }
  // Gruve 3 / Platåberget west of town
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
  const keys = new Set(kPts.map((p) => `${round4(p.lon)}|${round4(p.lat)}`));
  if (keys.size < 4) {
    errors.push(`Kirkenes industry pins still share exact coords (${keys.size} unique of 4)`);
  }
}

if (errors.length) {
  console.error("industry centroid densify QA failed:\n" + errors.join("\n"));
  process.exit(1);
}
console.log("OK: industry centroid densify checks passed (NGA Bjerkvik, AWA Gruve 3, Hotellneset, Kirkenes unstack)");
