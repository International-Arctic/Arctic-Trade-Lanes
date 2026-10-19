#!/usr/bin/env python3
"""Lock check: ARC-PORT-160 Mjoeyrarhofn Mjoeyrarbryggja quay face OSM way/210145938 ISRFJ (gis-loop-1019-1414)."""
import json, math, sys

ANCHOR = (65.0273990, -14.1134659)
OLD = (65.0284, -14.1121)
MAX_KM = 0.02

def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))

path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
errs = []
f = feats.get("ARC-PORT-160")
if not f:
    errs.append("ARC-PORT-160 missing")
else:
    lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
    d = km((lat, lon), ANCHOR)
    if d > MAX_KM:
        errs.append(f"ARC-PORT-160 is {d:.3f} km from Mjoeyrarbryggja quay-face midpoint (max {MAX_KM})")
    if km((lat, lon), OLD) < 0.08:
        errs.append("ARC-PORT-160 is still near the soft 65.0284/-14.1121 pin")
    pq = f["properties"].get("position_quality")
    if pq != "facility_site":
        errs.append(f"ARC-PORT-160 position_quality={pq!r} (expected facility_site)")
if errs:
    print("FAIL\n" + "\n".join(errs))
    sys.exit(1)
lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
print(
    f"OK ARC-PORT-160 Mjoeyrarhofn ISRFJ {lat:.7f},{lon:.7f} "
    f"({km((lat, lon), ANCHOR):.3f} km from quay-face midpoint; moved {km(OLD, ANCHOR):.2f} km off soft)"
)
