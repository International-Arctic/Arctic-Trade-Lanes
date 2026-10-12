#!/usr/bin/env python3
"""Lock check: ARC-FAC-352 Buksefjorden soft pin must stay quarantined (gis-fac352-1146).

ARC-FAC-352 was a soft duplicate of ARC-FAC-005 (NunaGreen/Nukissiorfiit Utoqqarmiut
Kangerluarsunnguat / Buksefjorden hydropower expansion, 76.9 MW). Soft coords were
64.16/-51.60 (~43.6 km NW of densified FAC-005 at GEM 63.9211/-50.8909 /
Wikidata Q1366227). Quarantine clears lat/lon so the atlas builder drops the pin
(same pattern as ARC-SHIP-022 / ARC-SHIP-025). Keep ARC-FAC-005 as the sole map feature.

Usage: python3 scripts/check_fac352_buksefjorden_quarantine.py [atlas.wgs84.geojson]
"""
import json, math, sys

KEEP = (63.9211, -50.8909)  # lat, lon FAC-005
OLD_SOFT = (64.16, -51.60)


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))


path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
errs = []
if "ARC-FAC-352" in feats:
    f = feats["ARC-FAC-352"]
    lon, lat = f["geometry"]["coordinates"][:2]
    errs.append(
        f"ARC-FAC-352 still on atlas at {lat},{lon} — expected quarantine drop "
        f"(duplicate of ARC-FAC-005; soft was {OLD_SOFT[0]}/{OLD_SOFT[1]})"
    )
f5 = feats.get("ARC-FAC-005")
if not f5:
    errs.append("ARC-FAC-005 missing (canonical Buksefjorden pin)")
else:
    lon, lat = f5["geometry"]["coordinates"][:2]
    d = km((lat, lon), KEEP)
    if d > 2.0:
        errs.append(f"ARC-FAC-005 drifted {d:.1f} km from GEM/WD anchor {KEEP}")
if errs:
    print("FAIL\n" + "\n".join(errs))
    sys.exit(1)
print(
    f"OK ARC-FAC-352 quarantined (absent); ARC-FAC-005 kept at "
    f"{f5['geometry']['coordinates'][1]:.4f},{f5['geometry']['coordinates'][0]:.4f} "
    f"({km((f5['geometry']['coordinates'][1], f5['geometry']['coordinates'][0]), KEEP):.2f} km from GEM; "
    f"soft-dup was {km(OLD_SOFT, KEEP):.0f} km NW)"
)
