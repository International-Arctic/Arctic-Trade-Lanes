#!/usr/bin/env python3
"""Lock for gis-lanewp-1418 (2026-10-12): lane waypoints that name a landmass must not sit on land.

GAZETTEER tokens "Alaska" (68N 152W, Brooks Range), "Yamal Peninsula" (71N 70E), "Kolguev Island"
(69N 49E), "Disko Bay" (69.5N 53W, on Disko Island) and "Mackenzie Delta" (69N 135W) resolve to points
on Natural Earth 10m land >15 km from water. The builder now moves them to open water and tags the lane
with `waypoint_water_snap`. Stdlib only.

Usage: python3 scripts/check_lane_waypoint_water.py [atlas.wgs84.geojson | URL]
"""
import json, math, sys, urllib.request

SRC = sys.argv[1] if len(sys.argv) > 1 else "https://arctictradelanes.com/atlas.wgs84.geojson"
RAW_LAND = {  # (lon, lat) of landlocked region tokens
    "Alaska": (-152.0, 68.0), "Yamal Peninsula": (70.0, 71.0), "Kolguev Island": (49.0, 69.0),
    "Disko Bay": (-53.0, 69.5), "Mackenzie Delta": (-135.0, 69.0),
}
EXPECT_SNAP = {"ARC-LANE-006", "ARC-LANE-010", "ARC-LANE-017", "ARC-LANE-023", "ARC-LANE-025"}
MAX_LAND_KM_AFTER = {"ARC-LANE-023": 60, "ARC-LANE-025": 60}


def hav(lo1, la1, lo2, la2):
    r = math.radians
    h = math.sin(r(la2 - la1) / 2) ** 2 + math.cos(r(la1)) * math.cos(r(la2)) * math.sin(r(lo2 - lo1) / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(h))


def load(src):
    if src.startswith("http"):
        req = urllib.request.Request(src, headers={"User-Agent": "atl-check/1.0"})
        return json.load(urllib.request.urlopen(req, timeout=60))
    return json.load(open(src, encoding="utf-8"))


fails = []
lanes = {f["properties"].get("id") or f.get("id"): f for f in load(SRC)["features"]
         if f["properties"].get("layer") == "lanes"}
for lid, f in sorted(lanes.items()):
    p = f["properties"]
    if "river" in (p.get("name") or "").lower():
        continue
    for lo, la in f["geometry"]["coordinates"]:
        for tok, (rlo, rla) in RAW_LAND.items():
            if hav(lo, la, rlo, rla) < 1.0:
                fails.append(f"{lid}: vertex on landlocked '{tok}' anchor {rla},{rlo}")
for lid in sorted(EXPECT_SNAP):
    if lid not in lanes:
        fails.append(f"{lid}: missing"); continue
    if not lanes[lid]["properties"].get("waypoint_water_snap"):
        fails.append(f"{lid}: no waypoint_water_snap tag")
for lid, mx in MAX_LAND_KM_AFTER.items():
    v = (lanes.get(lid) or {}).get("properties", {}).get("route_land_km_after")
    if v is None or v > mx:
        fails.append(f"{lid}: route_land_km_after={v} > {mx}")
l25 = lanes.get("ARC-LANE-025")
if l25:
    lo, la = l25["geometry"]["coordinates"][-1]
    if la < 70.2:
        fails.append(f"ARC-LANE-025: Transpolar ends inland at {la:.3f},{lo:.3f} (expected Beaufort coast >=70.2N)")
if fails:
    print("FAIL"); [print(" -", x) for x in fails]; sys.exit(1)
print(f"OK lane waypoint water: {len(lanes)} lanes, {len(EXPECT_SNAP)} snapped, 0 landlocked region vertices")
