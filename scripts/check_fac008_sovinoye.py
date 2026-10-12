#!/usr/bin/env python3
"""Lock check: ARC-FAC-008 Shelf-M / Sovinoye must stay on Wikidata deposit (gis-sovinoye-1213).

Prior soft deposit-area centroid was 68.45 / -179.4 (~144 km SW of the deposit).
Anchor = Wikidata Q4426549 P625 (69.5619444, 178.7491667) from ruwiki
«Совиное месторождение» (69°33′43″N 178°44′57″E). Co-sited ARC-PROG-303 uses the
same anchor (display may be co_site_nudged ~2 km). Prefer properties.position_anchor.
Usage: python3 scripts/check_fac008_sovinoye.py [atlas.wgs84.geojson]
"""
import json, math, sys

ANCHOR = (69.5619444, 178.7491667)  # lat, lon (WD Q4426549)
OLD = (68.45, -179.4)
MAX_KM = 3.0


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))


path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
errs = []
for fid in ("ARC-FAC-008", "ARC-PROG-303"):
    f = feats.get(fid)
    if not f:
        errs.append(f"{fid} missing")
        continue
    lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
    d = km((lat, lon), ANCHOR)
    if d > MAX_KM:
        errs.append(f"{fid} is {d:.1f} km from Wikidata Sovinoye anchor (max {MAX_KM})")
    if km((lat, lon), OLD) < 20:
        errs.append(f"{fid} is back on the soft 68.45/-179.4 deposit-area centroid")
    if not (69.3 <= lat <= 69.8 and 178.4 <= lon <= 179.1):
        errs.append(f"{fid} is outside the northern Chukotka Sovinoye box ({lat},{lon})")
if errs:
    print("FAIL\n" + "\n".join(errs))
    sys.exit(1)
f8 = feats["ARC-FAC-008"]
lon, lat = (f8["properties"].get("position_anchor") or f8["geometry"]["coordinates"])[:2]
print(
    f"OK ARC-FAC-008(+PROG-303) Sovinoye {lat:.4f},{lon:.4f} "
    f"({km((lat, lon), ANCHOR):.2f} km from WD Q4426549; moved {km(OLD, ANCHOR):.0f} km off soft centroid)"
)
