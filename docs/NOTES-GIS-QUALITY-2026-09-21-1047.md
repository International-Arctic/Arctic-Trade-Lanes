# GIS Quality Loop — 2026-09-21 ~10:47 MSK

## Win
- Densified **ARC-SHIP-074** Larsnes Mek. Verksted AS off soft pin `62.4500,6.0900` onto Wikidata Q52502362 P625 `62.203405,5.572472` (Larsnes/Sande, Møre og Romsdal).
- Official https://www.larsnes-mek.no/. Nominatim node/5778426043 Larsnesvegen 119 cross-check `62.2032300/5.5729820`. WD HQ densify (no OSM industrial=shipyard polygon).

## Atlas
- Rebuilt via `ArcticTradeLanes.com/atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`; synced Dataset + public/dist/www aliases (static only — no SPA redeploy / App.tsx).
- `generated` `2026-09-21T07:52:10Z`, 1321 features / 70 shipyards / 156 ports. CRS primary EPSG:3996.

## UM
- `filterPeoplePins` / `filterEventPins` smoke: accepted 4 dropped 6. No SPA redeploy.

## Quarantine unchanged
- PORT-034/069, SHIP-069, Ulstein #37, Zvezda, Wrangell.
- Remaining soft preferred queue: Kleven ARC-SHIP-026 62.35/6.15 (≠ ARC-SHIP-072 Green Yard Kleven); Arctech ARC-SHIP-009 60.17/24.94; Ulstein leave #37.
