#!/usr/bin/env python3
"""gis-loop-1019-1544: densify ARC-PORT-107 Juneau USCG Icebreaker Homeport Pier (CGC Storis, UN/LOCODE USJNU) onto the
existing Coast Guard Base/Station Juneau waterfront that the homeport recapitalization rebuilds (345 Egan Drive).

Soft pin 58.3019/-134.4197 (4-decimal) sat on the 17th CG District office (OSM node/8282072481, 709 W 9th St, Federal Building),
onshore ~0.57 km NW of the waterfront. Anchor: shoelace centroid of OSM man_made=pier landuse=military name=Coast Guard Wharf
way/891096273 (~3715 m2, name from NOAA chart 17315) at 58.2982001/-134.4128769 (~0.57 km SE).
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-107"
TAG = "gis-loop-1019-1544"
NEW_LAT, NEW_LON = "58.2982001", "-134.4128769"
OLD = ("58.3019", "-134.4197")
CONF = "92"
NOTE = 'GIS quality densify 2026-10-19 ~15:44 MSK gis-loop-1019-1544: moved off soft 58.3019/-134.4197 (4-decimal pin on the 17th Coast Guard District office OSM node/8282072481, 709 W 9th St Federal Building, onshore) to the USCG Base/Station Juneau waterfront at 345 Egan Drive that the Storis homeport recapitalization rebuilds: shoelace centroid of OSM man_made=pier landuse=military name=Coast Guard Wharf way/891096273 (~3715 m2 timber wharf; name from NOAA chart 17315) at 58.2982001/-134.4128769 (~0.57 km SE); adjacent OSM landuse=military seamark coastguard_station U.S. Coast Guard - Station Juneau way/891102519 (345 Egan Drive) ~40 m NE; NOAA/USCG SAM.gov sources-sought (design-build recapitalization of USCG Base Juneau waterfront at 345 Egan Drive, new wharf + floating pier, Storis + visiting cutter, USD 125-200M) + USCG Draft EA Cutter Homeporting Station Juneau (combined USCG + legacy NOAA timber wharves 655 ft) + KTOO 2026-07-01; new pier not yet built (completion ~2029), anchor is the existing wharf being replaced; no Wikidata item; facility_site'
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
                row[17] = (src + " + " + NOTE) if src else NOTE
            row[18] = CONF; row[19] = "2026-10-19"; rows[i] = row; hit = True
            print(f"row {old_lat}/{old_lon} -> {NEW_LAT}/{NEW_LON}", rp)
        if hit:
            shutil.copy2(rp, rp + ".bak-" + TAG)
            buf = io.StringIO(); csv.writer(buf, lineterminator=nl).writerows(rows)
            out = buf.getvalue()
            if not has_trailing and out.endswith(nl):
                out = out[: -len(nl)]
            open(rp, "w", encoding="utf-8", newline="").write(out); n += 1
ENTRY = '            "ARC-PORT-107": {\n                "position_quality": "facility_site",\n                "position_note": "USCG Base/Station Juneau waterfront (UN/LOCODE USJNU), 345 Egan Drive, site of the CGC Storis icebreaker homeport recapitalization (new wharf + floating pier, completion ~2029): shoelace centroid of OSM man_made=pier landuse=military Coast Guard Wharf way/891096273 (~3715 m2, NOAA chart 17315 name) at 58.2982001/-134.4128769; OSM Station Juneau way/891102519 ~40 m NE; NOAA/USCG SAM.gov sources-sought + USCG Draft EA (combined USCG + legacy NOAA timber wharves 655 ft); soft 58.3019/-134.4197 was ~0.57 km NW onshore on the 17th CG District office; facility_site",\n            },\n'
ANCH = '            "ARC-PORT-104": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp: continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-107": {' in s:
            print("builder already has entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp); continue
        shutil.copy2(rp, rp + ".bak-" + TAG)
        open(rp, "w", encoding="utf-8").write(s.replace(ANCH, ENTRY + ANCH))
        print("builder patched", rp)
print("csv files patched", n)
