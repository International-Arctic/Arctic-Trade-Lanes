# GIS Quality Loop — 2026-09-28 ~16:30 MSK (gis-densify-1630)

## Outcome
- **Densified ARC-SHIP-046 Seward Shipyard (JAG Alaska / Catalyst Marine Engineering)** off soft `60.1042,-149.4425` onto OSM **way/1287988507** `industrial=shipyard` `landuse=industrial` name="JAG Alaska Seward Shipyard". Nominatim centroid `60.0847277/-149.3510671` (extratags website=https://jagalaska.com/seward-shipyard-facility/).
- Soft→new ≈ **5.51 km**.
- **DISTINCT**: no other ARC-SHIP within 50 km.
- Tag `gis-densify-1630` (~16:30 MSK / fire 2026-09-28T13:30Z).
- Not touched: quarantine + ARC-PORT-164; soft ports Nuupiluk-127 / Indiga-128 / Ura Guba-148 / EMO-166 skip; softish shipyards 022/027/029/034/039/052 blockers unchanged; Vard-025 quarantine; Rosatom-075 planned empty; ARC-FAC-352 alias of densified ARC-FAC-005 (Buksefjord) — left soft.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-28T13:41:19Z**, **1321** features / **70** shipyards / **156** ports / **103** cities. CRS primary EPSG:3996.
- Synced Dataset atlas/data + site root/www/public/dist/data + arctic-trade-lanes mirrors + `/data/arctictradelanes/` + `/www/atlas` (static atlas only — **no SPA redeploy / App.tsx**).
- Live target: https://arctictradelanes.com/atlas/atlas.manifest.json; ARC-SHIP-046 at [-149.351067, 60.084728].

## Tried / deferred this cycle
- Soft ports 127/128/148: Nominatim still wrong/empty (Nuupiluk→Qeqqata cape; Indiga/Ura empty harbour geometry). Overpass mirrors TLS/timeout — no new pier/harbour.
- Softish shipyards 022/027/029/039/052: blockers hold (Overpass down; Nominatim empty / wrong).
- ARC-FAC-352 Buksefjorden: sibling/alias of ARC-FAC-005 @ GEM/WD Q1366227 P625 — do not conflate.
- ARC-FAC-353 Inuvialuit Corporate Centre OSM way/248754331 ~0.16 km — marginal, skipped.
- ARC-FAC-394 Sakatti WD Q11891986 ~1.07 km but P625 precision coarse (~0.023°) — skipped.
- ARC-SHIP-014 Aker Arctic OSM way/37777206 ~5.52 km — deferred (Seward was clearer industrial=shipyard match).

## Remaining soft preferred
- Cities: _(empty)_
- Ports: 127 Nuupiluk; 128 Indiga; 148 Ura Guba; 166 EMO (skip)
- Softish shipyards: 022, 027, 029, 034 (DEFER), 039, 052; Vard-025 quarantine; Rosatom-075 planned empty; optional next: ARC-SHIP-014 Aker Arctic Vuosaari

## UM ($UM-Radar)
- `@international-arctic/geo-filter` **0.1.4** left unchanged (no cheap client-side filter win this cycle).
