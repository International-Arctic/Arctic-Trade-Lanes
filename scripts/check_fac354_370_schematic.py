#!/usr/bin/env python3
"""Lock check: ARC-FAC-354 / ARC-FAC-370 keep intentional schematic pins + position_quality
(gis-npra-1123, 2026-10-12).

FAC-354 = NSR corridor-wide BURO 1440 space-comms schematic centre (73.0, 80.0) —
  position_quality=schematic_corridor_center. Do NOT invent a fake HQ.
FAC-370 = North Pole drift-ice base schematic (89.5, 0.0) —
  position_quality=schematic_north_pole. Do NOT move off the polar region.
Usage: python3 scripts/check_fac354_370_schematic.py [atlas.wgs84.geojson]
"""
import json, math, sys

EXPECT = {
    "ARC-FAC-354": {
        "coord": (73.0, 80.0),  # lat, lon
        "pq": "schematic_corridor_center",
        "max_km": 1.0,
    },
    "ARC-FAC-370": {
        "coord": (89.5, 0.0),
        "pq": "schematic_north_pole",
        "max_km": 1.0,
    },
}

def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))

path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
errs = []
ok = []
for fid, exp in EXPECT.items():
    f = feats.get(fid)
    if not f:
        errs.append(f"{fid} missing"); continue
    lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
    d = km((lat, lon), exp["coord"])
    pq = f["properties"].get("position_quality")
    if d > exp["max_km"]:
        errs.append(f"{fid} moved {d:.1f} km off schematic anchor {exp['coord']}")
    if pq != exp["pq"]:
        errs.append(f"{fid} position_quality={pq!r} (expected {exp['pq']!r})")
    ok.append(f"{fid} {lat},{lon} pq={pq}")
if errs:
    print("FAIL\n" + "\n".join(errs)); sys.exit(1)
print("OK " + "; ".join(ok))
