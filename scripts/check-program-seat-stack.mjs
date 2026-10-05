#!/usr/bin/env node
/**
 * CI helper (gis-quality 2026-10-05): measure co-located admin-seat pins in the
 * `programs` layer and verify geo-filter 0.1.5 `unstackAdminSeats` fans every stack
 * out (display-only, anchor preserved). Informational unless --strict.
 * Usage: bun scripts/check-program-seat-stack.mjs [atlas.4326.geojson] [--strict]
 */
import fs from "node:fs";
import { filterGeoJson } from "../packages/geo-filter/src/filterGeoJson.ts";

const args = process.argv.slice(2);
const strict = args.includes("--strict");
const path = args.find((a) => !a.startsWith("--")) || "atlas.4326.geojson";
const fc = JSON.parse(fs.readFileSync(path, "utf8"));
const key = (c) => `${Number(c[0]).toFixed(4)}|${Number(c[1]).toFixed(4)}`;

const stacks = new Map();
for (const f of fc.features || []) {
  if ((f.properties || {}).layer !== "programs" || f.geometry?.type !== "Point") continue;
  const k = key(f.geometry.coordinates);
  stacks.set(k, (stacks.get(k) || 0) + 1);
}
const multi = [...stacks.values()].filter((n) => n > 1);
const before = multi.reduce((a, n) => a + n, 0);

const out = filterGeoJson(fc, { unstackAdminSeats: true });
const progs = out.accepted.features.filter((f) => f.properties?.layer === "programs");
const after = new Map();
let anchorsOk = true;
for (const f of progs) {
  const k = key(f.geometry.coordinates);
  after.set(k, (after.get(k) || 0) + 1);
  const p = f.properties;
  if (p.position_quality === "admin_seat_fan") {
    const a = p.position_anchor;
    const d = Math.hypot(f.geometry.coordinates[0] - a[0], f.geometry.coordinates[1] - a[1]);
    if (!Array.isArray(a) || d > 2) anchorsOk = false; // fan stays local to the seat
  }
}
const stillStacked = [...after.values()].filter((n) => n > 1).length;
console.log(
  `programs ${progs.length}; raw stacks ${multi.length} seats / ${before} pins (max ${Math.max(0, ...multi)}); ` +
  `after unstackAdminSeats: ${stillStacked} stacked seats; anchors ${anchorsOk ? "OK" : "BAD"}; ` +
  `admin_seat_unstacked=${out.stats.reasons.admin_seat_unstacked || 0}`
);
if (stillStacked || !anchorsOk) { console.error("admin-seat unstack failed"); process.exit(1); }
if (strict && multi.length) { console.error("strict: raw programs layer still has co-located seat stacks"); process.exit(2); }
