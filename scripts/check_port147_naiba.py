#!/usr/bin/env python3
"""Guard (gis-naiba-1524): ARC-PORT-147 Naiba (Nayba) planned deep-water port must stay
within 3 km of Naiba village, Kharaulakh Bay (Wikidata Q4312374 P625 70.8496/130.7551).
Before 2026-10-05 it sat at 71.9/128.5 near Tiksi, ~142 km away.
Usage: python3 scripts/check_port147_naiba.py [atlas.wgs84.geojson]
"""
import json, math, sys
ANCHOR = (70.8496, 130.7551)
MAX_KM = 3.0
path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = [f for f in json.load(open(path, encoding="utf-8"))["features"] if f["properties"].get("id") == "ARC-PORT-147"]
if len(feats) != 1:
    sys.exit(f"FAIL expected 1 ARC-PORT-147 feature, got {len(feats)}")
lon, lat = feats[0]["geometry"]["coordinates"][:2]
p1, p2 = math.radians(lat), math.radians(ANCHOR[0])
d = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(ANCHOR[1] - lon) / 2) ** 2
km = 2 * 6371.0088 * math.asin(math.sqrt(d))
print(f"ARC-PORT-147 at {lat:.4f}/{lon:.4f}, {km:.2f} km from Naiba anchor")
sys.exit(0 if km <= MAX_KM else 1)
