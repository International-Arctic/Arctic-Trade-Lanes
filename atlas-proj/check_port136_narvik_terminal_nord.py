#!/usr/bin/env python3
"""Lock check: ARC-PORT-136 Narvik Terminal Nord at Kleivhammaren, Fagernesveien (gis-port136-1346).

Prior soft pin 68.4400 / 17.4200 sat ~1.8 km N in Narvik city/harbour.
Anchor = OSM node/6372382875 (bus stop 'Kleivhammarn' on Fagernesveien) 68.4241270 / 17.4309920.
Adopted area plan Narvikterminalen med Terminal Nord (PlanID 2021001, 18.04.2024): Terminal nord between the
RO-RO quay (Lillekleiva) and Kleivhammaren. Tag position_quality=facility_site (planned, not built).
Usage: python3 check_port136_narvik_terminal_nord.py [atlas.wgs84.geojson]
"""
import json, math, sys

ANCHOR = (68.4241270, 17.4309920)  # lat, lon
OLD = (68.4400, 17.4200)
MAX_KM = 1.0


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))


path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
errs = []
f = feats.get("ARC-PORT-136")
if not f:
    errs.append("ARC-PORT-136 missing")
else:
    lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
    d = km((lat, lon), ANCHOR)
    if d > MAX_KM:
        errs.append(f"ARC-PORT-136 is {d:.2f} km from the Kleivhammarn anchor (max {MAX_KM})")
    if km((lat, lon), OLD) < 1.0:
        errs.append("ARC-PORT-136 is back near the soft 68.4400/17.4200 pin")
    if not (68.415 <= lat <= 68.430 and 17.41 <= lon <= 17.44):
        errs.append(f"ARC-PORT-136 is outside the Lillekleiva-Kleiva box ({lat},{lon})")
    pq = f["properties"].get("position_quality")
    if pq != "facility_site":
        errs.append(f"ARC-PORT-136 position_quality={pq!r} (expected facility_site)")
if errs:
    print("FAIL\n" + "\n".join(errs))
    sys.exit(1)
lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
print(
    f"OK ARC-PORT-136 Narvik Terminal Nord {lat:.7f},{lon:.7f} "
    f"({km((lat, lon), ANCHOR):.3f} km from OSM node/6372382875; moved {km(OLD, ANCHOR):.2f} km off soft pin)"
)
