#!/usr/bin/env python3
"""gis-loop-1019-1048: densify ARC-PORT-109 Port of Reykjanes Keflavik Harbour onto OSM Keflavikurhofn port area.

Soft pin 63.9988/-22.5550 (4-decimal) sat on residential Solvallagata, Keflavik town (Nominatim reverse
way/496329734), ~0.52 km W of the harbour. The harbour is mapped as OSM relation/19845360
landuse=industrial industrial=port name=Keflavikurhofn (outer ways 1451071759 + 1451071766, ~1.39 ha),
shoelace centroid 63.9983860/-22.5443131. Njardvikurhofn relation/19845279 (~1.6 km SSE) and
ARC-PORT-111 Helguvik (~2.5 km N) are distinct. No Wikidata item for Keflavikurhofn found.
UN/LOCODE ISKEF unchanged. position_quality=facility_site (port-area polygon, not a surveyed berth).
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-109"
TAG = "gis-loop-1019-1048"
NEW_LAT, NEW_LON = "63.9983860", "-22.5443131"
NOTE = (
    "GIS quality densify 2026-10-19 ~10:48 MSK gis-loop-1019-1048: moved off soft 63.9988/-22.5550 "
    "(4-decimal; on residential Solvallagata in Keflavik town, not on the harbour) to OSM "
    "relation/19845360 landuse=industrial industrial=port name=Keflavikurhofn (outer ways 1451071759 + "
    "1451071766, ~1.39 ha) shoelace centroid 63.9983860/-22.5443131 (~0.52 km E, bearing ~95 deg); "
    "Njardvikurhofn relation/19845279 ~1.6 km SSE and ARC-PORT-111 Helguvik ~2.5 km N distinct; "
    "no Wikidata item found; UN/LOCODE ISKEF unchanged; facility_site port-area polygon, not a surveyed berth"
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
        rows = list(csv.reader(io.StringIO(raw)))
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
            if old_lat == NEW_LAT and old_lon == NEW_LON and TAG in (row[17] or ""):
                print("already", rp)
                continue
            if (old_lat, old_lon) not in (("63.9988", "-22.5550"), ("63.9988", "-22.555")):
                print("SKIP unexpected old coords", old_lat, old_lon, rp)
                continue
            row[4], row[5] = NEW_LAT, NEW_LON
            src = row[17] or ""
            if TAG not in src:
                row[17] = (src + " + " + NOTE) if src else NOTE
            row[18] = "95"
            row[19] = "2026-10-19"
            rows[i] = row
            hit = True
            print(f"row {old_lat}/{old_lon} -> {NEW_LAT}/{NEW_LON} locode {row[6]}", rp)
        if hit:
            shutil.copy2(rp, rp + ".bak-" + TAG)
            buf = io.StringIO()
            csv.writer(buf, lineterminator=nl).writerows(rows)
            out = buf.getvalue()
            if not has_trailing and out.endswith(nl):
                out = out[: -len(nl)]
            open(rp, "w", encoding="utf-8", newline="").write(out)
            n += 1
            print("patched", rp)

ENTRY = (
    '            "ARC-PORT-109": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Port of Reykjanes / Keflavik Harbour (Keflavíkurhöfn, Reykjanesbær; UN/LOCODE ISKEF): OSM relation/19845360 landuse=industrial industrial=port name=Keflavíkurhöfn (outer ways 1451071759 + 1451071766, ~1.39 ha), shoelace centroid 63.9983860/-22.5443131; Reykjaneshöfn municipal port; Njarðvíkurhöfn relation/19845279 ~1.6 km SSE and ARC-PORT-111 Helguvík ~2.5 km N distinct; no Wikidata harbour item found; soft 63.9988/-22.5550 was ~0.52 km W on residential Sólvallagata; facility_site port-area polygon, not a surveyed berth",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-066": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True) + glob.glob(r + "/build_atlas.py"):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-109": {' in s:
            print("builder already has entry", rp)
            continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp)
            continue
        shutil.copy2(rp, rp + ".bak-" + TAG)
        s = s.replace(ANCH, ENTRY + ANCH)
        open(rp, "w", encoding="utf-8").write(s)
        print("builder patched", rp)
print("csv files patched", n)
