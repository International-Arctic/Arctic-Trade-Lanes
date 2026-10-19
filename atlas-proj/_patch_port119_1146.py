#!/usr/bin/env python3
"""gis-loop-1019-1146: densify ARC-PORT-119 Blue Water Blue Imeq Greenland logistics hub (Nuuk) onto OSM Nuuk Imeq building.

Soft pin 64.1835/-51.7216 (4-decimal) sat ~0.28 km W of Blue Water's legacy Industrivej 22 office (OSM node/5130345724),
not the Blue Imeq hub. Blue Imeq is the former Nuuk Imeq bottling plant bought by Blue Water (bws.net news 26 Jul 2024;
sermitsiaq.ag), opened Mar 2026; operator address Blue Water Greenland A/S, Qeqertanut 2, 3905 Nuussuaq (bws.net contact).
OSM way/257366763 building=industrial name=Nuuk Imeq A/S addr Qeqertanut 2 3905 Nuussuaq (~8,400 m2), shoelace centroid
64.1765970/-51.7059645 (inside polygon). No Wikidata facility item (operator Blue Water Shipping Q12303853 not reused).
UN/LOCODE GLGOH unchanged. position_quality=facility_site.
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-119"
TAG = "gis-loop-1019-1146"
NEW_LAT, NEW_LON = "64.1765970", "-51.7059645"
OLD = ("64.1835", "-51.7216")
NOTE = (
    "GIS quality densify 2026-10-19 ~11:46 MSK gis-loop-1019-1146: moved off soft 64.1835/-51.7216 "
    "(4-decimal; ~0.28 km W of the legacy Blue Water Industrivej 22 office, not the Blue Imeq hub) to OSM "
    "way/257366763 building=industrial name=Nuuk Imeq A/S addr Qeqertanut 2 3905 Nuussuaq (former Nuuk Imeq bottling plant "
    "acquired by Blue Water 2024 per bws.net news and sermitsiaq.ag; operator address Qeqertanut 2 per bws.net contact) "
    "shoelace centroid 64.1765970/-51.7059645 (~1.08 km SE, bearing ~135 deg); no Wikidata facility item "
    "(operator Blue Water Shipping Q12303853 not reused); UN/LOCODE GLGOH unchanged; "
    "facility_site warehouse/terminal building, not a quay"
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
            if (old_lat, old_lon) != OLD:
                print("SKIP unexpected old coords", old_lat, old_lon, rp)
                continue
            row[4], row[5] = NEW_LAT, NEW_LON
            src = row[17] or ""
            if TAG not in src:
                row[17] = (src + " + " + NOTE) if src else NOTE
            row[18] = "90"
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
    '            "ARC-PORT-119": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Blue Water Blue Imeq hub, Nuuk (former Nuuk Imeq bottling plant, Qeqertanut 2, 3905 Nuussuaq; UN/LOCODE GLGOH): OSM way/257366763 building=industrial name=Nuuk Imeq A/S (~8,400 m2), shoelace centroid 64.1765970/-51.7059645; acquired by Blue Water 2024 (bws.net, sermitsiaq.ag), opened as Blue Imeq Mar 2026; soft 64.1835/-51.7216 was ~1.08 km NW near the legacy Industrivej 22 office; no Wikidata facility item (operator Blue Water Shipping Q12303853 not reused); facility_site warehouse/terminal building, not a quay",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-114": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True) + glob.glob(r + "/build_atlas.py"):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-119": {' in s:
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
