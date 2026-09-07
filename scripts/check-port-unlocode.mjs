#!/usr/bin/env node
/**
 * CI helper: assert atlas ports have valid UN/LOCODE shape (or empty),
 * no USNOM typo, no literal NULL, and no known alias port ids.
 * Usage: node scripts/check-port-unlocode.mjs [atlas.4326.geojson]
 */
import fs from "node:fs";

const path = process.argv[2] || "atlas.4326.geojson";
const data = JSON.parse(fs.readFileSync(path, "utf8"));
const bannedIds = new Set(["ARC-PORT-037", "ARC-PORT-103"]);
const errors = [];
let ports = 0;
for (const f of data.features || []) {
  const p = f.properties || {};
  if (p.layer !== "ports") continue;
  ports++;
  const id = f.id || p.id;
  if (bannedIds.has(id)) errors.push(`${id} should be dropped (alias/duplicate)`);
  const u = String(p.unlocode || "").trim().toUpperCase();
  if (!u) continue;
  if (u === "NULL" || u === "USNOM" || u === "NOVAW" || u.length === 3) errors.push(`${id} bad unlocode=${u}`);
  if (u.length !== 5 || !/^[A-Z]{2}[A-Z0-9]{3}$/.test(u)) errors.push(`${id} malformed unlocode=${u}`);
}
if (errors.length) {
  console.error("port UN/LOCODE QA failed:\n" + errors.join("\n"));
  process.exit(1);
}
console.log(`OK: ${ports} ports, LOCODE shape clean, banned aliases absent`);
