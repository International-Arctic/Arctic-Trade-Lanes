#!/usr/bin/env python3
"""Lock check: ARC-PORT-066 Vör Reykjavík Cruise Terminal OSM way/1391146178 (gis-loop-1019-1018)."""
import json, math, sys

ANCHOR = (64.1557650, -21.8646994)
OLD = (64.1680, -21.8520)
MAX_KM = 0.05


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))


path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
errs = []
f = feats.get("ARC-PORT-066")
if not f:
    errs.append("ARC-PORT-066 missing")
else:
    lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
    d = km((lat, lon), ANCHOR)
    if d > MAX_KM:
        errs.append(f"ARC-PORT-066 is {d:.3f} km from OSM way/1391146178 Vör anchor (max {MAX_KM})")
    if km((lat, lon), OLD) < 0.05:
        errs.append("ARC-PORT-066 is still on the soft 64.1680/-21.8520 pin")
    pq = f["properties"].get("position_quality")
    if pq != "facility_site":
        errs.append(f"ARC-PORT-066 position_quality={pq!r} (expected facility_site)")
# PORT-012 must stay at ferry terminal (not pulled onto Vör)
f12 = feats.get("ARC-PORT-012")
if f12:
    lon12, lat12 = (f12["properties"].get("position_anchor") or f12["geometry"]["coordinates"])[:2]
    d12 = km((lat12, lon12), (64.1564348, -21.8666787))
    if d12 > 0.05:
        errs.append(f"ARC-PORT-012 drifted from ferry_terminal node/694173331 ({d12:.3f} km)")
if errs:
    print("FAIL\n" + "\n".join(errs))
    sys.exit(1)
lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
print(
    f"OK ARC-PORT-066 Vör Reykjavík {lat:.7f},{lon:.7f} "
    f"({km((lat, lon), ANCHOR):.3f} km from OSM way/1391146178; moved {km(OLD, ANCHOR):.2f} km off soft)"
)
