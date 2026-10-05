#!/usr/bin/env node
// CI: no two point pins from different atlas layers may share one exact coordinate
// (only the top pin is clickable). Nudged pins must keep their true point in
// position_anchor and list their partners in co_site_ids, and stay within 3 km of it.
// Regression guard for gis-cosite-1045. Usage: node scripts/check-cosite-stack.mjs [atlas.wgs84.geojson]
import { readFileSync } from "node:fs";
const path = process.argv[2] || "atlas.wgs84.geojson";
const fc = JSON.parse(readFileSync(path, "utf8"));
const POINT_LAYERS = new Set(["ports", "industry", "shipyards", "airports", "rescue", "rail", "cities", "programs"]);
const byKey = new Map();
let fail = 0, nudged = 0;
const km = (a, b) => {
  const r = Math.PI / 180, dLat = (b[1] - a[1]) * r, dLon = (b[0] - a[0]) * r;
  const h = Math.sin(dLat / 2) ** 2 + Math.cos(a[1] * r) * Math.cos(b[1] * r) * Math.sin(dLon / 2) ** 2;
  return 12742 * Math.asin(Math.sqrt(h));
};
for (const f of fc.features) {
  const p = f.properties || {};
  if (!POINT_LAYERS.has(p.layer) || f.geometry?.type !== "Point") continue;
  const [x, y] = f.geometry.coordinates;
  const k = `${x.toFixed(4)},${y.toFixed(4)}`;
  if (!byKey.has(k)) byKey.set(k, []);
  byKey.get(k).push(`${p.layer}:${f.id ?? p.id}`);
  if (p.display_offset === "co_site_nudge") {
    nudged++;
    const id = f.id ?? p.id;
    if (!Array.isArray(p.position_anchor) || !Array.isArray(p.co_site_ids) || !p.co_site_ids.length) {
      console.error(`BAD ${id}: co_site_nudge without position_anchor/co_site_ids`); fail++;
    } else if (km(p.position_anchor, f.geometry.coordinates) > 3) {
      console.error(`BAD ${id}: nudged ${km(p.position_anchor, f.geometry.coordinates).toFixed(2)} km (>3 km) from anchor`); fail++;
    }
  }
}
for (const [k, ids] of byKey) {
  const layers = new Set(ids.map((s) => s.split(":")[0]));
  if (ids.length > 1 && layers.size > 1) { console.error(`STACK ${k}: ${ids.join(" | ")}`); fail++; }
}
if (fail) { console.error(`check-cosite-stack: ${fail} failure(s)`); process.exit(1); }
console.log(`check-cosite-stack: OK (0 cross-layer stacks; ${nudged} co_site_nudge pins anchored within 3 km)`);
