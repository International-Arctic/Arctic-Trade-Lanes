#!/usr/bin/env python3
"""CI / QA: sea lanes must not cut across land (regression guard for gis-lanewater-1214).

Measures, in EPSG:3996 (polar stereographic, never Mercator), how much of each lane
polyline lies on Natural Earth 10m land. River lanes ("River" in the name) are skipped.
Fails if total sea-lane land length exceeds MAX_LAND_PCT (default 8%), and lists the
worst lanes so contributors know where waypoints need work.

Usage: python3 scripts/check_lane_water.py [atlas.wgs84.geojson] [ne_10m_land.geojson]
Needs shapely>=2 and pyproj.
"""
import json, os, sys, urllib.request
from pyproj import Transformer
from shapely.geometry import shape, box, LineString
from shapely.ops import transform, unary_union

atlas = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
land = sys.argv[2] if len(sys.argv) > 2 else "/tmp/ne_10m_land.geojson"
MAX_LAND_PCT = float(os.environ.get("MAX_LAND_PCT", "8"))
if not os.path.exists(land):
    urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_land.geojson", land)
t = Transformer.from_crs(4326, 3996, always_xy=True)
clip = box(-180, 15, 180, 90)
polys = []
for f in json.load(open(land, encoding="utf-8"))["features"]:
    g = shape(f["geometry"]).buffer(0)
    if g.intersects(clip):
        polys.append(transform(t.transform, g.intersection(clip)).buffer(0))
L = unary_union(polys)

tot = on_land = 0.0
rows = []
for f in json.load(open(atlas, encoding="utf-8"))["features"]:
    p = f.get("properties") or {}
    if p.get("layer") != "lanes" or "river" in (p.get("name") or "").lower():
        continue
    g = LineString([t.transform(*c[:2]) for c in f["geometry"]["coordinates"]])
    il = g.intersection(L).length
    tot += g.length; on_land += il
    rows.append((il / 1000, g.length / 1000, f.get("id") or p.get("id"), p.get("geometry_quality")))
rows.sort(reverse=True)
for il, gl, lid, q in rows[:8]:
    print(f"  {lid}: {il:.0f} km of {gl:.0f} km on land ({100*il/gl:.1f}%) [{q}]")
pct = 100 * on_land / tot if tot else 0
print(f"sea lanes: {len(rows)}, land {on_land/1000:.0f} km of {tot/1000:.0f} km = {pct:.1f}% (max {MAX_LAND_PCT}%)")
sys.exit(1 if pct > MAX_LAND_PCT else 0)
