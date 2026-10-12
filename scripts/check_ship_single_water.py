#!/usr/bin/env python3
"""CI / QA lock for gis-shipland-1318 (2026-10-12): lone ships on land anchors.

Before: the open-water ship fan only ran for route anchors shared by >1 ship, so a lone
icebreaker kept its raw anchor even when that anchor is a town on land. CCGS John A.
Macdonald (ARC-ICE-022, "Arctic Operations" -> Cambridge Bay anchor 69.12/-105.05) was
drawn on the hamlet, not on the water.

After: lone ships whose anchor is on Natural Earth 10m land move to the nearest open-water
slot (>=~1 km offshore) only if one exists within ~13 km (SINGLE_SHIP_WATER_MAX_R=0.12 deg).
River / lake / narrow-fjord ports (Dudinka, Cheboygan, Kirkenes) keep the raw port anchor.

Checks:
  1. ARC-ICE-022 is in open water, within 15 km of its anchor, display_offset=water_fan,
     position_anchor == [-105.05, 69.12].
  2. Every ship with display_offset=water_fan is off the land mask.
  3. Lone route_anchor ships still on land are only the allowlisted port anchors.

Usage: python3 scripts/check_ship_single_water.py [atlas.wgs84.geojson] [ne_10m_land.geojson]
Needs shapely>=2. Land mask downloaded to /tmp if not given.
"""
import json, math, os, sys, urllib.request
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


def on_land(lon, lat):
    pt = Point(lon, lat)
    return any(polys[i].contains(pt) for i in tree.query(pt))


def km(a, b):
    (lo1, la1), (lo2, la2) = a, b
    p1, p2 = math.radians(la1), math.radians(la2)
    c = math.sin(p1) * math.sin(p2) + math.cos(p1) * math.cos(p2) * math.cos(math.radians(lo2 - lo1))
    return 6371.0 * math.acos(max(-1.0, min(1.0, c)))


PORT_ANCHOR_ALLOW = {"ARC-ICE-006", "ARC-ICE-026", "ARC-ICE-052"}  # Dudinka, Cheboygan, Kirkenes
fail = 0
seen = False
for f in json.load(open(atlas, encoding="utf-8"))["features"]:
    p = f.get("properties") or {}
    if p.get("layer") not in ("tankers", "icebreakers"):
        continue
    sid = f.get("id") or p.get("id")
    lon, lat = f["geometry"]["coordinates"][:2]
    if sid == "ARC-ICE-022":
        seen = True
        anc = p.get("position_anchor")
        if on_land(lon, lat):
            print(f"FAIL {sid}: still on land at {lon},{lat}"); fail += 1
        if p.get("display_offset") != "water_fan" or anc != [-105.05, 69.12]:
            print(f"FAIL {sid}: display_offset={p.get('display_offset')} anchor={anc}"); fail += 1
        elif km((lon, lat), anc) > 15:
            print(f"FAIL {sid}: {km((lon, lat), anc):.1f} km from anchor (>15)"); fail += 1
    if p.get("display_offset") == "water_fan" and on_land(lon, lat):
        print(f"FAIL {sid}: water_fan pin on land at {lon},{lat}"); fail += 1
    if p.get("position_quality") == "route_anchor" and on_land(lon, lat) and sid not in PORT_ANCHOR_ALLOW:
        print(f"FAIL {sid} {p.get('name')}: lone ship on land, not an allowlisted port anchor"); fail += 1
if not seen:
    print("FAIL ARC-ICE-022 missing"); fail += 1
if fail:
    sys.exit(1)
print("check_ship_single_water: OK (ICE-022 in Cambridge Bay water; lone on-land pins = allowlisted ports only)")
