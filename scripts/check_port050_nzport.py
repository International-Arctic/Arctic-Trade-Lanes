#!/usr/bin/env python3
"""Guard (gis-nzport-1555): ARC-PORT-050 Novaya Zemlya Ports must stay within 3 km of
Belushya Guba (Wikidata Q26324 P625 71.54075/52.336411), and ARC-PORT-164 (duplicate of
ARC-PORT-031 Lavna) must not render as its own pin. Before 2026-10-05 ARC-PORT-050 sat on
the Severny Island ice cap at 73.5/55.0 (~235 km away).
Usage: python3 scripts/check_port050_nzport.py [atlas.wgs84.geojson]
"""
import json, math, sys
ANCHOR = (71.54075, 52.336411)
MAX_KM = 3.0
path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = json.load(open(path, encoding="utf-8"))["features"]
ids = [f["properties"].get("id") for f in feats]
p050 = [f for f in feats if f["properties"].get("id") == "ARC-PORT-050"]
if len(p050) != 1:
    sys.exit(f"FAIL expected 1 ARC-PORT-050 feature, got {len(p050)}")
if "ARC-PORT-164" in ids:
    sys.exit("FAIL ARC-PORT-164 (Lavna duplicate of ARC-PORT-031) is rendered as its own pin")
lon, lat = p050[0]["geometry"]["coordinates"][:2]
p1, p2 = math.radians(lat), math.radians(ANCHOR[0])
d = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(ANCHOR[1] - lon) / 2) ** 2
km = 2 * 6371.0088 * math.asin(math.sqrt(d))
print(f"ARC-PORT-050 at {lat:.4f}/{lon:.4f}, {km:.2f} km from Belushya Guba anchor; ARC-PORT-164 alias dropped")
sys.exit(0 if km <= MAX_KM else 1)
