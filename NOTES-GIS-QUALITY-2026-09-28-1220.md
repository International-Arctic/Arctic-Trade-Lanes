# GIS Quality Loop — 2026-09-28 ~12:20 MSK (gis-densify-1220)

## Outcome
- **Densified ARC-SHIP-002 Zvezda Shipbuilding Complex** off soft `42.8200,132.3200` onto OSM **relation/10182135** Дальневосточный завод «Звезда» `landuse=industrial` multipolygon Nominatim centroid `43.1194759/132.3397981` (website https://www.fes-zvezda.ru/; OSM wikidata=Q4153364).
- Corroboration: Wikidata **Q120261208** Судостроительный комплекс «Звезда» P625 `43.12346111111111/132.3402138888889` (~0.44 km from OSM).
- Soft→new ≈ **33.34 km** (soft pin was ~33 km south of Bolshoy Kamen yard footprint).
- Sibling DISTINCT: no other ARC-SHIP within 50 km.
- Tag `gis-densify-1220` (~12:20 MSK).
- Preferred soft ports left soft (not re-litigated this cycle after 11:49 no-win): Nuupiluk-127 / Indiga-128 / Ura Guba-148 / EMO-166 (skip).
- Softish shipyards remaining blocked: Vigor-021, VT Halter-022, Eastern-023, Greenland-027, Northern Marine-029, Sembcorp-033, Hyundai-034, Wuchang-039, Kolskaya-052, Zhatay-076 (+ Vard-025 quarantine, Rosatom-075 planned empty). Quarantine + ARC-PORT-164 untouched.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-28T09:25:13Z**, **1321** features / **70** shipyards / **156** ports / **103** cities. CRS primary EPSG:3996.
- Synced Dataset atlas/data + site root/www/public/dist/data + arctic-trade-lanes mirrors + `/data/arctictradelanes/` (static atlas only — **no SPA redeploy / App.tsx**).
- Live target: https://arctictradelanes.com/atlas/atlas.manifest.json; ARC-SHIP-002 at [132.339798, 43.119476].

## Remaining soft preferred
- Cities: _(empty preferred)_
- Ports: 127 Nuupiluk; 128 Indiga; 148 Ura Guba; 166 EMO (skip)
- Softish shipyards: 021–023, 027, 029, 033–034, 039, 052, 076

## UM ($UM-Radar)
- `@international-arctic/geo-filter` **0.1.4** smoke left unchanged unless filter gap found.
