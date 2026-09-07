#!/usr/bin/env node
/**
 * CI helper: shipyard CSV column-shift / multi-site quarantine regressions.
 * - ARC-SHIP-033 must be a Singapore pin (lat~1.26, lon~103.83)
 * - ARC-SHIP-052 must be Kola Bay (lat~69.06, lon~33.2)
 * - ARC-SHIP-025 must stay quarantined (absent from atlas)
 * - No shipyard Point with |lat|>90 (classic lat/lon column swap)
 *
 * Usage: node scripts/check-shipyard-column-shift.mjs [atlas.4326.geojson]
 */
import fs from "node:fs";

const path = process.argv[2] || "atlas.4326.geojson";
const data = JSON.parse(fs.readFileSync(path, "utf8"));
const ships = (data.features || []).filter(
  (f) => (f.properties || {}).layer === "shipyards"
);
const byId = new Map();
for (const f of ships) {
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
  return { lon, lat };
}

if (byId.has("ARC-SHIP-025")) {
  errors.push("ARC-SHIP-025 Vard multi-site must stay quarantined (blank coords)");
}

const s033 = pt("ARC-SHIP-033");
if (s033) {
  // GeoJSON is [lon, lat]
  if (!(s033.lat > 1.0 && s033.lat < 1.5 && s033.lon > 103.5 && s033.lon < 104.2)) {
    errors.push(
      `ARC-SHIP-033 expected Singapore ~1.26,103.83 got ${s033.lat},${s033.lon}`
    );
  }
}

const s052 = pt("ARC-SHIP-052");
if (s052) {
  if (!(s052.lat > 68.5 && s052.lat < 69.5 && s052.lon > 32.5 && s052.lon < 34.0)) {
    errors.push(
      `ARC-SHIP-052 expected Kola Bay ~69.06,33.2 got ${s052.lat},${s052.lon}`
    );
  }
}

for (const f of ships) {
  const id = f.id || (f.properties || {}).id;
  if (f.geometry?.type !== "Point") continue;
  const [lon, lat] = f.geometry.coordinates || [];
  if (!Number.isFinite(lat) || !Number.isFinite(lon)) {
    errors.push(`${id}: non-finite coords`);
    continue;
  }
  if (Math.abs(lat) > 90) {
    errors.push(`${id}: |lat|>90 (likely CSV column shift) lat=${lat} lon=${lon}`);
  }
}

if (errors.length) {
  console.error("shipyard column-shift QA failed:\n" + errors.join("\n"));
  process.exit(1);
}
console.log(
  `OK: column-shift checks passed (${ships.length} shipyards; 033 Singapore, 052 Kola, 025 absent)`
);
