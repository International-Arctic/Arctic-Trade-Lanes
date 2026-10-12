#!/usr/bin/env python3
"""Lock check: ARC-PROG-717 BLM NPR-A lease sale pin must stay on the NPR-A area centroid
(gis-npra-1123, 2026-10-12).

It used to sit on a round soft 69.0 / -152.0 in the eastern NPR-A interior. Anchor =
OpenStreetMap protected_area relation/8870643 Nominatim centroid (69.7266466,
-156.7005363), corroborated by Wikidata Q6974897 P625 (70, -157) and Wikipedia
70°N 157°W. Prefer properties.position_anchor when display geometry is nudged.
DISTINCT from ARC-PROG-626 (Anchorage admin seat) and ARC-PROG-734 (Deadhorse).
Usage: python3 scripts/check_prog717_npra.py [atlas.wgs84.geojson]
"""
import json, math, sys

ANCHOR = (69.7266466, -156.7005363)  # lat, lon (OSM relation/8870643)
OLD = (69.0, -152.0)
MAX_KM = 5.0
SISTER_MIN_KM = {
    "ARC-PROG-626": 500.0,  # Anchorage admin seat
    "ARC-PROG-734": 100.0,  # Deadhorse / Prudhoe
}

def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371.0088 * 2 * math.asin(math.sqrt(h))

path = sys.argv[1] if len(sys.argv) > 1 else "atlas.wgs84.geojson"
feats = {f["properties"].get("id"): f for f in json.load(open(path, encoding="utf-8"))["features"]}
f = feats.get("ARC-PROG-717")
if not f:
    sys.exit("FAIL ARC-PROG-717 missing")
lon, lat = (f["properties"].get("position_anchor") or f["geometry"]["coordinates"])[:2]
d = km((lat, lon), ANCHOR)
errs = []
if d > MAX_KM:
    errs.append(f"ARC-PROG-717 is {d:.1f} km from the NPR-A OSM area centroid (max {MAX_KM})")
if km((lat, lon), OLD) < 50:
    errs.append("ARC-PROG-717 is back on the soft 69.0/-152.0 placeholder")
if not (68.0 <= lat <= 71.5 and -162.0 <= lon <= -150.5):
    errs.append("ARC-PROG-717 is outside the NPR-A bounding box")
pq = f["properties"].get("position_quality")
if pq not in ("area_centroid", None):
    # None allowed only on pre-tag atlases; prefer area_centroid after gis-npra-1123
    if pq and pq != "area_centroid":
        errs.append(f"ARC-PROG-717 position_quality={pq!r} (expected area_centroid)")
for sid, min_km in SISTER_MIN_KM.items():
    s = feats.get(sid)
    if not s:
        continue
    slon, slat = (s["properties"].get("position_anchor") or s["geometry"]["coordinates"])[:2]
    ds = km((lat, lon), (slat, slon))
    if ds < min_km:
        errs.append(f"ARC-PROG-717 is only {ds:.1f} km from {sid} (need ≥ {min_km})")
if errs:
    print("FAIL\n" + "\n".join(errs)); sys.exit(1)
print(
    f"OK ARC-PROG-717 NPR-A {lat:.4f},{lon:.4f} "
    f"({d:.2f} km from OSM centroid; moved {km(OLD, ANCHOR):.0f} km off soft grid; pq={pq!r})"
)
