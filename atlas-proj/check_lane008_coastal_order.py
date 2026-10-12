#!/usr/bin/env python3
"""Lock for gis-lane008-1843 (2026-10-12): ARC-LANE-008 Norwegian Coastal Route must follow the
Hurtigruten northbound coastal order and must not detour to the Barents Sea basin centroid.

Before: lanes.csv waypoints `Tromso-Barents Sea-Soroya Island-Mageroya Island-Vardo-Honningsvag`,
end_port ARC-PORT-040 Honningsvag. The generic "Barents Sea" gazetteer centroid (75N 40E) pulled the
coastal lane ~950 km out into the open sea and back, then the line hopped Vardo -> Honningsvag
backwards: 2,528 km drawn for a 420 nm (~778 km) lane.
After: `Tromso-Soroya Island-Mageroya Island-Honningsvag-Vardo`, end_port ARC-PORT-032 Vardo Harbor
(order per en.wikipedia.org/wiki/Hurtigruten: ...Hammerfest-Havoysund-Honningsvag-...-Vardo-Vadso-Kirkenes).
Drawn length ~750 km (~405 nm), consistent with typical_distance_nm 420.

Usage: python3 check_lane008_coastal_order.py [atlas.wgs84.geojson | URL]
"""
import json, math, sys, urllib.request

SRC = sys.argv[1] if len(sys.argv) > 1 else "https://arctictradelanes.com/atlas.wgs84.geojson"
VARDO = (31.104407, 70.374591)      # ARC-PORT-032 Vardo Harbor
TROMSO_FIRST_LON = 18.9
MAX_KM, MAX_LON, MAX_LAT = 1100.0, 32.0, 71.6


def hv(a, b):
    lo1, la1, lo2, la2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 12742 * math.asin(math.sqrt(h))


if SRC.startswith("http"):
    req = urllib.request.Request(SRC, headers={"User-Agent": "atl-check/1.0"})
    data = json.load(urllib.request.urlopen(req, timeout=60))
else:
    data = json.load(open(SRC))

lane = next(f for f in data["features"] if f["properties"].get("id") == "ARC-LANE-008")
c = lane["geometry"]["coordinates"]
km = sum(hv(c[i], c[i + 1]) for i in range(len(c) - 1))
errs = []
if km > MAX_KM:
    errs.append(f"length {km:.0f} km > {MAX_KM:.0f} (Barents Sea basin detour back?)")
if max(p[0] for p in c) > MAX_LON or max(p[1] for p in c) > MAX_LAT:
    errs.append(f"vertex beyond coastal box lon<={MAX_LON} lat<={MAX_LAT}")
if hv(c[-1], VARDO) > 5:
    errs.append(f"does not end at Vardo ARC-PORT-032 ({hv(c[-1], VARDO):.1f} km off)")
if c[0][0] < TROMSO_FIRST_LON - 0.5 or c[0][0] > TROMSO_FIRST_LON + 0.5:
    errs.append(f"does not start at Tromso ({c[0]})")
if errs:
    print("FAIL ARC-LANE-008: " + "; ".join(errs))
    sys.exit(1)
print(f"OK ARC-LANE-008 {len(c)} vertices, {km:.0f} km, ends Vardo (gen {data.get('generated') or '?'})")
