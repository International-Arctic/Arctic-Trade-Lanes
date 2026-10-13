#!/usr/bin/env python3
"""gis-port150-1828: densify ARC-PORT-150 Pyramiden Port onto the harbour crane / quay (OSM node/857534564).

Soft pin 78.6567/16.3250 is the settlement centre (Wikidata Q845396 P625 78.656111/16.325,
~0.07 km; OSM place node/273476498 78.655822/16.3228695). Anchor = OSM node/857534564
man_made=crane 78.654916/16.3553162 at the seaward end of the concrete embankment quay road
way/72761799 (highway=service surface=concrete embankment=yes) on the Billefjorden shore,
~0.69 km ESE of soft. Corroboration: Kystverket leading beacons Pyramiden Ovre ref 991900 (OSM
node/5323958065, ~0.16 km N) and Pyramiden Nedre ref 991800 (OSM node/5323958066, ~0.31 km E);
weather station node/6955534667 ~0.09 km N. Local OSM coastline (way/323883492, gadm/yahoo,
fixme=update) is coarse here. position_quality=facility_site (quay/crane, not a surveyed berth).
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-150"
NEW_LAT, NEW_LON = "78.654916", "16.3553162"
NOTE = (
    "GIS quality densify 2026-10-13 ~18:28 MSK gis-port150-1828: moved off soft 78.6567/16.3250 "
    "(settlement centre = WD Q845396 P625 78.656111/16.325; OSM place node/273476498) to OSM "
    "node/857534564 man_made=crane 78.654916/16.3553162 at the seaward end of the concrete quay "
    "road way/72761799 on the Billefjorden shore (~0.69 km ESE); Kystverket leading beacons "
    "Pyramiden Ovre ref 991900 (OSM node/5323958065 ~0.16 km N) and Pyramiden Nedre ref 991800 "
    "(OSM node/5323958066 ~0.31 km E); harbourmaps.com natural harbour 78.6528/16.3822 (~0.6 km E, "
    "anchorage); facility_site (quay crane, not a surveyed berth)"
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
        # Detect newline style
        nl = "\r\n" if "\r\n" in raw else "\n"
        has_trailing = raw.endswith("\n") or raw.endswith("\r\n")
        reader = csv.reader(io.StringIO(raw))
        rows = list(reader)
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
            if old_lat == NEW_LAT and old_lon == NEW_LON and "gis-port150-1828" in (row[17] or ""):
                print("already", rp)
                continue
            row[4] = NEW_LAT
            row[5] = NEW_LON
            src = row[17] or ""
            if "gis-port150-1828" not in src:
                row[17] = (src + " + " + NOTE) if src else NOTE
            row[18] = "92"
            row[19] = "2026-10-13"
            rows[i] = row
            hit = True
            print(f"row {old_lat}/{old_lon} -> {NEW_LAT}/{NEW_LON}", rp)
        if hit:
            shutil.copy2(rp, rp + ".bak-gis-port150-1828")
            buf = io.StringIO()
            writer = csv.writer(buf, lineterminator=nl)
            writer.writerows(rows)
            out = buf.getvalue()
            if not has_trailing and out.endswith(nl):
                out = out[: -len(nl)]
            open(rp, "w", encoding="utf-8", newline="").write(out)
            n += 1
            print("patched", rp)

ENTRY = (
    '            "ARC-PORT-150": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Pyramiden Port quay (Billefjorden, Spitsbergen): OSM node/857534564 man_made=crane 78.654916/16.3553162 at the seaward end of concrete embankment quay road way/72761799; Kystverket leading beacons Pyramiden Ovre ref 991900 (OSM node/5323958065 ~0.16 km N) and Pyramiden Nedre ref 991800 (OSM node/5323958066 ~0.31 km E); settlement WD Q845396 P625 78.656111/16.325 ~0.67 km W; was soft 78.6567/16.3250 settlement centre (~0.69 km); local OSM coastline coarse (gadm); facility_site quay crane, not a surveyed berth",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-171": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True) + glob.glob(
        r + "/build_atlas.py"
    ):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-150": {' in s:
            print("builder already has entry", rp)
            continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp)
            continue
        shutil.copy2(rp, rp + ".bak-gis-port150-1828")
        s = s.replace(ANCH, ENTRY + ANCH)
        open(rp, "w", encoding="utf-8").write(s)
        print("builder patched", rp)
print("csv files patched", n)
