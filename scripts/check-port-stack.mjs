#!/usr/bin/env node
/**
 * CI helper: fail if ports share identical UN/LOCODE + rounded WGS84 pin,
 * or if Vardø IATA leakage (NOVAW) / Primorsky Novy Port id survives.
 * Usage: node scripts/check-port-stack.mjs [atlas.4326.geojson]
 */
import fs from "node:fs";

const path = process.argv[2] || "atlas.4326.geojson";
const data = JSON.parse(fs.readFileSync(path, "utf8"));
const bannedIds = new Set([
  "ARC-PORT-055", "ARC-PORT-080", "ARC-PORT-081", "ARC-PORT-116", "ARC-PORT-117",
  "ARC-PORT-120", "ARC-PORT-122", "ARC-PORT-125", "ARC-PORT-131", "ARC-PORT-133",
  "ARC-PORT-141", "ARC-PORT-145", "ARC-PORT-152", "ARC-PORT-154", "ARC-PORT-168",
]);
const errors = [];
const seen = new Map();
let ports = 0;
for (const f of data.features || []) {
  const p = f.properties || {};
  if (p.layer !== "ports") continue;
  ports++;
  const id = f.id || p.id;
  if (bannedIds.has(id)) errors.push(`${id} should be dropped (project overlay / non-Arctic)`);
  const u = String(p.unlocode || "").trim().toUpperCase();
  if (u === "NOVAW") errors.push(`${id} uses IATA VAW as LOCODE; expect NOVAO`);
  const g = f.geometry || {};
  if (g.type === "Point" && Array.isArray(g.coordinates) && u) {
    const [lon, lat] = g.coordinates;
    const key = `${u}|${Number(lon).toFixed(4)}|${Number(lat).toFixed(4)}`;
    if (seen.has(key)) errors.push(`stack ${key}: ${seen.get(key)} and ${id}`);
    else seen.set(key, id);
  }
}
if (errors.length) {
  console.error("port stack QA failed:\n" + errors.join("\n"));
  process.exit(1);
}
console.log(`OK: ${ports} ports, no LOCODE+coord stacks, banned overlays absent`);
