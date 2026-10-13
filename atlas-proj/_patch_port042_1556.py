#!/usr/bin/env python3
"""gis-port042-1556: densify ARC-PORT-042 Egvekinot Port onto OSM main pier way/721745076.

Soft pin 66.3167/-179.1167 matches Rosmorrechflot registry AD-378-r (66deg19'N 179deg07'W)
and WD Q1240765 settlement P625 — a 4-decimal settlement/registry approx, not a pier.
Anchor = OSM way/721745076 man_made=pier (larger harbour pier area on Kresta Bay shore)
shoelace centroid 66.3192251/-179.1095237 (~0.43 km ENE of soft). Secondary pier
way/721745075 ~0.6 km SSW. Settlement place node/2891542781 = WD Q1240765 ~0.62 km NW.
position_quality=facility_site (mapped pier, not a berth survey).
"""
import glob, os, shutil, sys

PID = "ARC-PORT-042"
OLD_LL = ",Russia,66.3167,-179.1167,"
NEW_LL = ",Russia,66.3192251,-179.1095237,"
NOTE = (
    "GIS quality densify 2026-10-13 ~15:56 MSK gis-port042-1556: moved off soft 66.3167/-179.1167 "
    "(4-decimal Rosmorrechflot AD-378-r / WD Q1240765 settlement P625 approx) to OSM way/721745076 "
    "man_made=pier shoelace centroid 66.3192251/-179.1095237 (main Egvekinot harbour pier area, Kresta Bay); "
    "secondary pier way/721745075 ~0.6 km SSW; settlement place node/2891542781 = Wikidata Q1240765 "
    "Egvekinot ~0.62 km NW; UN/LOCODE RUEGV; Rosmorrechflot registry AD-378-r 24.12.2010 "
    "(66deg19'N 179deg07'W, ul. Portovaya 1); facility_site"
)
OLD_TAIL = "Chukotka Sea Port,State,,,"
NEW_TAIL = 'Chukotka Sea Port,State,"' + NOTE + '",90,2026-10-13'
assert '"' not in NOTE

roots = sys.argv[1:] or ["/home/workspace/ArcticTradeLanes-Dataset", "/home/workspace/ArcticTradeLanes.com"]
seen = set(); n = 0
for r in roots:
    for p in glob.glob(r + "/**/ports.csv", recursive=True):
        rp = os.path.realpath(p)
        if rp in seen or "node_modules" in rp or "_bak" in rp or ".bak" in rp:
            continue
        seen.add(rp)
        raw = open(rp, encoding="utf-8", newline="").read()
        lines = raw.split("\n")
        hit = False
        for i, l in enumerate(lines):
            cr = l.endswith("\r")
            body = l[:-1] if cr else l
            if body.startswith(PID + ",") and OLD_LL in body and body.endswith(OLD_TAIL):
                lines[i] = body.replace(OLD_LL, NEW_LL).removesuffix(OLD_TAIL) + NEW_TAIL + ("\r" if cr else "")
                hit = True
        if hit:
            shutil.copy2(rp, rp + ".bak-gis-port042-1556")
            open(rp, "w", encoding="utf-8", newline="").write("\n".join(lines))
            n += 1; print("patched", rp)
        elif any(l.lstrip("\r").startswith(PID + ",") or l.startswith(PID + ",") for l in lines):
            row = next(l for l in lines if PID + "," in l[:20])
            print("SKIP (row differs)", rp, repr(row[-140:]))

ENTRY = (
    '            "ARC-PORT-042": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Egvekinot seaport (RUEGV) main harbour pier on Kresta Bay: OSM way/721745076 man_made=pier shoelace centroid 66.3192251/-179.1095237; secondary pier way/721745075 ~0.6 km SSW; settlement node/2891542781 = WD Q1240765 ~0.62 km NW; Rosmorrechflot AD-378-r 24.12.2010 registry 66deg19N 179deg07W / ul. Portovaya 1; was soft 66.3167/-179.1167 (~0.43 km); facility_site",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-075": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True) + glob.glob(r + "/build_atlas.py"):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-042": {' in s:
            print("builder already has entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp); continue
        shutil.copy2(rp, rp + ".bak-gis-port042-1556")
        s = s.replace(ANCH, ENTRY + ANCH)
        open(rp, "w", encoding="utf-8").write(s)
        print("builder patched", rp)
print("csv files patched", n)
