# GIS Quality Loop — 2026-09-29 ~15:57 MSK (gis-densify-1557)

## Outcome
- **Densified ARC-FAC-353 Inuvialuit Regional Corporation / Inuvialuit Development Corporation** off soft `68.36,-133.73` onto OSM **way/248754331** Inuvialuit Corporate Centre (107 Mackenzie Road, Inuvik NT) **68.3587216/-133.7284756** (~0.16 km onto named IRC HQ building).
- Corroboration: OSM addr tags + `wikimedia_commons` File:Inuvialuit Corporate Centre (IRC building).jpg; IRC/IDC official sites (inuvialuit.com / irc.inuvialuit.com).
- **DISTINCT**: ARC-FAC-389 K'áhsho Got'ı̨nę Trades Centre ~339.2 km; ARC-FAC-363 Alyeschem ~613.3 km; ARC-FAC-383 STaX Franklin Bluffs ~641.6 km.
- Tag `gis-densify-1557` (~15:57 MSK). CI lock `check-fac353-inuvialuit-corporate-centre-densify.mjs`.
- Soft cities empty. Soft ports: none (skip 166 EMO). Soft industry remaining after this cycle: **008, 317, 321, 324, 352 (near-dup FAC-005), 354**. (Skipped 352 near-dup; 008 Sovinoye wiki DMS ~144 km — defer; 354 corridor-approx.)

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-29T13:03:30Z**, **1321** features / ports **156** / shipyards **70** / cities **103** / industry **110**. CRS primary EPSG:3996.
- Static atlas aliases synced — **no SPA redeploy / App.tsx**.

## UM ($UM-Radar)
- `@international-arctic/geo-filter` **0.1.4 stay** (confirmed on Zo ATL package.json). No i18n churn.
