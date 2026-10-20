#!/usr/bin/env python3
"""gis-loop-1020-1516: move ARC-PORT-082 Whittier ARRC Tunnel Double-Stack Upgrade (USWIT) onto the Whittier portal of the
Anton Anderson Memorial Tunnel (the funded ARRC rail asset).

Soft pin 60.7768/-148.7210 (4-decimal GIS-2026-09-07 'tunnel approach/portal' estimate, actually ~660 m east of the portal in the
Whittier staging area). OpenStreetMap: rail tunnel way/51231246 (Whittier Branch, operator Alaska Railroad Corporation,
tunnel:name Anton Anderson Memorial Tunnel, tunnel:wikidata Q2728238) east end node/653863539 = Whittier portal 60.7772824/-148.7330898
(west end node/65261724 = Bear Valley portal 60.7888861/-148.803615). ~660 m W. facility_site (tunnel portal of the funded rail
facility, not a quay). Confidence 90 kept.
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-082"
TAG = "gis-loop-1020-1516"
NEW_LAT, NEW_LON = "60.7772824", "-148.7330898"
OLD = ("60.7768", "-148.7210")
NOTE = (
    "GIS quality densify 2026-10-20 ~15:16 MSK gis-loop-1020-1516: moved off soft 60.7768/-148.7210 (4-decimal tunnel-approach estimate, "
    "~660 m east of the portal in the Whittier staging area) to the Whittier portal of the Anton Anderson Memorial Tunnel (the ARRC rail asset "
    "funded by the USD 20.4M PIDP double-stack clearance upgrade): OpenStreetMap rail tunnel way/51231246 (Whittier Branch, operator Alaska "
    "Railroad Corporation, tunnel:name Anton Anderson Memorial Tunnel, tunnel:wikidata Q2728238) east end node/653863539 = 60.7772824/-148.7330898 "
    "(~660 m W); facility_site = tunnel portal of the funded rail facility, not a quay; port-side rail barge slip is USACE NDC 0UWM ARRC Whittier "
    "Slip No 2 60.776667/-148.67472; confidence and other attributes left unchanged"
)
roots = sys.argv[1:] or ["."]
seen = set(); n = 0
for r in roots:
    for p in glob.glob(r + "/**/ports.csv", recursive=True):
        rp = os.path.realpath(p)
        if rp in seen or "node_modules" in rp or ".bak" in rp or "/_b" in rp or "/bak" in rp:
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
            row[19] = "2026-10-20"
            rows[i] = row
            hit = True
            print(f"row {old_lat}/{old_lon} -> {NEW_LAT}/{NEW_LON} conf {row[18]}", rp)
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
    '            "ARC-PORT-082": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Whittier ARRC Tunnel Double-Stack Upgrade (UN/LOCODE USWIT; Alaska Railroad Corporation PIDP FY2026 tunnel clearance project): Whittier portal of the Anton Anderson Memorial Tunnel, OpenStreetMap rail tunnel way/51231246 (Whittier Branch, tunnel:wikidata Q2728238) east end node/653863539 60.7772824/-148.7330898; soft 60.7768/-148.7210 was a 4-decimal tunnel-approach estimate in the Whittier staging area (~660 m E); tunnel portal of the funded rail facility, not a quay; port-side rail barge slip = USACE NDC 0UWM ARRC Whittier Slip No 2; facility_site",\n'
    '            },\n'
)
ANCH = '            "ARC-PORT-139": {\n'
KEY = '"ARC-PORT-082": {'
bseen = set()
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True):
        rp = os.path.realpath(path)
        if rp in bseen or "node_modules" in rp:
            continue
        bseen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if KEY in s:
            print("builder already has ARC-PORT-082 entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp); continue
        shutil.copy2(rp, rp + ".bak-" + TAG)
        open(rp, "w", encoding="utf-8").write(s.replace(ANCH, ENTRY + ANCH))
        print("builder patched", rp)
print("csv files patched", n)
