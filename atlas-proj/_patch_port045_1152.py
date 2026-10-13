#!/usr/bin/env python3
"""gis-port045-1152: densify ARC-PORT-045 Ambarchik onto OSM hamlet way/655223046."""
import glob, os, shutil

OLD_LL = ",Russia,69.6500,162.3500,"
NEW_LL = ",Russia,69.6252019,162.3024493,"
NOTE = (
    "OSM way/655223046 place=hamlet Ambarchik Nominatim centroid 69.6252019/162.3024493 "
    "(extratags wikidata=Q2629730 wikipedia=ru:Ambarchik_(selo) population=4 as of 2010-10-14); "
    "en.wikipedia.org/wiki/Ambarchik 69.62611111/162.30388889 (~0.12 km); "
    "WD Q2629730 P625 69.6167/162.2833 (~1.2 km, minute-rounded); "
    "UN/LOCODE RUABC 69.6167/162.3000 corroborates bay/settlement; "
    "historical Kolyma-mouth / Ambarchik Bay port (shipping later moved to Chersky); "
    "no dedicated modern pier OSM found — settlement_site; "
    "GIS quality densify 2026-10-13 ~11:52 MSK gis-port045-1152 (off soft 69.6500/162.3500, ~3.3 km)"
)
OLD_TAIL = "Ambarchik Port,State,,,"
NEW_TAIL = "Ambarchik Port,State,\"" + NOTE + "\",88,2026-10-13"

roots = ["/home/workspace/ArcticTradeLanes-Dataset", "/home/workspace/ArcticTradeLanes.com"]
seen = set()
n = 0
for r in roots:
    for p in glob.glob(r + "/**/ports.csv", recursive=True):
        rp = os.path.realpath(p)
        if rp in seen or "node_modules" in rp or "_bak" in rp:
            continue
        seen.add(rp)
        lines = open(rp, encoding="utf-8").read().split("\n")
        hit = False
        for i, l in enumerate(lines):
            if l.startswith("ARC-PORT-045,") and OLD_LL in l and l.endswith(OLD_TAIL):
                lines[i] = l.replace(OLD_LL, NEW_LL).removesuffix(OLD_TAIL) + NEW_TAIL
                hit = True
        if hit:
            shutil.copy2(rp, rp + ".bak-gis-port045-1152")
            open(rp, "w", encoding="utf-8").write("\n".join(lines))
            n += 1
            print("patched", rp)
        elif any(l.startswith("ARC-PORT-045,") for l in lines):
            row = next(l for l in lines if l.startswith("ARC-PORT-045,"))
            print("SKIP (row differs)", rp)
            print("  ends:", repr(row[-80:]))

ENTRY = (
    '            "ARC-PORT-045": {\n'
    '                "position_quality": "settlement_site",\n'
    '                "position_note": "Ambarchik rural locality / historic Kolyma-mouth port: OSM way/655223046 place=hamlet Nominatim 69.6252019/162.3024493 (WD Q2629730; enwiki Ambarchik 69.62611/162.30389); was soft 69.6500/162.3500 (~3.3 km); shipping later transferred to Chersky — settlement_site not a modern commercial terminal",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-048": {\n'
for b in ["atlas-proj/build_atlas.py", "arctic-trade-lanes/atlas-proj/build_atlas.py"]:
    path = os.path.join("/home/workspace/ArcticTradeLanes.com", b) if not b.startswith("/") else b
    if not os.path.isfile(path):
        # nested may share via symlink; try relative from ATL.com
        path = "/home/workspace/ArcticTradeLanes.com/" + b
    if not os.path.isfile(path):
        print("missing builder", path)
        continue
    s = open(path, encoding="utf-8").read()
    if '"ARC-PORT-045": {' in s:
        print("builder already has entry", path)
        continue
    assert s.count(ANCH) == 1, path
    shutil.copy2(path, path + ".bak-gis-port045-1152")
    open(path, "w", encoding="utf-8").write(s.replace(ANCH, ENTRY + ANCH))
    print("builder patched", path)

print("csv files patched", n)
