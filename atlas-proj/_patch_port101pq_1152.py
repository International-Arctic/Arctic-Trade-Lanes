#!/usr/bin/env python3
"""gis-loop-1020-1152: metadata-only follow-up to gis-loop-1020-1120 (ARC-PORT-101 Clyde River SCH, CACLR).

The 1120 cycle moved ARC-PORT-101 onto the DFO Small Craft Harbours point 70.466932/-68.597123 in ports.csv, but the
builder-stamp step of _patch_port101_1120.py tested for the wrong id (ARC-PORT-139) and skipped, so the live atlas carried
the new geometry without a position_quality/position_note. This adds the ARC-PORT-101 entry to the builder
position_quality table. No coordinate change; ports.csv untouched.
"""
import glob, os, shutil, sys

TAG = "gis-loop-1020-1152"
ENTRY = (
    '            "ARC-PORT-101": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Clyde River Small Craft Harbour (UN/LOCODE CACLR; DFO Small Craft Harbours Harbour_number 5992, Core Fishing): official Fisheries and Oceans Canada open-data harbour point 70.466932/-68.597123 (Small Craft Harbours Locations and Information, egisp.dfo-mpo.gc.ca small_craft_harbours_en layer 0); soft 70.4753/-68.5890 was inland in Clyde River hamlet (~0.98 km NNE); registry harbour point, not a surveyed berth line; facility_site",\n'
    '            },\n'
)
ANCH = '            "ARC-PORT-139": {\n'
KEY = '"ARC-PORT-101": {'
roots = sys.argv[1:] or ["."]
seen = set(); n = 0
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if KEY in s:
            print("builder already has ARC-PORT-101 entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp); continue
        shutil.copy2(rp, rp + ".bak-" + TAG)
        open(rp, "w", encoding="utf-8").write(s.replace(ANCH, ENTRY + ANCH))
        print("builder patched", rp); n += 1
print("builders patched", n)
