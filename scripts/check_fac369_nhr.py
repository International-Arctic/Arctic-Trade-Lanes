#!/usr/bin/env python3
"""Lock check: ARC-FAC-369 Nordic Hydrogen Route must stay on the Tornio-Haparanda border crossing (gis-nhr-1025, 2026-10-12).

It used to sit on a round soft 59.8, 20.8 in open water south-east of the Aland islands, ~690 km south of the
route it describes. NHR is a buried coastal pipeline round the Bothnian Bay (Vaasa - Haparanda/Tornio - Ornskoldsvik,
branch Lulea - Gallivare/Kiruna). Nordion Energi's consultation names Haparanda as the node joining the
Haparanda-Ornskoldsvik and Haparanda-Vaasa sections; Gasgrid's Sep 2025 H2 information package describes the
cross-border engineering and permitting work in the Tornio River. Anchor = Wikidata Q588976 Haparanda urban area.
Usage: python3 scripts/check_fac369_nhr.py [atlas.wgs84.geojson]
"""
import json, math, sys

ANCHOR = (65.834178, 24.117033)  # lat, lon (Wikidata Q588976 P625)
OLD = (59.8, 20.8)
MAX_KM = 3.0

def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))

path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
f = feats.get("ARC-FAC-369")
if not f:
    sys.exit("FAIL ARC-FAC-369 missing")
lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
d = km((lat, lon), ANCHOR)
errs = []
if d > MAX_KM:
    errs.append(f"ARC-FAC-369 is {d:.1f} km from the Haparanda anchor (max {MAX_KM})")
if km((lat, lon), OLD) < 50:
    errs.append("ARC-FAC-369 is back in the open sea south of Aland")
if not (63.0 <= lat <= 68.5 and 16.5 <= lon <= 26.5):
    errs.append("ARC-FAC-369 is outside the Bothnian Bay corridor box")
if errs:
    print("FAIL\n" + "\n".join(errs)); sys.exit(1)
print(f"OK ARC-FAC-369 Nordic Hydrogen Route {lat:.4f},{lon:.4f} ({d:.2f} km from anchor; moved {km(OLD, ANCHOR):.0f} km off open water)")
