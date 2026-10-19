#!/usr/bin/env python3
"""gis-loop-1019-1018: densify ARC-PORT-066 Vör — Reykjavík Cruise Terminal onto OSM Vör building.

Soft pin 64.1680/-21.8520 (4-decimal) sat ~1.5 km NNE toward Viðey / Viðeyjarsund picnic/viewpoint
land, not on the Sundahöfn cruise quay. The Vör terminal building is mapped as OSM way/1391146178
building=transportation addr:housename=Vör addr:street=Skarfagarðar addr:housenumber=6 start_date=2026
(~3103 m² footprint), shoelace centroid 64.1557650/-21.8646994. Adjacent Skarfabakki quay service road
way/108336302 (~542 m) and ferry_terminal node/694173331 (ARC-PORT-012 Reykjavik Port, ~0.12 km NW)
are distinct. Wikidata Q16427805 Sundahöfn P625 64.1494/-21.8565 is the port-basin point ~0.81 km SE
(not reused as anchor). No dedicated Wikidata item for Vör yet. UN/LOCODE ISREY unchanged (same Faxaports
complex as ARC-PORT-012). position_quality=facility_site (building footprint, not a surveyed berth).
Near-duplicate ARC-PORT-079 (soft 64.1628/-21.8514, same Vör/Skarfabakki story) left untouched this cycle.
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-066"
TAG = "gis-loop-1019-1018"
NEW_LAT, NEW_LON = "64.1557650", "-21.8646994"
NOTE = (
    "GIS quality densify 2026-10-19 ~10:18 MSK gis-loop-1019-1018: moved off soft 64.1680/-21.8520 "
    "(4-decimal; ~1.49 km NNE toward Viðey / Viðeyjarsund, not on the Sundahöfn cruise quay) to OSM "
    "way/1391146178 building=transportation addr:housename=Vör addr:street=Skarfagarðar "
    "addr:housenumber=6 start_date=2026 shoelace centroid 64.1557650/-21.8646994 (~1.49 km SSW, "
    "bearing ~204 deg); Skarfabakki quay road way/108336302 (~542 m) adjacent; ARC-PORT-012 ferry_terminal "
    "node/694173331 ~0.12 km NW (distinct); Wikidata Q16427805 Sundahöfn P625 ~0.81 km SE not reused; "
    "UN/LOCODE ISREY unchanged; facility_site building footprint, not a surveyed berth"
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
            if (old_lat, old_lon) not in (("64.1680", "-21.8520"), ("64.168", "-21.852")):
                print("SKIP unexpected old coords", old_lat, old_lon, rp)
                continue
            row[4], row[5] = NEW_LAT, NEW_LON
            src = row[17] or ""
            if TAG not in src:
                row[17] = (src + " + " + NOTE) if src else NOTE
            row[18] = "95"
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
    '            "ARC-PORT-066": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Vör Reykjavík Cruise Terminal (Skarfabakki / Skarfagarðar, Sundahöfn, Viðeyjarsund; UN/LOCODE ISREY): OSM way/1391146178 building=transportation addr:housename=Vör addr:street=Skarfagarðar addr:housenumber=6 start_date=2026, shoelace centroid 64.1557650/-21.8646994 (~3103 m2 footprint); Skarfabakki quay service road way/108336302 (~542 m) adjacent; Faxaflóahafnir / Faxaports; ARC-PORT-012 Reykjavik Port ferry_terminal node/694173331 ~0.12 km NW (distinct); Wikidata Q16427805 Sundahöfn P625 64.1494/-21.8565 ~0.81 km SE not reused; no dedicated Vör Wikidata item yet; soft 64.1680/-21.8520 was ~1.49 km NNE toward Viðey; facility_site building footprint, not a surveyed berth",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-065": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True) + glob.glob(r + "/build_atlas.py"):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-066": {' in s:
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
