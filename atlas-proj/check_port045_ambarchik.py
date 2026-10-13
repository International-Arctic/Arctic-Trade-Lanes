#!/usr/bin/env python3
"""Lock check: ARC-PORT-045 Ambarchik on OSM hamlet way/655223046 (gis-port045-1152).

Prior soft pin 69.6500 / 162.3500 sat ~3.3 km NE of the Ambarchik rural locality.
Anchor = OSM way/655223046 Nominatim 69.6252019 / 162.3024493 (WD Q2629730).
Tag position_quality=settlement_site. Prefer properties.position_anchor.
Usage: python3 check_port045_ambarchik.py [atlas.wgs84.geojson]
"""
import json, math, sys

ANCHOR = (69.6252019, 162.3024493)  # lat, lon
OLD = (69.6500, 162.3500)
MAX_KM = 1.0


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))


path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
errs = []
f = feats.get("ARC-PORT-045")
if not f:
    errs.append("ARC-PORT-045 missing")
else:
    lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
    d = km((lat, lon), ANCHOR)
    if d > MAX_KM:
        errs.append(f"ARC-PORT-045 is {d:.1f} km from OSM Ambarchik anchor (max {MAX_KM})")
    if km((lat, lon), OLD) < 1.0:
        errs.append("ARC-PORT-045 is back on the soft 69.6500/162.3500 pin")
    if not (69.60 <= lat <= 69.65 and 162.25 <= lon <= 162.35):
        errs.append(f"ARC-PORT-045 is outside the Ambarchik Bay box ({lat},{lon})")
    pq = f["properties"].get("position_quality")
    if pq != "settlement_site":
        errs.append(f"ARC-PORT-045 position_quality={pq!r} (expected settlement_site)")
if errs:
    print("FAIL\n" + "\n".join(errs))
    sys.exit(1)
lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
print(
    f"OK ARC-PORT-045 Ambarchik {lat:.7f},{lon:.7f} "
    f"({km((lat, lon), ANCHOR):.3f} km from OSM way/655223046; moved {km(OLD, ANCHOR):.1f} km off soft pin)"
)
