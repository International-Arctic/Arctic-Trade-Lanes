#!/usr/bin/env python3
"""gis-loop-1019-1521: densify ARC-PORT-104 Narvik Port Dock 5 New Shiploader (LKAB, UN/LOCODE NONVK) onto the quay 5 shiploader.

Soft pin 68.4205/17.4332 (4-decimal) sat onshore in the Narvik residential area (~0.4 km from ARC-PORT-136 Kleiva terminal),
~2.1 km ESE of the LKAB ore harbour. Anchor: shoelace centroid of OSM man_made=crane building=yes name=Malmuskippingsanlegg
way/104708054 (ship loader on LKAB quay 5 pier way/1113478606) at 68.4300757/17.3881101 (~2.13 km WNW).
Quay 7 loader (OSM crane way/1113478612 on pier way/1113478609, 68.4304/17.3999) is the 2016 redundant loader, ~0.48 km E.
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-104"
TAG = "gis-loop-1019-1521"
NEW_LAT, NEW_LON = "68.4300757", "17.3881101"
OLD = ("68.4205", "17.4332")
CONF = "96"
NOTE = 'GIS quality densify 2026-10-19 ~15:21 MSK gis-loop-1019-1521: moved off soft 68.4205/17.4332 (4-decimal pin onshore in Narvik town ~0.4 km from ARC-PORT-136 Kleiva, not on the LKAB ore harbour) to the LKAB quay 5 ship loader: shoelace centroid of OSM man_made=crane building=yes name=Malmuskippingsanlegg way/104708054 (~1500 m2 loader footprint on LKAB quay 5 pier way/1113478606, western tip of the LKAB ore harbour) at 68.4300757/17.3881101 (~2.13 km WNW); quay 7 redundant loader (2016) = OSM crane way/1113478612 on pier way/1113478609 ~0.48 km E (matches public LKAB Kai 7 place 68.430417/17.400040 within ~7 m), so the western loader is quay 5 by elimination; LKAB news 2022-11-02 + 2025-09-24 + press 2025-11-27 (new U5 loader assembled on the renovated slewing base at quay 5, replacing 1977 U5; inaugurated 27 Nov 2025); Sarens 2026-01-15 install note; DigitaltMuseum/Museum Nord photos kai 5 + kai 7; parent ARC-PORT-019 Narvik Port (68.4294644/17.4239955) ~1.47 km E kept separate; no Wikidata item for the loader; facility_site'
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
ENTRY = '            "ARC-PORT-104": {\n                "position_quality": "facility_site",\n                "position_note": "LKAB Narvik quay 5 ship loader (UN/LOCODE NONVK): shoelace centroid of OSM man_made=crane name=Malmuskippingsanlegg way/104708054 (~1500 m2, on quay 5 pier way/1113478606) at 68.4300757/17.3881101; quay 7 redundant 2016 loader OSM crane way/1113478612 on pier way/1113478609 ~0.48 km E (public LKAB Kai 7 place 68.430417/17.400040 ~7 m) so the western loader is quay 5; LKAB 2022-11-02/2025-09-24/2025-11-27: new U5 loader mounted on the renovated slewing base at quay 5, inaugurated 27 Nov 2025; parent ARC-PORT-019 Narvik Port ~1.47 km E kept separate; soft 68.4205/17.4332 was ~2.13 km ESE onshore in town; facility_site",\n            },\n'
ANCH = '            "ARC-PORT-165": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp: continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-104": {' in s:
            print("builder already has entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp); continue
        shutil.copy2(rp, rp + ".bak-" + TAG)
        open(rp, "w", encoding="utf-8").write(s.replace(ANCH, ENTRY + ANCH))
        print("builder patched", rp)
print("csv files patched", n)
