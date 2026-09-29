# GIS Quality Loop — 2026-09-29 ~12:20 MSK (gis-densify-1220)

## Outcome
- **Densified ARC-FAC-394 Anglo American — Sakatti Cu-Ni-PGE-Au-Co Mining Project (Sodankylä, Finnish Lapland)** off soft `67.5500,26.7500` (coarse deposit-area pin) onto Wikidata **Q11891986** Sakatti mine / Sakatin kaivos P625 **67.5491667/26.7750000**.
- Soft→new ≈ **1.07 km**.
- Corroboration: fi.wikipedia *Sakatin malmiesiintymä* (WD sitelink); OSM **relation/11221546** `natural=wetland` Viiankiaapa Nominatim centroid **67.5414125/26.7706869** (~0.88 km from WD — orebody under western corner of Natura mire per company docs; wetland centroid corroborates location family, not used as pin).
- **DISTINCT**: OSM **way/397619252** office="Sakatti Mining Oy" Tuohiaavantie 2 Sodankylä **67.4075206/26.6413013** (~16.75 km — town HQ ≠ deposit); nearest same-class ARC-FAC-304 Sokli ~106.8 km. No conflation.
- Tag `gis-densify-1220` (~12:20 MSK). CI lock `check-fac394-sakatti-densify.mjs`.
- Soft cities empty. Soft ports 127 Nuupiluk (planned; no named OSM) / 128 Indiga (Cape Rumyanichny — village OSM ≠ cape/port site) skip; EMO-166 skip. Softish shipyards 022/027/029/034 DEFER/039/052 blocked; Vard-025 quarantine; Rosatom-075 planned empty; Sevgiprorybflot-069 Issue #34; quarantine + ARC-PORT-164 untouched. FAC-356 Skaergaard still WD-only optional (~3.67 km to Q1970121) deferred this cycle in favour of preferred Sakatti micro-move.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-29T09:28:25Z**, **1321** features / ports **156** / shipyards **70** / cities **103** / industry **110**. CRS primary EPSG:3996.
- Static atlas aliases synced (Dataset atlas/data + site root/www/public/dist + arctic-trade-lanes dist/public/www + `/data/arctictradelanes/`) — **no SPA redeploy / App.tsx**. Restarted `svc_UpoHDo9rDHs`.

## UM ($UM-Radar)
- `@international-arctic/geo-filter` **0.1.4** left unchanged (ATL densify win shipped; UM no bump).
