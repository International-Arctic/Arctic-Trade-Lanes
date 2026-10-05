#!/usr/bin/env python3
"""gis-seatland-1754 regression: no admin-seat-fanned program pin may sit in open water.

Usage: python3 scripts/check_program_seat_land.py [atlas.4326.geojson|URL] [ne_10m_land.geojson]
Defaults: live https://arctictradelanes.com/atlas.4326.geojson and Natural Earth 10m land
(public domain, https://naciscdn.org/naturalearth/10m/physical/ne_10m_land.zip, converted to GeoJSON).
Requires shapely>=2. Exits 1 if any fanned program pin is in water or any exact point stack remains.
"""
import json, math, sys, urllib.request, collections
from shapely.geometry import shape, Point
from shapely.strtree import STRtree

src = sys.argv[1] if len(sys.argv) > 1 else "https://arctictradelanes.com/atlas.4326.geojson"
mask = sys.argv[2] if len(sys.argv) > 2 else "ne_10m_land.geojson"
atlas = json.load(urllib.request.urlopen(src)) if src.startswith("http") else json.load(open(src))
polys = []
for f in json.load(open(mask))["features"]:
    g = shape(f["geometry"])
    polys += list(g.geoms) if g.geom_type == "MultiPolygon" else [g]
tree = STRtree(polys)

def on_land(lon, lat):
    pt = Point(lon, lat)
    return any(polys[i].contains(pt) for i in tree.query(pt))

fanned, wet, far = 0, [], 0.0
for f in atlas["features"]:
    p = f["properties"]
    if p.get("layer") != "programs" or p.get("position_quality") != "admin_seat_fan":
        continue
    fanned += 1
    lon, lat = f["geometry"]["coordinates"][:2]
    alon, alat = p["position_anchor"]
    far = max(far, math.hypot((lon - alon) * 111.32 * math.cos(math.radians(alat)), (lat - alat) * 110.57))
    if not on_land(lon, lat):
        wet.append(p.get("id"))
pts = collections.Counter(tuple(f["geometry"]["coordinates"]) for f in atlas["features"] if f["geometry"]["type"] == "Point")
stacked = sum(v for v in pts.values() if v > 1)
print(f"generated={atlas.get('generated')} fanned_programs={fanned} in_water={len(wet)} max_km_from_seat={far:.1f} exact_stacked_points={stacked}")
if wet:
    print("in water:", ", ".join(map(str, wet[:30])))
sys.exit(1 if (wet or stacked) else 0)
