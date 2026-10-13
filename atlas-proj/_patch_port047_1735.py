#!/usr/bin/env python3
"""gis-port047-1735: densify ARC-PORT-047 Nordvik Port (historic) onto WD Q2364258.

Soft pin 73.9980/111.4693 is a 4-decimal approx matching OSM place=locality
node/3290343023 Нордвик, with empty sources (no OSM/WD cited). No OSM pier/harbour
mapped within ~25 km. Wikidata Q2364258 (former port and settlement in Krasnoyarsk
Krai, USSR; founded ~1930, abolished 1956) P625 73.9975/111.463333 is the verifiable
historic port/settlement facility centroid (~0.19 km W of soft). Some stale copies
still carried coarser 74.5000/111.5000. position_quality=facility_site (historic port
site; no surviving berth mapped).
"""
import glob, os, re, shutil, sys

PID = "ARC-PORT-047"
NEW_LAT, NEW_LON = "73.9975", "111.463333"
NOTE = (
    "GIS quality densify 2026-10-13 ~17:35 MSK gis-port047-1735: moved off soft 73.9980/111.4693 "
    "(4-decimal approx = OSM place=locality node/3290343023 Нордвик; empty OSM/WD in sources; "
    "stale copies also had 74.5000/111.5000) to Wikidata Q2364258 Nordvik former port and "
    "settlement P625 73.9975/111.463333 (~0.19 km W; founded ~1930 abolished 1956; Khatanga Gulf / "
    "Laptev Sea, Taymyr, Krasnoyarsk Krai); no OSM pier/harbour mapped nearby; UN/LOCODE RUNVK; "
    "facility_site (historic port site, not a surveyed berth)"
)
assert '"' not in NOTE
NEW_TAIL = f',"{NOTE}",90,2026-10-13'

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
            if not body.startswith(PID + ","):
                continue
            # Replace lat/lon (fields 5,6 after split) and trailing operator/ownership/sources/confidence/verified
            parts = body.split(",")
            # CSV is simple for this row (no quoted commas until we add NOTE)
            # Structure: 20 columns; sources may be empty
            # Re-parse carefully: known prefix through ownership_type
            m = re.match(
                r"^(ARC-PORT-047,Nordvik Port \(historic\),ARC-CITY-046,Russia,)([-+0-9.]+),([-+0-9.]+),(RUNVK,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL)(?:,.*)?$",
                body,
            )
            if not m:
                print("SKIP parse", rp, repr(body[-120:])); continue
            new_body = m.group(1) + NEW_LAT + "," + NEW_LON + "," + m.group(4) + NEW_TAIL
            if new_body == body:
                print("already", rp); continue
            lines[i] = new_body + ("\r" if cr else "")
            hit = True
        if hit:
            shutil.copy2(rp, rp + ".bak-gis-port047-1735")
            open(rp, "w", encoding="utf-8", newline="").write("\n".join(lines))
            n += 1; print("patched", rp)

ENTRY = (
    '            "ARC-PORT-047": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Nordvik Port (historic) / former USSR port-settlement on Khatanga Gulf (Laptev Sea): Wikidata Q2364258 Nordvik P625 73.9975/111.463333 (founded ~1930, abolished 1956); OSM place=locality node/3290343023 Нордвик 73.9980/111.4693 ~0.19 km E; UN/LOCODE RUNVK; no OSM pier/harbour mapped; was soft 73.9980/111.4693 (and stale 74.5000/111.5000) - facility_site historic, not a surveyed berth",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-051": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True) + glob.glob(r + "/build_atlas.py"):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-047": {' in s:
            print("builder already has entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp); continue
        shutil.copy2(rp, rp + ".bak-gis-port047-1735")
        s = s.replace(ANCH, ENTRY + ANCH)
        open(rp, "w", encoding="utf-8").write(s)
        print("builder patched", rp)
print("csv files patched", n)
