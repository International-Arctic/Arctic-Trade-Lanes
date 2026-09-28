# GIS Quality Loop — 2026-09-28 ~17:00 MSK (gis-densify-1700)

## Outcome
- **Densified ARC-SHIP-014 Aker Arctic Technology** off soft `60.2104,25.0808` (mis-labeled Herttoniemi) onto OSM **way/37777206** `building=yes` name="Aker Arctic". Nominatim centroid `60.2122521/25.1806431` (Merenkulkijankatu 6, Vuosaari, Helsinki). WD **Q4700623** (company; no P625). Website http://www.akerarctic.fi.
- Soft→new ≈ **5.52 km**.
- **DISTINCT**: no other ARC-SHIP within 1 km; nearest siblings ARC-SHIP-009 Arctech Helsinki ~15.16 km and ARC-SHIP-010 Helsinki Shipyard ~15.32 km (different facilities).
- Tag `gis-densify-1700` (~17:00 MSK / fire 2026-09-28T14:00Z).
- Not touched: quarantine + ARC-PORT-164; soft ports Nuupiluk-127 / Indiga-128 / Ura Guba-148 / EMO-166 skip; softish shipyards 022/027/029/034 DEFER/039/052; Vard-025 quarantine; Rosatom-075 planned empty.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-28T14:06:57Z**, **1321** features / **70** shipyards / **156** ports / **103** cities. CRS primary EPSG:3996.
- Synced Dataset atlas/data + site root/www/public/dist/data + arctic-trade-lanes mirrors + `/data/arctictradelanes/` + `/www/atlas` (static atlas only — **no SPA redeploy / App.tsx**).
- Live target: https://arctictradelanes.com/atlas/atlas.manifest.json; ARC-SHIP-014 at [25.180643, 60.212252].

## Remaining soft preferred
- Cities: _(empty)_
- Ports: 127 Nuupiluk; 128 Indiga; 148 Ura Guba; 166 EMO (skip)
- Softish shipyards: 022, 027, 029, 034 (DEFER), 039, 052; Vard-025 quarantine; Rosatom-075 planned empty

## UM (\$UM-Radar)
- `@international-arctic/geo-filter` **0.1.4** left unchanged (no cheap client-side filter win this cycle).
