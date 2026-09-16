# GIS densify — ARC-SHIP-006 Sredne-Nevsky Shipyard (2026-09-16 ~10:36 MSK)

Politically neutral OSINT only. Verifiable OSM industrial geometry; no invented offsets; not conflated with Severnaya Verf.

| ID | Name | Old soft-pin (WGS84) | New (WGS84) | OSM | Wikidata |
|----|------|---------------------|-------------|-----|----------|
| ARC-SHIP-006 | Sredne-Nevsky Shipyard | 59.8750, 30.2000 | 59.7884684, 30.6294525 | [relation/2830545](https://www.openstreetmap.org/relation/2830545) Средне-Невский судостроительный завод `landuse=industrial` `industrial=shipyard` (Nominatim centroid, Pontonny) | [Q4438482](https://www.wikidata.org/wiki/Q4438482) |

## Notes
- Soft-pin sat ~2 km west of densified **ARC-SHIP-003** Severnaya Verf ([relation/1411836](https://www.openstreetmap.org/relation/1411836)); real yard is downstream at Pontonny / Korchmino (~15 km SE).
- Official site cited in sources: https://snsz.ru/

## Still open
- ARC-SHIP-069 Sevgiprorybflot — Murmansk city centroid (help wanted #34).
- ARC-PORT-034 / 069 / 153 — no pier/LNG OSM yet (help wanted #32).

## Atlas
- Rebuild: `python3 atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`
- Live static sync only (no App.tsx / SPA redeploy).
- CI: `scripts/check-ship006-sredne-nevsky-densify.mjs`
