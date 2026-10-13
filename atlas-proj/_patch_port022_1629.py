#!/usr/bin/env python3
"""gis-port022-1629: densify ARC-PORT-022 Tuktoyaktuk Port onto OSM way/513281075 industrial=port.

Soft pin 69.4457/-133.0360 sits in the hamlet ~0.25 km from OSM place node/107350410
Tuktoyaktuk (= WD Q719547, P625 69.4428/-133.031) - a 4-decimal settlement approx, not the port.
Anchor = OSM way/513281075 landuse=industrial + industrial=port (closed, 29 nodes, ~0.16 km2,
tank farm of ~21 man_made=storage_tank ways inside) on the Tuktoyaktuk Harbour shore south of
Cache Point; shoelace centroid 69.4281426/-132.9885229 (~2.69 km SE of soft).
Corroboration: Tuktoyaktuk Harbour WD Q116456484 (CGNDB LAYQW) P625 69.4333/-132.9694 ~1.0 km NE;
DFO/CHS tide station 6485 Tuktoyaktuk 69.438226/-132.994402 ~1.2 km NNW; GNWT INF Marine
Transportation Services lists a Tuktoyaktuk freight-handling terminal; CMSN infrastructure
profile: cargo pier (MTS terminal) + oil terminal. UN/LOCODE CATUK, WPI 20491.
position_quality=facility_site (mapped port land, not a surveyed berth line).
"""
import glob, os, shutil, sys

PID = "ARC-PORT-022"
OLD_LL = ",Canada,69.4457,-133.0360,"
NEW_LL = ",Canada,69.4281426,-132.9885229,"
NOTE = (
    "GIS quality densify 2026-10-13 ~16:29 MSK gis-port022-1629: moved off soft 69.4457/-133.0360 "
    "(4-decimal hamlet approx ~0.25 km from OSM place node/107350410 = Wikidata Q719547 Tuktoyaktuk) to OSM way/513281075 "
    "landuse=industrial industrial=port shoelace centroid 69.4281426/-132.9885229 (port land + tank farm on Tuktoyaktuk Harbour "
    "shore S of Cache Point); Tuktoyaktuk Harbour Wikidata Q116456484 (CGNDB LAYQW) ~1.0 km NE; DFO/CHS tide station 6485 "
    "69.438226/-132.994402 ~1.2 km NNW; GNWT INF Marine Transportation Services Tuktoyaktuk freight terminal; UN/LOCODE CATUK; "
    "WPI 20491; facility_site"
)
OLD_TAIL = "Inuvialuit Regional Corporation,Indigenous,,,"
NEW_TAIL = 'Inuvialuit Regional Corporation,Indigenous,"' + NOTE + '",90,2026-10-13'
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
            shutil.copy2(rp, rp + ".bak-gis-port022-1629")
            open(rp, "w", encoding="utf-8", newline="").write("\n".join(lines))
            n += 1; print("patched", rp)
        elif any(l.startswith(PID + ",") for l in lines):
            row = next(l for l in lines if l.startswith(PID + ","))
            print("SKIP (row differs)", rp, repr(row[-140:]))

ENTRY = (
    '            "ARC-PORT-022": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Tuktoyaktuk port land on the Tuktoyaktuk Harbour shore S of Cache Point: OSM way/513281075 landuse=industrial industrial=port (tank farm ~21 storage_tank ways) shoelace centroid 69.4281426/-132.9885229; Tuktoyaktuk Harbour WD Q116456484 (CGNDB LAYQW) ~1.0 km NE; DFO/CHS tide station 6485 ~1.2 km NNW; hamlet node/107350410 = WD Q719547 ~2.4 km NW; GNWT INF MTS Tuktoyaktuk freight terminal; UN/LOCODE CATUK; was soft 69.4457/-133.0360 in the hamlet (~2.69 km); facility_site not a surveyed berth",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-042": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True) + glob.glob(r + "/build_atlas.py"):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-022": {' in s:
            print("builder already has entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp); continue
        shutil.copy2(rp, rp + ".bak-gis-port022-1629")
        s = s.replace(ANCH, ENTRY + ANCH)
        open(rp, "w", encoding="utf-8").write(s)
        print("builder patched", rp)
print("csv files patched", n)
