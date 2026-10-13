#!/usr/bin/env python3
"""Lock check: ARC-PORT-048 Wrangel Island Port on Ushakovskoye OSM settlement (gis-port048-wrangel).

Prior soft pin was 71.0167 / -178.5000 (~4.1 km inland/NW of the abandoned SE-coast
settlement). Anchor = OpenStreetMap node/1554927593 (70.98046, -178.48159);
Wikipedia Ushakovskoye, Chukotka 70deg58'51"N 178deg29'27"W (70.98083, -178.49083)
corroborates. Tag position_quality=settlement_site. Prefer properties.position_anchor.
Usage: python3 scripts/check_port048_wrangel.py [atlas.wgs84.geojson]
"""
import json, math, sys

ANCHOR = (70.98046, -178.48159)  # lat, lon (OSM node/1554927593)
OLD = (71.0167, -178.5000)
MAX_KM = 1.0


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))


path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
errs = []
f = feats.get("ARC-PORT-048")
if not f:
    errs.append("ARC-PORT-048 missing")
else:
    lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
    d = km((lat, lon), ANCHOR)
    if d > MAX_KM:
        errs.append(f"ARC-PORT-048 is {d:.1f} km from OSM Ushakovskoye anchor (max {MAX_KM})")
    if km((lat, lon), OLD) < 1.0:
        errs.append("ARC-PORT-048 is back on the soft 71.0167/-178.5000 pin")
    if not (70.95 <= lat <= 71.02 and -178.55 <= lon <= -178.40):
        errs.append(f"ARC-PORT-048 is outside the Wrangel SE Ushakovskoye box ({lat},{lon})")
    pq = f["properties"].get("position_quality")
    if pq != "settlement_site":
        errs.append(f"ARC-PORT-048 position_quality={pq!r} (expected settlement_site)")
if errs:
    print("FAIL\n" + "\n".join(errs))
    sys.exit(1)
lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
print(
    f"OK ARC-PORT-048 Wrangel/Ushakovskoye {lat:.5f},{lon:.5f} "
    f"({km((lat, lon), ANCHOR):.3f} km from OSM node/1554927593; moved {km(OLD, ANCHOR):.1f} km off soft pin)"
)
