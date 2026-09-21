# GIS Quality Loop — 2026-09-21 ~13:37 MSK

## Win (ATL)
- Densified **ARC-SHIP-019** Seaspan Vancouver Shipyards off soft pin `49.2900,-123.1200` onto OSM **way/709281886** Nominatim centroid `49.3139099,-123.1070059`.
- OSM tags: `landuse=industrial` + **`industrial=shipyard`**, name Seaspan Vancouver Shipyard, operator Seaspan; Overpass center ~`49.3139001/-123.1054270`; addr 2 Pemberton Avenue, North Vancouver. No Wikidata P625 (OSM industrial=shipyard densify).
- Location label updated Vancouver → North Vancouver (yard sits in District of North Vancouver).

## Atlas
- Rebuilt via `ArcticTradeLanes.com/atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`; synced Dataset + public/dist/www/arctic-trade-lanes aliases (static only — no SPA redeploy / App.tsx).
- `generated` `2026-09-21T10:38:04Z`, 1321 features / 70 shipyards / 156 ports. CRS primary EPSG:3996.

## UM
- `filterPeoplePins` / `filterEventPins` smoke: see cycle log (client-side bad-geo filter kept; no SPA redeploy / i18n untouched).

## Quarantine unchanged
- PORT-034/069, SHIP-069, Ulstein #37, Zvezda, Wrangell.
- Softish shipyards 20→19.
- Remaining soft preferred next: Naval Group ARC-SHIP-015 (no ready industrial=shipyard yet); Far East/Asia soft pins (Sembcorp/Hyundai/Daewoo/Hudong/Wuchang/MHI/Kawasaki/Imabari); Ulstein ARC-SHIP-024 leave #37 unless OSM industrial=shipyard found.
- CI: `check-ship019-seaspan-densify.mjs`.
