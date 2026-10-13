#!/usr/bin/env python3
"""gis-port051-1700: densify ARC-PORT-051 Nome Snake River Moorage onto west-bank slipway.

Soft pin 64.4980/-165.4200 is a 4-decimal approx lacking OSM/WD in sources; distinct from
ARC-PORT-026 Nome Harbor [-165.437672, 64.496022]. City of Nome Strategic Development Plan
Phase B (Apr 2025) + MARAD FONSI (Aug 2026) place Snake River Floats / Moorage on the west
shore of the Snake River, south of Satellite Drive and north of the RO/RO facility.
Anchor = OSM way/1268826085 leisure=slipway (service=slipway) centroid 64.5014256/-165.4286323
on the west bank in that corridor (~0.56 km from soft; Satellite Drive way/8983909 ~0.29 km N;
Snake River WD Q7547059 P625 64.5044/-165.4242 ~0.39 km NE; PORT-026 piers ~0.74 km SW).
Floats not yet built (35% design; dredge package early 2027). position_quality=facility_site.
"""
import glob, os, shutil, sys

PID = "ARC-PORT-051"
OLD_LL = ",USA,64.4980,-165.4200,"
NEW_LL = ",USA,64.5014256,-165.4286323,"
NOTE = (
    "GIS quality densify 2026-10-13 ~17:00 MSK gis-port051-1700: moved off soft 64.4980/-165.4200 "
    "(4-decimal approx; empty OSM/WD in sources) to OSM way/1268826085 leisure=slipway centroid "
    "64.5014256/-165.4286323 on west shore of Snake River in City of Nome Snake River Moorage / "
    "Floats corridor (south of Satellite Drive way/8983909 ~0.29 km N; north of RO/RO; "
    "Snake River WD Q7547059 P625 64.5044/-165.4242 ~0.39 km NE); DISTINCT from ARC-PORT-026 Nome Harbor "
    "piers way/336012429+847015621 ~0.74 km SW; MARAD FONSI Aug 2026 + RAISE $13.2M; floats not built "
    "(35% design; dredge bid early 2027); facility_site"
)
OLD_TAIL = (
    "City of Nome,Municipal,dot.alaska.gov (Governor Dunleavy $13.2M DOT RAISE grant 2025 for ~1700ft new floating dock; "
    "matched by City of Nome; permitting+design in progress); digital.akbizmag.com Deepwater Arising Mar 2026 "
    "(DOT grant; Snake River Floats alignment); knom.org local press (Snake River moorage context),78,2026-09-01"
)
NEW_TAIL = 'City of Nome,Municipal,"' + NOTE + '",90,2026-10-13'
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
            shutil.copy2(rp, rp + ".bak-gis-port051-1700")
            open(rp, "w", encoding="utf-8", newline="").write("\n".join(lines))
            n += 1; print("patched", rp)
        elif any(l.lstrip("\r").startswith(PID + ",") for l in lines):
            row = next(l for l in lines if l.startswith(PID + ",") or l.lstrip("\r").startswith(PID + ","))
            print("SKIP (row differs)", rp, repr(row[-160:]))

ENTRY = (
    '            "ARC-PORT-051": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Planned Nome Snake River Moorage Facility / Snake River Floats (City of Nome; MARAD FONSI Aug 2026; RAISE $13.2M): west shore of Snake River south of Satellite Drive and north of the RO/RO facility; anchor OSM way/1268826085 leisure=slipway 64.5014256/-165.4286323 (west-bank slipway in project corridor; Satellite Drive way/8983909 ~0.29 km N; Snake River WD Q7547059 P625 64.5044/-165.4242 ~0.39 km NE); ARC-PORT-026 Nome Harbor piers ~0.74 km SW; floats not yet built (35% design, dredge bid early 2027) - facility_site not a surveyed berth; was soft 64.4980/-165.4200 (~0.56 km)",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-022": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True) + glob.glob(r + "/build_atlas.py"):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-051": {' in s:
            print("builder already has entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp); continue
        shutil.copy2(rp, rp + ".bak-gis-port051-1700")
        s = s.replace(ANCH, ENTRY + ANCH)
        open(rp, "w", encoding="utf-8").write(s)
        print("builder patched", rp)
print("csv files patched", n)
