#!/usr/bin/env node
/**
 * CI helper: soft-stacked project ports + leftover industry city-centroid offs.
 * Usage: node scripts/check-port-soft-stack-densify.mjs [atlas.4326.geojson]
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
  ["ARC-PORT-096", "ARC-PORT-040"],
  ["ARC-PORT-097", "ARC-PORT-015"],
  ["ARC-PORT-100", "ARC-PORT-056"],
  ["ARC-PORT-146", "ARC-PORT-027"],
];
const expect = {
  "ARC-PORT-096": { lat: 70.98091, lon: 25.968988 },
  "ARC-PORT-097": { lat: 69.726774, lon: 30.0348534 },
  "ARC-PORT-100": { lat: 71.290224, lon: -156.794962 },
  "ARC-PORT-146": { lat: 65.663578, lon: 24.530333 },
  "ARC-FAC-320": { lat: 65.562638, lon: 22.20016 },
  "ARC-FAC-333": { lat: 67.288803, lon: 14.396978 },
  "ARC-FAC-340": { lat: 64.171378, lon: -51.72059 },
};
const cityBanned = {
  "ARC-FAC-320": { lat: 65.5848, lon: 22.1567 },
  "ARC-FAC-333": { lat: 67.2804, lon: 14.4049 },
  "ARC-FAC-340": { lat: 64.1814, lon: -51.6941 },
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
function r3(n) {
  return Math.round(n * 1000) / 1000;
}
for (const [child, parent] of pairs) {
  const c = pt(child);
  const p = pt(parent);
  if (c && p) {
    if (r3(c.lat) === r3(p.lat) && r3(c.lon) === r3(p.lon)) {
      errors.push(`${child} still 3dp-stacked on parent ${parent}`);
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
for (const [id, ban] of Object.entries(cityBanned)) {
  const p = pt(id);
  if (!p) continue;
  if (Math.abs(p.lat - ban.lat) < 5e-4 && Math.abs(p.lon - ban.lon) < 5e-4) {
    errors.push(`${id} still on banned city centroid ${ban.lat},${ban.lon}`);
  }
}
// global: no port 3dp multi-stacks among densify children/parents set
const watch = new Set(pairs.flat());
const stacks = new Map();
for (const f of data.features || []) {
  const id = f.id || (f.properties || {}).id;
  if (!watch.has(id) || f.geometry?.type !== "Point") continue;
  const [lon, lat] = f.geometry.coordinates;
  const k = `${r3(lon)},${r3(lat)}`;
  if (!stacks.has(k)) stacks.set(k, []);
  stacks.get(k).push(id);
}
for (const [k, ids] of stacks) {
  if (ids.length > 1) errors.push(`watch-set 3dp stack at ${k}: ${ids.join(",")}`);
}
if (errors.length) {
  console.error("port soft-stack densify QA failed:\n" + errors.join("\n"));
  process.exit(1);
}
console.log("OK: 4 soft-stack ports densified off parents; 3 industry city-centroid offs OK");
