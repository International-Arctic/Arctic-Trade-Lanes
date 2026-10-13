#!/usr/bin/env python3
"""gis-port041-1216: densify ARC-PORT-041 Mys Shmidta onto OSM settlement way/93613726."""
import glob, os, shutil

OLD_LL = ",Russia,68.8700,-179.4000,"
NEW_LL = ",Russia,68.8928813,-179.4130958,"
NOTE = (
    "OSM way/93613726 place=hamlet Mys Shmidta (official_status urban-type settlement) Nominatim centroid 68.8928813/-179.4130958 "
    "(extratags wikidata=Q1020259 wikipedia=ru:Mys_Shmidta_(posyolok) population=140 as of 2018-01-01); "
    "WD Q1020259 P625 68.91056/-179.45889 (~2.7 km NW, toward Cape Schmidt WD Q2603783 68.92056/-179.45333); "
    "old soft pin sat on a tertiary road (OSM way/93603325) S of the settlement near the airport; "
    "Chukchi Sea coast settlement/port, no OSM harbour/pier mapped - settlement_site; "
    "GIS quality densify 2026-10-13 ~12:16 MSK gis-port041-1216 (off soft 68.8700/-179.4000, ~2.6 km)"
)
OLD_TAIL = "Chukotka Mining,Private,,,"
NEW_TAIL = "Chukotka Mining,Private,\"" + NOTE + "\",88,2026-10-13"

roots = ["/home/workspace/ArcticTradeLanes-Dataset", "/home/workspace/ArcticTradeLanes.com"]
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
            if l.startswith("ARC-PORT-041,") and OLD_LL in l and l.endswith(OLD_TAIL):
                lines[i] = l.replace(OLD_LL, NEW_LL).removesuffix(OLD_TAIL) + NEW_TAIL
                hit = True
        if hit:
            shutil.copy2(rp, rp + ".bak-gis-port041-1216")
            open(rp, "w", encoding="utf-8").write("\n".join(lines))
            n += 1; print("patched", rp)
        elif any(l.startswith("ARC-PORT-041,") for l in lines):
            row = next(l for l in lines if l.startswith("ARC-PORT-041,"))
            print("SKIP (row differs)", rp, repr(row[-80:]))

ENTRY = (
    '            "ARC-PORT-041": {\n'
    '                "position_quality": "settlement_site",\n'
    '                "position_note": "Mys Shmidta urban-type settlement / Chukchi Sea coast port: OSM way/93613726 Nominatim 68.8928813/-179.4130958 (WD Q1020259); was soft 68.8700/-179.4000 on a road near the airport (~2.6 km); no OSM harbour/pier mapped - settlement_site not a surveyed berth",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-048": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True):
        rp = os.path.realpath(path)
        if rp in seen: continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-041": {' in s:
            print("builder already has entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor count", s.count(ANCH), rp); continue
        shutil.copy2(rp, rp + ".bak-gis-port041-1216")
        open(rp, "w", encoding="utf-8").write(s.replace(ANCH, ENTRY + ANCH))
        print("builder patched", rp)
print("csv files patched", n)
