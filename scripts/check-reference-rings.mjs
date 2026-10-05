#!/usr/bin/env node
// CI: atlas reference overlays (Arctic Circle, 75N, 80N, 75-80N band) must sit on their
// named parallels in the WGS84 export and be projected metres in the EPSG:3996 export.
// Regression guard for gis-refring-1015 (rings had collapsed onto ~89.999N).
// Usage: node scripts/check-reference-rings.mjs [atlas.wgs84.geojson] [atlas.3996.geojson]
import { readFileSync } from "node:fs";
const wgsPath = process.argv[2] || "atlas.wgs84.geojson";
const polPath = process.argv[3] || "atlas.3996.geojson";
const wgs = JSON.parse(readFileSync(wgsPath, "utf8"));
const pol = JSON.parse(readFileSync(polPath, "utf8"));
const expect = { "REF-ARCTIC-CIRCLE": [66.5, 66.5], "REF-75N": [75, 75], "REF-80N": [80, 80], "REF-TARGET-BAND": [75, 80] };
const flat = (g) => (g.type === "Polygon" ? g.coordinates.flat() : g.coordinates);
let fail = 0;
for (const [id, [lo, hi]] of Object.entries(expect)) {
  const f = wgs.features.find((x) => x.id === id || x.properties?.id === id);
  if (!f) { console.error(`MISSING ${id} in ${wgsPath}`); fail++; continue; }
  const lats = flat(f.geometry).map((c) => c[1]);
  const mn = Math.min(...lats), mx = Math.max(...lats);
  if (Math.abs(mn - lo) > 1e-3 || Math.abs(mx - hi) > 1e-3) { console.error(`BAD ${id} lat ${mn}..${mx}, want ${lo}..${hi}`); fail++; }
  const p = pol.features.find((x) => x.id === id || x.properties?.id === id);
  const metres = p && flat(p.geometry).every((c) => Math.abs(c[0]) > 180 || Math.abs(c[1]) > 90);
  if (!metres) { console.error(`BAD ${id} in ${polPath}: coordinates look like degrees, expected EPSG:3996 metres`); fail++; }
}
if (fail) { console.error(`check-reference-rings: ${fail} failure(s)`); process.exit(1); }
console.log("check-reference-rings: OK (4 reference overlays on their parallels; 3996 in metres)");
