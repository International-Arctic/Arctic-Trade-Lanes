#!/usr/bin/env python3
"""gis-port171-1805: densify ARC-PORT-171 Port Elga — Manorsky Cape onto OSM way/1316635669.

Soft pin 55.1167/135.7000 is Wikipedia-class (~55°07′N 135°42′E) matching Wikidata
Q115763861 Эльга (морской порт) P625 55.11667/135.7 (imported from ruwiki). No OSM
pier/quay mapped yet. Anchor = OSM way/1316635669 landuse=construction
construction=industrial name=Порт Эльга (wikipedia=ru:Эльга (порт)); shoelace
centroid 55.1173682/135.6970483 (~0.20 km WNW of soft). Corroboration: мыс Манорский
OSM node/2643962546 55.1142092/135.6950826 (~0.37 km SW); Cape Manorsky WD Q37884830
P625 55.117222/135.6925 (~0.29 km W); UN/LOCODE RUVNN (within Vanino seaport
boundaries). Distinct from Elga mine near Neryungri and Vanino town berths.
position_quality=facility_site (mapped terminal construction area, not a surveyed berth).
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-171"
NEW_LAT, NEW_LON = "55.1173682", "135.6970483"
NOTE = (
    "GIS quality densify 2026-10-13 ~18:05 MSK gis-port171-1805: moved off soft 55.1167/135.7000 "
    "(Wikipedia-class ~55deg07N 135deg42E = WD Q115763861 Elga port P625 55.11667/135.7) to OSM "
    "way/1316635669 landuse=construction construction=industrial name=Port Elga / Порт Эльга "
    "(wikipedia=ru:Эльга (порт)) shoelace centroid 55.1173682/135.6970483 (~0.20 km WNW); "
    "мыс Манорский OSM node/2643962546 55.1142092/135.6950826 (~0.37 km SW); Cape Manorsky "
    "WD Q37884830 P625 55.117222/135.6925 (~0.29 km W); UN/LOCODE RUVNN (Vanino seaport "
    "boundaries); facility_site (construction area, not a surveyed berth)"
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
        # Detect newline style
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
            if old_lat == NEW_LAT and old_lon == NEW_LON and "gis-port171-1805" in (row[17] or ""):
                print("already", rp)
                continue
            row[4] = NEW_LAT
            row[5] = NEW_LON
            src = row[17] or ""
            if "gis-port171-1805" not in src:
                row[17] = (src + " + " + NOTE) if src else NOTE
            row[18] = "92"
            row[19] = "2026-10-13"
            rows[i] = row
            hit = True
            print(f"row {old_lat}/{old_lon} -> {NEW_LAT}/{NEW_LON}", rp)
        if hit:
            shutil.copy2(rp, rp + ".bak-gis-port171-1805")
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
    '            "ARC-PORT-171": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Port Elga — Manorsky Cape Coal Marine Terminal (Sea of Okhotsk / Uda Bay, within Vanino seaport RUVNN): OSM way/1316635669 landuse=construction construction=industrial name=Порт Эльга (wikipedia=ru:Эльга (порт)) shoelace centroid 55.1173682/135.6970483; мыс Манорский OSM node/2643962546 55.1142092/135.6950826 ~0.37 km SW; Cape Manorsky WD Q37884830 P625 55.117222/135.6925 ~0.29 km W; WD Q115763861 Elga port soft P625 55.11667/135.7; was soft 55.1167/135.7000 (~0.20 km); facility_site construction area, not a surveyed berth",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-047": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True) + glob.glob(
        r + "/build_atlas.py"
    ):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-171": {' in s:
            print("builder already has entry", rp)
            continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp)
            continue
        shutil.copy2(rp, rp + ".bak-gis-port171-1805")
        s = s.replace(ANCH, ENTRY + ANCH)
        open(rp, "w", encoding="utf-8").write(s)
        print("builder patched", rp)
print("csv files patched", n)
