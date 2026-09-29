# GIS Quality Loop — 2026-09-29 ~19:01 MSK (gis-densify-1901)

## Outcome
- **Densified ARC-FAC-349 Longkou Nanshan LNG Terminal (PipeChina/Nanshan)** off soft `37.655,120.325` (Longkou port-area approximate) onto GEM **exact** + LNG Atlas GeoCoordinates `37.680774/120.220284` — **~9.65 km WNW**.
- Sources: [gem.wiki/Longkou_Nanshan_LNG_Terminal](https://www.gem.wiki/Longkou_Nanshan_LNG_Terminal) Phase 1/2/3 coordinates marked exact; [lngatlas.org](https://lngatlas.org/terminal/longkou-nanshan-lng-terminal-cn/) accuracy=exact (display 37.6808/120.2203).
- **DISTINCT**: densified ARC-FAC-348 Sinopec Longkou `37.6497398/120.2907759` ~7.10 km; next nearest Arctic features ~716 km (Shanghai shipyards ARC-SHIP-036/037).
- Tag `gis-densify-1901`. CI lock `check-fac349-longkou-nanshan-gem-densify.mjs`.
- Skipped: soft industry 008 defer / 324 blocked / 352 near-dup / 354 corridor; softish 365/369/370 multi-site; shipyard blocks 022/027/029/034/039/052 + Vard-025 quarantine; Rosatom-075 planned empty; Sevgiprorybflot-069 (Issue #34); PORT-164 untouched. FAC-348 left as densified (gis-densify-1834).

## Atlas
- Rebuilt via `ArcticTradeLanes.com/atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- Static atlas aliases synced — **no SPA redeploy / App.tsx**.
- generated `2026-09-29T16:07:27Z` — 1321 features / ports 156 / shipyards 70 / cities 103 / industry 110 (EPSG:3996).

## UM ($UM-Radar)
- Geo-filter stay **0.1.4** (null-island/OOB/swap filter already active); no SPA smash.
