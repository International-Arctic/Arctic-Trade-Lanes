# GIS Quality Loop — 2026-09-21 ~15:37 MSK

## Win (ATL)
- Densified **ARC-SHIP-042** Imabari Shipbuilding (Arctic) off soft pin `34.0700,133.0000` onto OSM **way/879275271** Nominatim centroid `34.1100581,132.9723741`.
- OSM tags: `landuse=industrial` + **`industrial=shipyard`**, name `今治造船株式会社` / Imabari Shipbuilding Co., Ltd.; Overpass center ~`34.1103155/132.9721501`; WD **Q120836304** Imabari Shipyard (no P625); company **Q8207464** P159→Imabari city secondary.
- Location label updated Imabari → Imabari (Hashihama).

## Skips this loop
- Naval Group ARC-SHIP-015 / Issue #43: still blocked (Arsenal `military=naval_base` only).
- Ulstein ARC-SHIP-024 / Issue #37: leave alone.
- Sembcorp ARC-SHIP-033: Tuas yard `landuse=industrial` only (no `industrial=shipyard`) — skip.
- Hyundai ARC-SHIP-034 soft: Nominatim empty near soft; ARC-SHIP-058 already densified HD Hyundai Ulsan — avoid duplicate.
- Kawasaki / Hudong / Wuchang: no verified `industrial=shipyard` Nominatim hit this cycle.

## Atlas
- Rebuilt via `ArcticTradeLanes.com/atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`; synced Dataset + public/dist/www/arctic-trade-lanes aliases (static only — no SPA redeploy / App.tsx).
- Softish shipyards 17→16.
- CI: `check-ship042-imabari-densify.mjs`.

## Quarantine unchanged
- PORT-034/069, SHIP-069, Ulstein #37, Zvezda, Wrangell.
