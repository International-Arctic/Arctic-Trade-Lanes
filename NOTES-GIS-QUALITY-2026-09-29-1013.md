# GIS Quality Loop — 2026-09-29 ~10:13 MSK (gis-densify-1013)

## Outcome
- **Densified ARC-FAC-304 Sokli Mining Project (Finnish Minerals Group)** off soft `67.8060,29.2800` (coarse Savukoski-region pin) onto OSM **way/440037634** `building=industrial` name=`Soklin koetehdas` wikidata=`Q11894014` wikipedia=`fi:Soklin malmio`. Nominatim centroid `67.7806477/29.2278900`.
- Soft→new ≈ **3.57 km**.
- WD corroboration: **Q11894014** Sokli mine P625 `67.7872/29.23` (~1 km from OSM industrial building).
- **DISTINCT**: nearest same-class ARC-FAC-394 Sakatti ~108 km.
- Tag `gis-densify-1013` (~10:13 MSK).
- Also closed prior live-atlas sync gap (Zo Dataset had `2026-09-29T06:59:56Z` after FAC-004 while live still served `2026-09-28T15:45:12Z`).
- Soft cities empty. Preferred soft ports 127/128/148 still unverifiable; EMO-166 skip; softish shipyards 022/027/029/034 DEFER/039/052 blocked; Vard-025 quarantine; Rosatom-075 planned empty; Sevgiprorybflot-069 Issue #34; quarantine + ARC-PORT-164 untouched. FAC-368 left soft (Stegra=FAC-319); FAC-308/333/344/398 no new site OSM this cycle; Sakatti FAC-394 still approx (office≠deposit). FAC-356 Skaergaard has WD Q1970121 P625 but no OSM named geometry this cycle (deferred).

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-29T07:21:52Z**, **1321** features / ports **156** / shipyards **70** / cities **103** / industry **110**. CRS primary EPSG:3996.
- Static atlas aliases synced (Dataset atlas/data + site root/www/public/dist + arctic-trade-lanes dist/public/www + `/data/arctictradelanes/`) — **no SPA redeploy / App.tsx**. Restarted `svc_UpoHDo9rDHs`.

## UM ($UM-Radar)
- `@international-arctic/geo-filter` **0.1.4** left unchanged.
