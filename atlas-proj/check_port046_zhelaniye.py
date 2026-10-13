#!/usr/bin/env python3
"""Lock check: ARC-PORT-046 Zhelaniye on OSM cape node/429774624 (gis-port046-1247).

Prior soft pin 76.9500 / 68.5500 sat ~0.59 km SW of Cape Zhelaniya (Mys Zhelaniya).
Anchor = OSM node/429774624 Nominatim 76.9542826 / 68.5639747 (WD Q2464613).
Tag position_quality=facility_site. Prefer properties.position_anchor.
Usage: python3 check_port046_zhelaniye.py [atlas.wgs84.geojson]
"""
import json, math, sys

ANCHOR = (76.9542826, 68.5639747)  # lat, lon
OLD = (76.9500, 68.5500)
MAX_KM = 1.0


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))


path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
errs = []
f = feats.get("ARC-PORT-046")
if not f:
    errs.append("ARC-PORT-046 missing")
else:
    lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
    d = km((lat, lon), ANCHOR)
    if d > MAX_KM:
        errs.append(f"ARC-PORT-046 is {d:.1f} km from OSM Cape Zhelaniya anchor (max {MAX_KM})")
    if km((lat, lon), OLD) < 0.3:
        errs.append("ARC-PORT-046 is back on the soft 76.9500/68.5500 pin")
    if not (76.94 <= lat <= 76.97 and 68.53 <= lon <= 68.59):
        errs.append(f"ARC-PORT-046 is outside the Cape Zhelaniya box ({lat},{lon})")
    pq = f["properties"].get("position_quality")
    if pq != "facility_site":
        errs.append(f"ARC-PORT-046 position_quality={pq!r} (expected facility_site)")
if errs:
    print("FAIL\n" + "\n".join(errs))
    sys.exit(1)
lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
print(
    f"OK ARC-PORT-046 Zhelaniye {lat:.7f},{lon:.7f} "
    f"({km((lat, lon), ANCHOR):.3f} km from OSM node/429774624; moved {km(OLD, ANCHOR):.2f} km off soft pin)"
)
