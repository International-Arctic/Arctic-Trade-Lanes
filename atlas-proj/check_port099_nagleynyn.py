#!/usr/bin/env python3
"""Lock check: ARC-PORT-099 Pevek Cape Nagleynyn Marine Terminal at the mapped terminal site (gis-port099-1424).

Prior soft pin 69.7200 / 170.2000 sat in Pevek Strait water ~82 km NE of the real site.
Anchor = OSM way/1514011213 'Naglyoygnyn Port' centroid 69.0382643 / 169.3878168, ~5 km SSE of
Cape Nagleynyn (OSM node/9513605008, Wikidata Q37885662). Tag position_quality=facility_site (under construction).
Usage: python3 check_port099_nagleynyn.py [atlas.wgs84.geojson]
"""
import json, math, sys

ANCHOR = (69.0382643, 169.3878168)  # lat, lon
CAPE = (69.0792927, 169.3310737)
OLD = (69.7200, 170.2000)
MAX_KM = 2.0


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))


path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
errs = []
f = feats.get("ARC-PORT-099")
if not f:
    errs.append("ARC-PORT-099 missing")
else:
    lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
    d = km((lat, lon), ANCHOR)
    if d > MAX_KM:
        errs.append(f"ARC-PORT-099 is {d:.2f} km from the Naglyoygnyn Port anchor (max {MAX_KM})")
    if km((lat, lon), OLD) < 20.0:
        errs.append("ARC-PORT-099 is back near the soft 69.7200/170.2000 Pevek Strait pin")
    if km((lat, lon), CAPE) > 10.0:
        errs.append("ARC-PORT-099 is more than 10 km from Cape Nagleynyn")
    pq = f["properties"].get("position_quality")
    if pq != "facility_site":
        errs.append(f"ARC-PORT-099 position_quality={pq!r} (expected facility_site)")
if errs:
    print("FAIL\n" + "\n".join(errs))
    sys.exit(1)
lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
print(
    f"OK ARC-PORT-099 Cape Nagleynyn terminal {lat:.7f},{lon:.7f} "
    f"({km((lat, lon), ANCHOR):.3f} km from OSM way/1514011213; {km((lat, lon), CAPE):.2f} km from the cape; moved {km(OLD, ANCHOR):.1f} km off soft pin)"
)
