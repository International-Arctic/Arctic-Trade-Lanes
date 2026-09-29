# GIS Quality Loop — 2026-09-29 ~16:30 MSK (gis-densify-1630)

## Outcome
- **Densified ARC-FAC-317 Azane Fuel Solutions / Azane Infrastructure AS — Norwegian Coastal Ammonia Bunkering Terminal Network** off soft `60.82,5.03` onto Wikidata **Q1774322** Mongstad industrial complex P625 **60.81342778/5.029225** (~0.73 km onto named Mongstad hub).
- Corroboration: WD Q1774322 + enwiki Mongstad; WD Q59199378 Mongstad Refinery P625 `60.81022/5.02979` (~1.09 km from soft); azanefs.com Mongstad primary hub (Florø / Stavanger-Risavika / Mongstad network).
- **DISTINCT**: ARC-FAC-329 Horvnes Maritime Hub ~689.3 km; ARC-FAC-377 Helgeland Aqua Service ~721.0 km; ARC-FAC-350 Luxcara × GreenH Bodø ~849.3 km.
- Tag `gis-densify-1630` (~16:30 MSK). CI lock `check-fac317-mongstad-wd-densify.mjs`.
- Soft cities empty. Soft ports: none (skip 166 EMO). Soft industry remaining after this cycle: **008 (defer wiki DMS ~144 km), 321, 324, 352 (near-dup FAC-005), 354 (corridor-approx)**. Skipped 352 near-dup; 008 Sovinoye still deferred; 354 corridor-wide.
- OSS: Dataset / ATL SHAs filled after push; Issue #48 comment posted.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-29T13:36:50Z**, **1321** features / ports **156** / shipyards **70** / cities **103** / industry **110**. CRS primary EPSG:3996.
- Static atlas aliases synced — **no SPA redeploy / App.tsx**.

## UM ($UM-Radar)
- `@international-arctic/geo-filter` **0.1.4 stay** (confirmed Zo ATL `packages/geo-filter/package.json`). No i18n churn.
