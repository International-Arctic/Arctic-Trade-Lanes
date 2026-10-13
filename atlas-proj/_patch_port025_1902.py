#!/usr/bin/env python3
"""gis-port025-1902: densify ARC-PORT-025 Port of Anchorage (Port of Alaska, USANC) onto the main cargo dock pier.

Soft pin 61.2387/-149.9076 (4-decimal, empty sources) sat on the Ship Creek / downtown edge, not on the dock.
Anchor = OSM way/28577877 man_made=pier area=yes centroid 61.2408396/-149.8872591 inside the Port of Alaska
OSM relation/10511522 (landuse=industrial, operator Municipality of Anchorage, wikidata Q3398440), ~1.11 km ENE
of soft. Corroboration: Wikidata Q3398440 Port of Alaska P625 61.2403/-149.886 (~0.09 km), P1937 UN/LOCODE USANC;
OSM Terminal Road way/28577529 and Alaska Railroad City Dock Track spurs way/319205158 / way/1157471331 behind the dock.
Relation centroid 61.2446867/-149.8816953 is already used by ARC-PORT-113 (Terminal 1 replacement) so the parent is
kept on the existing cargo pier instead (~0.52 km SW of PORT-113, no stacking). position_quality=facility_site.
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-025"
NEW_LAT, NEW_LON = "61.2408396", "-149.8872591"
NOTE = (
    "GIS quality densify 2026-10-13 ~19:02 MSK gis-port025-1902: moved off soft 61.2387/-149.9076 "
    "(4-decimal, no sources; Ship Creek / downtown edge) to OSM way/28577877 man_made=pier centroid "
    "61.2408396/-149.8872591 (main cargo dock, ~1.11 km ENE) inside Port of Alaska OSM relation/10511522 "
    "(landuse=industrial, operator Municipality of Anchorage); Wikidata Q3398440 Port of Alaska P625 "
    "61.2403/-149.886 (~0.09 km) P1937 USANC; OSM Terminal Road way/28577529; Alaska Railroad City Dock Track "
    "way/319205158; portofalaska.com; facility_site (cargo pier, not a surveyed berth)"
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
            if old_lat == NEW_LAT and old_lon == NEW_LON and "gis-port025-1902" in (row[17] or ""):
                print("already", rp)
                continue
            row[4] = NEW_LAT
            row[5] = NEW_LON
            src = row[17] or ""
            if "gis-port025-1902" not in src:
                row[17] = (src + " + " + NOTE) if src else NOTE
            row[18] = "92"
            row[19] = "2026-10-13"
            rows[i] = row
            hit = True
            print(f"row {old_lat}/{old_lon} -> {NEW_LAT}/{NEW_LON}", rp)
        if hit:
            shutil.copy2(rp, rp + ".bak-gis-port025-1902")
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
    '            "ARC-PORT-025": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Port of Anchorage / Port of Alaska (Knik Arm, Cook Inlet; UN/LOCODE USANC): OSM way/28577877 man_made=pier area=yes centroid 61.2408396/-149.8872591 = main cargo dock inside Port of Alaska OSM relation/10511522 (landuse=industrial, operator Municipality of Anchorage, wikidata Q3398440); Wikidata Q3398440 P625 61.2403/-149.886 ~0.09 km; Terminal Road way/28577529 and Alaska Railroad City Dock Track way/319205158 behind the dock; relation centroid 61.2446867/-149.8816953 kept for ARC-PORT-113 Terminal 1 replacement (~0.52 km NE); was soft 61.2387/-149.9076 (~1.11 km); facility_site cargo pier, not a surveyed berth",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-150": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True) + glob.glob(
        r + "/build_atlas.py"
    ):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-025": {' in s:
            print("builder already has entry", rp)
            continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp)
            continue
        shutil.copy2(rp, rp + ".bak-gis-port025-1902")
        s = s.replace(ANCH, ENTRY + ANCH)
        open(rp, "w", encoding="utf-8").write(s)
        print("builder patched", rp)
print("csv files patched", n)
