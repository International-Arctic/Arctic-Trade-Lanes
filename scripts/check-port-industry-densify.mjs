#!/usr/bin/env node
/**
 * CI helper: White Mountain off Kangerlussuaq; Whittier dock≠tunnel;
 * Norterminal/KILA off Kirkenes centroid; Kangerlussuaq uses GLKAN.
 * Usage: node scripts/check-port-industry-densify.mjs [atlas.4326.geojson]
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
const wm = pt("ARC-PORT-083");
const kan = pt("ARC-PORT-151");
if (wm && kan) {
  if (Math.abs(wm.lat - kan.lat) < 1e-3 && Math.abs(wm.lon - kan.lon) < 1e-3) {
    errors.push("ARC-PORT-083 still stacked on Kangerlussuaq");
  }
  if (String(wm.p.unlocode || "").toUpperCase() === "GLKAN") {
    errors.push("ARC-PORT-083 must not use GLKAN");
  }
  if (String(kan.p.unlocode || "").toUpperCase() !== "GLKAN") {
    errors.push(`ARC-PORT-151 expected GLKAN, got ${kan.p.unlocode}`);
  }
  // White Mountain should be west of Kangerlussuaq (more negative lon) and not inland town
  if (!(wm.lon < -51.5 && wm.lat > 66.0 && wm.lat < 67.2)) {
    errors.push(`ARC-PORT-083 unexpected Qaqortorsuaq region ${wm.lat},${wm.lon}`);
  }
}
const d068 = pt("ARC-PORT-068");
const d082 = pt("ARC-PORT-082");
if (d068 && d082) {
  if (Math.abs(d068.lat - d082.lat) < 1e-4 && Math.abs(d068.lon - d082.lon) < 1e-4) {
    errors.push("Whittier Delong Dock still stacked on ARRC tunnel pin");
  }
}
const nt = pt("ARC-FAC-372");
const kila = pt("ARC-FAC-314");
const kirkenes = { lat: 69.7271, lon: 30.045 };
if (nt) {
  if (Math.abs(nt.lat - kirkenes.lat) < 1e-3 && Math.abs(nt.lon - kirkenes.lon) < 1e-3) {
    errors.push("Norterminal still on Kirkenes centroid");
  }
}
if (kila) {
  if (Math.abs(kila.lat - kirkenes.lat) < 1e-3 && Math.abs(kila.lon - kirkenes.lon) < 1e-3) {
    errors.push("KILA still on Kirkenes centroid");
  }
}
if (errors.length) {
  console.error("port/industry densify QA failed:\n" + errors.join("\n"));
  process.exit(1);
}
console.log("OK: White Mountain, Whittier, Gamneset/KILA densify checks passed");
