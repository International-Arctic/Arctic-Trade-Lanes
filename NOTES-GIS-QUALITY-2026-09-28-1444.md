# GIS Quality Loop — 2026-09-28 ~14:44 MSK (gis-densify-1444)

## Outcome
- **Densified ARC-SHIP-023 Eastern Shipbuilding** off soft `30.1600,-85.6600` onto OSM **way/1136084840** `industrial=shipyard` `landuse=industrial` (unnamed; sibling ways 1136084839/1136084841 same Nelson Street complex). Centroid `30.1423702/-85.6280760`.
- Corroboration: Nominatim reverse → 2500 Nelson Street, Millville, Panama City FL 32401; official Nelson Street Shipyard https://www.easternshipbuilding.com/who-we-are/facilities addr **2200 Nelson Street**, Panama City, FL 32401; WD **Q30687989** Eastern Shipbuilding Group corporate (no yard P625).
- Soft→new ≈ **3.64 km** (city-center soft pin → Nelson Street yard footprint).
- Sibling DISTINCT: no other ARC-SHIP within 50 km (nearest ARC-SHIP-068 Bollinger Mississippi ~281 km).
- Note: Allanton commercial yard (13300 Allanton Rd) has separate unnamed OSM shipyard way/1136084844 ~22 km SE — kept Nelson as soft-pin target (city waterfront / soft coords).
- Tag `gis-densify-1444` (~14:44 MSK).
- Not touched: quarantine + ARC-PORT-164; soft ports Nuupiluk-127 / Indiga-128 / Ura Guba-148 / EMO-166 skip; remaining softish shipyards 022, 027, 029, 034, 039, 052; Hyundai-034 deferred; Vard-025 quarantine; Rosatom-075 planned empty.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-28T11:58:09Z**, **1321** features / **70** shipyards / **156** ports / **103** cities. CRS primary EPSG:3996.
- Synced Dataset atlas/data + site root/www/public/dist/data + arctic-trade-lanes public/dist (+ /atlas) + `/data/arctictradelanes/` + Zo space assets (static atlas only — **no SPA redeploy / App.tsx**). Restarted `svc_UpoHDo9rDHs`.
- Live target: https://arctictradelanes.com/atlas/atlas.manifest.json; ARC-SHIP-023 at [-85.628076, 30.14237].

## Tried / deferred this cycle
- ARC-SHIP-022 VT Halter / Bollinger Mississippi: WD Q29093553 alias OK but **no named OSM shipyard** near Bayou Casotte (do not use Ingalls way/244343830 — wrong company). Address 900 Bayou Casotte geocodes road-only.
- ARC-SHIP-027/029/039/052: prior blockers unchanged (no/wrong OSM).

## Remaining soft preferred
- Cities: _(empty preferred)_
- Ports: 127 Nuupiluk; 128 Indiga; 148 Ura Guba; 166 EMO (skip)
- Softish shipyards: 022, 027, 029, 034, 039, 052

## UM ($UM-Radar)
- `@international-arctic/geo-filter` **0.1.4** left unchanged (no cheap client-side win).
