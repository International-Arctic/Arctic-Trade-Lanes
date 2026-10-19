#!/usr/bin/env python3
"""gis-loop-1019-1319: densify ARC-PORT-158 Sortland Havn KF onto Terminalkaia (main quay, Sortlandssundet west side).

Soft pin 68.6964/15.4145 (4-decimal) sat in Sortland town centre on land (Strandgata/Gardsalleen shops), ~0.44 km SSW of the quay.
Anchor: OSM natural=coastline ways 552701435 (v2) + 552701437 (v1) form one straight 434 m quay face at bearing 348.9 deg
(node 5335888572 68.6978898/15.4209075 -> node 5335888593 68.7017107/15.4188371, via Hurtigrute ferry_terminal node/279276240).
sortland-havn.no Terminalkaia: length 438 m, heading 348/168 deg, 10,500 m2 quay area, 10 m (N) to 7.5 m (S) depth.
New pin = geodesic midpoint of that quay face 68.6998001/15.4198705; official Sortland Havn harbour position
UTM33 E517007 N7620922 (= 68.69957/15.41952) lies ~29 m away. position_quality=facility_site.
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-158"
TAG = "gis-loop-1019-1319"
NEW_LAT, NEW_LON = "68.6998001", "15.4198705"
OLD = ("68.6964", "15.4145")
NOTE = (
    "GIS quality densify 2026-10-19 ~13:19 MSK gis-loop-1019-1319: moved off soft 68.6964/15.4145 "
    "(4-decimal pin on land in Sortland town centre, ~0.44 km SSW of the quay) to the midpoint of Terminalkaia, the main quay: "
    "OSM natural=coastline way/552701435 + way/552701437 form one straight 434 m quay face at bearing ~349 deg "
    "(node/5335888572 to node/5335888593, past Hurtigrute ferry_terminal node/279276240), geodesic midpoint 68.6998001/15.4198705 "
    "(~0.44 km NNE, bearing ~30 deg); corroborated by sortland-havn.no Terminalkaia (438 m, heading 348/168 deg, 10,500 m2 quay area, "
    "10 m to 7.5 m depth, ISPS terminal) and the official harbour position UTM33 E517007 N7620922 (68.69957/15.41952, ~29 m away); "
    "no OSM harbour/quay polygon and no Wikidata port item; OSM ferry node carries ref:LOCODE NOSLX vs row NOSLD (left unchanged, flagged for review); "
    "facility_site main quay, not a single berth"
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
            if (old_lat, old_lon) != OLD:
                print("SKIP unexpected old coords", old_lat, old_lon, rp)
                continue
            row[4], row[5] = NEW_LAT, NEW_LON
            src = row[17] or ""
            if TAG not in src:
                row[17] = (src + " + " + NOTE) if src else NOTE
            row[18] = "88"
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
    '            "ARC-PORT-158": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Sortland Havn KF Terminalkaia (main quay, west side of Sortlandssundet, Vesteralen; row UN/LOCODE NOSLD, OSM ferry node ref:LOCODE NOSLX): OSM natural=coastline way/552701435 + way/552701437 form one straight 434 m quay face at bearing ~349 deg (node/5335888572 to node/5335888593, past Hurtigrute ferry_terminal node/279276240); pin = geodesic midpoint 68.6998001/15.4198705; sortland-havn.no Terminalkaia 438 m, heading 348/168 deg, 10,500 m2 quay area corroborates; official harbour position UTM33 E517007 N7620922 (68.69957/15.41952) ~29 m away; soft 68.6964/15.4145 was on land in the town centre ~0.44 km SSW; no OSM harbour polygon, no Wikidata item; facility_site main quay, not a single berth",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-140": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True) + glob.glob(r + "/build_atlas.py"):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-158": {' in s:
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
