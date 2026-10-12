#!/usr/bin/env python3
"""gis-riverlane-1346 lock: river lanes in the atlas are ordered upstream -> mouth and carry no
teleport endpoint. Fails if any "River" lane has a leg longer than 1500 km, if LANE-015 Lena
still touches Franz Josef Land (ARC-PORT-049, 80.7975N 47.5568E), or if a river lane's latitude
drops by more than 0.5 deg between consecutive vertices before its mouth tail.
Usage: python3 check_river_lane_order.py [atlas.wgs84.geojson | https://arctictradelanes.com/atlas.wgs84.geojson]
"""
import json, math, sys, urllib.request

src = sys.argv[1] if len(sys.argv) > 1 else "out/atlas.wgs84.geojson"
if src.startswith("http"):
    d = json.load(urllib.request.urlopen(urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0 (ATL check_river_lane_order)"}), timeout=60))
else:
    d = json.load(open(src))


def hav(a, b):
    lon1, lat1, lon2, lat2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 2 * 6371.0088 * math.asin(math.sqrt(h))


bad = []
seen = 0
for f in d["features"]:
    p = f["properties"]
    if p.get("layer") != "lanes" or "river" not in (p.get("name") or "").lower():
        continue
    seen += 1
    cs = f["geometry"]["coordinates"]
    legs = [hav(a, b) for a, b in zip(cs, cs[1:])]
    if max(legs) > 1500:
        bad.append((p["id"], "leg_km", round(max(legs))))
    if p.get("geometry_quality") != "river_ordered":
        bad.append((p["id"], "not river_ordered", p.get("geometry_quality")))
    # monotonic north until the highest-latitude vertex (mouth), tail may step back <=150 km
    top = max(range(len(cs)), key=lambda i: cs[i][1])
    for a, b in zip(cs[:top], cs[1:top + 1]):
        if b[1] < a[1] - 0.5:
            bad.append((p["id"], "zigzag", a, b))
    for c in cs[top + 1:]:
        if hav(cs[top], c) > 150 and c[1] < cs[top][1]:
            bad.append((p["id"], "tail_after_mouth", c))
    if p["id"] == "ARC-LANE-015" and any(abs(c[1] - 80.7975) < 0.01 and abs(c[0] - 47.5568) < 0.01 for c in cs):
        bad.append((p["id"], "still ends at Franz Josef Land"))

if seen < 2:
    bad.append(("river lanes", "expected >=2", seen))
print("check_river_lane_order:", "OK" if not bad else "FAIL", seen, "river lanes", bad)
sys.exit(1 if bad else 0)
