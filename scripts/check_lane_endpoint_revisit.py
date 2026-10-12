#!/usr/bin/env python3
"""Lock for gis-endrevisit-1743 (2026-10-12): lanes must not retrace back to an endpoint port
they already visited as an interior waypoint.

ARC-LANE-027 (Ningbo..Kara Gates-Murmansk-Hamburg-Felixstowe, end_port Murmansk) and ARC-LANE-010
(Nuuk..Ilulissat-Upernavik-Melville Bay, end_port Ilulissat) re-appended their end port after the
last waypoint, drawing a ~6,500 km / ~1,600 km duplicate line back along the coast.
build_atlas.py now skips an endpoint port already present as an interior vertex (<= 5 km), tagged
endpoint_revisit_skipped (toggle ATL_LANE_ENDPOINT_REVISIT=0).

Fails if any lane's first/last vertex reappears (<5 km) as a non-adjacent interior vertex AND the
trailing/leading retrace is longer than RETRACE_MAX_KM (short port hops like LANE-008 stay allowed).

Usage: python3 check_lane_endpoint_revisit.py [atlas.wgs84.geojson | URL]
"""
import json, math, sys, urllib.request

SRC = sys.argv[1] if len(sys.argv) > 1 else "https://arctictradelanes.com/atlas.wgs84.geojson"
NEAR_KM, RETRACE_MAX_KM = 5.0, 500.0


def hv(a, b):
    lo1, la1, lo2, la2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 12742 * math.asin(math.sqrt(h))


if SRC.startswith("http"):
    req = urllib.request.Request(SRC, headers={"User-Agent": "atl-check/1.0"})
    data = json.load(urllib.request.urlopen(req, timeout=60))
else:
    data = json.load(open(SRC, encoding="utf-8"))
bad = n = 0
for f in data["features"]:
    p = f["properties"]
    if p.get("layer") != "lanes" or f["geometry"]["type"] != "LineString":
        continue
    n += 1
    c = f["geometry"]["coordinates"]
    for side, idx in (("end", len(c) - 1), ("start", 0)):
        hits = [i for i in range(1, len(c) - 1) if abs(i - idx) > 1 and hv(c[i], c[idx]) < NEAR_KM]
        if not hits:
            continue
        j = max(hits) if side == "end" else min(hits)
        seg = c[j:] if side == "end" else c[:j + 1]
        km = sum(hv(seg[k], seg[k + 1]) for k in range(len(seg) - 1))
        if km > RETRACE_MAX_KM:
            print("FAIL", p.get("id"), side, f"retrace {km:.0f} km back to vertex #{j}")
            bad += 1
for lid, end in (("ARC-LANE-027", (1.35, 51.96)), ("ARC-LANE-010", (-62.0, 75.5))):
    f = next((x for x in data["features"] if x["properties"].get("id") == lid), None)
    if not f or hv(f["geometry"]["coordinates"][-1], end) > 15:
        print("FAIL", lid, "unexpected terminal", f and f["geometry"]["coordinates"][-1]); bad += 1
print("OK" if not bad else f"{bad} failures", f"({n} lanes, gen {data.get('generated', '?')})")
sys.exit(1 if bad else 0)
