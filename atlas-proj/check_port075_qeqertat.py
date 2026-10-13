#!/usr/bin/env python3
"""Lock check: ARC-PORT-075 Nuuk Qeqertat quay on OSM industrial=port south of container terminal (gis-port075-1525).

Prior soft pin 64.1700 / -51.7100 (2-decimal Qeqertanut approx).
Anchor = OSM way/627906959 industrial=port shoelace centroid 64.1678488 / -51.7140694
(VVM A246375 + Sikuki: west side of Qeqertaq Avalleq, south of 2017 container terminal).
Usage: python3 check_port075_qeqertat.py [atlas.wgs84.geojson]
"""
import json, math, sys

ANCHOR = (64.1678488, -51.7140694)
OLD = (64.1700, -51.7100)
MAX_KM = 0.5


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))


path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
errs = []
f = feats.get("ARC-PORT-075")
if not f:
    errs.append("ARC-PORT-075 missing")
else:
    lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
    d = km((lat, lon), ANCHOR)
    if d > MAX_KM:
        errs.append(f"ARC-PORT-075 is {d:.2f} km from the industrial=port anchor (max {MAX_KM})")
    if km((lat, lon), OLD) < 0.05:
        errs.append("ARC-PORT-075 is still on the soft 64.1700/-51.7100 pin")
    pq = f["properties"].get("position_quality")
    if pq != "facility_site":
        errs.append(f"ARC-PORT-075 position_quality={pq!r} (expected facility_site)")
    # co-site: must not collapse onto ARC-PORT-009
    f9 = feats.get("ARC-PORT-009")
    if f9:
        lon9, lat9 = (f9["properties"].get("position_anchor") or f9["geometry"]["coordinates"])[:2]
        if km((lat, lon), (lat9, lon9)) < 0.25:
            errs.append(f"ARC-PORT-075 too close to ARC-PORT-009 ({km((lat, lon), (lat9, lon9)):.3f} km)")
if errs:
    print("FAIL\n" + "\n".join(errs)); sys.exit(1)
lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
print(f"OK ARC-PORT-075 Nuuk Qeqertat quay {lat:.7f},{lon:.7f} ({km((lat, lon), ANCHOR):.3f} km from OSM way/627906959; moved {km(OLD, ANCHOR):.2f} km off soft pin)")
