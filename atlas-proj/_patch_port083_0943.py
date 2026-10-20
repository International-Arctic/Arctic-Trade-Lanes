#!/usr/bin/env python3
"""gis-loop-1020-0943: densify ARC-PORT-083 Lumina White Mountain Mine Port (Qartorqsuaq) off the Qaqortorsuaq
mountain summit onto the mine's mapped quay on Kangerlussuaq Fjord.

Soft pin 66.5369/-52.3091 (4-decimal) == OSM node/12615395211 natural=peak name=Qaqortorsuaq (66.5368517/-52.3091267,
source nunat aqqi) - a summit ~10.9 km WSW of the port, not port infrastructure.
Anchor: OSM way/1362676696 man_made=quay, length-weighted midpoint 66.5576559/-52.0679314 (76 m quay), next to
OSM way/1362676698 industrial=port, way/1362676699 man_made=pier, way/1362676697 building=warehouse and node/12615366365
man_made=mine name='White Mountain / Qaqortorsuaq' operator=Lumina (mapped 2025-02).
Corroboration: DCE/GINR Technical Report 353 (Environmental monitoring at the Qaqortorsuaq anorthosite mine 2024):
mine by Kangerlussuaq Fjord, processing plant close to the coast and the harbour, product shipped out through
Kangerlussuaq Fjord; Hudson Resources White Mountain EIA (2015): project ~66°33'N 52°10'W incl. a port;
lumina.gl: operations ~80 km west of Kangerlussuaq. Confidence left at 85 (single-mapper OSM geometry).
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-083"
TAG = "gis-loop-1020-0943"
NEW_LAT, NEW_LON = "66.5576559", "-52.0679314"
OLD = ("66.5369", "-52.3091")
NOTE = (
    "GIS quality densify 2026-10-20 ~09:43 MSK gis-loop-1020-0943: moved off soft 66.5369/-52.3091 (4-decimal pin equal "
    "to OSM node/12615395211 natural=peak Qaqortorsuaq, a mountain summit ~10.9 km WSW of the port) to the mine quay on "
    "Kangerlussuaq Fjord: length-weighted midpoint of OSM way/1362676696 man_made=quay (76 m) at 66.5576559/-52.0679314, "
    "beside OSM way/1362676698 industrial=port, way/1362676699 pier, way/1362676697 warehouse and node/12615366365 "
    "man_made=mine 'White Mountain / Qaqortorsuaq' operator=Lumina; DCE/GINR Technical Report 353 (dce.au.dk, monitoring "
    "2024): processing plant close to the coast and the harbour, product shipped through Kangerlussuaq Fjord; Hudson "
    "Resources White Mountain EIA 2015 (naalakkersuisut.gl): project ~66°33'N 52°10'W incl. port; facility_site quay point, "
    "not a surveyed berth line; confidence and max_depth left unchanged"
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
    '            "ARC-PORT-083": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Lumina White Mountain (Qaqortorsuaq) anorthosite mine quay on Kangerlussuaq Fjord: length-weighted midpoint of OSM way/1362676696 man_made=quay (76 m) at 66.5576559/-52.0679314, beside OSM way/1362676698 industrial=port, way/1362676699 pier, way/1362676697 warehouse and node/12615366365 man_made=mine operator=Lumina; DCE/GINR TR353: processing plant close to the coast and the harbour, product shipped through Kangerlussuaq Fjord; soft 66.5369/-52.3091 was the Qaqortorsuaq summit (OSM node/12615395211 natural=peak, ~10.9 km WSW); facility_site",\n'
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
        if '"ARC-PORT-083": {' in s:
            print("builder already has entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp); continue
        shutil.copy2(rp, rp + ".bak-" + TAG)
        open(rp, "w", encoding="utf-8").write(s.replace(ANCH, ENTRY + ANCH))
        print("builder patched", rp)
print("csv files patched", n)
