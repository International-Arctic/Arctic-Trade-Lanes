#!/usr/bin/env python3
"""gis-port136-1346: densify ARC-PORT-136 Narvik Terminal Nord (Kleiva) onto Kleivhammaren on Fagernesveien.

Soft pin 68.4400/17.4200 sat ~1.8 km N in Narvik city/harbour, north of the planned terminal.
Adopted area plan 'Narvikterminalen med Terminal Nord' (PlanID 2021001, Narvik kommunestyre 18.04.2024, sak 040/24):
"Terminal nord mellom RO-RO-kaia og Kleivhammaren" - sea fill along Fagernesveien, Fagernesveien moved east ~500 m
past Kleivhammaren, access north of the existing furniture store.
Anchor = OSM node/6372382875 bus stop 'Kleivhammarn' (NSR quay 85150) on Fagernesveien 68.4241270/17.4309920.
Corroboration: OSM node/6372384369 'Lillekleiva' stop (ro-ro terminal end, ~0.33 km S); OSM node/7590047622
Fagmobler Narvik (the furniture store, ~0.08 km N). Planned terminal not built: position_quality=facility_site.
"""
import glob, os, shutil, sys

PID = "ARC-PORT-136"
OLD_LL = ",Norway,68.4400,17.4200,"
NEW_LL = ",Norway,68.4241270,17.4309920,"
NOTE = (
    "; GIS quality densify 2026-10-13 ~13:46 MSK gis-port136-1346: moved off soft 68.4400/17.4200 (Narvik city/harbour ~1.8 km N) "
    "to OSM node/6372382875 Kleivhammarn bus stop on Fagernesveien 68.4241270/17.4309920; "
    "adopted area plan Narvikterminalen med Terminal Nord PlanID 2021001 (Narvik kommunestyre 18.04.2024 sak 040/24) planbeskrivelse: "
    "Terminal nord between the RO-RO quay (Lillekleiva) and Kleivhammaren with sea fill along Fagernesveien and access north of the furniture store "
    "(OSM node/7590047622 Fagmobler); OSM node/6372384369 Lillekleiva stop ~0.33 km S; planned terminal not built - facility_site"
)
OLD_TAIL = 'Narvik NATO logistics hub, 740m LKAB trains)",85,2026-08-25'
NEW_TAIL = 'Narvik NATO logistics hub, 740m LKAB trains)' + NOTE + '",90,2026-10-13'
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
            shutil.copy2(rp, rp + ".bak-gis-port136-1346")
            open(rp, "w", encoding="utf-8", newline="").write("\n".join(lines))
            n += 1; print("patched", rp)
        elif any(l.startswith(PID + ",") for l in lines):
            row = next(l for l in lines if l.startswith(PID + ","))
            print("SKIP (row differs)", rp, repr(row[-90:]))

ENTRY = (
    '            "ARC-PORT-136": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Planned Narvik Terminal Nord (Narvik Havn KF + Bane NOR; area plan Narvikterminalen med Terminal Nord PlanID 2021001 adopted 18.04.2024): between the RO-RO quay at Lillekleiva and Kleivhammaren with sea fill along Fagernesveien; anchor OSM node/6372382875 Kleivhammarn bus stop 68.4241270/17.4309920 (Lillekleiva stop node/6372384369 ~0.33 km S; Fagmobler node/7590047622 = access-north-of-furniture-store reference); was soft 68.4400/17.4200 in Narvik city/harbour (~1.8 km N); not built - facility_site not a surveyed berth",\n'
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
        if '"ARC-PORT-136": {' in s:
            print("builder already has entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor missing", rp); continue
        shutil.copy2(rp, rp + ".bak-gis-port136-1346")
        s = s.replace(ANCH, ENTRY + ANCH)
        open(rp, "w", encoding="utf-8").write(s)
        print("builder patched", rp)
print("csv files patched", n)
