# Port↔city centroid densify (batch 09:36 MSK) — 2026-09-14

## Problem
After the 09:14 NSR densify, **25** harbour rows still shared an exact WGS84 pin with their parent city centroid. Separately, live `/atlas.geojson` stayed frozen at `generated` `2026-09-08T14:32:36Z` because `build_atlas.py` wrote `atlas.wgs84.geojson` / `atlas.4326.geojson` / `atlas.3996.geojson` but **not** the bare `atlas.geojson` alias the SPA + CF proxy fetch.

## Fixes (dataset)
Densified **two** harbours onto verifiable OSM Overpass `man_made=pier` ways (User-Agent `ArcticTradeLanes-GIS-QualityLoop/1.0`), then rebuilt + published static atlas (no App.tsx smash / no SPA redeploy).

| ID | Name | Old lat,lon | New lat,lon | OSM note |
|----|------|-------------|-------------|----------|
| `ARC-PORT-006` | Tiksi Sea Port | 71.6400, 128.8600 | 71.6453769, 128.8907265 | pier way/1081390289 Портовый флот |
| `ARC-PORT-144` | Ny-Ålesund / Kings Bay Arctic Research Port | 78.9167, 11.9333 | 78.9280349, 11.9358348 | pier way/588897062 |

## Builder hygiene
Zo `atlas-proj/build_atlas.py` now also emits `atlas.geojson` as a byte alias of the WGS84 FeatureCollection so `/atlas.geojson` cannot lag the stamped CRS files.

## Live
- https://arctictradelanes.com / https://www.arctictradelanes.com `/atlas.geojson` (+ `/data/atlas.geojson`, `/atlas.wgs84.geojson`, `/atlas.4326.geojson`, `/atlas.3996.geojson`)
- ports **156**, features **1321**, `generated` `2026-09-14T06:45:18Z`
- Remaining exact port↔city stacks after this batch: **23**
- CI: `node scripts/check-port-city-centroid-densify-0936.mjs [atlas.4326.geojson]`

UM: `filterPeoplePins` / `filterEventPins` smoke OK (null-island / OOB-as-swap / dedupe) — no SPA redeploy.

Politically neutral OSINT hygiene — no editorial layer changes, commercial rails (x402) untouched.
