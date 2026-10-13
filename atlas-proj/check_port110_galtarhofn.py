#!/usr/bin/env python3
"""Lock check: ARC-PORT-110 Galtarhofn on Galtarlaekur farmstead OSM way/560639791 (gis-port110-1128).

Prior soft pin 64.32 / -21.85 sat ~3.6 km SW of the zoned Galtarlaekur land (Hvalfjardarsveit notice:
~102 ha below Route 1 in landi Galtarlaekjar). Anchor = OSM way/560639791 64.3470050 / -21.8087513.
Tag position_quality=facility_site.
Usage: python3 check_port110_galtarhofn.py [atlas.wgs84.geojson]
"""
import json, math, sys
ANCHOR = (64.3470050, -21.8087513)
OLD = (64.32, -21.85)
MAX_KM = 1.0
def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))
path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
f = feats.get("ARC-PORT-110"); errs = []
if not f:
    errs.append("ARC-PORT-110 missing")
else:
    lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
    if km((lat, lon), ANCHOR) > MAX_KM: errs.append(f"{km((lat, lon), ANCHOR):.1f} km from OSM way/560639791 anchor")
    if km((lat, lon), OLD) < 1.0: errs.append("back on soft 64.32/-21.85")
    if f["properties"].get("position_quality") != "facility_site": errs.append("position_quality != facility_site")
if errs:
    print("FAIL\n" + "\n".join(errs)); sys.exit(1)
print(f"OK ARC-PORT-110 Galtarhofn {lat:.4f},{lon:.4f} ({km((lat, lon), ANCHOR):.3f} km from OSM way/560639791; moved {km(OLD, ANCHOR):.1f} km off soft pin)")
