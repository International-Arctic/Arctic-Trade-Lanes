# GIS Quality Loop — 2026-09-21 ~14:48 MSK

## Win (ATL)
- Densified **ARC-SHIP-040** Mitsubishi Heavy Industries (Arctic) off soft pin `32.7500,129.8700` onto OSM **way/737747058** Nominatim centroid `32.7014777,129.8220234`.
- OSM tags: `landuse=industrial` + **`industrial=shipyard`**, name `三菱重工 長崎造船所 香焼工場` / MHI Nagasaki Shipyard Koyagi Plant; Overpass center ~`32.7014627/129.8229409`; WD **Q11357147** P625 ~`32.742194/129.858528` (main works secondary).
- Location label updated Nagasaki → Nagasaki (Koyagi).

## Skips this loop
- Naval Group ARC-SHIP-015 / Issue #43: still blocked (Arsenal `military=naval_base` only).
- Ulstein ARC-SHIP-024 / Issue #37: leave alone (quarantine preference).
- Sembcorp ARC-SHIP-033: prior loop — Tuas yard lacks `industrial=shipyard`.
- Hyundai ARC-SHIP-034 soft: no shipyard polygon near soft (ARC-SHIP-058 already densified).
- Kawasaki / Imabari / Hudong / Wuchang: Overpass timeouts or no verified `industrial=shipyard` near soft this cycle — next preferred.

## Atlas
- Rebuilt via `ArcticTradeLanes.com/atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`; synced Dataset + public/dist/www/arctic-trade-lanes aliases (static only — no SPA redeploy / App.tsx).
- `generated` `2026-09-21T11:51:43Z`, 1321 features / 70 shipyards / 156 ports. CRS primary EPSG:3996.

## UM
- `filterPeoplePins` / `filterEventPins` smoke: accepted 5 dropped 6 (null_island/dup/swapped/oob/missing). No SPA redeploy / i18n untouched.

## Quarantine unchanged
- PORT-034/069, SHIP-069, Ulstein #37, Zvezda, Wrangell.
- Softish shipyards 18→17.
- Remaining soft preferred next: Naval Group #43 (blocked); Sembcorp (needs shipyard tag); Hyundai soft; Hudong/Wuchang/Kawasaki/Imabari; Ulstein #37 leave alone.
- CI: `check-ship040-mhi-nagasaki-densify.mjs`.
