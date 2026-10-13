#!/usr/bin/env python3
"""gis-port036-1444: densify ARC-PORT-036 Tiksi East Port onto East Pier No.1 of Tiksi seaport.

Soft pin 71.6800/128.9500 sat in Tiksi Bay water on the N edge of anchorage district No.1 (~4.3 km NNE of the quays).
No public source names a separate 'Tiksi East Port'; the Mintrans order No.50 of 14.02.2017 (Obligatory Regulations,
seaport Tiksi, west shore of Tiksi Bay) lists the only operating berths as No.11 + No.12 on 'Vostochny pirs No.1'
(East Pier No.1, 157.5 m each, 5.8 m depth); East Pier No.2 (berths 1-4, 13, 14) decommissioned.
Anchor = OSM way/1081390287 man_made=pier 'Vostochny pirs I' vertex centroid 71.6448592/128.8963706
(seamark berth nodes 9911507906 '11' + 9911507905 '12', depth 5.8); East Pier II = way/1081390288 ~0.12 km SE.
ARC-PORT-006 Tiksi Sea Port stays on way/1081390289 'Portovy flot' pier ~0.21 km W.
Identity inferred (East Port = East piers), so position_quality=facility_site.
"""
import glob, os, shutil, sys

PID = "ARC-PORT-036"
OLD_LL = ",Russia,71.6800,128.9500,"
NEW_LL = ",Russia,71.6448592,128.8963706,"
NOTE = (
    "GIS quality densify 2026-10-13 ~14:44 MSK gis-port036-1444: moved off soft 71.6800/128.9500 (Tiksi Bay water, N edge of anchorage district 1, ~4.3 km NNE) "
    "to OSM way/1081390287 man_made=pier Vostochny pirs I (East Pier No.1) vertex centroid 71.6448592/128.8963706; "
    "Mintrans order No.50 of 14.02.2017 (Obligatory Regulations seaport Tiksi, legalacts.ru) Annex 3: operating berths No.11 + No.12 on East Pier No.1 (157.5 m, 5.8 m depth), East Pier No.2 berths 1-4/13/14 decommissioned; "
    "OSM seamark berth nodes 9911507906 (11) + 9911507905 (12); East Pier II way/1081390288 ~0.12 km SE; harbour way/233652114; town Wikidata Q500895, Tiksi Bay Q2152754; "
    "no public source for a separate Tiksi East Port entity (identity inferred = East piers of Tiksi seaport; RUTIE code and Rosatom operator unverified) - facility_site"
)
OLD_TAIL = ",35,Rosatom,State,,,"
NEW_TAIL = ',35,Rosatom,State,"' + NOTE + '",85,2026-10-13'
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
            shutil.copy2(rp, rp + ".bak-gis-port036-1444")
            open(rp, "w", encoding="utf-8", newline="").write("\n".join(lines))
            n += 1; print("patched", rp)
        elif any(l.startswith(PID + ",") for l in lines):
            row = next(l for l in lines if l.startswith(PID + ","))
            print("SKIP (row differs)", rp, repr(row[-90:]))

ENTRY = (
    '            "ARC-PORT-036": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Tiksi East Port read as the East piers of Tiksi seaport (west shore of Tiksi Bay): anchor OSM way/1081390287 man_made=pier Vostochny pirs I (East Pier No.1) vertex centroid 71.6448592/128.8963706 with seamark berths 11 + 12; Mintrans order No.50 of 14.02.2017 Annex 3: berths 11-12 on East Pier No.1 operating (157.5 m, 5.8 m), East Pier No.2 decommissioned; was soft 71.6800/128.9500 in Tiksi Bay anchorage water (~4.3 km NNE); no public source for a separate East Port entity - facility_site, identity inferred",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-136": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True) + glob.glob(r + "/build_atlas.py"):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-036": {' in s:
            print("builder already has entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor missing", rp); continue
        shutil.copy2(rp, rp + ".bak-gis-port036-1444")
        s = s.replace(ANCH, ENTRY + ANCH)
        open(rp, "w", encoding="utf-8").write(s)
        print("builder patched", rp)
print("csv files patched", n)
