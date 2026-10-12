#!/usr/bin/env python3
"""Lock for gis-port037-1454 (2026-10-12): missing ARC-PORT-037 retargeted to real ports.

lanes.csv referenced ARC-PORT-037 (no row in ports.csv) as Alaska Arctic end for five lanes.
Builder fell back to GAZETTEER / city centroids: Transpolar ended on Harrison Bay coast after
landlocked Alaska snap; NWP Deep Water ended at schematic Beaufort -135/72. Retarget:
  ARC-LANE-005/018/019/025 -> ARC-PORT-056 Utqiagvik (Barrow) Port (OSM node/846364136)
  ARC-LANE-016             -> ARC-PORT-026 Nome Harbor (waypoints end at Nome)

Usage: python3 scripts/check_port037_utqiagvik.py [atlas.wgs84.geojson | URL | lanes.csv]
"""
import csv, json, math, sys, urllib.request

SRC = sys.argv[1] if len(sys.argv) > 1 else "https://arctictradelanes.com/atlas.wgs84.geojson"
UTQ = (-156.756832, 71.304296)  # ARC-PORT-056
NOME = (-165.437672, 64.496022)  # ARC-PORT-026
EXPECT_END = {
    "ARC-LANE-005": UTQ,
    "ARC-LANE-016": NOME,
    "ARC-LANE-019": UTQ,
    "ARC-LANE-025": UTQ,
}
EXPECT_START = {"ARC-LANE-018": UTQ}
MAX_KM = 2.5

def hav(a, b):
    lo1, la1 = a; lo2, la2 = b
    r = math.radians
    h = math.sin(r(la2 - la1) / 2) ** 2 + math.cos(r(la1)) * math.cos(r(la2)) * math.sin(r(lo2 - lo1) / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(h))

def load(src):
    if src.endswith(".csv"):
        return ("csv", list(csv.DictReader(open(src, encoding="utf-8"))))
    if src.startswith("http"):
        req = urllib.request.Request(src, headers={"User-Agent": "atl-check/1.0"})
        return ("atlas", json.load(urllib.request.urlopen(req, timeout=60)))
    return ("atlas", json.load(open(src, encoding="utf-8")))

kind, data = load(SRC)
fails = []
if kind == "csv":
    for r in data:
        lid = r.get("lane_id")
        if lid in EXPECT_END and r.get("end_port_id") not in (
            "ARC-PORT-056" if EXPECT_END[lid] == UTQ else "ARC-PORT-026",
        ):
            fails.append(f"{lid}: end_port_id={r.get('end_port_id')}")
        if lid in EXPECT_START and r.get("start_port_id") != "ARC-PORT-056":
            fails.append(f"{lid}: start_port_id={r.get('start_port_id')}")
        if "037" in (r.get("start_port_id") or "") + (r.get("end_port_id") or ""):
            fails.append(f"{lid}: still references ARC-PORT-037")
else:
    lanes = {f["properties"].get("id"): f for f in data["features"] if f["properties"].get("layer") == "lanes"}
    for lid, target in EXPECT_END.items():
        f = lanes.get(lid)
        if not f:
            fails.append(f"{lid}: missing"); continue
        last = tuple(f["geometry"]["coordinates"][-1][:2])
        d = hav(last, target)
        if d > MAX_KM:
            fails.append(f"{lid}: end {last} is {d:.2f} km from target {target}")
    for lid, target in EXPECT_START.items():
        f = lanes.get(lid)
        if not f:
            fails.append(f"{lid}: missing"); continue
        first = tuple(f["geometry"]["coordinates"][0][:2])
        d = hav(first, target)
        if d > MAX_KM:
            fails.append(f"{lid}: start {first} is {d:.2f} km from target {target}")
    # PORT-037 must not appear as a feature
    if any(f["properties"].get("id") == "ARC-PORT-037" for f in data["features"]):
        fails.append("ARC-PORT-037 feature unexpectedly present")
if fails:
    print("FAIL"); [print(" -", x) for x in fails]; sys.exit(1)
print(f"OK port037 retarget: 4 lanes end at Utqiagvik PORT-056, LANE-016 at Nome PORT-026, LANE-018 starts Utqiagvik")
