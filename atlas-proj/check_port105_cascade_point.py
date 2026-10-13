#!/usr/bin/env python3
"""Lock check: ARC-PORT-105 Cascade Point Ferry Terminal at the north end of Glacier Highway (gis-port105-1314).

Prior soft pin 58.8500 / -135.0200 sat in upper Berners Bay water ~17.3 km N of the site.
Anchor = OSM node/2835378419 (north terminus of Glacier Highway, way/217384152 + turnaround way/1033357934)
58.7001371 / -134.9378631. Alaska DOT&PF places the planned AMHS terminal at Cascade Point, Mile 42 Glacier Highway.
Tag position_quality=facility_site (planned, not built). Prefer properties.position_anchor.
Usage: python3 check_port105_cascade_point.py [atlas.wgs84.geojson]
"""
import json, math, sys

ANCHOR = (58.7001371, -134.9378631)  # lat, lon
OLD = (58.8500, -135.0200)
MAX_KM = 2.0


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))


path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
errs = []
f = feats.get("ARC-PORT-105")
if not f:
    errs.append("ARC-PORT-105 missing")
else:
    lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
    d = km((lat, lon), ANCHOR)
    if d > MAX_KM:
        errs.append(f"ARC-PORT-105 is {d:.1f} km from the Glacier Highway north-end anchor (max {MAX_KM})")
    if km((lat, lon), OLD) < 5:
        errs.append("ARC-PORT-105 is back near the soft 58.8500/-135.0200 Berners Bay pin")
    if not (58.68 <= lat <= 58.72 and -134.97 <= lon <= -134.90):
        errs.append(f"ARC-PORT-105 is outside the Cascade Point box ({lat},{lon})")
    pq = f["properties"].get("position_quality")
    if pq != "facility_site":
        errs.append(f"ARC-PORT-105 position_quality={pq!r} (expected facility_site)")
if errs:
    print("FAIL\n" + "\n".join(errs))
    sys.exit(1)
lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
print(
    f"OK ARC-PORT-105 Cascade Point {lat:.7f},{lon:.7f} "
    f"({km((lat, lon), ANCHOR):.3f} km from OSM node/2835378419; moved {km(OLD, ANCHOR):.2f} km off soft pin)"
)
