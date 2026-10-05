#!/usr/bin/env python3
"""Lock check for gis-fjlport-1850 (2026-10-05).

ARC-PORT-049 "Franz Josef Land Ports" used to sit on a round soft coordinate
80.0/55.0 in open water (~25 km from the nearest island). It is now anchored to
Nagurskoye, Alexandra Land (OSM way/1549655114 place=village; Wikidata Q1529324
Nagurskoye airfield ~2 km away), the main year-round base on the archipelago.

Usage: python3 scripts/check_port049_fjl.py [atlas.wgs84.geojson | URL]
Default: https://arctictradelanes.com/atlas/atlas.wgs84.geojson
"""
import json, math, sys, urllib.request

SRC = sys.argv[1] if len(sys.argv) > 1 else "https://arctictradelanes.com/atlas/atlas.wgs84.geojson"
ANCHOR = (80.7975295, 47.5567856)  # OSM way/1549655114 (lat, lon)
OLD = (80.0, 55.0)
LANES_ENDING_HERE = {"ARC-LANE-015", "ARC-LANE-024"}


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371.0088 * math.asin(math.sqrt(h))


def load(src):
    if src.startswith("http"):
        req = urllib.request.Request(src, headers={"User-Agent": "ATL-GIS-QA/1.0"})
        return json.load(urllib.request.urlopen(req, timeout=60))
    return json.load(open(src))


feats = {f["properties"].get("id"): f for f in load(SRC)["features"]}
ok = True
p = feats["ARC-PORT-049"]["geometry"]["coordinates"]
pt = (p[1], p[0])
d_anchor, d_old = km(pt, ANCHOR), km(pt, OLD)
print(f"ARC-PORT-049 at {pt[0]:.4f}/{pt[1]:.4f}: {d_anchor:.2f} km from Nagurskoye, {d_old:.1f} km from old soft pin")
if d_anchor > 3:
    ok = False
    print("FAIL: ARC-PORT-049 drifted >3 km from the Nagurskoye anchor")
for lid in sorted(LANES_ENDING_HERE):
    end = feats[lid]["geometry"]["coordinates"][-1]
    d = km((end[1], end[0]), pt)
    print(f"{lid} last vertex {d:.2f} km from ARC-PORT-049")
    if d > 1:
        ok = False
        print(f"FAIL: {lid} no longer ends at ARC-PORT-049")
print("OK" if ok else "FAILED")
sys.exit(0 if ok else 1)
