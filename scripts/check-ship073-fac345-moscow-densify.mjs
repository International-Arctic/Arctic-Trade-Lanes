#!/usr/bin/env node
/** Assert ARC-SHIP-073 + ARC-FAC-345 left the Moscow Red Square soft-stack (gis-densify-1407). */
import { readFileSync } from "node:fs";
const atlasPath = process.argv[2] || "dataset/atlas.4326.geojson";
const g = JSON.parse(readFileSync(atlasPath, "utf8"));
const want = {
  "ARC-SHIP-073": [37.520658, 55.672897],
  "ARC-FAC-345": [37.623268, 55.739873],
};
const bad = [37.6173, 55.7558];
let failed = 0;
for (const f of g.features || []) {
  const id = (f.properties || {}).id;
  if (!(id in want)) continue;
  const c = f.geometry?.coordinates || [];
  const [lon, lat] = c;
  const [wl, wa] = want[id];
  if (Math.abs(lon - bad[0]) < 1e-6 && Math.abs(lat - bad[1]) < 1e-6) {
    console.error(id, "still on Moscow centroid", c);
    failed++;
  } else if (Math.abs(lon - wl) > 1e-5 || Math.abs(lat - wa) > 1e-5) {
    console.error(id, "unexpected coords", c, "want", want[id]);
    failed++;
  } else {
    console.log(id, "ok", c);
  }
}
if (failed) process.exit(1);
console.log("check-ship073-fac345-moscow-densify: pass");
