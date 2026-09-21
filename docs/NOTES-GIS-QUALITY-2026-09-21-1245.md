# GIS Quality Loop — 2026-09-21 ~12:45 MSK

## Win (ATL)
- Densified **ARC-SHIP-030** Damen Shiprepair Amsterdam off soft pin `52.3800,4.9000` onto OSM **way/693058619** Nominatim centroid `52.4069734,4.8837803`.
- OSM tags: `landuse=industrial` + **`industrial=shipyard`**, name Damen Shiprepair; polygon centroid ~`52.4075627/4.8826124`; website damen.com/shiprepair-amsterdam. No Wikidata P625 on the way (OSM industrial=shipyard densify).

## Atlas
- Rebuilt via `ArcticTradeLanes.com/atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`; synced Dataset + public/dist/www aliases (static only — no SPA redeploy / App.tsx).
- `generated` `2026-09-21T09:53:34Z`, 1321 features / 70 shipyards / 156 ports. CRS primary EPSG:3996.

## UM
- `filterPeoplePins` / `filterEventPins` smoke: accepted 5 dropped 6 (null_island/dup/swapped/oob/missing). No SPA redeploy / i18n untouched.

## Quarantine unchanged
- PORT-034/069, SHIP-069, Ulstein #37, Zvezda, Wrangell.
- Softish shipyards 24→23.
- Remaining soft preferred next: Sefine ARC-SHIP-045 (OSM way/1124414309 industrial=shipyard ready); Ulstein ARC-SHIP-024 leave #37 unless OSM industrial=shipyard found.
- CI: `check-ship030-damen-amsterdam-densify.mjs`.
