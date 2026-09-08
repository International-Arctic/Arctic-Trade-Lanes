# Port↔city centroid densify (batch 17:18 MSK) — 2026-09-08

## Problem
Fifty-two operational harbour rows still shared a **3-dp WGS84 pin** with their parent city centroid after the 16:09 batch, so polar/Mercator atlas UX showed port + city as one stacked marker.

## Fixes (dataset)
Densified six harbours onto verifiable OSM Overpass harbour / ferry_terminal / industrial=port nodes (User-Agent `ArcticTradeLanes-GIS-QualityLoop/1.0`), then rebuilt live atlas (static atlas publish only — no SPA redeploy).

| ID | Name | Old lat,lon | New lat,lon | OSM note |
|----|------|-------------|-------------|----------|
| `ARC-PORT-070` | Maniitsoq Port (Atlantkaj) | 65.4151, -52.8999 | 65.4115420, -52.8992878 | harbour node/1938313089 Maniitsoq |
| `ARC-PORT-071` | Mehamn Fishing Port | 71.0358, 27.8511 | 71.0374618, 27.8422850 | harbour node/5355453058 |
| `ARC-PORT-072` | Oksfjord Fishing Port | 70.2392, 22.3499 | 70.2379430, 22.3496727 | ferry_terminal way/665781769 Loppa Havn KF |
| `ARC-PORT-095` | Kjøllefjord Fishing Harbour | 70.9458, 27.3464 | 70.9479126, 27.3353868 | harbour node/5355453097 |
| `ARC-PORT-098` | Port of Seward | 60.1128, -149.4425 | 60.1189282, -149.4278488 | harbour way/264719377 Seward Cruise Dock |
| `ARC-PORT-162` | Fuglafjørður Port | 62.2370, -6.8130 | 62.2410997, -6.8188386 | industrial=port way/1164163007 |

## Live
- https://arctictradelanes.com / https://www.arctictradelanes.com `/atlas.geojson` + `/atlas.manifest.json`
- ports **156**, features **1321**, `generated` `2026-09-08T14:32:36Z`, `crs_primary` 3996 / atlas.4326 stamps EPSG:4326
- Remaining exact port↔city stacks after this batch: **46**
- CI: `node scripts/check-port-city-centroid-densify-1718.mjs [atlas.4326.geojson]`

Politically neutral OSINT hygiene — no editorial layer changes, no SPA redeploy, commercial rails untouched.
