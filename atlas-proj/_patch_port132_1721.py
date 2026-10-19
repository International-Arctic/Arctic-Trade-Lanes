#!/usr/bin/env python3
"""gis-loop-1019-1721: densify ARC-PORT-132 Murmansk NSR Container Transshipment Terminal (NewNew Shipping container
berth, UN/LOCODE RUMMK) onto Murmansk Commercial Sea Port (MCSP) berth No. 15, the berth where MCSP's specialised
container terminal was set up in 2025 and where the first NewNew Shipping Line NSR container ship moored (Aug 2026).

Soft pin 68.9783/33.0680 (4-decimal) = OSM name node/4185004064 'Murmanskiy Morskoy Torgovyy Port' (port office /
central gate area on Portovyy proyezd), not quay infrastructure.
Anchor: OSM node/9910923976 seamark:type=berth seamark:berth:name=15 seamark:berth:minimum_depth=10.47
(description 68 59,08' 033 03,79') at 68.9846667/33.0631667, inside OSM way/85150513 landuse=industrial
'Murmanskiy morskoy torgovyy port' (~0.73 km NNW of soft; ~0.42 km N of parent ARC-PORT-001 MCSP yard centroid).
Sources: mvestnik.ru #233137 + murmansk.ru/55954 (moored at berth 15; container terminal set up 2025 with Port Alliance;
return potash at berth 17), abnews.ru 2026-08-21 (terminal built at berth No. 15), portnews.ru/news/395720, morport.com.
"""
import csv, glob, io, os, re, shutil, sys

PID = "ARC-PORT-132"
TAG = "gis-loop-1019-1721"
NEW_LAT, NEW_LON = "68.9846667", "33.0631667"
OLD = ("68.9783", "33.0680")
CONF = "90"
NOTE = (
    "GIS quality densify 2026-10-19 ~17:21 MSK gis-loop-1019-1721: moved off soft 68.9783/33.0680 (4-decimal pin on the "
    "OSM name node/4185004064 Murmansk Commercial Sea Port office / central gate area on Portovyy proyezd, not quay "
    "infrastructure) to MCSP berth No. 15, where the port's specialised container terminal was set up in 2025 and where "
    "the first NewNew Shipping Line container ship via the NSR moored on 19 Aug 2026: OSM node/9910923976 seamark:type=berth "
    "seamark:berth:name=15 minimum_depth 10.47 m at 68.9846667/33.0631667 (~0.73 km NNW), inside OSM way/85150513 "
    "landuse=industrial Murmansk Commercial Sea Port; berth 17 (potash return cargo) OSM node/9910923973 ~0.29 km NNW; "
    "sources mvestnik.ru/newslent/v-murmanske-vstretili-pervyj-kontejnerovoz-iz-kitaya-preodolevshij-severnyj-morskoj-put/ "
    "+ murmansk.ru/55954 (berth 15; terminal created 2025) + abnews.ru 2026-08-21 (terminal at berth No. 15) + "
    "portnews.ru/news/395720 + morport.com; parent ARC-PORT-001 MCSP yard centroid ~0.42 km S kept separate; "
    "berth depth 10.47 m per OSM seamark (row max_depth left unchanged); facility_site berth point, not a surveyed berth line"
)
roots = sys.argv[1:] or ["."]
seen = set(); n = 0
for r in roots:
    for p in glob.glob(r + "/**/ports.csv", recursive=True):
        rp = os.path.realpath(p)
        if rp in seen or "node_modules" in rp or ".bak" in rp:
            continue
        seen.add(rp)
        raw = open(rp, encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in raw else "\n"
        has_trailing = raw.endswith("\n") or raw.endswith("\r\n")
        rows = list(csv.reader(io.StringIO(raw)))
        hit = False
        for i, row in enumerate(rows):
            if not row or row[0] != PID or len(row) < 20:
                continue
            old_lat, old_lon = row[4], row[5]
            if old_lat == NEW_LAT and old_lon == NEW_LON and TAG in (row[17] or ""):
                print("already", rp); continue
            if (old_lat, old_lon) != OLD:
                print("SKIP unexpected old coords", old_lat, old_lon, rp); continue
            row[4], row[5] = NEW_LAT, NEW_LON
            src = row[17] or ""
            if TAG not in src:
                row[17] = (src + " | " + NOTE) if src else NOTE
            row[18] = CONF
            row[19] = "2026-10-19"
            rows[i] = row
            hit = True
            print(f"row {old_lat}/{old_lon} -> {NEW_LAT}/{NEW_LON}", rp)
        if hit:
            shutil.copy2(rp, rp + ".bak-" + TAG)
            buf = io.StringIO()
            csv.writer(buf, lineterminator=nl).writerows(rows)
            out = buf.getvalue()
            if not has_trailing and out.endswith(nl):
                out = out[: -len(nl)]
            open(rp, "w", encoding="utf-8", newline="").write(out)
            n += 1

ENTRY = (
    '            "ARC-PORT-132": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Murmansk Commercial Sea Port berth No. 15 (UN/LOCODE RUMMK), site of the MCSP specialised container terminal (set up 2025) used by the NewNew Shipping Line NSR container service (first call 19 Aug 2026): OSM node/9910923976 seamark:type=berth seamark:berth:name=15 min depth 10.47 m at 68.9846667/33.0631667 inside OSM way/85150513 landuse=industrial Murmansk Commercial Sea Port; berth 17 OSM node/9910923973 ~0.29 km NNW; mvestnik.ru + murmansk.ru/55954 + abnews.ru (berth 15) + portnews.ru/news/395720; soft 68.9783/33.0680 was the OSM port-office name node/4185004064 (~0.73 km SSE); parent ARC-PORT-001 yard centroid ~0.42 km S; facility_site",\n'
    '            },\n'
)
ANCH = '            "ARC-PORT-113": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-132": {' in s and NEW_LAT in s:
            print("builder already has entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp); continue
        shutil.copy2(rp, rp + ".bak-" + TAG)
        open(rp, "w", encoding="utf-8").write(s.replace(ANCH, ENTRY + ANCH))
        print("builder patched", rp)
print("csv files patched", n)
