#!/usr/bin/env python3
"""Lock check: ARC-FAC-330 Sarfartoq must stay on Mindat carbonatite locality (gis-1244).

Prior GEUS Bulletin 17 half-degree map centre was 66.5000 / -51.2500 (66°30′N 51°15′W).
Anchor = Mindat loc-123391 (66.4833333, -51.3166667) = 66°29′N 51°19′W for the
Sarfartoq carbonatite complex (Isortoq Fjord / Qeqqata). GEUS Bulletin 17 fig.1B
(66°30′N / 51°15′–51°18′W) corroborates the same complex (~3.5 km).
Usage: python3 scripts/check_fac330_sarfartoq.py [atlas.wgs84.geojson]
"""
import json, math, sys

ANCHOR = (66.4833333, -51.3166667)  # lat, lon (Mindat loc-123391)
OLD = (66.5000, -51.2500)
MAX_KM = 3.0


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))


path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
errs = []
f = feats.get("ARC-FAC-330")
if not f:
    errs.append("ARC-FAC-330 missing")
else:
    lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
    d = km((lat, lon), ANCHOR)
    if d > MAX_KM:
        errs.append(f"ARC-FAC-330 is {d:.1f} km from Mindat Sarfartoq anchor (max {MAX_KM})")
    if km((lat, lon), OLD) < 0.5:
        errs.append("ARC-FAC-330 is back on the GEUS half-degree 66.5000/-51.2500 grid centre")
    if not (66.40 <= lat <= 66.55 and -51.55 <= lon <= -51.10):
        errs.append(f"ARC-FAC-330 is outside the Sarfartoq carbonatite box ({lat},{lon})")
if errs:
    print("FAIL\n" + "\n".join(errs))
    sys.exit(1)
lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
print(
    f"OK ARC-FAC-330 Sarfartoq {lat:.7f},{lon:.7f} "
    f"({km((lat, lon), ANCHOR):.3f} km from Mindat loc-123391; moved {km(OLD, ANCHOR):.2f} km off GEUS grid)"
)
