# Port↔city centroid densify (batch 09:09 MSK) — 2026-09-09

## Problem
Forty-six operational harbour rows still shared a **4-dp WGS84 pin** with their parent city centroid after the 17:18 batch, so polar/Mercator atlas UX showed port + city as one stacked marker.

## Fixes (dataset)
Densified nine commercial harbours onto verifiable OSM Overpass harbour / ferry_terminal / industrial=port / pier nodes (User-Agent `ArcticTradeLanes-GIS-QualityLoop/1.0`), then rebuilt live atlas (static atlas publish only — no SPA redeploy).

| ID | Name | Old lat,lon | New lat,lon | OSM note |
|----|------|-------------|-------------|----------|
| `ARC-PORT-009` | Nuuk Port | 64.1814, -51.6941 | 64.1727800, -51.7225536 | harbour node/995384594 Port of Nuuk |
| `ARC-PORT-011` | Ilulissat Port | 69.2198, -51.0986 | 69.2241501, -51.0988283 | harbour node/13472302840 Iliuissat |
| `ARC-PORT-021` | Iqaluit Deep Sea Port | 63.7467, -68.5170 | 63.7230185, -68.5226163 | industrial=port way/1276081762 |
| `ARC-PORT-026` | Nome Harbor | 64.5011, -165.4064 | 64.4960224, -165.4376724 | pier way/336012429 |
| `ARC-PORT-057` | Torshavn Port | 62.0094, -6.7717 | 62.0084594, -6.7674851 | ferry_terminal node/596797404 |
| `ARC-PORT-062` | Aasiaat Port | 68.7067, -52.8694 | 68.7088992, -52.8732373 | harbour way/659589430 |
| `ARC-PORT-077` | Ísafjörður Harbour | 66.0745, -23.1150 | 66.0708207, -23.1241308 | harbour node/1852758904 |
| `ARC-PORT-163` | Klaksvík Harbour (Norðhavnin) | 62.2335, -6.5930 | 62.2530714, -6.5815773 | industrial=port way/1054234898 Norðhavnin |
| `ARC-PORT-172` | Kristiansand Port | 58.1467, 7.9956 | 58.1436937, 7.9883855 | harbour node/689452567 Vestre havn |

## Live
- https://arctictradelanes.com / https://www.arctictradelanes.com `/atlas.geojson` + `/atlas.manifest.json`
- ports **156**, features **1321**, `generated` `2026-09-09T06:10:42Z`, `crs_primary` 3996 / atlas.4326 stamps EPSG:4326
- Remaining exact port↔city stacks after this batch: **37**
- CI: `node scripts/check-port-city-centroid-densify-0909.mjs [atlas.4326.geojson]`

Politically neutral OSINT hygiene — no editorial layer changes, no SPA redeploy, commercial rails untouched.
