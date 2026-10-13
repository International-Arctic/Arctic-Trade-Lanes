#!/usr/bin/env python3
"""Lock check: ARC-PORT-041 Mys Shmidta on OSM hamlet way/93613726 (gis-port041-1216).

Prior soft pin 69.6500 / 162.3500 sat ~2.6 km S of the Mys Shmidta settlement (on a road near the airport).
Anchor = OSM way/93613726 Nominatim 69.6252019 / 162.3024493 (WD Q1020259).
Tag position_quality=settlement_site. Prefer properties.position_anchor.
Usage: python3 check_port045_ambarchik.py [atlas.wgs84.geojson]
"""
import json, math, sys

ANCHOR = (68.8928813, -179.4130958)  # lat, lon
OLD = (68.8700, -179.4000)
MAX_KM = 1.0


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))


path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
errs = []
f = feats.get("ARC-PORT-041")
if not f:
    errs.append("ARC-PORT-041 missing")
else:
    lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
    d = km((lat, lon), ANCHOR)
    if d > MAX_KM:
        errs.append(f"ARC-PORT-041 is {d:.1f} km from OSM Mys Shmidta anchor (max {MAX_KM})")
    if km((lat, lon), OLD) < 1.0:
        errs.append("ARC-PORT-041 is back on the soft 68.8700/-179.4000 pin")
    if not (68.87 <= lat <= 68.92 and -179.46 <= lon <= -179.38):
        errs.append(f"ARC-PORT-041 is outside the Cape Schmidt box ({lat},{lon})")
    pq = f["properties"].get("position_quality")
    if pq != "settlement_site":
        errs.append(f"ARC-PORT-041 position_quality={pq!r} (expected settlement_site)")
if errs:
    print("FAIL\n" + "\n".join(errs))
    sys.exit(1)
lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
print(
    f"OK ARC-PORT-041 Mys Shmidta {lat:.7f},{lon:.7f} "
    f"({km((lat, lon), ANCHOR):.3f} km from OSM way/93613726; moved {km(OLD, ANCHOR):.1f} km off soft pin)"
)
