#!/usr/bin/env node
/**
 * CI helper: expansion/project ports that previously soft-deduped must be present
 * and not share exact 4dp coords with their parent harbour.
 * Usage: node scripts/check-port-expansion-densify.mjs [atlas.4326.geojson]
 */
import fs from "node:fs";

const path = process.argv[2] || "atlas.4326.geojson";
const data = JSON.parse(fs.readFileSync(path, "utf8"));
const byId = new Map();
for (const f of data.features || []) {
  const id = f.id || (f.properties || {}).id;
  if (id) byId.set(id, f);
}
const pairs = [
  ["ARC-PORT-073", "ARC-PORT-002"],
  ["ARC-PORT-132", "ARC-PORT-001"],
  ["ARC-PORT-104", "ARC-PORT-019"],
  ["ARC-PORT-113", "ARC-PORT-025"],
  ["ARC-PORT-165", "ARC-PORT-032"],
  ["ARC-PORT-140", "ARC-PORT-077"],
  ["ARC-PORT-091", "ARC-PORT-053"],
];
const expect = {
  "ARC-PORT-073": { lat: 64.7083, lon: 40.5135 },
  "ARC-PORT-132": { lat: 68.9783, lon: 33.068 },
  "ARC-PORT-104": { lat: 68.4205, lon: 17.4332 },
  "ARC-PORT-113": { lat: 61.2447, lon: -149.8817 },
  "ARC-PORT-165": { lat: 70.374, lon: 31.1019 },
  "ARC-PORT-140": { lat: 66.0755, lon: -23.108 },
  "ARC-PORT-091": { lat: 60.7225, lon: -46.0335 },
  "ARC-FAC-365": { lat: 68.98, lon: 33.07 },
};
const errors = [];
function pt(id) {
  const f = byId.get(id);
  if (!f || f.geometry?.type !== "Point") {
    errors.push(`missing point ${id}`);
    return null;
  }
  const [lon, lat] = f.geometry.coordinates;
  return { lon, lat };
}
for (const [child, parent] of pairs) {
  const c = pt(child);
  const p = pt(parent);
  if (c && p) {
    if (c.lat.toFixed(4) === p.lat.toFixed(4) && c.lon.toFixed(4) === p.lon.toFixed(4)) {
      errors.push(`${child} still stacked on parent ${parent}`);
    }
  }
}
for (const [id, exp] of Object.entries(expect)) {
  const p = pt(id);
  if (!p) continue;
  if (Math.abs(p.lat - exp.lat) > 5e-3 || Math.abs(p.lon - exp.lon) > 5e-3) {
    errors.push(`${id} expected ~${exp.lat},${exp.lon} got ${p.lat},${p.lon}`);
  }
}
if (errors.length) {
  console.error("port expansion densify QA failed:\n" + errors.join("\n"));
  process.exit(1);
}
console.log("OK: 7 expansion ports present and densified off parents; Port Alliance offset OK");
