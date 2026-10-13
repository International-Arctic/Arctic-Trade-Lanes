#!/usr/bin/env python3
"""gis-port075-1525: densify ARC-PORT-075 Nuuk Qeqertat quay onto OSM industrial=port south of container terminal.

Soft pin 64.1700/-51.7100 is a 2-decimal approx on Qeqertanut / Qeqertaq Avalleq (Fyrø).
Sikuki + Naalakkersuisut VVM (A246375-VVM-001, 2024) + KNR: the 350 m expansion (200 m trawler
+ 150 m dual-use naval; KJ Greenland; groundbreaking 2026-07-07; completion Nov 2028) is on the
west side of Qeqertaq Avalleq immediately south of the 2017 container terminal (Umiarsualiviup Qeqertai).
Anchor = OSM way/627906959 landuse=industrial industrial=port polygon shoelace centroid
64.1678488/-51.7140694 (~310 m WSW of soft; west-face ~310 m N-S matches planned quay length).
ARC-PORT-009 Nuuk Port stays on harbour node/995384594 (~0.69 km NW). No separate pier way yet
(under construction) -> position_quality=facility_site. Related WD Q3398532 = Port of Nuuk (existing).
"""
import glob, os, shutil, sys

PID = "ARC-PORT-075"
OLD_LL = ",Greenland,64.1700,-51.7100,"
NEW_LL = ",Greenland,64.1678488,-51.7140694,"
NOTE = (
    "; GIS quality densify 2026-10-13 ~15:25 MSK gis-port075-1525: moved off soft 64.1700/-51.7100 (2-decimal Qeqertanut approx) "
    "to OSM way/627906959 landuse=industrial industrial=port shoelace centroid 64.1678488/-51.7140694 on Qeqertaq Avalleq (Fyrø) "
    "immediately south of the 2017 container terminal; west face of that polygon ~310 m N-S (nodes 2590218967-2590218977) matches planned quay length; "
    "Sikuki 2026-07-08 groundbreaking on Qeqertaq Avalleq (200 m trawler + 150 m dual-use naval, completion Nov 2028); "
    "Naalakkersuisut VVM A246375-VVM-001 (2024): west side of Qeqertaq Avalleq just south of container terminal, kajkant continues south; "
    "KNR: 350 m new quay in extension of container terminal on Qeqertaq Avalleq; ARC-PORT-009 stays on OSM harbour node/995384594 (~0.69 km NW); "
    "no OSM pier/quay way for the new berth yet (under construction) - facility_site; related Wikidata Q3398532 Port of Nuuk"
)
OLD_TAIL = 'ground-breaking ceremony held Jul 7 2026 - construction underway",90,2026-08-23'
NEW_TAIL = 'ground-breaking ceremony held Jul 7 2026 - construction underway' + NOTE + '",90,2026-10-13'
assert '"' not in NOTE

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
            if body.startswith(PID + ",") and OLD_LL in body and body.endswith(OLD_TAIL):
                lines[i] = body.replace(OLD_LL, NEW_LL).removesuffix(OLD_TAIL) + NEW_TAIL + ("\r" if cr else "")
                hit = True
        if hit:
            shutil.copy2(rp, rp + ".bak-gis-port075-1525")
            open(rp, "w", encoding="utf-8", newline="").write("\n".join(lines))
            n += 1; print("patched", rp)
        elif any(l.startswith(PID + ",") for l in lines):
            row = next(l for l in lines if l.startswith(PID + ","))
            print("SKIP (row differs)", rp, repr(row[-120:]))

ENTRY = (
    '            "ARC-PORT-075": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Nuuk Harbour Expansion Qeqertat quay (Sikuki / KJ Greenland; 200 m trawler + 150 m dual-use naval; groundbreaking 2026-07-07; completion Nov 2028): on west side of Qeqertaq Avalleq (Fyrø) immediately south of the 2017 container terminal; anchor OSM way/627906959 landuse=industrial industrial=port shoelace centroid 64.1678488/-51.7140694 (west face ~310 m N-S); Naalakkersuisut VVM A246375-VVM-001 2024 + Sikuki 2026-07-08 + KNR; was soft 64.1700/-51.7100 (~0.31 km); ARC-PORT-009 on harbour node/995384594 ~0.69 km NW; no pier way yet - facility_site under construction",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-036": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True) + glob.glob(r + "/build_atlas.py"):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-075": {' in s:
            print("builder already has entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor missing", rp); continue
        shutil.copy2(rp, rp + ".bak-gis-port075-1525")
        s = s.replace(ANCH, ENTRY + ANCH)
        open(rp, "w", encoding="utf-8").write(s)
        print("builder patched", rp)
print("csv files patched", n)
