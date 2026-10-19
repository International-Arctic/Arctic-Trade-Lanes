#!/usr/bin/env python3
"""gis-loop-1019-1758: densify ARC-PORT-079 Reykjavik Vör Cruise Terminal (Skarfabakki 312, Viðeyjarsund; ISREK)
onto the Skarfabakki cruise quay in Sundahöfn.

Soft pin 64.1628/-21.8514 (4-decimal) sits on Viðey island (OSM relation/8385552 'Viðey', ~0.27 km NE of the Viðey
ferry landing node/4451609056), across Viðeyjarsund from the cruise quay - not port infrastructure.
Anchor: OSM way/108336302 highway=service access=no name=Skarfabakki (the 542 m quay-apron road along the Skarfabakki
berth face), length-weighted midpoint 64.1550151/-21.8620629 (~1.01 km SSW of soft).
Faxaports Port Information Guide: Skarfabakki 650 m / 12.0 m MLWS, cruise + general cargo + bulk + trawlers, ISPS;
Sundahöfn 64°09,1'N 021°51,0'W. Sibling ARC-PORT-066 (Vör terminal building OSM way/1391146178) ~0.15 km NW kept separate.
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-079"
TAG = "gis-loop-1019-1758"
NEW_LAT, NEW_LON = "64.1550151", "-21.8620629"
OLD = ("64.1628", "-21.8514")
CONF = "85"
NOTE = (
    "GIS quality densify 2026-10-19 ~17:58 MSK gis-loop-1019-1758: moved off soft 64.1628/-21.8514 (4-decimal pin on "
    "Viðey island, OSM relation/8385552, ~0.27 km NE of the Viðey ferry landing node/4451609056, across Viðeyjarsund from "
    "the cruise quay) to the Skarfabakki cruise quay in Sundahöfn: length-weighted midpoint of OSM way/108336302 "
    "highway=service access=no name=Skarfabakki (542 m quay-apron road along the berth face) at 64.1550151/-21.8620629 "
    "(~1.01 km SSW); Faxaports Port Information Guide (datocms-assets.com/164301/1788441122-port-information-guide-"
    "faxafloahafnir.pdf): Skarfabakki 650 m length, 12.0 m depth MLWS, cruise/general cargo/bulk/trawlers, ISPS; "
    "iceland-highlights.com: Skarfabakki 312 = main cruise berth with the Vör terminal; sibling ARC-PORT-066 (Vör "
    "terminal building OSM way/1391146178) ~0.15 km NW kept separate (near-duplicate entity); facility_site quay point, "
    "not a surveyed berth line; row max_depth left unchanged"
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
    '            "ARC-PORT-079": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Skarfabakki cruise quay, Sundahöfn, Reykjavík (Skarfabakki 312 main cruise berth with the Vör terminal; UN/LOCODE ISREK): length-weighted midpoint of OSM way/108336302 highway=service access=no name=Skarfabakki (542 m quay-apron road along the berth face) at 64.1550151/-21.8620629; Faxaports Port Information Guide: Skarfabakki 650 m, 12.0 m MLWS, cruise/general cargo/bulk/trawlers, ISPS; soft 64.1628/-21.8514 was on Viðey island (OSM relation/8385552, ~1.01 km NNE); sibling ARC-PORT-066 Vör terminal building way/1391146178 ~0.15 km NW; facility_site",\n'
    '            },\n'
)
ANCH = '            "ARC-PORT-132": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-079": {' in s:
            print("builder already has entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp); continue
        shutil.copy2(rp, rp + ".bak-" + TAG)
        open(rp, "w", encoding="utf-8").write(s.replace(ANCH, ENTRY + ANCH))
        print("builder patched", rp)
print("csv files patched", n)
