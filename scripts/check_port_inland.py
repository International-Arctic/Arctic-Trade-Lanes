#!/usr/bin/env python3
"""QA: flag maritime pins (ports, shipyards) that sit far inland.

Added in gis-portbay-1245 after ARC-PORT-169 (VLT KORF, Korf Bay, Kamchatka) was found
~55 km inland at 60.25/163.05, about 150 km west of the bay it is named for.

A port can legitimately sit inland (river ports such as Dudinka or Salekhard, lake
yards such as Onega, company HQ rows), so this script REPORTS by default and only
FAILS for ids listed in LOCKED (pins that were fixed and must not regress).
Distance is to the Natural Earth 10m coastline; rivers and lakes are not in that mask,
so river ports show large distances. Review the report, do not bulk-move pins.

Usage: python3 scripts/check_port_inland.py [atlas.wgs84.geojson] [ne_10m_land.geojson] [--km 5]
Needs shapely>=2. Land mask is public-domain Natural Earth; downloaded to /tmp if missing.
"""
import json, math, os, sys, urllib.request
from shapely.geometry import shape, Point
from shapely.ops import unary_union, nearest_points

args = [a for a in sys.argv[1:] if not a.startswith("--")]
km_lim = 5.0
if "--km" in sys.argv:
    km_lim = float(sys.argv[sys.argv.index("--km") + 1]); args = [a for a in args if a != str(sys.argv[sys.argv.index("--km") + 1])]
atlas = args[0] if args else "atlas.wgs84.geojson"
land = args[1] if len(args) > 1 else "/tmp/ne_10m_land.geojson"
if not os.path.exists(land):
    urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_land.geojson", land)
L = unary_union([shape(f["geometry"]) for f in json.load(open(land, encoding="utf-8"))["features"]])
coast = L.boundary

# Fixed pins that must stay at the coast/bay (id -> max km inland allowed).
LOCKED = {"ARC-PORT-169": 0.0}

def hav_km(a, b):
    (lo1, la1), (lo2, la2) = a, b
    p1, p2 = math.radians(la1), math.radians(la2)
    d = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lo2 - lo1) / 2) ** 2
    return 2 * 6371.0088 * math.asin(math.sqrt(d))

rows, fail = [], 0
for f in json.load(open(atlas, encoding="utf-8"))["features"]:
    p = f.get("properties") or {}
    if p.get("layer") not in ("ports", "shipyards") or (f.get("geometry") or {}).get("type") != "Point":
        continue
    pt = Point(*f["geometry"]["coordinates"][:2])
    if not L.contains(pt):
        km = 0.0
    else:
        q = nearest_points(pt, coast)[1]
        km = hav_km((pt.x, pt.y), (q.x, q.y))
    pid = p.get("id") or f.get("id")
    if pid in LOCKED and km > LOCKED[pid]:
        print(f"FAIL {pid} {p.get('name')}: {km:.1f} km inland at {pt.x:.4f},{pt.y:.4f}"); fail += 1
    elif km > km_lim:
        rows.append((km, pid, p.get("layer"), (p.get("name") or "")[:70], round(pt.y, 4), round(pt.x, 4)))
rows.sort(reverse=True)
print(f"REVIEW {len(rows)} maritime pins > {km_lim} km from NE10m coastline (river/lake/HQ rows are expected):")
for r in rows:
    print(f"  {r[0]:7.1f} km  {r[1]}  [{r[2]}]  {r[3]}  ({r[4]}, {r[5]})")
print("OK" if not fail else f"{fail} locked pin(s) regressed")
sys.exit(1 if fail else 0)
