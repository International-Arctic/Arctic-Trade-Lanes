#!/usr/bin/env python3
"""gis-loop-1019-0913: densify ARC-PORT-039 Rankin Inlet Port onto the Itivia barge dock.

Soft pin 62.8094/-92.0853 (4-decimal) sat on the hamlet core (Rankin Inlet town node 107351556 is ~0.7 km S;
Kivalliq Inuit Association ARC-PROG-405 ~0.2 km N), not on water-side port infrastructure.
Anchor = OSM way/1537457615 man_made=pier area=yes floating=no surface=concrete (Itivia barge dock / sealift
landing, mapped 2026-07-11) shoelace centroid 62.7990461/-92.0920014 (~1.20 km SSW, bearing ~196 deg).
Corroboration: OSM way/1537459872 landuse=harbour industrial=port (Itivia harbour yard) centroid
62.8009827/-92.0959941 (~0.30 km NW); Agnico Eagle Itivia Project (aemnunavut.ca: Itivia Harbour laydown,
fuel farm, 6 km bypass to Meliadine) with OSM storage tanks way/762095264, way/762095265 (~0.38 km W);
rankininlet.ca tourism: barge dock and FOL at Itivia; Wikimapia 5549311 Itivia 62.79944/-92.09000 (~0.11 km);
Nunatsiaq/pentictonherald 2022: new boat launch ~152 m from the Itivia barge where sealift and Agnico offload.
Distinct from the Johnston Cove small craft harbour (OSM way/514257325 landuse=harbour, ~1.80 km NE).
No Wikidata harbour item (hamlet Q1021766 not reused). UN/LOCODE CARAN left unchanged (not re-verified).
position_quality=facility_site (pier outline, not a surveyed berth).
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-039"
TAG = "gis-loop-1019-0913"
NEW_LAT, NEW_LON = "62.7990461", "-92.0920014"
NOTE = (
    "GIS quality densify 2026-10-19 ~09:13 MSK gis-loop-1019-0913: moved off soft 62.8094/-92.0853 "
    "(4-decimal; hamlet core, not port infrastructure) to OSM way/1537457615 man_made=pier concrete "
    "Itivia barge dock / sealift landing shoelace centroid 62.7990461/-92.0920014 (~1.20 km SSW, bearing "
    "~196 deg); OSM way/1537459872 landuse=harbour industrial=port Itivia harbour yard ~0.30 km NW; "
    "Agnico Eagle Itivia Project (aemnunavut.ca: Itivia Harbour laydown + fuel farm + bypass road to "
    "Meliadine) with OSM tanks way/762095264 way/762095265 ~0.38 km W; rankininlet.ca barge dock and FOL "
    "at Itivia; Wikimapia 5549311 Itivia 62.79944/-92.09000 ~0.11 km; distinct from Johnston Cove small "
    "craft harbour (OSM way/514257325 ~1.80 km NE); no Wikidata harbour item (hamlet Q1021766 not reused); "
    "UN/LOCODE CARAN unchanged; facility_site (pier outline mapped 2026, not a surveyed berth)"
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
    '            "ARC-PORT-039": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Rankin Inlet Port / Itivia barge dock (Kangiqiniq, Kivalliq, Nunavut; UN/LOCODE CARAN): OSM way/1537457615 man_made=pier area=yes concrete Itivia barge dock / sealift landing, shoelace centroid 62.7990461/-92.0920014 (mapped 2026); OSM way/1537459872 landuse=harbour industrial=port Itivia harbour yard ~0.30 km NW; Agnico Eagle Itivia Project laydown + fuel farm (OSM tanks way/762095264, way/762095265 ~0.38 km W) serving Meliadine; rankininlet.ca barge dock and FOL at Itivia; Wikimapia 5549311 Itivia ~0.11 km; no Wikidata harbour item (hamlet Q1021766 not reused); soft 62.8094/-92.0853 was ~1.20 km NNE on the hamlet core; distinct from Johnston Cove small craft harbour (OSM way/514257325 ~1.80 km NE); facility_site pier outline, not a surveyed berth",\n'
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
        if '"ARC-PORT-039": {' in s:
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
