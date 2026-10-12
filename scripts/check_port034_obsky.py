#!/usr/bin/env python3
"""Lock check: ARC-PORT-034 Obskaya LNG Terminal must stay at Sabetta seaport (gis-obsky-0947, 2026-10-12).

It used to be a centroid clone of ARC-CITY-047 Novy Urengoy (66.0833, 76.6333), ~580 km inland.
Glavgosexpertiza (2020-03-10) places the terminal in Sabetta seaport on the west shore of the Gulf of Ob;
GEM wiki gives approx 71.2733, 72.0725. Usage: python3 scripts/check_port034_obsky.py [atlas.wgs84.geojson]
"""
import json, math, sys

ANCHOR = (71.2733, 72.0725)  # lat, lon
MAX_KM = 3.0

def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))

path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
f = feats.get("ARC-PORT-034")
if not f:
    sys.exit("FAIL ARC-PORT-034 missing")
p = f["properties"]
lon, lat = (p.get("position_anchor") or f["geometry"]["coordinates"])[:2]
d = km((lat, lon), ANCHOR)
errs = []
if d > MAX_KM:
    errs.append(f"ARC-PORT-034 is {d:.1f} km from the Sabetta anchor (max {MAX_KM})")
if p.get("geo_quality") == "centroid_clone":
    errs.append("ARC-PORT-034 is still stamped centroid_clone")
if km((lat, lon), (66.0833, 76.6333)) < 50:
    errs.append("ARC-PORT-034 is back on Novy Urengoy")
if errs:
    print("FAIL\n" + "\n".join(errs)); sys.exit(1)
print(f"OK ARC-PORT-034 Obskaya LNG Terminal {lat:.4f},{lon:.4f} ({d:.2f} km from anchor)")
