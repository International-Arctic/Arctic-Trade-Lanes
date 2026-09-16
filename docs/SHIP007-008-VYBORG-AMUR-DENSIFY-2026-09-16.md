# GIS densify — ARC-SHIP-008 Vyborg + ARC-SHIP-007 Amur (2026-09-16 ~11:35 MSK)

Politically neutral OSINT only. Verifiable OSM industrial geometries; no invented offsets.

| ID | Name | Old soft-pin (WGS84) | New (WGS84) | OSM | Wikidata |
|----|------|---------------------|-------------|-----|----------|
| ARC-SHIP-008 | Vyborg Shipyard | 60.7100, 28.7400 | 60.6962191, 28.7509727 | [relation/7738660](https://www.openstreetmap.org/relation/7738660) Выборгский судостроительный завод `landuse=industrial` `industrial=shipyard` (Nominatim centroid) | [Q4128552](https://www.wikidata.org/wiki/Q4128552) (P402→relation/7738660) |
| ARC-SHIP-007 | Amur Shipbuilding Plant | 50.5500, 137.0200 | 50.5440002, 137.0460195 | [relation/3482541](https://www.openstreetmap.org/relation/3482541) Амурский судостроительный завод `landuse=industrial` (Nominatim centroid) | [Q838929](https://www.wikidata.org/wiki/Q838929) |

## Notes
- Vyborg: Wikidata P402 confirms OSM relation/7738660; ~1.7 km SE of city soft-pin onto named shipyard industrial polygon.
- Amur: name-exact industrial relation in Komsomolsk-on-Amur; ~1.9 km E of prior soft-pin.
- Skipped this cycle: ARC-SHIP-002 Zvezda (no solid Nominatim industrial hit); Rauma/Turku deferred (Rauma hit is office/building-scale; Turku Meyer way available for a later cycle).

## Still open / quarantine
- ARC-SHIP-069 Sevgiprorybflot — Murmansk city centroid (help wanted #34).
- ARC-PORT-034 Obskaya, ARC-PORT-069 Chevak — no pier/LNG OSM yet (help wanted #32).
- Wrangell PORT-086 / SHIP-051 planned-only skip.

## Atlas
- Rebuild: `python3 atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`
- Live static sync only (no App.tsx / SPA redeploy).
- CI: `scripts/check-ship008-vyborg-densify.mjs`, `scripts/check-ship007-amur-densify.mjs`
