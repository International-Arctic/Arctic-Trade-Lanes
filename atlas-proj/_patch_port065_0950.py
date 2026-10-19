#!/usr/bin/env python3
"""gis-loop-1019-0950: densify ARC-PORT-065 Port of Kokkola (Deep Port + Silverstone) onto the Deep Port basin.

Soft pin 63.8472/23.1133 (4-decimal) sat in Kokkola town east of the harbour (~1.3 km from ARC-CITY-071 Kokkola),
not on port infrastructure. The port is at Ykspihlaja ~4.5 km WNW.
Anchor = OSM relation/11003166 landuse=industrial industrial=port name=Kokkolan syvasatama (Deep Port)
operator=Kokkolan satama wikidata=Q10543787 website=portofkokkola.fi; net shoelace centroid (outer way/792462335
minus inner ways 506266877, 506266875; 0.43 km2) 63.865509/23.0312818, point-in-polygon verified.
Moved ~4.50 km WNW (bearing ~297 deg).
portofkokkola.fi/en/ports/silverstone-port: Silverstone Port shares the same basin with the Deep Port.
Corroboration: Wikidata Q10543787 Port of Kokkola (P1937 UN/LOCODE FIKOK) P625 63.844439/23.022219 is the
port-wide point on the General Port / Kokkolan kantasatama (OSM way/759190646, also wikidata=Q10543787), ~2.38 km SSW;
OSM way/519261340 Suurteollisuusalue (KIP industrial park, industrial=port) ~0.9 km S.
UN/LOCODE FIKOK unchanged (matches WD P1937). position_quality=facility_site (port-area polygon, not a surveyed berth).
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-065"
TAG = "gis-loop-1019-0950"
NEW_LAT, NEW_LON = "63.865509", "23.0312818"
NOTE = (
    "GIS quality densify 2026-10-19 ~09:50 MSK gis-loop-1019-0950: moved off soft 63.8472/23.1133 "
    "(4-decimal; Kokkola town east of the harbour, not port infrastructure) to OSM relation/11003166 "
    "landuse=industrial industrial=port Kokkolan syvasatama (Deep Port; operator Kokkolan satama; wikidata=Q10543787) "
    "net shoelace centroid 63.865509/23.0312818 (~4.50 km WNW, bearing ~297 deg); portofkokkola.fi: Silverstone Port "
    "shares the same basin with the Deep Port; Wikidata Q10543787 Port of Kokkola P1937 FIKOK P625 63.844439/23.022219 "
    "is the port-wide point on the General Port / Kokkolan kantasatama (OSM way/759190646) ~2.38 km SSW; "
    "UN/LOCODE FIKOK unchanged; facility_site (port-area polygon, not a surveyed berth)"
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
            if (old_lat, old_lon) != ("63.8472", "23.1133"):
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
    '            "ARC-PORT-065": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Port of Kokkola Deep Port + Silverstone (Ykspihlaja, Kokkola, Finland; UN/LOCODE FIKOK): OSM relation/11003166 landuse=industrial industrial=port Kokkolan syvasatama (operator Kokkolan satama, wikidata=Q10543787), net shoelace centroid 63.865509/23.0312818 (outer way/792462335 minus inner ways 506266877, 506266875); portofkokkola.fi: Silverstone Port shares the same basin with the Deep Port; Wikidata Q10543787 P625 63.844439/23.022219 (port-wide point on General Port / Kokkolan kantasatama OSM way/759190646) ~2.38 km SSW; soft 63.8472/23.1133 was ~4.50 km ESE in Kokkola town; facility_site port-area polygon, not a surveyed berth",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-093": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True) + glob.glob(r + "/build_atlas.py"):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-065": {' in s:
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
