#!/usr/bin/env python3
"""Lock check: ARC-PORT-022 Tuktoyaktuk Port on OSM way/513281075 industrial=port (gis-port022-1629).

Prior soft pin 69.4457 / -133.0360 (4-decimal hamlet approx, WD Q719547).
Anchor = OSM way/513281075 shoelace centroid 69.4281426 / -132.9885229.
Usage: python3 check_port022_tuktoyaktuk.py [atlas.wgs84.geojson]
"""
import json, math, sys

ANCHOR = (69.4281426, -132.9885229)
OLD = (69.4457, -133.0360)
MAX_KM = 0.5


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))


path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
errs = []
f = feats.get("ARC-PORT-022")
if not f:
    errs.append("ARC-PORT-022 missing")
else:
    lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
    d = km((lat, lon), ANCHOR)
    if d > MAX_KM:
        errs.append(f"ARC-PORT-022 is {d:.2f} km from the port-land anchor (max {MAX_KM})")
    if km((lat, lon), OLD) < 0.05:
        errs.append("ARC-PORT-022 is still on the soft 69.4457/-133.0360 pin")
    pq = f["properties"].get("position_quality")
    if pq != "facility_site":
        errs.append(f"ARC-PORT-022 position_quality={pq!r} (expected facility_site)")
if errs:
    print("FAIL\n" + "\n".join(errs)); sys.exit(1)
lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
print(f"OK ARC-PORT-022 Tuktoyaktuk Port {lat:.7f},{lon:.7f} ({km((lat, lon), ANCHOR):.3f} km from OSM way/513281075; moved {km(OLD, ANCHOR):.2f} km off soft pin)")
