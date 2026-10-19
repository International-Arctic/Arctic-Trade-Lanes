#!/usr/bin/env python3
"""gis-loop-1019-1245: densify ARC-PORT-140 Isafjordur Pier Extension (Sundabakki, Sundahofn; UN/LOCODE ISISA)
onto the OSM cruise quay polygon.

Soft pin 66.0755/-23.1080 (4-decimal; schematic offset from the ISISA parent ARC-PORT-077, ~1.2 km NE of the pier,
not on any quay). OSM way/1294792142 man_made=quay mooring=cruise name=Cruise Port (~16,400 m2, ~509 m long, v5),
shoelace centroid 66.0657813/-23.1204589 (inside polygon), south end of Sundahofn next to the Cruise Port Information
Center (OSM node/13048366035). Corroboration: vegagerdin.is "Sundabakki" (~300 m steel-sheet quay extension south of
the older addition, 11 m dredging, ~6,000 m2 deck; ships up to 330 m); cruisemapper.com (pier 190 m -> 500 m, ISK 1B).
No Wikidata item. position_quality=facility_site.
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-140"
TAG = "gis-loop-1019-1245"
NEW_LAT, NEW_LON = "66.0657813", "-23.1204589"
OLD = ("66.0755", "-23.1080")
NOTE = (
    "GIS quality densify 2026-10-19 ~12:45 MSK gis-loop-1019-1245: moved off soft 66.0755/-23.1080 "
    "(4-decimal schematic offset from ISISA parent ARC-PORT-077, ~1.2 km NE of the pier, not on a quay) to OSM "
    "way/1294792142 man_made=quay mooring=cruise Cruise Port (Sundabakki, Sundahofn; ~16,400 m2, ~509 m long) "
    "shoelace centroid 66.0657813/-23.1204589 (~1.22 km SSW, bearing ~207 deg); corroborated by vegagerdin.is Sundabakki project page "
    "(~300 m steel-sheet quay extension south of the older addition, 11 m dredging, ~6,000 m2 concrete deck, ships to 330 m) "
    "and cruisemapper.com (pier 190 m to 500 m, ISK 1B); next to Cruise Port Information Center OSM node/13048366035; "
    "no Wikidata item; UN/LOCODE ISISA unchanged; facility_site cruise quay, not a single berth"
)
assert '"' not in NOTE

roots = sys.argv[1:] or ["/home/workspace/ArcticTradeLanes-Dataset", "/home/workspace/ArcticTradeLanes.com"]
seen = set()
n = 0
for r in roots:
    for p in glob.glob(r + "/**/ports.csv", recursive=True):
        rp = os.path.realpath(p)
        if rp in seen or "node_modules" in rp or "_bak" in rp or ".bak" in rp:
            continue
        seen.add(rp)
        raw = open(rp, encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in raw else "\n"
        has_trailing = raw.endswith("\n") or raw.endswith("\r\n")
        rows = list(csv.reader(io.StringIO(raw)))
        if not rows:
            continue
        hit = False
        for i, row in enumerate(rows):
            if not row or row[0] != PID:
                continue
            if len(row) < 20:
                print("SKIP short row", rp, len(row))
                continue
            old_lat, old_lon = row[4], row[5]
            if old_lat == NEW_LAT and old_lon == NEW_LON and TAG in (row[17] or ""):
                print("already", rp)
                continue
            if (old_lat, old_lon) != OLD:
                print("SKIP unexpected old coords", old_lat, old_lon, rp)
                continue
            row[4], row[5] = NEW_LAT, NEW_LON
            src = row[17] or ""
            if TAG not in src:
                row[17] = (src + " + " + NOTE) if src else NOTE
            row[18] = "90"
            row[19] = "2026-10-19"
            rows[i] = row
            hit = True
            print(f"row {old_lat}/{old_lon} -> {NEW_LAT}/{NEW_LON} locode {row[6]}", rp)
        if hit:
            shutil.copy2(rp, rp + ".bak-" + TAG)
            buf = io.StringIO()
            csv.writer(buf, lineterminator=nl).writerows(rows)
            out = buf.getvalue()
            if not has_trailing and out.endswith(nl):
                out = out[: -len(nl)]
            open(rp, "w", encoding="utf-8", newline="").write(out)
            n += 1
            print("patched", rp)

ENTRY = (
    '            "ARC-PORT-140": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Isafjordur cruise pier extension, Sundabakki / Sundahofn (Hafnir Isafjardarbaejar; UN/LOCODE ISISA): OSM way/1294792142 man_made=quay mooring=cruise Cruise Port (~16,400 m2, ~509 m long), shoelace centroid 66.0657813/-23.1204589; Vegagerdin Sundabakki project (~300 m steel-sheet extension south of the older addition, 11 m dredging) and cruisemapper.com (190 m to 500 m) corroborate; soft 66.0755/-23.1080 was a schematic offset ~1.22 km NNE of the pier; no Wikidata item; facility_site cruise quay, not a single berth",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-134": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True) + glob.glob(r + "/build_atlas.py"):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-140": {' in s:
            print("builder already has entry", rp)
            continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp)
            continue
        shutil.copy2(rp, rp + ".bak-" + TAG)
        s = s.replace(ANCH, ENTRY + ANCH)
        open(rp, "w", encoding="utf-8").write(s)
        print("builder patched", rp)
print("csv files patched", n)
