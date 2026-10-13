#!/usr/bin/env python3
"""Lock check: ARC-PORT-078 Finnafjord Port on Wikidata Q106075430 P625 (gis-port078-1053).

Prior soft pin 66.27 / -15.25 sat in open sea off Langanes (~18.8 km N of the fjord).
Anchor = Wikidata Q106075430 P625 66.1062 / -15.1502 (= enwiki Finnafjord Port), inside
Finnafjordur (OSM relation/8413765). Tag position_quality=facility_site.
Usage: python3 check_port078_finnafjord.py [atlas.wgs84.geojson]
"""
import json, math, sys
ANCHOR = (66.1062, -15.1502)
OLD = (66.27, -15.25)
MAX_KM = 1.0
def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))
path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
f = feats.get("ARC-PORT-078"); errs = []
if not f:
    errs.append("ARC-PORT-078 missing")
else:
    lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
    if km((lat, lon), ANCHOR) > MAX_KM: errs.append(f"{km((lat, lon), ANCHOR):.1f} km from WD Q106075430 anchor")
    if km((lat, lon), OLD) < 1.0: errs.append("back on soft 66.27/-15.25")
    if f["properties"].get("position_quality") != "facility_site": errs.append("position_quality != facility_site")
if errs:
    print("FAIL\n" + "\n".join(errs)); sys.exit(1)
print(f"OK ARC-PORT-078 Finnafjord {lat:.4f},{lon:.4f} ({km((lat, lon), ANCHOR):.3f} km from WD Q106075430; moved {km(OLD, ANCHOR):.1f} km off soft pin)")
