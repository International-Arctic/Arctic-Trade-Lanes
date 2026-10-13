#!/usr/bin/env python3
"""gis-port099-1424: densify ARC-PORT-099 Pevek Cape Nagleynyn Marine Terminal onto the mapped terminal site.

Soft pin 69.7200/170.2000 sat in Pevek Strait water off Pevek town, ~82 km NE of the real site
(old sources note said "Cape Nagleynyn adjacent NW of existing Pevek quays" - wrong).
government.ru/news/48261 (RF govt order): Pevek seaport borders extended by land + water "u mysa Nagleynyn"
for the Baimskaya GOK terminal (~2 Mt/yr); gge.ru (Glavgosexpertiza): terminal "u mysa Nagleynyn v zalive
Chaunskaya Guba", 275 m berth, approach channel sited for the shortest run from Chaun Bay to the cape.
Cape = OSM node/9513605008 natural=cape 69.0792927/169.3310737 (Wikidata Q37885662 cape P625 69.0772/169.3269, ~0.28 km).
Anchor = OSM way/1514011213 landuse=industrial "Naglyoygnyn Port" (mys Nagleygnyn port; Sentinel-2-mapped,
changeset 182704371, 2026-05-15) vertex centroid 69.0382643/169.3878168 (~5 km SSE of the cape); same changeset maps
pier way/1514011280 (~1.0 km E), breakwaters way/1514011278/1514011279 and fuel depot way/1514011277.
Terminal under construction: position_quality=facility_site.
"""
import glob, os, shutil, sys

PID = "ARC-PORT-099"
OLD_LL = ",Russia,69.7200,170.2000,"
NEW_LL = ",Russia,69.0382643,169.3878168,"
NOTE = (
    "; GIS quality densify 2026-10-13 ~14:24 MSK gis-port099-1424: CORRECTION - the terminal is NOT next to the Pevek quays; "
    "moved off soft 69.7200/170.2000 (Pevek Strait water ~82 km NE) to OSM way/1514011213 Naglyoygnyn Port (landuse=industrial, "
    "Sentinel-2-mapped changeset 182704371) centroid 69.0382643/169.3878168 on the Chaunskaya Guba shore; "
    "government.ru/news/48261 (Pevek port borders extended at Cape Nagleynyn) + gge.ru Glavgosexpertiza (terminal at Cape Nagleynyn in Chaunskaya Guba bay); "
    "cape OSM node/9513605008 69.0792927/169.3310737 = Wikidata Q37885662 (~5 km NNW); pier way/1514011280 ~1.0 km E; under construction - facility_site"
)
OLD_TAIL = 'coords approx: Cape Nagleynyn adjacent NW of existing Pevek quays in Chaunskaya Bay",90,2026-08-23'
NEW_TAIL = 'coords approx: Cape Nagleynyn adjacent NW of existing Pevek quays in Chaunskaya Bay' + NOTE + '",90,2026-10-13'
assert '"' not in NOTE

roots = sys.argv[1:] or ["."]
seen = set(); n = 0
for r in roots:
    for p in glob.glob(r + "/**/ports.csv", recursive=True):
        rp = os.path.realpath(p)
        if rp in seen or "node_modules" in rp or "_bak" in rp or ".bak" in rp:
            continue
        seen.add(rp)
        raw = open(rp, encoding="utf-8", newline="").read()
        lines = raw.split("\n")
        hit = False
        for i, l in enumerate(lines):
            cr = l.endswith("\r")
            body = l[:-1] if cr else l
            if body.startswith(PID + ",") and OLD_LL in body and body.endswith(OLD_TAIL):
                lines[i] = body.replace(OLD_LL, NEW_LL).removesuffix(OLD_TAIL) + NEW_TAIL + ("\r" if cr else "")
                hit = True
        if hit:
            shutil.copy2(rp, rp + ".bak-gis-port099-1424")
            open(rp, "w", encoding="utf-8", newline="").write("\n".join(lines))
            n += 1; print("patched", rp)
        elif any(l.startswith(PID + ",") for l in lines):
            row = next(l for l in lines if l.startswith(PID + ","))
            print("SKIP (row differs)", rp, repr(row[-90:]))

ENTRY = (
    '            "ARC-PORT-099": {\n'
    '                "position_quality": "facility_site",\n'
    '                "position_note": "Baimskaya GOK marine terminal of Pevek seaport at Cape Nagleynyn, Chaunskaya Guba (RF govt order government.ru/news/48261 extended Pevek port borders there; Glavgosexpertiza gge.ru: 275 m berth, approach channel from Chaun Bay); anchor OSM way/1514011213 Naglyoygnyn Port landuse=industrial (Sentinel-2-mapped) centroid 69.0382643/169.3878168; cape OSM node/9513605008 = Wikidata Q37885662 ~5 km NNW; pier way/1514011280 ~1.0 km E; was soft 69.7200/170.2000 in Pevek Strait (~82 km NE); under construction - facility_site not a surveyed berth",\n'
    "            },\n"
)
ANCH = '            "ARC-PORT-136": {\n'
for r in roots:
    for path in glob.glob(r + "/**/atlas-proj/build_atlas.py", recursive=True) + glob.glob(r + "/build_atlas.py"):
        rp = os.path.realpath(path)
        if rp in seen or "node_modules" in rp:
            continue
        seen.add(rp)
        s = open(rp, encoding="utf-8").read()
        if '"ARC-PORT-099": {' in s:
            print("builder already has entry", rp); continue
        if s.count(ANCH) != 1:
            print("builder anchor missing", rp); continue
        shutil.copy2(rp, rp + ".bak-gis-port099-1424")
        s = s.replace(ANCH, ENTRY + ANCH)
        open(rp, "w", encoding="utf-8").write(s)
        print("builder patched", rp)
print("csv files patched", n)
