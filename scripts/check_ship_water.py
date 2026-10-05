#!/usr/bin/env python3
"""CI / QA: no schematic ship pin (tankers, icebreakers) may sit on land.

Regression guard for gis-shipwater-1152. Ships in the ATL atlas carry no AIS truth;
they are fanned around a route anchor. The fan must stay in open water.
Single-ship `route_anchor` pins sit on their real port (river or lake ports such as
Dudinka or Cheboygan) and are reported but not failed.

Usage: python3 scripts/check_ship_water.py [atlas.wgs84.geojson] [ne_10m_land.geojson]
Land mask: Natural Earth 10m land (public domain); downloaded to /tmp if not given.
Needs shapely>=2.
"""
import json, os, sys, urllib.request
from shapely.geometry import shape, Point
from shapely.strtree import STRtree

atlas = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
land = sys.argv[2] if len(sys.argv) > 2 else "/tmp/ne_10m_land.geojson"
if not os.path.exists(land):
    urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_land.geojson", land)
polys = []
for f in json.load(open(land, encoding="utf-8"))["features"]:
    g = shape(f["geometry"])
    polys.extend(list(g.geoms) if g.geom_type == "MultiPolygon" else [g])
tree = STRtree(polys)

fail = warn = n = 0
for f in json.load(open(atlas, encoding="utf-8"))["features"]:
    p = f.get("properties") or {}
    if p.get("layer") not in ("tankers", "icebreakers"):
        continue
    n += 1
    pt = Point(*f["geometry"]["coordinates"][:2])
    if not any(polys[i].contains(pt) for i in tree.query(pt)):
        continue
    sid = f.get("id") or p.get("id")
    if p.get("position_quality") == "schematic_route_anchor":
        print(f"FAIL {sid} {p.get('name')}: schematic ship on land at {list(pt.coords)[0]}")
        fail += 1
    else:
        print(f"note {sid} {p.get('name')}: single route_anchor on land mask (port pin) at {list(pt.coords)[0]}")
        warn += 1
if fail:
    print(f"check_ship_water: {fail} schematic ship(s) on land of {n}")
    sys.exit(1)
print(f"check_ship_water: OK ({n} ships, 0 schematic on land, {warn} single port anchors noted)")
