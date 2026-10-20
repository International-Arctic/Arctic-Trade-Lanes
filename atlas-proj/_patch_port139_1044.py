#!/usr/bin/env python3
"""gis-loop-1020-1044: pin ARC-PORT-139 Tromsø Havn to the Breivika cargo port (owner decision 2026-10-20).

Soft pin 69.6546/18.9590 (4-decimal) reverse-geocodes to St. Hanshaugen 5, Nordbyen, Tromsø (on land, city residential area).
Tromsø Havn (tromso.havn.no/tjenester/kaiplass, /en/services/quays) names Breivika its main cargo port area (Kai 20, 21-24,
24 nord, 25, 28, 38 nord; Ro-Ro ramp). The record names no single quay, so the pin goes to the Breivika harbour point from the
Norwegian Coastal Administration: OSM node/5355453054 harbour=yes seamark:type=harbour seamark:name=Tromsø source=Kystverket at
69.6757237/18.989445, in the harbour water off the ~450 m straight Breivika quay front (Kai 21-24, 410 m). ~2.6 km NNE.
Confidence 82 and other attributes unchanged. No Prostneset feature added (no distinct Prostneset record exists).
"""
import csv, glob, io, os, shutil, sys

PID = "ARC-PORT-139"
TAG = "gis-loop-1020-1044"
NEW_LAT, NEW_LON = "69.6757237", "18.9894450"
OLD = ("69.6546", "18.9590")
NOTE = (
    "GIS quality densify 2026-10-20 ~10:44 MSK gis-loop-1020-1044: moved off soft 69.6546/18.9590 (4-decimal pin on land at "
    "St. Hanshaugen, Nordbyen, Tromsø city) to the Breivika cargo port, which Tromsø Havn lists as its main cargo port area "
    "(tromso.havn.no quays: Kai 20, Kai 21-24 410 m 10.4-11.0 m, Kai 24 nord, Kai 25 11.5 m, Kai 28, Kai 38 nord, Ro-Ro ramp); "
    "pin = Norwegian Coastal Administration harbour point OSM node/5355453054 harbour=yes seamark:type=harbour seamark:name=Tromsø "
    "source=Kystverket at 69.6757237/18.989445 (~2.6 km NNE), in the harbour water off the Breivika quay front; facility_site "
    "harbour point, not a surveyed berth line; record names no single quay; confidence and other attributes left unchanged; "
    "the inner-harbour/Prostneset area remains covered by ARC-PORT-014"
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
    '            "ARC-PORT-139": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Tromsø Havn Breivika cargo port (UN/LOCODE NOTRO; Tromsø Havn main cargo area, Kai 20-25/28/38 nord): Kystverket harbour point OSM node/5355453054 harbour=yes seamark:type=harbour seamark:name=Tromsø source=Kystverket at 69.6757237/18.989445, in the harbour water off the Breivika quay front (Kai 21-24, 410 m); soft 69.6546/18.9590 was on land at St. Hanshaugen, Nordbyen (~2.6 km SSW); inner harbour covered by ARC-PORT-014; facility_site",\n'
    '            },\n'
)
ANCH = '            "ARC-PORT-135": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-139": {' in s:
            print("builder already has entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor missing/count", s.count(ANCH), rp); continue
        shutil.copy2(rp, rp + ".bak-" + TAG)
        open(rp, "w", encoding="utf-8").write(s.replace(ANCH, ENTRY + ANCH))
        print("builder patched", rp)
print("csv files patched", n)
