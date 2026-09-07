#!/usr/bin/env node
/** QA: core atlas layers must carry iso2; soft layers reported. */
import { readFileSync } from "node:fs";

const path = process.argv[2];
if (!path) {
  console.error("Usage: node scripts/check-port-iso2.mjs <atlas.4326.geojson>");
  process.exit(2);
}

const CORE = new Set(["ports", "cities", "tankers", "icebreakers"]);
const SOFT = new Set([
  "shipyards",
  "programs",
  "airports",
  "industry",
  "rail",
  "rescue",
]);

const atlas = JSON.parse(readFileSync(path, "utf8"));
const feats = (atlas.features || []).filter((f) =>
  CORE.has(f?.properties?.layer) || SOFT.has(f?.properties?.layer)
);

let coreMissing = 0;
let softMissing = 0;
const bad = [];
const counts = {};
for (const f of feats) {
  const p = f.properties || {};
  const iso = (p.iso2 || "").trim();
  const layer = p.layer;
  if (!iso || !/^[A-Z]{2}$/.test(iso)) {
    if (CORE.has(layer)) {
      coreMissing++;
      if (bad.length < 15) bad.push(`${layer}:${p.name}`);
    } else {
      softMissing++;
    }
    continue;
  }
  const u = String(p.unlocode || "").trim().toUpperCase();
  if (u === "NULL" && iso === "NU") {
    coreMissing++;
    bad.push(`NULL→NU:${p.name}`);
    continue;
  }
  counts[iso] = (counts[iso] || 0) + 1;
}

const ports = feats.filter((f) => f.properties?.layer === "ports");
const portsMissing = ports.filter((f) => !(f.properties?.iso2 || "").trim()).length;

const ok = coreMissing === 0 && portsMissing === 0;
console.log(
  JSON.stringify(
    {
      features_checked: feats.length,
      ports: ports.length,
      ports_missing_iso2: portsMissing,
      core_missing_iso2: coreMissing,
      soft_missing_iso2: softMissing,
      iso2_counts: counts,
      samples_bad: bad,
      ok,
    },
    null,
    2
  )
);
process.exit(ok ? 0 : 1);
