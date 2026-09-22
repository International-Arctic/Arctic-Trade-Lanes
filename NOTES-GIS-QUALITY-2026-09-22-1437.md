# GIS Quality Loop — 2026-09-22 ~14:37 MSK

## Outcome
- **Densified ARC-PORT-126 Evenes Industrial Seaport (EIS)** off soft atlas `68.49,16.68` (and prior CSV near-airport `68.4916172,16.7323337`) onto Nominatim **OSM node/3117063492** `68.4645799,16.7755428` — official address *Nerveien 251, 8534 Liland* from evenes-seaport.no.
- **Synced ARC-PORT-087 Port of Piteå (Haraholmen)** soft atlas `65.219,21.558` → Dataset CSV `65.235163,21.6361624` (portofpitea.se). Atlas was stale vs CSV; rebuild closed the gap.
- Tag `gis-densify-1437`. Softish shipyards blocked **13–14** unchanged. Ura Guba-148 and planned soft ports left soft.
- Quarantine + ARC-PORT-164 untouched.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`.
- `generated` **2026-09-22T11:48:34Z**, **1321** features / **70** shipyards / **156** ports. CRS primary EPSG:3996.
- Live: https://arctictradelanes.com/data/atlas.geojson

## UM
- No package bump (geo-filter already **0.1.4**).
