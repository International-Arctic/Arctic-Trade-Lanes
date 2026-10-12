#!/usr/bin/env python3
"""Lock for gis-wpport-1636 (2026-10-12): redundant endpoint-town lane waypoints.

Lanes repeated their own start/end port as a town GAZETTEER waypoint (Prudhoe Bay, Sabetta,
Barrow, Murmansk, Pevek, ...). The token resolved to a settlement centroid on Natural Earth 10m
land a few km from the harbour pin, so the lane hopped inland and back (LANE-016/017: 9 km).
build_atlas.py now gives such a waypoint its own endpoint port pin (toggle ATL_LANE_WP_PORT_SNAP=0)
and the consecutive-duplicate pass drops it. This check fails if a town centroid comes back.

Usage: python3 check_wpport_endpoint_spur.py [atlas.wgs84.geojson | URL]
"""
import json, sys, urllib.request

SRC = sys.argv[1] if len(sys.argv) > 1 else "https://arctictradelanes.com/atlas.wgs84.geojson"
C = {
    "Prudhoe Bay": (-148.3816, 70.2554), "Sabetta": (72.052, 71.256), "Barrow": (-156.7887, 71.2906),
    "Murmansk": (33.0827, 68.9585), "Pevek": (170.27, 69.7008), "Arkhangelsk": (40.5185, 64.5393),
    "Reykjavik": (-21.9426, 64.1466), "Nuuk": (-51.6941, 64.1814), "Oulu": (25.4651, 65.0121),
    "Kaliningrad": (20.4522, 54.7104), "Kristiansand": (8.0, 58.15),
}
EXPECT_ABSENT = {
    "ARC-LANE-001": ["Murmansk"], "ARC-LANE-002": ["Pevek"], "ARC-LANE-003": ["Murmansk"],
    "ARC-LANE-006": ["Murmansk"], "ARC-LANE-007": ["Arkhangelsk"], "ARC-LANE-010": ["Nuuk"],
    "ARC-LANE-012": ["Sabetta", "Kaliningrad"], "ARC-LANE-013": ["Sabetta"],
    "ARC-LANE-016": ["Prudhoe Bay"], "ARC-LANE-017": ["Prudhoe Bay"], "ARC-LANE-018": ["Barrow"],
    "ARC-LANE-019": ["Barrow"], "ARC-LANE-020": ["Reykjavik", "Nuuk"], "ARC-LANE-021": ["Oulu", "Murmansk"],
    "ARC-LANE-022": ["Kaliningrad"], "ARC-LANE-023": ["Sabetta"], "ARC-LANE-025": ["Murmansk"],
    "ARC-LANE-026": ["Kristiansand"], "ARC-LANE-027": ["Murmansk"],
}

if SRC.startswith("http"):
    req = urllib.request.Request(SRC, headers={"User-Agent": "atl-check/1.0"})
    data = json.load(urllib.request.urlopen(req, timeout=60))
else:
    data = json.load(open(SRC, encoding="utf-8"))
lanes = {f["properties"].get("id"): f for f in data["features"] if f["properties"].get("layer") == "lanes"}
bad = 0
for lid, towns in EXPECT_ABSENT.items():
    f = lanes.get(lid)
    if not f:
        print("MISSING", lid); bad += 1; continue
    cs = f["geometry"]["coordinates"]
    for t in towns:
        lo, la = C[t]
        if any(abs(c[0] - lo) < 1e-4 and abs(c[1] - la) < 1e-4 for c in cs):
            print("FAIL", lid, "still has", t, "town centroid", C[t]); bad += 1
print("OK" if not bad else f"{bad} failures", f"({len(EXPECT_ABSENT)} lanes checked, gen {data.get('generated', '?')})")
sys.exit(1 if bad else 0)
