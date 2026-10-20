#!/usr/bin/env python3
"""gis-loop-1020-1120: move ARC-PORT-101 Clyde River Small Craft Harbour (CACLR) onto the official DFO Small Craft Harbours point.

Soft pin 70.4753/-68.5890 (4-decimal) sat inland in Clyde River hamlet (OSM residential way/400079381, near the health centre).
Fisheries and Oceans Canada open data "Small Craft Harbours Locations and Information" (open.canada.ca 262451e7-6416-47b5-8453-f31d212ea657;
egisp.dfo-mpo.gc.ca small_craft_harbours_en MapServer layer 0) lists Harbour_number 5992 "Clyde River", NU, Core Fishing at
70.466932/-68.597123. ~0.98 km SSW. facility_site (official registry harbour point, not a surveyed berth). Confidence 97 kept.
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-101"
TAG = "gis-loop-1020-1120"
NEW_LAT, NEW_LON = "70.4669320", "-68.5971230"
OLD = ("70.4753", "-68.5890")
NOTE = (
    "GIS quality densify 2026-10-20 ~11:20 MSK gis-loop-1020-1120: moved off soft 70.4753/-68.5890 (4-decimal pin inland in Clyde River "
    "hamlet, residential street near the health centre) to the official Fisheries and Oceans Canada Small Craft Harbours point "
    "(DFO open data Small Craft Harbours Locations and Information, open.canada.ca 262451e7-6416-47b5-8453-f31d212ea657; "
    "egisp.dfo-mpo.gc.ca small_craft_harbours_en layer 0): Harbour_number 5992 Clyde River NU, Core Fishing, 70.466932/-68.597123 "
    "(~0.98 km SSW); facility_site registry harbour point, not a surveyed berth line; confidence and other attributes left unchanged"
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
    '            "ARC-PORT-101": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Clyde River Small Craft Harbour (UN/LOCODE CACLR; DFO Small Craft Harbours Harbour_number 5992, Core Fishing): official Fisheries and Oceans Canada open-data harbour point 70.466932/-68.597123 (Small Craft Harbours Locations and Information, egisp.dfo-mpo.gc.ca small_craft_harbours_en layer 0); soft 70.4753/-68.5890 was inland in Clyde River hamlet (~0.98 km NNE); registry harbour point, not a surveyed berth line; facility_site",\n'
    '            },\n'
)
ANCH = '            "ARC-PORT-139": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-139": {' in s:
            print("builder already has entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp); continue
        shutil.copy2(rp, rp + ".bak-" + TAG)
        open(rp, "w", encoding="utf-8").write(s.replace(ANCH, ENTRY + ANCH))
        print("builder patched", rp)
print("csv files patched", n)
