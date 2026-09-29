# GIS Quality Loop — 2026-09-29 ~18:34 MSK (gis-densify-1834)

## Outcome
- **Densified ARC-FAC-348 Sinopec Longkou LNG Import Terminal** off soft `37.640,120.330` (Longkou port-area approximate) onto GEM **exact** + LNG Atlas GeoCoordinates `37.6497398/120.2907759` — **~3.62 km WNW**.
- Sources: [gem.wiki/Sinopec_Longkou_LNG_Terminal](https://www.gem.wiki/Sinopec_Longkou_LNG_Terminal) Phase 1/2 coordinates marked exact; [lngatlas.org](https://lngatlas.org/terminal/sinopec-longkou-lng-terminal-cn/) schema.org Place geo + accuracy=exact (same WGS84). NDRC approval corroborates project identity (发改能源〔2021〕1373号).
- **DISTINCT**: soft ARC-FAC-349 Longkou Nanshan ~3.07 km; GEM Nanshan exact `37.680774/120.220284` ~7.1 km (FAC-349 left soft for later); next nearest Arctic features ~712 km (Shanghai shipyards).
- Bonus: atlas rebuild/sync also promotes prior **ARC-FAC-398** densify (CSV already had Nordmoveien pin; live/Dataset atlas copies had lagged on soft Evenes).
- Tag `gis-densify-1834`. CI lock `check-fac348-longkou-sinopec-gem-densify.mjs`.
- Skipped: soft industry 008 defer / 324 blocked / 352 near-dup / 354 corridor; softish 365/369/370 multi-site; shipyard blocks + Vard-025 quarantine; Sevgiprorybflot-069 still centroid_clone (Issue #34); PORT-164 untouched. FAC-330 already locked to GEUS minute pin (gis-densify-1244).

## Atlas
- Rebuilt via `ArcticTradeLanes.com/atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- Static atlas aliases synced — **no SPA redeploy / App.tsx**.
- generated `2026-09-29T15:42:55Z` — 1321 features / ports 156 / shipyards 70 / cities 103 / industry 110 (EPSG:3996).

## UM ($UM-Radar)
- Geo-filter stay **0.1.4** (null-island/OOB/swap filter already active in filterPeoplePins); no SPA smash. Package.json reports 1.0.0 app version; filter module unchanged this cycle.
