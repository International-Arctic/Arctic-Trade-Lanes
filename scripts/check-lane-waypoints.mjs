#!/usr/bin/env node
/**
 * Fail if live (or local) atlas.manifest.json still has unresolved_lane_waypoints.
 * Usage:
 *   node scripts/check-lane-waypoints.mjs
 *   node scripts/check-lane-waypoints.mjs ./atlas.manifest.json
 *   ATLAS_MANIFEST_URL=https://arctictradelanes.com/data/atlas.manifest.json node scripts/check-lane-waypoints.mjs
 */
import { readFileSync } from "node:fs";

const arg = process.argv[2];
const url =
  process.env.ATLAS_MANIFEST_URL ||
  "https://arctictradelanes.com/data/atlas.manifest.json";

async function load() {
  if (arg) {
    return JSON.parse(readFileSync(arg, "utf8"));
  }
  const res = await fetch(url, {
    headers: { "user-agent": "ATL-lane-waypoint-check/1.0" },
  });
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
  return res.json();
}

const m = await load();
const unresolved = m.unresolved_lane_waypoints || [];
const generated = m.generated || "?";
console.log(`generated=${generated}`);
console.log(`unresolved_count=${unresolved.length}`);
if (unresolved.length) {
  console.error("FAIL unresolved_lane_waypoints:", unresolved);
  process.exit(1);
}
console.log("OK unresolved_lane_waypoints empty");
