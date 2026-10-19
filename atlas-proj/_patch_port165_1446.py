#!/usr/bin/env python3
"""gis-loop-1019-1446: densify ARC-PORT-165 Vardo fiskerihavn (Vardoya, UN/LOCODE NOVAO) onto the inner-harbour fishing pier.

Soft pin 70.3740/31.1019 (4-decimal) sat on the OSM 'Vardo havn' name node (node/6372262628) on Kaigata street onshore.
Anchor: shoelace centroid of OSM man_made=pier area=yes ref:LOCODE=NOVAO way/987326753 (~1260 m2 concrete fishing pier,
inner harbour inside indre molo) at 70.3760571/31.1021737 (~0.23 km N).
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-165"
TAG = "gis-loop-1019-1446"
NEW_LAT, NEW_LON = "70.3760571", "31.1021737"
OLD = ("70.3740", "31.1019")
CONF = "94"
NOTE = 'GIS quality densify 2026-10-19 ~14:46 MSK gis-loop-1019-1446: moved off soft 70.3740/31.1019 (4-decimal pin on the OSM Vardo havn name node/6372262628 on Kaigata street onshore) to the inner fishing harbour: shoelace centroid of OSM man_made=pier area=yes floating=no ref:LOCODE=NOVAO way/987326753 (~1260 m2 fishing pier inside indre molo) at 70.3760571/31.1021737 (~0.23 km N); twin NOVAO pier way/987326754 ~45 m NW; Vestre molo flytebrygge way/1526392564 ~0.10 km N; OSM seamark harbour node/5355495287 category=fishing Vardo ~0.19 km E; distinct from parent ARC-PORT-032 Hurtigruten terminal node/269242524 (~0.18 km SSE); kystverket.no Vardo fiskerihavn project page (planned 595 m outer molo 300 m north of existing molo, Hasselneset dredging; not yet built) + Menon/Kystverket samfunnsokonomisk analyse (indre havn liggeplasser); vardohavn.no port position 70 22N 031 06E (coarse); no Wikidata port item; facility_site existing fishing harbour pier, project works offshore not yet built'
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
ENTRY = '            "ARC-PORT-165": {\n                "position_quality": "facility_site",\n                "position_note": "Vardo fiskerihavn (Vardoya, UN/LOCODE NOVAO) inner fishing harbour: shoelace centroid of OSM man_made=pier area=yes ref:LOCODE=NOVAO way/987326753 (~1260 m2) at 70.3760571/31.1021737; twin NOVAO pier way/987326754 ~45 m NW; OSM seamark harbour node/5355495287 category=fishing ~0.19 km E; parent ARC-PORT-032 Hurtigruten terminal node/269242524 ~0.18 km SSE kept separate; kystverket.no project: planned 595 m outer molo 300 m N of existing molo + Hasselneset dredging (not yet built); soft 70.3740/31.1019 was ~0.23 km S on the onshore Vardo havn name node; no Wikidata port item; facility_site existing harbour pier, not the future molo",\n            },\n'
ANCH = '            "ARC-PORT-160": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp: continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-165": {' in s:
            print("builder already has entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp); continue
        shutil.copy2(rp, rp + ".bak-" + TAG)
        open(rp, "w", encoding="utf-8").write(s.replace(ANCH, ENTRY + ANCH))
        print("builder patched", rp)
print("csv files patched", n)
