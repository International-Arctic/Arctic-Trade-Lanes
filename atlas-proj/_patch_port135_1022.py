#!/usr/bin/env python3
"""gis-loop-1020-1022: densify ARC-PORT-135 Kalvåg New Fishing Harbor off land onto the Kystverket harbour point.

Soft pin 61.7625/4.8763 (4-decimal) reverse-geocodes to Bontlabo service road, Liset, Kalvåg (on land, OSM way/518544959).
Anchor: OSM node/5359785046 harbour=yes seamark:type=harbour seamark:harbour:category=fishing seamark:name=Kalvåg
source=Kystverket (Norwegian Coastal Administration import) at 61.764832/4.8758683, ~0.26 km N, inside the Kalvåg
harbour basin among OSM man_made=pier ways 1307682631-1307682642 / 1331485463-1331485472 / 571341676.
Confidence 88 and other attributes unchanged.
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-135"
TAG = "gis-loop-1020-1022"
NEW_LAT, NEW_LON = "61.764832", "4.8758683"
OLD = ("61.7625", "4.8763")
NOTE = (
    "GIS quality densify 2026-10-20 ~10:22 MSK gis-loop-1020-1022: moved off soft 61.7625/4.8763 (4-decimal pin on land at "
    "Bontlabo, Liset, Kalvåg) to the Kalvåg fishing harbour point from the Norwegian Coastal Administration: OSM "
    "node/5359785046 harbour=yes seamark:type=harbour seamark:harbour:category=fishing seamark:name=Kalvåg source=Kystverket "
    "at 61.764832/4.8758683 (~0.26 km N), inside the harbour basin among the mapped OSM man_made=pier ways; facility_site "
    "harbour point, not a surveyed berth line; confidence and other attributes left unchanged"
)
roots = sys.argv[1:] or ["."]
seen = set(); n = 0
for r in roots:
    for p in glob.glob(r + "/**/ports.csv", recursive=True):
        rp = os.path.realpath(p)
        if rp in seen or "node_modules" in rp or ".bak" in rp or "/_b" in rp or "/bak" in rp:
            continue
        seen.add(rp)
        raw = open(rp, encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in raw else "\n"
        has_trailing = raw.endswith("\n") or raw.endswith("\r\n")
        rows = list(csv.reader(io.StringIO(raw)))
        hit = False
        for i, row in enumerate(rows):
            if not row or row[0] != PID or len(row) < 20:
                continue
            old_lat, old_lon = row[4], row[5]
            if old_lat == NEW_LAT and old_lon == NEW_LON and TAG in (row[17] or ""):
                print("already", rp); continue
            if (old_lat, old_lon) != OLD:
                print("SKIP unexpected old coords", old_lat, old_lon, rp); continue
            row[4], row[5] = NEW_LAT, NEW_LON
            src = row[17] or ""
            if TAG not in src:
                row[17] = (src + " | " + NOTE) if src else NOTE
            row[19] = "2026-10-20"
            rows[i] = row
            hit = True
            print(f"row {old_lat}/{old_lon} -> {NEW_LAT}/{NEW_LON} conf {row[18]}", rp)
        if hit:
            shutil.copy2(rp, rp + ".bak-" + TAG)
            buf = io.StringIO()
            csv.writer(buf, lineterminator=nl).writerows(rows)
            out = buf.getvalue()
            if not has_trailing and out.endswith(nl):
                out = out[: -len(nl)]
            open(rp, "w", encoding="utf-8", newline="").write(out)
            n += 1

ENTRY = (
    '            "ARC-PORT-135": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Kalvåg fishing harbour (Bremanger, UN/LOCODE NOKVG): Kystverket harbour point OSM node/5359785046 harbour=yes seamark:type=harbour seamark:harbour:category=fishing source=Kystverket at 61.764832/4.8758683, inside the harbour basin among the mapped OSM man_made=pier ways; soft 61.7625/4.8763 was on land at Bontlabo, Liset (~0.26 km S); facility_site",\n'
    '            },\n'
)
ANCH = '            "ARC-PORT-132": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-135": {' in s:
            print("builder already has entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp); continue
        shutil.copy2(rp, rp + ".bak-" + TAG)
        open(rp, "w", encoding="utf-8").write(s.replace(ANCH, ENTRY + ANCH))
        print("builder patched", rp)
print("csv files patched", n)
