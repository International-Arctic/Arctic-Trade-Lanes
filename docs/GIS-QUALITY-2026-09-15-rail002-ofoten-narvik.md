# GIS Quality — 2026-09-15 ~11:55 MSK

## Win
Densified **ARC-RAIL-002** (Ofoten Line / Iron Ore Line Malmbanan) off **ARC-CITY-020** Narvik city centroid.

| Field | Before | After |
|-------|--------|-------|
| lat,lon | 68.4385, 17.426 (~53 m from CITY-020) | 68.4415503, 17.4411132 |
| OSM | — | railway=station Narvik [node/5526332038](https://www.openstreetmap.org/node/5526332038) |
| Context | soft city pin | Ofotbanen / Malmbanan northern terminus station |

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py`; public+dist+Dataset aliases synced (static only — no SPA redeploy).
- `generated` `2026-09-15T08:58:21Z`, **1321** features / **156** ports / rail 14 / CRS EPSG:3996.
- Remaining `centroid_clone` (unchanged): PORT-034, PORT-069, PORT-153, SHIP-069.

## CI
`scripts/check-rail002-ofoten-narvik-densify.mjs` — locks RAIL-002 off CITY-020 on Narvik station OSM band.

## UM
Live bundle people/event pin filters present (`null_island` / `swapped_lat_lng` / `out_of_bounds`). No SPA redeploy.

Neutral OSM/Nominatim sourcing only.
