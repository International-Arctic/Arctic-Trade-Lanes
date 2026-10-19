#!/usr/bin/env python3
"""gis-loop-1019-1119: densify ARC-PORT-114 Port of Yeongilman (Pohang) onto OSM Pohang Yeongil New Port harbour area.

Soft pin 36.0194/129.4256 (4-decimal) sat inside POSCO Pohang Steelworks (Cheongnim-dong, Nam-gu; Nominatim
reverse way/996515174 residential road), ~9.15 km S of Yeongilman Port. Yeongilman Port (Pohang Yeongil New Port,
Heunghae-eup, Buk-gu) is mapped as OSM way/550199344 landuse=harbour name=포항영일신항만 (~136 ha, v7),
shoelace centroid 36.1013341/129.4354711 (inside polygon). Wikidata has no port item (only Yeongilmanhang Station
Q72246064 / Yeongilman Bay Q11260549 - not reused). UN/LOCODE KRKPO unchanged. position_quality=facility_site.
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-114"
TAG = "gis-loop-1019-1119"
NEW_LAT, NEW_LON = "36.1013341", "129.4354711"
NOTE = (
    "GIS quality densify 2026-10-19 ~11:19 MSK gis-loop-1019-1119: moved off soft 36.0194/129.4256 "
    "(4-decimal; inside POSCO Pohang Steelworks, Cheongnim-dong Nam-gu, not Yeongilman Port) to OSM "
    "way/550199344 landuse=harbour name=Pohang Yeongil Sinhangman (Pohang Yeongil New Port, Heunghae-eup Buk-gu, ~136 ha) "
    "shoelace centroid 36.1013341/129.4354711 (~9.15 km N, bearing ~6 deg); no Wikidata port item found "
    "(Yeongilmanhang Station Q72246064 and Yeongilman Bay Q11260549 not reused); UN/LOCODE KRKPO unchanged; "
    "facility_site harbour-area polygon, not a surveyed berth"
)
assert '"' not in NOTE

roots = sys.argv[1:] or ["/home/workspace/ArcticTradeLanes-Dataset", "/home/workspace/ArcticTradeLanes.com"]
seen = set()
n = 0
for r in roots:
    for p in glob.glob(r + "/**/ports.csv", recursive=True):
        rp = os.path.realpath(p)
        if rp in seen or "node_modules" in rp or "_bak" in rp or ".bak" in rp:
            continue
        seen.add(rp)
        raw = open(rp, encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in raw else "\n"
        has_trailing = raw.endswith("\n") or raw.endswith("\r\n")
        rows = list(csv.reader(io.StringIO(raw)))
        if not rows:
            continue
        hit = False
        for i, row in enumerate(rows):
            if not row or row[0] != PID:
                continue
            if len(row) < 20:
                print("SKIP short row", rp, len(row))
                continue
            old_lat, old_lon = row[4], row[5]
            if old_lat == NEW_LAT and old_lon == NEW_LON and TAG in (row[17] or ""):
                print("already", rp)
                continue
            if (old_lat, old_lon) != ("36.0194", "129.4256"):
                print("SKIP unexpected old coords", old_lat, old_lon, rp)
                continue
            row[4], row[5] = NEW_LAT, NEW_LON
            src = row[17] or ""
            if TAG not in src:
                row[17] = (src + " + " + NOTE) if src else NOTE
            row[18] = "92"
            row[19] = "2026-10-19"
            rows[i] = row
            hit = True
            print(f"row {old_lat}/{old_lon} -> {NEW_LAT}/{NEW_LON} locode {row[6]}", rp)
        if hit:
            shutil.copy2(rp, rp + ".bak-" + TAG)
            buf = io.StringIO()
            csv.writer(buf, lineterminator=nl).writerows(rows)
            out = buf.getvalue()
            if not has_trailing and out.endswith(nl):
                out = out[: -len(nl)]
            open(rp, "w", encoding="utf-8", newline="").write(out)
            n += 1
            print("patched", rp)

ENTRY = (
    '            "ARC-PORT-114": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Port of Yeongilman / Pohang Yeongil New Port (포항영일신항만, Heunghae-eup, Buk-gu, Pohang; UN/LOCODE KRKPO): OSM way/550199344 landuse=harbour name=포항영일신항만 (~136 ha), shoelace centroid 36.1013341/129.4354711; NSR specialised-hub concept study subject; soft 36.0194/129.4256 was ~9.15 km S inside POSCO Pohang Steelworks (Nam-gu); no Wikidata port item (Yeongilmanhang Station Q72246064 / Yeongilman Bay Q11260549 not reused); facility_site harbour-area polygon, not a surveyed berth",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-109": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True) + glob.glob(r + "/build_atlas.py"):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-114": {' in s:
            print("builder already has entry", rp)
            continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp)
            continue
        shutil.copy2(rp, rp + ".bak-" + TAG)
        s = s.replace(ANCH, ENTRY + ANCH)
        open(rp, "w", encoding="utf-8").write(s)
        print("builder patched", rp)
print("csv files patched", n)
