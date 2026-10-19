#!/usr/bin/env python3
"""Lock check: ARC-PORT-165 Vardo fiskerihavn inner fishing pier OSM way/987326753 NOVAO (gis-loop-1019-1446)."""
import json, math, sys

ANCHOR = (70.3760571, 31.1021737)
OLD = (70.3740, 31.1019)
MAX_KM = 0.02

def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))

path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
errs = []
f = feats.get("ARC-PORT-165")
if not f:
    errs.append("ARC-PORT-165 missing")
else:
    lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
    d = km((lat, lon), ANCHOR)
    if d > MAX_KM:
        errs.append(f"ARC-PORT-165 is {d:.3f} km from NOVAO fishing pier centroid (max {MAX_KM})")
    if km((lat, lon), OLD) < 0.08:
        errs.append("ARC-PORT-165 is still near the soft 70.3740/31.1019 pin")
    pq = f["properties"].get("position_quality")
    if pq != "facility_site":
        errs.append(f"ARC-PORT-165 position_quality={pq!r} (expected facility_site)")
if errs:
    print("FAIL\n" + "\n".join(errs))
    sys.exit(1)
lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
print(
    f"OK ARC-PORT-165 Vardo fiskerihavn NOVAO {lat:.7f},{lon:.7f} "
    f"({km((lat, lon), ANCHOR):.3f} km from pier centroid; moved {km(OLD, ANCHOR):.2f} km off soft)"
)
