# GIS Quality Loop — 2026-09-28 ~14:16 MSK (gis-densify-1416)

## Outcome
- **Densified ARC-SHIP-021 Vigor Shipyard** off soft `47.6000,-122.3300` onto OSM **way/223565674** `building=yes` name="Vigor Ship Yard" (addr: 1801 16th Avenue Southwest, Seattle, WA 98134; Harbor Island). Nominatim centroid `47.5858778/-122.3572698`.
- Corroboration: official Vigor Marine Group facility page https://www.vigormarine.com/facilities/seattle + contact list same address; King County GIS / data.seattle.gov OSM source; WD **Q7928998** Vigor Marine Group corporate (no yard P625; P159 Portland).
- Soft→new ≈ **2.58 km** (city-center soft pin → Harbor Island yard footprint).
- Sibling DISTINCT: no other ARC-SHIP within 50 km (nearest Seaspan Vancouver ARC-SHIP-019 ~197 km).
- Tag `gis-densify-1416` (~14:16 MSK).
- Not touched this cycle: quarantine + ARC-PORT-164; soft ports Nuupiluk-127 / Indiga-128 / Ura Guba-148 / EMO-166 skip; remaining softish shipyards 022–023, 027, 029, 034, 039, 052; Hyundai-034 deferred; Vard-025 quarantine; Rosatom-075 planned empty.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-28T11:22:36Z**, **1321** features / **70** shipyards / **156** ports / **103** cities. CRS primary EPSG:3996.
- Synced Dataset atlas/data + site root/www/public/dist/data + arctic-trade-lanes dist/public (+ /atlas) + `/data/arctictradelanes/` + Zo space assets (static atlas only — **no SPA redeploy / App.tsx**). Restarted `svc_UpoHDo9rDHs`.
- Live target: https://arctictradelanes.com/atlas/atlas.manifest.json; ARC-SHIP-021 at [-122.357270, 47.585878].

## Remaining soft preferred
- Cities: _(empty preferred)_
- Ports: 127 Nuupiluk; 128 Indiga; 148 Ura Guba; 166 EMO (skip)
- Softish shipyards: 022–023, 027, 029, 034, 039, 052

## UM ($UM-Radar)
- `@international-arctic/geo-filter` **0.1.4** smoke left unchanged (no filter gap found).
