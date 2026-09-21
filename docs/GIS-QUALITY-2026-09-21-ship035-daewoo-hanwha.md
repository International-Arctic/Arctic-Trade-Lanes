# GIS Quality Loop — 2026-09-21 ~14:15 MSK

## Win (ATL)
- Densified **ARC-SHIP-035** Daewoo Shipbuilding (Arctic) / Hanwha Ocean Okpo off soft pin `34.8800,128.7200` onto OSM **way/398858956** Nominatim centroid `34.8759932,128.7044843`.
- OSM tags: `landuse=industrial` + **`industrial=shipyard`**, name `한화오션 옥포조선소` / `name:en=Hanwha Ocean` (ex-Daewoo/DSME); Overpass center ~`34.8760003/128.7085637`; WD **Q497860** P159 HQ qualifier P625 ~`34.874665/128.704147` (secondary).
- Location label updated Okpo → Geoje (Okpo) (yard sits in Geoje-si / 거제시).

## Naval Group ARC-SHIP-015 / Issue #43 — NOT densified
- Overpass bbox Cherbourg: only **CMN** way/22944118 has `industrial=shipyard` (different operator).
- Arsenal de Cherbourg way/984780191 is `landuse=military` + `military=naval_base` (not shipyard). WD Q3398673 P625 is Arsenal/naval base, not Naval Group commercial yard.
- Left soft `49.6400,-1.6200`; Issue #43 remains open (help wanted).

## Far East skips this loop
- Sembcorp ARC-SHIP-033: Nominatim way/1004233134 named Tuas Boulevard Yard `landuse=industrial` but **no** `industrial=shipyard` — deferred.
- Hyundai ARC-SHIP-034: no `industrial=shipyard` polygon in Overpass bbox around soft pin (ARC-SHIP-058 already densified HD Hyundai Ulsan).

## Atlas
- Rebuilt via `ArcticTradeLanes.com/atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`; synced Dataset + public/dist/www/arctic-trade-lanes aliases (static only — no SPA redeploy / App.tsx).
- `generated` `2026-09-21T11:14:34Z`, 1321 features / 70 shipyards / 156 ports. CRS primary EPSG:3996.

## UM
- `filterPeoplePins` / `filterEventPins` smoke: (see run). No SPA redeploy / i18n untouched.

## Quarantine unchanged
- PORT-034/069, SHIP-069, Ulstein #37, Zvezda, Wrangell.
- Softish shipyards 19→18.
- Remaining soft preferred next: Naval Group #43 (still no industrial=shipyard); Sembcorp (needs shipyard tag or P625 site); Hyundai soft; Hudong/Wuchang/MHI/Kawasaki/Imabari; Ulstein #37 leave alone unless OSM industrial=shipyard found.
- CI: `check-ship035-daewoo-hanwha-densify.mjs`.
