#!/usr/bin/env python3
"""gis-loop-1019-1352: densify ARC-PORT-159 Hadsel Havn KF onto Stokmarknes Nordnes / Hurtigruten terminal (NOSKN).

Soft pin 68.5648/15.2207 (4-decimal) sat ~12.56 km ESE of the real harbour — wrong longitude.
Anchor: OSM amenity=ferry_terminal node/75102834 Hurtigruten Stokmarknes with ref:LOCODE=NOSKN
at 68.5710140/14.9117250. Official Kystdatahuset/Allemannsdata NOSKN 68.57093/14.91198 ~14 m away.
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-159"
TAG = "gis-loop-1019-1352"
NEW_LAT, NEW_LON = "68.5710140", "14.9117250"
OLD = ("68.5648", "15.2207")
NOTE = (
    "GIS quality densify 2026-10-19 ~13:52 MSK gis-loop-1019-1352: moved off soft 68.5648/15.2207 "
    "(4-decimal pin ~12.56 km ESE of Stokmarknes harbour, wrong longitude toward Sortlandssundet) "
    "to Hadsel Havn KF Stokmarknes Nordnes / Hurtigruten terminal: OSM amenity=ferry_terminal "
    "node/75102834 Hurtigruten Stokmarknes with ref:LOCODE=NOSKN at 68.5710140/14.9117250 "
    "(~12.57 km WNW); corroborated by Kystdatahuset/Allemannsdata official NOSKN harbour "
    "68.57093/14.91198 (~14 m away) and secondary OSM ferry_terminal node/9512006003 "
    "Stokmarknes hurtigbatkai also ref:LOCODE=NOSKN; hadselhavn.no Nordnes kai I = Kystruten "
    "+ container/cargo; no Wikidata port item; Hadsel Havn KF also runs Melbu/Boroya/Miljohavn "
    "etc. (left as separate sites); facility_site Stokmarknes instrumental port, not a single berth"
)
assert '"' not in NOTE

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
            row[18] = "90"; row[19] = "2026-10-19"; rows[i] = row; hit = True
            print(f"row {old_lat}/{old_lon} -> {NEW_LAT}/{NEW_LON}", rp)
        if hit:
            shutil.copy2(rp, rp + ".bak-" + TAG)
            buf = io.StringIO(); csv.writer(buf, lineterminator=nl).writerows(rows)
            out = buf.getvalue()
            if not has_trailing and out.endswith(nl):
                out = out[: -len(nl)]
            open(rp, "w", encoding="utf-8", newline="").write(out); n += 1
ENTRY = (
    '            "ARC-PORT-159": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Hadsel Havn KF Stokmarknes Nordnes / Hurtigruten terminal (UN/LOCODE NOSKN): OSM amenity=ferry_terminal node/75102834 Hurtigruten Stokmarknes with ref:LOCODE=NOSKN at 68.5710140/14.9117250; Kystdatahuset/Allemannsdata official NOSKN harbour 68.57093/14.91198 ~14 m away; secondary OSM ferry_terminal node/9512006003 Stokmarknes hurtigbatkai also NOSKN; hadselhavn.no Nordnes kai I = Kystruten + container/cargo quay; soft 68.5648/15.2207 was ~12.56 km ESE on wrong longitude; no Wikidata port item; facility_site instrumental Stokmarknes port (Hadsel also operates Melbu/Boroya/Miljohavn as separate sites), not a single berth",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-158": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp: continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-159": {' in s:
            print("builder already has entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp); continue
        shutil.copy2(rp, rp + ".bak-" + TAG)
        open(rp, "w", encoding="utf-8").write(s.replace(ANCH, ENTRY + ANCH))
        print("builder patched", rp)
print("csv files patched", n)
