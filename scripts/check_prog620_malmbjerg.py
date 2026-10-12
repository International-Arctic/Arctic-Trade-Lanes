#!/usr/bin/env python3
"""Lock check: ARC-PROG-620 Malmbjerg financing pin must stay on the mine (gis-malmbjerg-1048, 2026-10-12).

It used to sit on a round soft 71.9 / -22.5 about 62 km east of the deposit. Anchor = OpenStreetMap
historic=mine node/10703886750 (71.9605614, -24.2798494), which sits inside the NI 43-101 FS band
(71.57-71.59N / 24.14-24.19W) and matches GEUS Bulletin 17 / mapcarta.com/N10703886750.
Prefer properties.position_anchor when co-site nudge moves the display geometry (~2 km).
Usage: python3 scripts/check_prog620_malmbjerg.py [atlas.wgs84.geojson]
"""
import json, math, sys

ANCHOR = (71.9605614, -24.2798494)  # lat, lon (OSM node/10703886750)
OLD = (71.9, -22.5)
MAX_KM = 3.0

def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))

path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
f = feats.get("ARC-PROG-620")
if not f:
    sys.exit("FAIL ARC-PROG-620 missing")
lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
d = km((lat, lon), ANCHOR)
errs = []
if d > MAX_KM:
    errs.append(f"ARC-PROG-620 is {d:.1f} km from the Malmbjerg OSM mine anchor (max {MAX_KM})")
if km((lat, lon), OLD) < 20:
    errs.append("ARC-PROG-620 is back on the soft 71.9/-22.5 placeholder")
if not (71.5 <= lat <= 72.2 and -25.0 <= lon <= -23.5):
    errs.append("ARC-PROG-620 is outside the east-central Greenland Malmbjerg box")
if errs:
    print("FAIL\n" + "\n".join(errs)); sys.exit(1)
print(f"OK ARC-PROG-620 Malmbjerg {lat:.4f},{lon:.4f} ({d:.2f} km from OSM mine; moved {km(OLD, ANCHOR):.0f} km off soft grid)")
