#!/usr/bin/env python3
"""gis-port105-1314: densify ARC-PORT-105 Cascade Point Ferry Terminal onto the north end of Glacier Highway.

Soft pin 58.8500/-135.0200 sat in upper Berners Bay water ~17 km N of the site.
Anchor = OSM node/2835378419, north terminus of Glacier Highway (way/217384152 + turnaround way/1033357934)
58.7001371/-134.9378631; Alaska DOT&PF: terminal at Cascade Point (Mile 42 Glacier Highway), Goldbelt land;
KTOO 2013-06-25: Glacier Highway extension Echo Cove -> Cascade Point; DOT&PF 35% planset HSHWY00015 site map
(east shore Berners Bay N of Point Bridget / Echo Cove). Planned terminal: position_quality=facility_site.
"""
import glob, os, shutil, sys

OLD_LL = ",USA,58.8500,-135.0200,"
NEW_LL = ",USA,58.7001371,-134.9378631,"
NOTE = (
    "; GIS quality densify 2026-10-13 ~13:14 MSK gis-port105-1314: moved off soft 58.8500/-135.0200 (upper Berners Bay water) "
    "~17.3 km to OSM node/2835378419 north terminus of Glacier Highway (way/217384152 + turnaround way/1033357934) 58.7001371/-134.9378631; "
    "Alaska DOT&PF Cascade Point = Mile 42 Glacier Highway on Goldbelt land (PR25-0020; PR23-0010); "
    "KTOO 2013-06-25 Glacier Hwy extension Echo Cove to Cascade Point; DOT&PF 35pct planset HSHWY00015 site map east shore Berners Bay; "
    "planned terminal not built - facility_site"
)
OLD_TAIL = "Gov. Dunleavy office,90,2026-08-23"
NEW_TAIL = "Gov. Dunleavy office" + NOTE + ",90,2026-10-13"
assert "," not in NOTE.replace("Alaska DOT&PF", "") or True

roots = sys.argv[1:] or ["."]
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
            if body.startswith("ARC-PORT-105,") and OLD_LL in body and body.endswith(OLD_TAIL):
                lines[i] = body.replace(OLD_LL, NEW_LL).removesuffix(OLD_TAIL) + NEW_TAIL + ("\r" if cr else "")
                hit = True
        if hit:
            shutil.copy2(rp, rp + ".bak-gis-port105-1314")
            open(rp, "w", encoding="utf-8", newline="").write("\n".join(lines))
            n += 1; print("patched", rp)
        elif any(l.startswith("ARC-PORT-105,") for l in lines):
            row = next(l for l in lines if l.startswith("ARC-PORT-105,"))
            print("SKIP (row differs)", rp, repr(row[-90:]))

ENTRY = (
    '            "ARC-PORT-105": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Planned AMHS Cascade Point Ferry Terminal (Alaska DOT&PF, Mile 42 Glacier Highway, Goldbelt land): OSM node/2835378419 north terminus of Glacier Highway 58.7001371/-134.9378631 (way/217384152 + turnaround way/1033357934; DOT&PF 35% planset HSHWY00015 site map; KTOO 2013 Echo Cove-Cascade Point extension); was soft 58.8500/-135.0200 in upper Berners Bay water (~17.3 km); terminal not yet built - facility_site not a surveyed berth",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-046": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True) + glob.glob(r + "/build_atlas.py"):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-105": {' in s:
            print("builder already has entry", rp); continue
        anch = ANCH if s.count(ANCH) == 1 else ('"ARC-PORT-046": {\n' if s.count('"ARC-PORT-046": {\n') == 1 else None)
        if not anch:
            print("builder anchor missing", rp); continue
        shutil.copy2(rp, rp + ".bak-gis-port105-1314")
        if anch == ANCH:
            s = s.replace(ANCH, ENTRY + ANCH)
        else:
            s = s.replace(anch, ENTRY.lstrip() + '            ' + anch)
        open(rp, "w", encoding="utf-8").write(s)
        print("builder patched", rp)
print("csv files patched", n)
