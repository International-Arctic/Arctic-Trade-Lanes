#!/usr/bin/env python3
"""Lock check: ARC-PORT-053 Qaqortoq Port RAL harbour yard OSM way/511853551 (gis-port053-0945)."""
import json, math, sys

ANCHOR = (60.7178523, -46.0365644)
OLD = (60.7288, -46.0278)
MAX_KM = 0.5


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))


path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
errs = []
f = feats.get("ARC-PORT-053")
if not f:
    errs.append("ARC-PORT-053 missing")
else:
    lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
    d = km((lat, lon), ANCHOR)
    if d > MAX_KM:
        errs.append(f"ARC-PORT-053 is {d:.2f} km from OSM way/511853551 anchor (max {MAX_KM})")
    if km((lat, lon), OLD) < 0.05:
        errs.append("ARC-PORT-053 is still on the soft 60.7288/-46.0278 pin")
    pq = f["properties"].get("position_quality")
    if pq != "facility_site":
        errs.append(f"ARC-PORT-053 position_quality={pq!r} (expected facility_site)")
g = feats.get("ARC-PORT-091")
if g:
    lo2, la2 = g["geometry"]["coordinates"][:2]
    if f and km((la2, lo2), ANCHOR) < 0.2:
        errs.append("ARC-PORT-091 collapsed onto ARC-PORT-053 anchor")
if errs:
    print("FAIL\n" + "\n".join(errs))
    sys.exit(1)
lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
print(
    f"OK ARC-PORT-053 Qaqortoq {lat:.7f},{lon:.7f} "
    f"({km((lat, lon), ANCHOR):.3f} km from OSM way/511853551; moved {km(OLD, ANCHOR):.2f} km off soft)"
)
