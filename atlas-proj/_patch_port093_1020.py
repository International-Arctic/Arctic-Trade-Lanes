#!/usr/bin/env python3
"""gis-port093-1020: densify ARC-PORT-093 Alta Urnesbukta Floating Quay onto the Molokaia floating quay.

Soft pin 69.9686/23.2717 (4-decimal) sat ~2.3 km SW of Urnesbukta, inland in Alta (Bossekop side).
Anchor = OSM way/795270408 man_made=pier floating=yes area=yes (outer floating breakwater-quay of
Urnesbukta marina og fiskerihavn, Amtmannsnes; ~142 m x ~4 m outline mapped 2020) shoelace centroid
69.9859524/23.3061572 (~2.33 km NE, bearing ~34 deg). Alta Havn KF official quay list (altahavn.no/kaier)
gives Kai 7 Molokaia (public fishery quay, 100 m x 6 m, 5-15 m depth, 29 sheds) at 69.985979/23.306159,
~3 m from the OSM centroid. Marina Solutions reference (April 2026): new 100 m two-unit flytemolo in
Urnesbukta for Alta Havn KF. Corroboration: OSM node/1345229303 Urnesbukta Marina (~0.13 km W),
node/1376347030 natural=bay Urnesbukta (~0.39 km W), Fiskerihavna road way/123402386, Kystverket pile
Innerberget ref 929503 (node/10813971232). No Wikidata harbour item (Alta municipality Q6535 not reused).
UN/LOCODE corrected NOALT (not in UN/LOCODE) -> NOALF (Alta, function 1-34; Alta Havn ISPS codes NOALF-00xx).
Distinct from Alta Havn Bukta main port (Bukta flytekai 69.978171/23.330122, ~1.25 km SE; no ATL port
record there). position_quality=facility_site (floating quay outline; OSM outline predates 2026 molo).
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-093"
TAG = "gis-port093-1020"
NEW_LAT, NEW_LON = "69.9859524", "23.3061572"
OLD_LOCODE, NEW_LOCODE = "NOALT", "NOALF"
NOTE = (
    "GIS quality densify 2026-10-14 ~10:20 MSK gis-port093-1020: moved off soft 69.9686/23.2717 "
    "(4-decimal; ~2.3 km SW of Urnesbukta, inland) to OSM way/795270408 man_made=pier floating=yes "
    "outer floating quay of Urnesbukta marina og fiskerihavn (Amtmannsnes) shoelace centroid "
    "69.9859524/23.3061572 (~2.33 km NE, bearing ~34 deg); Alta Havn KF altahavn.no/kaier Kai 7 "
    "Molokaia (public fishery quay 100 m x 6 m, depth 5-15 m, 29 sheds) 69.985979/23.306159 ~3 m from "
    "OSM centroid; marinasolutions.no April 2026 new 100 m flytemolo Urnesbukta; OSM node/1345229303 "
    "Urnesbukta Marina ~0.13 km W, node/1376347030 bay Urnesbukta; Kystverket pile Innerberget ref "
    "929503 (node/10813971232); no Wikidata harbour item (Alta municipality Q6535 not reused); "
    "UN/LOCODE corrected NOALT (not listed) -> NOALF (Alta, Alta Havn ISPS NOALF-00xx); distinct from "
    "Alta Havn Bukta main port (~1.25 km SE, no ATL port record); facility_site (floating quay outline "
    "mapped 2020, not a surveyed berth)"
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
            row[4], row[5] = NEW_LAT, NEW_LON
            if row[6] == OLD_LOCODE:
                row[6] = NEW_LOCODE
            src = row[17] or ""
            if TAG not in src:
                row[17] = (src + " + " + NOTE) if src else NOTE
            row[18] = "90"
            row[19] = "2026-10-14"
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
    '            "ARC-PORT-093": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Alta Urnesbukta Floating Quay / Molokaia (Alta Havn KF, Amtmannsnes, Altafjorden; UN/LOCODE NOALF): OSM way/795270408 man_made=pier floating=yes area=yes outer floating quay of Urnesbukta marina og fiskerihavn, shoelace centroid 69.9859524/23.3061572 (~142 m x 4 m outline mapped 2020); Alta Havn KF altahavn.no/kaier Kai 7 Molokaia 100 m x 6 m depth 5-15 m at 69.985979/23.306159 (~3 m); marinasolutions.no April 2026 new 100 m flytemolo; OSM node/1345229303 Urnesbukta Marina ~0.13 km W; Kystverket pile Innerberget ref 929503; no Wikidata harbour item (Alta municipality Q6535 not reused); soft 69.9686/23.2717 was ~2.33 km SW inland; distinct from Alta Havn Bukta main port (~1.25 km SE, no ATL port record); facility_site floating quay outline, not a surveyed berth",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-053": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True) + glob.glob(r + "/build_atlas.py"):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-093": {' in s:
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
