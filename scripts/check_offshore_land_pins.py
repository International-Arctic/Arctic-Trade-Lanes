#!/usr/bin/env python3
"""QA: flag land-based ATL pins that sit far out at sea, and test the longitude sign-flip.

Added in gis-lonflip-1352 (2026-10-05). Three Anadyr rows (ARC-PORT-166 northern-supply
line, ARC-FAC-392 Nutekin gold, ARC-PROG-699 TOR Chukotka) had longitude -177.5 instead
of +177.5 (Anadyr is 64.73 N 177.50 E, Wikidata Q7978), which put them ~79 km out in the
Gulf of Anadyr on the wrong side of the antimeridian. Two more program rows were in open
sea for other reasons (Bilibino row in Norton Sound, a CanNor row east of Iceland).

For every Point in a land layer (cities, programs, industry, airports, rail, rescue, and
ports/shipyards with a looser limit) the script measures distance to the Natural Earth
10m coastline when the point is NOT on land. If it is further than --km offshore it also
tests the mirror point (-lon, lat) when the pin is within 10 degrees of the
antimeridian or the prime meridian: a mirror that lands on or next to land is a strong
hint the source row has a negated longitude (common near 180 E/W and 0 E/W).

Offshore by design (drift-ice bases, offshore wind, subsea cables, schematic routes) is
fine; add those ids to EXPECTED_OFFSHORE. Ids in LOCKED fail the run if they regress.

Usage: python3 scripts/check_offshore_land_pins.py [atlas.wgs84.geojson] [ne_10m_land.geojson] [--km 10]
Needs shapely>=2. Land mask is public-domain Natural Earth; downloaded to /tmp if missing.
"""
import json, math, os, sys, urllib.request
from shapely.geometry import shape, Point
from shapely.ops import unary_union, nearest_points
from shapely.prepared import prep

argv = sys.argv[1:]
km_lim = 10.0
if "--km" in argv:
    i = argv.index("--km"); km_lim = float(argv[i + 1]); del argv[i:i + 2]
atlas = argv[0] if argv else "atlas.wgs84.geojson"
land_p = argv[1] if len(argv) > 1 else "/tmp/ne_10m_land.geojson"
if not os.path.exists(land_p):
    urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_land.geojson", land_p)
L = unary_union([shape(f["geometry"]) for f in json.load(open(land_p, encoding="utf-8"))["features"]])
PL, coast = prep(L), L.boundary

FLIP_BAND = 10.0  # degrees from 180 E/W or 0 where a negated longitude stays nearby
LAND_LAYERS = {"cities", "programs", "industry", "airports", "rail", "rescue"}
COAST_LAYERS = {"ports": 3.0, "shipyards": 3.0}   # extra slack for quays/anchorages
EXPECTED_OFFSHORE = {
    "ARC-FAC-370",  # North Pole drift ice base (sea ice by definition)
    "ARC-FAC-399",  # Skyborn Polargrund offshore wind farm
    "ARC-FAC-354",  # NSR satellite-comms coverage layer (schematic, Kara Sea)
    "ARC-FAC-369",  # Nordic Hydrogen Route (schematic cross-border pipeline)
}
# Fixed in gis-lonflip-1352: must stay within this many km of land.
LOCKED = {"ARC-PORT-166": 3.0, "ARC-FAC-392": 3.0, "ARC-PROG-699": 3.0,
          "ARC-PROG-716": 3.0, "ARC-PROG-603": 3.0}

def hav_km(lo1, la1, lo2, la2):
    p1, p2 = math.radians(la1), math.radians(la2)
    d = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(lo2 - lo1) / 2) ** 2
    return 2 * 6371.0088 * math.asin(math.sqrt(d))

def offshore_km(x, y):
    pt = Point(x, y)
    if PL.contains(pt):
        return 0.0
    q = nearest_points(pt, coast)[1]
    return hav_km(x, y, q.x, q.y)

rows, flips, fail = [], [], 0
for f in json.load(open(atlas, encoding="utf-8"))["features"]:
    p = f.get("properties") or {}
    layer, g = p.get("layer"), f.get("geometry") or {}
    if g.get("type") != "Point" or (layer not in LAND_LAYERS and layer not in COAST_LAYERS):
        continue
    pid = p.get("id") or f.get("id")
    x, y = g["coordinates"][:2]
    km = offshore_km(x, y)
    if pid in LOCKED and km > LOCKED[pid]:
        print(f"FAIL {pid}: {km:.1f} km offshore at {y:.4f},{x:.4f}"); fail += 1
    lim = km_lim + COAST_LAYERS.get(layer, 0.0)
    if km <= lim or pid in EXPECTED_OFFSHORE:
        continue
    # Only test the mirror where a sign flip lands nearby: within FLIP_BAND degrees of
    # the antimeridian or the prime meridian. Elsewhere (-lon, lat) is a random spot on
    # another continent and "on land" means nothing.
    near_flip = abs(abs(x) - 180.0) <= FLIP_BAND or abs(x) <= FLIP_BAND
    mirror = offshore_km(-x, y) if near_flip else None
    rec = (km, pid, layer, (p.get("name") or "")[:70], round(y, 4), round(x, 4),
           None if mirror is None else round(mirror, 1))
    rows.append(rec)
    if mirror is not None and mirror <= 3.0:
        flips.append(rec)
rows.sort(reverse=True)
print(f"REVIEW {len(rows)} land-layer pins > {km_lim} km offshore (NE10m), mirror = km offshore at (-lon, lat), only tested within {FLIP_BAND} deg of 0/180:")
for r in rows:
    tag = "  <-- sign-flip suspect" if r in flips else ""
    print(f"  {r[0]:7.1f} km  {r[1]}  [{r[2]}]  {r[3]}  ({r[4]}, {r[5]})  mirror {"-" if r[6] is None else str(r[6]) + " km"}{tag}")
print(f"sign-flip suspects: {len(flips)} (a mirror on land is a hint, not proof: check the row's city/source)")
sys.exit(1 if fail else 0)
