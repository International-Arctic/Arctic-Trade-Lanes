# GIS Quality Loop — 2026-09-21 ~11:13 MSK

## Win
- Densified **ARC-SHIP-026** Kleven Verft off soft pin `62.3500,6.1500` onto Wikidata Q1774285 P159/P625 `62.32329874,5.84101439` (Ulsteinvik / Klubbenesvegen–Dimnasund).
- Cross-check OSM way/588997812 Kleven Maritime AS landuse=industrial ~62.3229687/5.8407574; way/390641698 Greenyard Kleven Maritime ~62.323057/5.8407145; Nominatim node/4839744354 Klubbenesvegen 39 `62.323089/5.837390`. No OSM industrial=shipyard tag (WD HQ densify).
- **Distinct from ARC-SHIP-072** Green Yard Kleven AS (untouched at `62.3442,5.8471`, ~2.3 km N).

## Atlas
- Rebuilt via `ArcticTradeLanes.com/atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`; synced Dataset + public/dist/www aliases (static only — no SPA redeploy / App.tsx).
- `generated` `2026-09-21T08:19:10Z`, 1321 features / 70 shipyards / 156 ports. CRS primary EPSG:3996.

## UM
- `filterPeoplePins` / `filterEventPins` smoke: accepted 4 dropped 6. No SPA redeploy.

## Quarantine unchanged
- PORT-034/069, SHIP-069, Ulstein #37, Zvezda, Wrangell.
- Softish shipyards 25→24.
- Remaining soft preferred queue: Arctech ARC-SHIP-009 60.17/24.94; Ulstein ARC-SHIP-024 leave #37 unless OSM industrial=shipyard found.
