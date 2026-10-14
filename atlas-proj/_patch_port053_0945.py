#!/usr/bin/env python3
"""gis-port053-0945: densify ARC-PORT-053 Qaqortoq Port onto the Royal Arctic Line harbour yard.

Soft pin 60.7288/-46.0278 sat ~1.3 km NNE of the harbour, inland in the upper town.
Anchor = OSM way/511853551 landuse=industrial harbourfront port yard (11.4k m2, on coastline
way/1476531377, shares nodes with piers way/598638435 + way/598638436 and the Arctic Umiaq Line
ferry route way/512918611) shoelace centroid 60.7178523/-46.0365644 (~1.31 km SSW, bearing ~201 deg).
OSM building way/351129063 'Royal Arctic Line' (building=industrial, Torvevej B-163) lies inside the
yard (~33 m). Konge Bro pier way/378873667 + ferry_terminal node/3822342850 ~0.10 km E.
Town WD Q221203 P625 60.7167/-46.0333 (settlement precision 1') not reused. UN/LOCODE GLJJU.
DISTINCT from ARC-PORT-091 dual-use expansion (60.7225/-46.0335, ~0.54 km N, untouched) and
ARC-PORT-127 Nuupiluk (~11.2 km WNW). position_quality=facility_site.
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-053"
NEW_LAT, NEW_LON = "60.7178523", "-46.0365644"
NOTE = 'GIS quality densify 2026-10-14 ~09:45 MSK gis-port053-0945: moved off soft 60.7288/-46.0278 (4-decimal; ~1.3 km NNE of harbour in upper town) to OSM way/511853551 landuse=industrial harbourfront port yard centroid 60.7178523/-46.0365644 (~1.31 km SSW, bearing ~201 deg; 11.4k m2 on coastline way/1476531377; shares nodes with piers way/598638435 + way/598638436 and Arctic Umiaq Line ferry route way/512918611); OSM building way/351129063 Royal Arctic Line (Torvevej B-163) inside yard ~33 m; Konge Bro pier way/378873667 + ferry_terminal node/3822342850 ~0.10 km E; town WD Q221203 P625 60.7167/-46.0333 settlement only; UN/LOCODE GLJJU; DISTINCT from ARC-PORT-091 dual-use (~0.54 km N, untouched) and ARC-PORT-127 Nuupiluk (~11.2 km WNW); facility_site (port yard polygon, not a surveyed berth)'
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
            if old_lat == NEW_LAT and old_lon == NEW_LON and "gis-port053-0945" in (row[17] or ""):
                print("already", rp)
                continue
            row[4] = NEW_LAT
            row[5] = NEW_LON
            src = row[17] or ""
            if "gis-port053-0945" not in src:
                row[17] = (src + " + " + NOTE) if src else NOTE
            row[18] = "90"
            row[19] = "2026-10-14"
            rows[i] = row
            hit = True
            print(f"row {old_lat}/{old_lon} -> {NEW_LAT}/{NEW_LON}", rp)
        if hit:
            shutil.copy2(rp, rp + ".bak-gis-port053-0945")
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
    '            "ARC-PORT-053": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Qaqortoq Port (Royal Arctic Line; South Greenland; UN/LOCODE GLJJU): OSM way/511853551 landuse=industrial harbourfront port yard shoelace centroid 60.7178523/-46.0365644 (11.4k m2 on coastline way/1476531377; shares nodes with piers way/598638435 + way/598638436 and Arctic Umiaq Line ferry route way/512918611); OSM building way/351129063 Royal Arctic Line (Torvevej B-163) inside yard ~33 m; Konge Bro pier way/378873667 + ferry_terminal node/3822342850 ~0.10 km E; town WD Q221203 P625 60.7167/-46.0333 settlement only; soft 60.7288/-46.0278 was ~1.31 km NNE in upper town; DISTINCT from ARC-PORT-091 dual-use expansion (60.7225/-46.0335, ~0.54 km N, untouched) and ARC-PORT-127 Nuupiluk (~11.2 km WNW); facility_site port yard polygon, not a surveyed berth",\n'
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
        if '"ARC-PORT-053": {' in s:
            print("builder already has entry", rp)
            continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp)
            continue
        shutil.copy2(rp, rp + ".bak-gis-port053-0945")
        s = s.replace(ANCH, ENTRY + ANCH)
        open(rp, "w", encoding="utf-8").write(s)
        print("builder patched", rp)
print("csv files patched", n)
