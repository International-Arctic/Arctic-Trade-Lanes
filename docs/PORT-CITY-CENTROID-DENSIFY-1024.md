# Port↔city centroid densify (batch 10:24 MSK) — 2026-09-14

## Problem
After the 09:36 densify (Tiksi + Ny-Ålesund), **23** harbour rows still shared an exact WGS84 pin with their parent city centroid.

## Fixes (dataset)
Densified **four** harbours onto verifiable OSM Overpass pier/ferry-terminal geometries (User-Agent `ArcticTradeLanes-GIS-QualityLoop/1.0`), then rebuilt + published static atlas (no App.tsx smash / no SPA redeploy).

| ID | Name | Old lat,lon | New lat,lon | OSM note |
|----|------|-------------|-------------|----------|
| `ARC-PORT-149` | Barentsburg Port (Arktikugol) | 78.0667, 14.2167 | 78.0621120, 14.2026026 | pier way/741977198 coal-loading berth |
| `ARC-PORT-033` | Salekhard River Port | 66.5308, 66.6019 | 66.5228621, 66.6011381 | ferry_terminal node/8611184008 |
| `ARC-PORT-137` | Utrenniy LNG Export Terminal (Arctic LNG 2) | 71.0010, 73.7960 | 71.0093732, 73.7891686 | pier way/651001100 (+ ferry_terminal «причал Арктик СПГ-2») |
| `ARC-PORT-155` | Vopnafjörður Deep-Water Port | 65.746, -14.780 | 65.7555718, -14.8223849 | pier way/220753596 Löndunarbryggja |

Skipped this cycle (no distinct OSM harbour within search radius / planned-only): Utqiagvik, Kangerlussuaq, Steensby, Ittoqqortoormiit, Grays Bay, Cape Blossom.

## Live
- https://arctictradelanes.com / https://www.arctictradelanes.com `/atlas.geojson` (+ `/data/atlas.geojson`, `/atlas.wgs84.geojson`, `/atlas.4326.geojson`, `/atlas.3996.geojson`)
- ports **156**, features **1321**, `generated` `2026-09-14T07:35:58Z`
- Remaining exact port↔city stacks after this batch: **19**
- CI: `node scripts/check-port-city-centroid-densify-1024.mjs [atlas.4326.geojson]`

UM: people/events filter modules present; site HTTP 200 — no SPA redeploy.

Politically neutral OSINT hygiene — no editorial layer changes, commercial rails (x402) untouched.
