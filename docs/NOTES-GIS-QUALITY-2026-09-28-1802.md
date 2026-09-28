# GIS Quality Loop — 2026-09-28 ~18:02 MSK (gis-densify-1802)

## Outcome
- **Densified ARC-FAC-380 Kajaani Raksila / LUMI+CSC campus** off soft `64.2270,27.7349` (~0.26 km from Kajaani admin centroid Nominatim relation/2525693) onto OSM **way/705545655** `building=industrial` name=CSC alt_name=LUMI addr Tehdaskatu 15, 87100 Kajaani. Nominatim centroid `64.2319866/27.6914770`.
- Soft→new ≈ **2.17 km**.
- **DISTINCT**: nearest same-class ARC-FAC-325 ~20.56 km.
- Tag `gis-densify-1802` (~18:02 MSK).
- Preferred soft ports 127/128/148 still unverifiable; EMO-166 skip; softish shipyards 022/027/029/034 DEFER/039/052 blocked; quarantine + ARC-PORT-164 untouched. Soft cities empty.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- Static atlas aliases synced only — **no SPA redeploy / App.tsx**.

## UM ($UM-Radar)
- `@international-arctic/geo-filter` **0.1.4** left unchanged.
