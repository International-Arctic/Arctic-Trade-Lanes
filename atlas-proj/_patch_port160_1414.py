#!/usr/bin/env python3
"""gis-loop-1019-1414: densify ARC-PORT-160 Mjoeyrarhofn (Reydarfjordur, ISRFJ) onto the Mjoeyrarbryggja quay face.

Soft pin 65.0284/-14.1121 (4-decimal) sat on the harbour backland ~0.13 km NNE of the berth.
Anchor: midpoint of the 384 m quay face (OSM natural=coastline way/210145938, outer member of
OSM relation/2819859 landuse=industrial industrial=port name=Mjoeyrarhofn) at 65.0273990/-14.1134659.
Official fjardabyggdarhafnir.is: Mjoeyrarbryggja 383 m, 14.2 m, steel sheet pile; port position
65 01.66N 014 06.80W (~30 m away).
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-160"
TAG = "gis-loop-1019-1414"
NEW_LAT, NEW_LON = "65.0273990", "-14.1134659"
OLD = ("65.0284", "-14.1121")
CONF = "92"
NOTE = (
    "GIS quality densify 2026-10-19 ~14:14 MSK gis-loop-1019-1414: moved off soft 65.0284/-14.1121 "
    "(4-decimal pin on harbour backland ~0.13 km NNE of the berth) to the Mjoeyrarbryggja quay face: "
    "midpoint of the 384 m OSM natural=coastline way/210145938 (bearing 80/260 deg), outer member of "
    "OSM relation/2819859 landuse=industrial industrial=port name=Mjoeyrarhofn (~7.1 ha, centroid "
    "65.0282174/-14.1133016) at 65.0273990/-14.1134659 (~0.13 km SSW); corroborated by "
    "fjardabyggdarhafnir.is official Mjoeyrarhofn page (Mjoeyrarbryggja 383 m, 14.2 m, steel sheet pile; "
    "port position 65 01.66N 014 06.80W ~30 m away) and OSM seamark harbour node/626578135 "
    "Mjoeyrarhofn (~0.13 km W); no Wikidata port item; facility_site single-quay bulk harbour serving "
    "the adjacent Alcoa Fjardaal smelter; planned quay extension not yet built"
)
roots = sys.argv[1:] or ["."]
seen = set(); n = 0
for r in roots:
    for p in glob.glob(r + "/**/ports.csv", recursive=True):
        rp = os.path.realpath(p)
        if rp in seen or "node_modules" in rp or ".bak" in rp:
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
                row[17] = (src + " + " + NOTE) if src else NOTE
            row[18] = CONF; row[19] = "2026-10-19"; rows[i] = row; hit = True
            print(f"row {old_lat}/{old_lon} -> {NEW_LAT}/{NEW_LON}", rp)
        if hit:
            shutil.copy2(rp, rp + ".bak-" + TAG)
            buf = io.StringIO(); csv.writer(buf, lineterminator=nl).writerows(rows)
            out = buf.getvalue()
            if not has_trailing and out.endswith(nl):
                out = out[: -len(nl)]
            open(rp, "w", encoding="utf-8", newline="").write(out); n += 1
ENTRY = (
    '            "ARC-PORT-160": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Mjoeyrarhofn (Reydarfjordur, UN/LOCODE ISRFJ) Mjoeyrarbryggja quay face: midpoint of 384 m OSM natural=coastline way/210145938, outer member of OSM relation/2819859 landuse=industrial industrial=port Mjoeyrarhofn, at 65.0273990/-14.1134659; fjardabyggdarhafnir.is official Mjoeyrarbryggja 383 m / 14.2 m and port position 65 01.66N 014 06.80W ~30 m away; OSM seamark harbour node/626578135 ~0.13 km W; soft 65.0284/-14.1121 was ~0.13 km NNE on harbour backland; no Wikidata port item; facility_site single-quay bulk harbour next to Alcoa Fjardaal (planned extension not built)",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-159": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp: continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-160": {' in s:
            print("builder already has entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp); continue
        shutil.copy2(rp, rp + ".bak-" + TAG)
        open(rp, "w", encoding="utf-8").write(s.replace(ANCH, ENTRY + ANCH))
        print("builder patched", rp)
print("csv files patched", n)
