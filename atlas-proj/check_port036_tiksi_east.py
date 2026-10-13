#!/usr/bin/env python3
"""Lock check: ARC-PORT-036 Tiksi East Port on East Pier No.1 of Tiksi seaport (gis-port036-1444).

Prior soft pin 71.6800 / 128.9500 sat in Tiksi Bay anchorage water ~4.3 km NNE.
Anchor = OSM way/1081390287 'Vostochny pirs I' centroid 71.6448592 / 128.8963706 (Mintrans order No.50, 2017: berths 11-12).
Usage: python3 check_port036_tiksi_east.py [atlas.wgs84.geojson]
"""
import json, math, sys

ANCHOR = (71.6448592, 128.8963706)
OLD = (71.6800, 128.9500)
MAX_KM = 0.5


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))


path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
errs = []
f = feats.get("ARC-PORT-036")
if not f:
    errs.append("ARC-PORT-036 missing")
else:
    lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
    d = km((lat, lon), ANCHOR)
    if d > MAX_KM:
        errs.append(f"ARC-PORT-036 is {d:.2f} km from the East Pier I anchor (max {MAX_KM})")
    if km((lat, lon), OLD) < 2.0:
        errs.append("ARC-PORT-036 is back near the soft 71.6800/128.9500 bay pin")
    pq = f["properties"].get("position_quality")
    if pq != "facility_site":
        errs.append(f"ARC-PORT-036 position_quality={pq!r} (expected facility_site)")
if errs:
    print("FAIL\n" + "\n".join(errs)); sys.exit(1)
lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
print(f"OK ARC-PORT-036 Tiksi East Pier I {lat:.7f},{lon:.7f} ({km((lat, lon), ANCHOR):.3f} km from OSM way/1081390287; moved {km(OLD, ANCHOR):.2f} km off soft pin)")
