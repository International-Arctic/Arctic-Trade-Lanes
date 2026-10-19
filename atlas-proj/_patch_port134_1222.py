#!/usr/bin/env python3
"""gis-loop-1019-1222: densify ARC-PORT-134 Port of Argentia / Cooper Cove Marine Terminal onto OSM landuse=harbour terminal polygon.

Soft pin 47.2953/-53.9858 (4-decimal) sat ~0.21 km SW of the Argentia marine terminal, just outside the harbour lands.
OSM way/845500563 landuse=harbour (~4.0 ha, v1, along Waterfront Drive, bordering Cooper Cove OSM relation/13574863),
shoelace centroid 47.2968528/-53.9842123 (inside polygon). Corroboration: NL EA Reg. 2279 project summary (Oct 2023)
UTM 22N (NAD83) wharf-face start N5242739.41 E274633.14 = 47.299333/-53.981152 (~0.36 km NE of centroid, at the
polygon NE edge; extension of the existing fleet dock into Cooper Cove). No Wikidata port item (Argentia settlement
Q2860953 not reused). UN/LOCODE CANWP unchanged. position_quality=facility_site.
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-134"
TAG = "gis-loop-1019-1222"
NEW_LAT, NEW_LON = "47.2968528", "-53.9842123"
OLD = ("47.2953", "-53.9858")
NOTE = (
    "GIS quality densify 2026-10-19 ~12:22 MSK gis-loop-1019-1222: moved off soft 47.2953/-53.9858 "
    "(4-decimal; ~0.21 km SW of the Argentia marine terminal, just outside the harbour lands) to OSM "
    "way/845500563 landuse=harbour (~4.0 ha, Waterfront Drive, bordering Cooper Cove OSM relation/13574863) "
    "shoelace centroid 47.2968528/-53.9842123 (~0.21 km NE, bearing ~35 deg); corroborated by NL EA Reg. 2279 "
    "project summary Oct 2023 (UTM 22N wharf-face start N5242739.41 E274633.14 = 47.299333/-53.981152, ~0.36 km NE "
    "at the polygon NE edge, existing fleet dock extended into Cooper Cove); no Wikidata port item "
    "(Argentia settlement Q2860953 not reused); UN/LOCODE CANWP unchanged; "
    "facility_site terminal harbour lands, not a single berth"
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
    '            "ARC-PORT-134": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Port of Argentia marine terminal / Cooper Cove (Argentia Harbour, Placentia Bay, NL; UN/LOCODE CANWP): OSM way/845500563 landuse=harbour (~4.0 ha, Waterfront Drive, bordering Cooper Cove OSM relation/13574863), shoelace centroid 47.2968528/-53.9842123; NL EA Reg. 2279 (Oct 2023) Cooper Cove wharf-face start UTM 22N N5242739.41 E274633.14 = 47.299333/-53.981152 sits ~0.36 km NE at the polygon NE edge; soft 47.2953/-53.9858 was ~0.21 km SW just outside the harbour lands; no Wikidata port item (Argentia settlement Q2860953 not reused); facility_site terminal harbour lands, not a single berth",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-119": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True) + glob.glob(r + "/build_atlas.py"):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-134": {' in s:
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
