#!/usr/bin/env node
/**
 * Fail if live atlas has continent-scale lane vertex jumps or non-empty lane_teleport_drops.
 * Usage:
 *   node scripts/check-lane-teleport.mjs
 *   node scripts/check-lane-teleport.mjs ./atlas.4326.geojson ./atlas.manifest.json
 *   ATLAS_4326_URL=... ATLAS_MANIFEST_URL=... node scripts/check-lane-teleport.mjs
 */
import { readFileSync } from "node:fs";

const MAX_KM = Number(process.env.LANE_TELEPORT_MAX_KM || 7500); // > AK↔NO (~7.1k); allows Ningbo→Bering (~6.1k)
const geoArg = process.argv[2];
const manArg = process.argv[3];
const geoUrl =
  process.env.ATLAS_4326_URL ||
  "https://arctictradelanes.com/data/atlas.4326.geojson";
const manUrl =
  process.env.ATLAS_MANIFEST_URL ||
  "https://arctictradelanes.com/data/atlas.manifest.json";

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

const bad = [];
for (const ft of geo.features || []) {
  if ((ft.properties || {}).layer !== "lanes") continue;
  if (ft.geometry?.type !== "LineString") continue;
  const coords = ft.geometry.coordinates || [];
  for (let i = 1; i < coords.length; i++) {
    const [lon0, lat0] = coords[i - 1];
    const [lon1, lat1] = coords[i];
    const km = haversineKm(lon0, lat0, lon1, lat1);
    if (km > MAX_KM) {
      bad.push({
        name: ft.properties.name,
        i,
        km: Math.round(km),
        from: coords[i - 1],
        to: coords[i],
      });
    }
  }
}

console.log(`teleport_jumps_gt_${MAX_KM}km=${bad.length}`);
if (bad.length) {
  console.error("FAIL lane teleport jumps:", bad);
  process.exit(1);
}
console.log("OK no continent-scale lane teleports");
