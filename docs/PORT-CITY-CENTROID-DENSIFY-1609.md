# Port↔city centroid densify (batch 16:09 MSK) — 2026-09-08

## Problem
Sixty operational harbour rows still shared a **3-dp WGS84 pin** with their parent city centroid, so polar/Mercator atlas UX showed port + city as one stacked marker.

## Fixes (dataset)
Densified six harbours onto verifiable OSM Nominatim nodes (User-Agent `ArcticTradeLanes-GIS-QualityLoop/1.0`), then rebuilt live atlas (no SPA redeploy).

| ID | Name | New lat,lon | OSM note |
|----|------|-------------|----------|
| `ARC-PORT-010` | Sisimiut Port | 66.9400725, -53.6749927 | Umiarsualivik/Havn (harbour-area stop) |
| `ARC-PORT-013` | Akureyri Port | 65.6851709, -18.0790671 | Oddeyrarbryggja pier street |
| `ARC-PORT-020` | Churchill Port | 58.7759414, -94.1944813 | Port of Churchill industrial |
| `ARC-PORT-023` | Valdez Marine Terminal | 61.0831733, -146.3817280 | Valdez Marine Terminal industrial |
| `ARC-PORT-027` | Kemi Port | 65.6747392, 24.5852607 | Ajos harbour suburb (kept `ARC-PORT-146` on Kemin satama) |
| `ARC-PORT-054` | Raahe Port | 64.6585543, 24.4178846 | Raahen satama industrial |

## Live
- https://arctictradelanes.com / https://www.arctictradelanes.com `/data/atlas.manifest.json`
- ports **156**, features **1321**, `generated` `2026-09-08T13:24:12Z`, `crs_primary` 3996
- CI: `node scripts/check-port-city-centroid-densify-1609.mjs [atlas.4326.geojson]`

Politically neutral OSINT hygiene — no editorial layer changes, no SPA redeploy, commercial rails untouched.
