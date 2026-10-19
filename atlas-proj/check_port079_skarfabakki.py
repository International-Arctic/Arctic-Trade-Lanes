#!/usr/bin/env python3
"""Lock: ARC-PORT-079 stays on the Skarfabakki cruise quay (gis-loop-1019-1758)."""
import json, sys
p = sys.argv[1] if len(sys.argv) > 1 else "out/atlas.4326.geojson"
f = [x for x in json.load(open(p))["features"] if x["properties"].get("id") == "ARC-PORT-079"][0]
lon, lat = f["geometry"]["coordinates"][:2]
assert abs(lat - 64.155015) < 2e-4 and abs(lon + 21.862063) < 4e-4, (lat, lon)
assert f["properties"].get("position_quality") == "facility_site"
print("ARC-PORT-079 lock OK", lat, lon)
