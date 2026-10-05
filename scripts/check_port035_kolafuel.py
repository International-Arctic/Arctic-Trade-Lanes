#!/usr/bin/env python3
"""Guard (gis-kolafuel-1704): ARC-PORT-035 Kola Bay Fuel Terminal must stay within 2 km of
the Kola Bay oil-depot pier (OSM man_made=pier way/86115687 "Нефтебаза", 68.93177/33.03303,
west shore of Kola Bay, south Murmansk). Before 2026-10-05 it sat on land at 69.0/33.25,
~8.7 km east of Murmansk and ~11.5 km from this pier. The match of this row to that depot is
not confirmed by an operator source, so the dataset row carries confidence 60.
Usage: python3 scripts/check_port035_kolafuel.py [atlas.wgs84.geojson]
"""
import json, math, sys
ANCHOR = (68.93177, 33.03303)
MAX_KM = 2.0
path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = json.load(open(path, encoding="utf-8"))["features"]
hit = [f for f in feats if f["properties"].get("id") == "ARC-PORT-035"]
if len(hit) != 1:
    sys.exit(f"FAIL expected 1 ARC-PORT-035 feature, got {len(hit)}")
lon, lat = hit[0]["geometry"]["coordinates"][:2]
p1, p2 = math.radians(lat), math.radians(ANCHOR[0])
d = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(ANCHOR[1] - lon) / 2) ** 2
km = 2 * 6371.0088 * math.asin(math.sqrt(d))
print(f"ARC-PORT-035 at {lat:.5f}/{lon:.5f}, {km:.2f} km from the Kola Bay oil-depot pier anchor")
sys.exit(0 if km <= MAX_KM else 1)
