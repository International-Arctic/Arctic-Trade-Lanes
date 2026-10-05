#!/usr/bin/env python3
"""QA: lane-depth.json must sample lanes as drawn in EPSG:3996 (gis-lanedepth-1826).

Fails if any lane's sampled path_km+out-of-grid share disagrees with its EPSG:3996
polyline length by >15%, or if any scored lane has <60% ocean coverage (sea lanes only).
Before the fix, antimeridian legs (179.9E -> 179.9W) were densified the long way round
the globe: Bering Strait Transit scored 17,866 km at 23% ocean coverage.

Usage: python3 scripts/check_lane_depth_antimeridian.py [base_url_or_dir]
  default base: https://arctictradelanes.com
"""
import json, math, os, sys, urllib.request

base = sys.argv[1] if len(sys.argv) > 1 else "https://arctictradelanes.com"

def load(rel):
    if base.startswith("http"):
        req = urllib.request.Request(base.rstrip("/") + "/" + rel, headers={"User-Agent": "atl-qa/1.0 (+https://github.com/International-Arctic/Arctic-Trade-Lanes)"})
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    return json.load(open(os.path.join(base, rel)))

lanes = load("bathy/lane-depth.json")["lanes"]
atlas = load("atlas.3996.geojson")
len3996 = {}
for f in atlas["features"]:
    if f["properties"].get("layer") != "lanes":
        continue
    g = f["geometry"]
    parts = g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]
    len3996[f["properties"]["id"]] = sum(math.hypot(b[0] - a[0], b[1] - a[1]) for p in parts for a, b in zip(p, p[1:])) / 1000.0

bad = []
for lid, v in sorted(lanes.items()):
    ref = len3996.get(lid)
    lane_km = v.get("lane_km", v.get("path_km"))
    if ref is None or lane_km is None:
        bad.append((lid, "missing")); continue
    # 3996 scale factor is ~0.97-1.05 in 60-85N; 15% tolerance covers it
    ratio = lane_km / ref if ref else 0
    river = "River" in (v.get("name") or "")
    cov = v.get("ocean_coverage_pct", 0)
    ok = 0.85 <= ratio <= 1.15 and (river or cov >= 60)
    print(f"{'OK ' if ok else 'BAD'} {lid} {v.get('name','')[:34]:34} lane_km={lane_km:>8} 3996_km={ref:8.1f} ratio={ratio:.2f} ocean%={cov}")
    if not ok:
        bad.append((lid, ratio, cov))
print(f"\n{len(lanes)} lanes checked, {len(bad)} failing")
sys.exit(1 if bad else 0)
