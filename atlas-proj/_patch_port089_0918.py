#!/usr/bin/env python3
"""gis-port089-0918: densify ARC-PORT-089 Grundarfjarðarhöfn onto Norðurgarður main pier.

Soft pin 64.9183/-23.2503 matches grundport.is harbour position (64°55'6\"N 23°15'1\"W)
but is the harbour reference, not the pier face. Anchor = OSM way/51858019 man_made=pier
area=yes shoelace centroid 64.9231680/-23.2469906 (~0.56 km NNE) — longest pier polygon
in the basin (maxspan ~319 m; official Norðurgarður main pier 365 m / width 40 m).
Secondary pier way/51858020 (~0.92 km N) left unused. Town WD Q27014314 P625 is settlement,
not reused. UN/LOCODE ISGRU. position_quality=facility_site.
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-089"
NEW_LAT, NEW_LON = "64.9231680", "-23.2469906"
NOTE = (
    "GIS quality densify 2026-10-14 ~09:18 MSK gis-port089-0918: moved off soft 64.9183/-23.2503 (4-decim"
    "al; matches grundport.is harbour position 64d55m6s N 23d15m1s W but not pier face) to OSM way/518580"
    "19 man_made=pier area=yes centroid 64.9231680/-23.2469906 (Nordurgardur main pier, maxspan ~319 m; o"
    "fficial pier 365 m / 40 m wide, Berth 1+2; ~0.56 km NNE); secondary pier way/51858020 ~0.92 km N unu"
    "sed; industrial hinterland way/203802229; town WD Q27014314 P625 64.92427/-23.26313 settlement only;"
    " UN/LOCODE ISGRU; grundport.is; facility_site (pier polygon, not a surveyed berth)"
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
        reader = csv.reader(io.StringIO(raw))
        rows = list(reader)
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
            if old_lat == NEW_LAT and old_lon == NEW_LON and "gis-port089-0918" in (row[17] or ""):
                print("already", rp)
                continue
            row[4] = NEW_LAT
            row[5] = NEW_LON
            src = row[17] or ""
            if "gis-port089-0918" not in src:
                row[17] = (src + " + " + NOTE) if src else NOTE
            row[18] = "92"
            row[19] = "2026-10-14"
            rows[i] = row
            hit = True
            print(f"row {old_lat}/{old_lon} -> {NEW_LAT}/{NEW_LON}", rp)
        if hit:
            shutil.copy2(rp, rp + ".bak-gis-port089-0918")
            buf = io.StringIO()
            writer = csv.writer(buf, lineterminator=nl)
            writer.writerows(rows)
            out = buf.getvalue()
            if not has_trailing and out.endswith(nl):
                out = out[: -len(nl)]
            open(rp, "w", encoding="utf-8", newline="").write(out)
            n += 1
            print("patched", rp)

ENTRY = (
    '            "ARC-PORT-089": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Grundarfjarðarhöfn / Grundarfjörður Harbour (Snæfellsnes, Iceland; UN/LOCODE ISGRU): OSM way/51858019 man_made=pier area=yes shoelace centroid 64.9231680/-23.2469906 = Norðurgarður main pier (maxspan ~319 m; grundport.is pier 365 m / 40 m, Berth 1 135 m @ 9.5 m + Berth 2 220 m); secondary pier way/51858020 ~0.92 km N unused; industrial hinterland way/203802229; town WD Q27014314 P625 64.92427/-23.26313 settlement only (~0.78 km WNW); soft 64.9183/-23.2503 matched harbour position DMS (~0.56 km); facility_site pier polygon, not a surveyed berth",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-025": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True) + glob.glob(
        r + "/build_atlas.py"
    ):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-089": {' in s:
            print("builder already has entry", rp)
            continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp)
            continue
        shutil.copy2(rp, rp + ".bak-gis-port089-0918")
        s = s.replace(ANCH, ENTRY + ANCH)
        open(rp, "w", encoding="utf-8").write(s)
        print("builder patched", rp)
print("csv files patched", n)
