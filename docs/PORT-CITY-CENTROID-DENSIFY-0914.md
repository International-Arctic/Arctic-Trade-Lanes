# Port↔city centroid densify (batch 09:14 MSK) — 2026-09-14

## Problem
After the 09:09 densify, **28** operational harbour rows still shared an exact WGS84 pin with their parent `city_id` centroid, so polar atlas UX stacked port + city markers.

## Fixes (dataset)
Densified **three** commercial NSR harbours onto verifiable OSM Overpass `industrial=port` ways (User-Agent `ArcticTradeLanes-GIS-Quality/1.0`), then rebuilt live atlas (static atlas publish only — no SPA redeploy).

| ID | Name | Old lat,lon | New lat,lon | OSM note |
|----|------|-------------|-------------|----------|
| `ARC-PORT-004` | Sabetta LNG Terminal | 71.2560, 72.0520 | 71.2804697, 72.0611660 | industrial=port way/533105947 Порт Сабетта |
| `ARC-PORT-007` | Dikson Sea Port | 73.5070, 80.5460 | 73.5043654, 80.5151725 | industrial=port way/1080460349 |
| `ARC-PORT-008` | Khatanga River Port | 71.9800, 102.4700 | 71.9841653, 102.4753286 | industrial=port way/1080440778 |

## Live
- https://arctictradelanes.com / https://www.arctictradelanes.com `/atlas.geojson` + `/atlas.manifest.json`
- ports **156**, features **1321**, `generated` `2026-09-14T06:16:11Z`, `crs_primary` 3996 / atlas.4326 stamps EPSG:4326
- Remaining exact port↔city stacks after this batch: **25**
- CI: `node scripts/check-port-city-centroid-densify-0914.mjs [atlas.4326.geojson]`

UM: `filterPeoplePins` / `filterEventPins` smoke OK (null-island / OOB / swap / dedupe) — no SPA redeploy.

Politically neutral OSINT hygiene — no editorial layer changes, commercial rails untouched.
