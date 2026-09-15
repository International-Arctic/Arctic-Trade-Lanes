# GIS Quality — 2026-09-15 ~11:06 MSK

## Win
Densified **ARC-RAIL-005** (North Bothnia Line / Norrbotniabanan) off **ARC-CITY-056** Umeå city centroid.

| Field | Before | After |
|-------|--------|-------|
| lat,lon | 63.8258, 20.2630 (= CITY-056) | 63.8718587, 20.2429322 |
| OSM | — | railway=construction Norrbotniabanan [way/973282865](https://www.openstreetmap.org/way/973282865) |
| Context | city pin | Umeå–Dåva first segment under construction (Trafikverket) |

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py` on Zo; Dataset + public aliases synced (static only — no SPA redeploy).
- `generated` `2026-09-15T08:13:19Z`, **1321** features / **156** ports / rail 14.
- Remaining `centroid_clone` (unchanged): PORT-034, PORT-069, PORT-153, SHIP-069 — no new verifiable harbour/pier OSM this cycle.

## CI
`scripts/check-rail005-norrbotniabanan-densify.mjs` — locks RAIL-005 off CITY-056 on Norrbotniabanan OSM band.

## UM
`check-people-event-pin-filter.mjs` smoke pass. No SPA redeploy.

Neutral OSM/Nominatim sourcing only.
