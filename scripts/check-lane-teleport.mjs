#!/usr/bin/env node
/**
 * Fail if live atlas has mismatched lane teleports:
 *  - non-empty lane_teleport_drops on manifest
 *  - non-Americas/Polar-named lanes carrying lon < -100 vertices (AK tip on NO corridor)
 *  - optional consecutive jump > LANE_TELEPORT_MAX_KM (default 7500)
 *
 * Usage:
 *   node scripts/check-lane-teleport.mjs
 *   node scripts/check-lane-teleport.mjs ./atlas.4326.geojson ./atlas.manifest.json
 */
import { readFileSync } from "node:fs";

const MAX_KM = Number(process.env.LANE_TELEPORT_MAX_KM || 7500);
const geoArg = process.argv[2];
const manArg = process.argv[3];
const geoUrl =
  process.env.ATLAS_4326_URL ||
  "https://arctictradelanes.com/data/atlas.4326.geojson";
const manUrl =
  process.env.ATLAS_MANIFEST_URL ||
  "https://arctictradelanes.com/data/atlas.manifest.json";

const AMERICAS_OK =
  /alaska|beaufort|chukchi|bering|northwest passage|arctic bridge|prudhoe|nome|churchill|mackenzie|tuktoyaktuk|transpolar|northern sea route|northeast passage|nsr scheduled|china-europe|yamal/i;

function haversineKm(lon1, lat1, lon2, lat2) {
  const R = 6371;
  const toRad = (d) => (d * Math.PI) / 180;
  const p1 = toRad(lat1);
  const p2 = toRad(lat2);
  const dphi = toRad(lat2 - lat1);
  const dlmb = toRad(lon2 - lon1);
  const a =
    Math.sin(dphi / 2) ** 2 +
    Math.cos(p1) * Math.cos(p2) * Math.sin(dlmb / 2) ** 2;
  return 2 * R * Math.asin(Math.min(1, Math.sqrt(a)));
}

async function loadJson(pathOrUrl, isPath) {
  if (isPath) return JSON.parse(readFileSync(pathOrUrl, "utf8"));
  const res = await fetch(pathOrUrl, {
    headers: { "user-agent": "ATL-lane-teleport-check/1.0" },
  });
  if (!res.ok) throw new Error(`HTTP ${res.status} for ${pathOrUrl}`);
  return res.json();
}

const geo = await loadJson(geoArg || geoUrl, Boolean(geoArg));
const man = await loadJson(manArg || manUrl, Boolean(manArg));

const drops = man.lane_teleport_drops || [];
console.log(`generated=${man.generated || "?"}`);
console.log(`lane_teleport_drops=${drops.length}`);
if (drops.length) {
  console.error("FAIL lane_teleport_drops:", drops);
  process.exit(1);
}

const badWest = [];
const badJump = [];
for (const ft of geo.features || []) {
  if ((ft.properties || {}).layer !== "lanes") continue;
  if (ft.geometry?.type !== "LineString") continue;
  const name = ft.properties.name || "";
  const coords = ft.geometry.coordinates || [];
  const americasLane = AMERICAS_OK.test(name);
  for (let i = 0; i < coords.length; i++) {
    const [lon, lat] = coords[i];
    if (!americasLane && lon < -100) {
      badWest.push({ name, i, lon, lat });
    }
    if (i > 0) {
      const [lon0, lat0] = coords[i - 1];
      const km = haversineKm(lon0, lat0, lon, lat);
      if (km > MAX_KM) {
        badJump.push({ name, i, km: Math.round(km), from: coords[i - 1], to: coords[i] });
      }
    }
  }
}

console.log(`unexpected_west_lon_vertices=${badWest.length}`);
console.log(`teleport_jumps_gt_${MAX_KM}km=${badJump.length}`);
if (badWest.length) {
  console.error("FAIL non-Americas lane has lon < -100 (likely start_port teleport):", badWest);
  process.exit(1);
}
if (badJump.length) {
  console.error("FAIL lane teleport jumps:", badJump);
  process.exit(1);
}
console.log("OK no continent-scale lane teleports");
