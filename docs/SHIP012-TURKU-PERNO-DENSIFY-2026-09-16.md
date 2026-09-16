# GIS densify — ARC-SHIP-012 Turku / Meyer Perno (2026-09-16 ~12:15 MSK)

Politically neutral OSINT only. Verifiable OSM industrial geometry; no invented offsets.

| ID | Name | Old soft-pin (WGS84) | New (WGS84) | OSM | Wikidata |
|----|------|---------------------|-------------|-----|----------|
| ARC-SHIP-012 | Turku Shipyard (Meyer Turku) | 60.4500, 22.2700 | 60.4563106, 22.1303761 | [way/32198547](https://www.openstreetmap.org/way/32198547) Pernon telakka `landuse=industrial` `industrial=shipyard` operator=Meyer Turku (Nominatim centroid) | [Q11887488](https://www.wikidata.org/wiki/Q11887488) Perno shipyard |

## Notes
- Soft-pin was Turku city-ish (22.27E); densify moves ~7.7 km W onto Perno/Telakkakatu shipyard polygon.
- Wikidata P625 ≈ 60.454407, 22.126118 corroborates Nominatim centroid.
- ARC-SHIP-009 Arctech Helsinki left alone (Hietalahti complex with SHIP-010).
- ARC-SHIP-011 Rauma still soft — Nominatim way/1418979404 is a named building without `industrial=shipyard` (later cycle).

## Still open / quarantine
- ARC-SHIP-069 Sevgiprorybflot — Murmansk city centroid (help wanted #34).
- ARC-PORT-034 Obskaya, ARC-PORT-069 Chevak — no pier/LNG OSM yet (help wanted #32).
- ARC-SHIP-002 Zvezda — Nominatim still empty for named industrial geometry.
- Wrangell PORT-086 / SHIP-051 planned-only skip.

## Atlas
- Rebuild on Zo: `python3 atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`
- Live static sync only (no App.tsx / SPA redeploy).
- CI: `scripts/check-ship012-turku-perno-densify.mjs`
