#!/usr/bin/env python3
"""gis-port046-1247: densify ARC-PORT-046 Zhelaniye onto OSM cape node/429774624."""
import glob, os, shutil

OLD_LL = ",Russia,76.9500,68.5500,"
NEW_LL = ",Russia,76.9542826,68.5639747,"
NOTE = (
    "OSM node/429774624 natural=cape Mys Zhelaniya Nominatim 76.9542826/68.5639747 "
    "(extratags wikidata=Q2464613 wikipedia=ru:Mys_Zhelaniya); "
    "WD Q2464613 Cape Zhelaniya P625 76.9546/68.57589 (~0.8 km E); "
    "WD Q86004798 former polar station P625 76.95056/68.54194 (~0.2 km from old soft pin); "
    "UN/LOCODE RUZHE; Rosmorport; Novaya Zemlya N tip; Overpass/Nominatim: no harbour/pier/quay mapped - facility_site; "
    "GIS quality densify 2026-10-13 ~12:47 MSK gis-port046-1247 (off soft 76.9500/68.5500, ~0.59 km)"
)
OLD_TAIL = "Rosmorport,State,,,"
NEW_TAIL = "Rosmorport,State,\"" + NOTE + "\",88,2026-10-13"

roots = ["."]
import sys
if len(sys.argv) > 1:
    roots = sys.argv[1:]
seen = set(); n = 0
for r in roots:
    for p in glob.glob(r + "/**/ports.csv", recursive=True):
        rp = os.path.realpath(p)
        if rp in seen or "node_modules" in rp or "_bak" in rp:
            continue
        seen.add(rp)
        lines = open(rp, encoding="utf-8").read().split("\n")
        hit = False
        for i, l in enumerate(lines):
            if l.startswith("ARC-PORT-046,") and OLD_LL in l and l.endswith(OLD_TAIL):
                lines[i] = l.replace(OLD_LL, NEW_LL).removesuffix(OLD_TAIL) + NEW_TAIL
                hit = True
        if hit:
            shutil.copy2(rp, rp + ".bak-gis-port046-1247")
            open(rp, "w", encoding="utf-8").write("\n".join(lines))
            n += 1; print("patched", rp)
        elif any(l.startswith("ARC-PORT-046,") for l in lines):
            row = next(l for l in lines if l.startswith("ARC-PORT-046,"))
            print("SKIP (row differs)", rp, repr(row[-120:]))

ENTRY = (
    '            "ARC-PORT-046": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Cape Zhelaniya (Mys Zhelaniya) / Rosmorport RUZHE area: OSM node/429774624 Nominatim 76.9542826/68.5639747 (WD Q2464613 cape; WD Q86004798 former polar station nearby); was soft 76.9500/68.5500 (~0.59 km); no OSM harbour/pier mapped - facility_site not a surveyed berth",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-045": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True):
        rp = os.path.realpath(path)
        if rp in seen: continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-046": {' in s:
            print("builder already has entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor count", s.count(ANCH), rp); continue
        shutil.copy2(rp, rp + ".bak-gis-port046-1247")
        open(rp, "w", encoding="utf-8").write(s.replace(ANCH, ENTRY + ANCH))
        print("builder patched", rp)
print("csv files patched", n)
