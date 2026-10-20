#!/usr/bin/env python3
"""gis-loop-1020-1247: move ARC-PORT-068 Whittier DeLong Dock (USWIT) onto the official USACE Navigation Facilities point.

Soft pin 60.7785/-148.6680 (4-decimal, GIS-2026-09-07 'east waterfront' estimate). U.S. Army Corps of Engineers Navigation Data
Center, Navigation Facilities (Master Docks) layer (services7.arcgis.com/n1YM8pTrFmm7L4hs/ArcGIS/rest/services/Docks/FeatureServer/0):
NAV_UNIT_ID 0UWL "DEFENSE FUEL SUPPLY POINT, WHITTIER DELONG PIER - AKRR", Dock, Validated for TOWS and Public, owner/operator
Alaska Railroad Corp. and City of Whittier, Delong-type pier barges, depth 45 ft MLLW (=13.7 m, matches max_depth_m), berthing 675 ft,
60.778333/-148.66722. ~46 m ESE. facility_site (registry dock point, not a surveyed berth line). Confidence 90 kept.
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-068"
TAG = "gis-loop-1020-1247"
NEW_LAT, NEW_LON = "60.7783330", "-148.6672200"
OLD = ("60.7785", "-148.6680")
NOTE = (
    "GIS quality densify 2026-10-20 ~12:47 MSK gis-loop-1020-1247: moved off soft 60.7785/-148.6680 (4-decimal east-waterfront estimate) "
    "to the official U.S. Army Corps of Engineers Navigation Data Center Navigation Facilities point (USACE NDC Docks layer, "
    "services7.arcgis.com/n1YM8pTrFmm7L4hs/ArcGIS/rest/services/Docks/FeatureServer/0): NAV_UNIT_ID 0UWL Whittier DeLong Pier "
    "(Alaska Railroad Corp. and City of Whittier; Delong-type pier barges; depth 45 ft MLLW = 13.7 m; berthing 675 ft), "
    "60.778333/-148.66722 (~46 m ESE); facility_site registry dock point, not a surveyed berth line; confidence and other attributes left unchanged"
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
    '            "ARC-PORT-068": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Whittier DeLong Dock (UN/LOCODE USWIT; USACE Navigation Data Center NAV_UNIT_ID 0UWL Whittier DeLong Pier, Alaska Railroad Corp. and City of Whittier; depth 45 ft MLLW): official USACE Navigation Facilities dock point 60.778333/-148.66722 (services7.arcgis.com/n1YM8pTrFmm7L4hs Docks FeatureServer layer 0); soft 60.7785/-148.6680 was a 4-decimal east-waterfront estimate (~46 m WNW); registry dock point, not a surveyed berth line; facility_site",\n'
    '            },\n'
)
ANCH = '            "ARC-PORT-139": {\n'
KEY = '"ARC-PORT-068": {'
bseen = set()
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True):
        rp = os.path.realpath(path)
        if rp in bseen or "node_modules" in rp:
            continue
        bseen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if KEY in s:
            print("builder already has ARC-PORT-068 entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp); continue
        shutil.copy2(rp, rp + ".bak-" + TAG)
        open(rp, "w", encoding="utf-8").write(s.replace(ANCH, ENTRY + ANCH))
        print("builder patched", rp)
print("csv files patched", n)
