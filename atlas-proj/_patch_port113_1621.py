#!/usr/bin/env python3
"""gis-loop-1019-1621: densify ARC-PORT-113 Don Young Port of Alaska Cargo Terminal 1 (PAMP Phase 2B, USANC)
onto the Matson/T1 (southern) half of the Port of Alaska cargo pier.

Soft pin 61.2447/-149.8817 (4-decimal) is the OSM relation/10511522 Port of Alaska industrial-yard
centroid (61.2446867/-149.8816953), ~0.52 km NE of parent ARC-PORT-025 pier-wide centroid and adjacent
to the TOTE/T2 (northern) end. PAMP Phase 2B Terminal 1 is the Matson berth (south); Terminal 2 is TOTE.
New T1 wharf is unbuilt (~140 ft seaward of existing, completion ~2029) — facility_site on existing T1 pier.

Anchor: shoelace centroid of the southern half of OSM man_made=pier area=yes way/28577877
(nodes with lat <= mid-lat of pier bbox 61.2375677..61.2441116) at 61.2389299/-149.8885158
(~0.74 km SSW of soft; ~0.22 km SSW of parent ARC-PORT-025 61.2408396/-149.8872591).
Corroboration: Matson Navigation Company OSM node/5900610301 61.2381337/-149.8843209 (~0.24 km E);
Port of Anchorage waterway=dock node/5071860424 + Wikidata Q3398440; portofalaska.com PAMP Phase 2B
(T1 Matson / T2 TOTE).
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-113"
TAG = "gis-loop-1019-1621"
NEW_LAT, NEW_LON = "61.2389299", "-149.8885158"
OLD = ("61.2447", "-149.8817")
CONF = "93"
NOTE = (
    "GIS quality densify 2026-10-19 ~16:21 MSK gis-loop-1019-1621: moved off soft 61.2447/-149.8817 "
    "(4-decimal = OSM relation/10511522 Port of Alaska landuse=industrial yard centroid 61.2446867/-149.8816953, "
    "~0.52 km NE of parent ARC-PORT-025 pier centroid and on the TOTE/T2 northern end) to the Matson/Terminal 1 "
    "(southern) half of the continuous Port of Alaska cargo pier: shoelace centroid of southern-half nodes "
    "(lat <= mid-lat) of OSM man_made=pier area=yes way/28577877 at 61.2389299/-149.8885158 (~0.74 km SSW); "
    "parent ARC-PORT-025 remains at pier-wide centroid 61.2408396/-149.8872591 (~0.22 km NNE); "
    "Matson Navigation Company OSM node/5900610301 61.2381337/-149.8843209 ~0.24 km E; "
    "PAMP Phase 2B (portofalaska.com): T1=Matson berth, T2=TOTE berth; new T1 wharf unbuilt "
    "(~140 ft seaward, completion ~2029) so anchor is the existing T1 pier being replaced; "
    "Wikidata Q3398440 Port of Alaska; facility_site"
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
    '            "ARC-PORT-113": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Don Young Port of Alaska Cargo Terminal 1 / Matson berth (PAMP Phase 2B; UN/LOCODE USANC): shoelace centroid of southern half (lat <= mid-lat) of OSM man_made=pier area=yes way/28577877 at 61.2389299/-149.8885158; parent ARC-PORT-025 pier-wide centroid 61.2408396/-149.8872591 ~0.22 km NNE kept separate; Matson Navigation Company OSM node/5900610301 ~0.24 km E; soft 61.2447/-149.8817 was OSM relation/10511522 yard centroid on the TOTE/T2 northern end (~0.74 km NNE); new T1 wharf unbuilt (~140 ft seaward, ~2029); Wikidata Q3398440; facility_site",\n'
    '            },\n'
)
# Insert before ARC-PORT-107 block (keep newest densifies near top of schematic dict)
ANCH = '            "ARC-PORT-107": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-113": {' in s and '61.2389299' in s:
            print("builder already has entry", rp); continue
        # If old soft-only mention exists without entry, just add entry
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp); continue
        shutil.copy2(rp, rp + ".bak-" + TAG)
        # Remove any prior ARC-PORT-113 schematic entry if present with different coords
        import re
        s2 = re.sub(
            r'            "ARC-PORT-113": \{.*?\n            \},\n',
            '',
            s,
            count=1,
            flags=re.S,
        )
        if '"ARC-PORT-113": {' in s2:
            print("could not clear old 113 entry", rp); continue
        open(rp, "w", encoding="utf-8").write(s2.replace(ANCH, ENTRY + ANCH))
        print("builder patched", rp)
print("csv files patched", n)
