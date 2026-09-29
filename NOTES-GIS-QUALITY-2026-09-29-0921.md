# GIS Quality Loop — 2026-09-29 ~09:21 MSK (gis-densify-0921)

## Outcome
- **Densified ARC-FAC-375 GreenRoc Strategic Materials / Greenland Graphite A/S — Piiaaffik Amitsoq** off soft `60.3500,-45.3500` (coarse Nanortalik-region pin) onto OSM **node/2432749259** `historic=mine` name="Deserted Graphite Mine" `resource=graphite` operator="Greenroc Mining" website=https://greenrocmining.com/project/amitsoq-graphite-greenland/. Nominatim `60.2845060/-45.1266140`.
- Soft→new ≈ **14.29 km**.
- Cross-check: Amitsoq Island WD **Q24839578** P625 `60.3627/-44.9993` / OSM relation/10796567 nearby.
- **DISTINCT**: nearest same-class ARC-FAC-393 Tanbreez ~76.32 km.
- Tag `gis-densify-0921` (~09:21 MSK).
- Soft cities empty. Preferred soft ports 127/128/148 still unverifiable; EMO-166 skip; softish shipyards 022/027/029/034 DEFER/039/052 blocked; Vard-025 quarantine; Rosatom-075 planned empty; Sevgiprorybflot-069 Issue #34; quarantine + ARC-PORT-164 untouched. FAC-368 left soft (Stegra=FAC-319); FAC-308/333/344/398 no verifiable site OSM this cycle; Sakatti FAC-394 still approx (office≠deposit; Viiankiaapa wetland only).

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-29T06:30:42Z**, **1321** features / ports **156** / shipyards **70** / cities **103** / industry **110**. CRS primary EPSG:3996.
- Static atlas aliases synced only — **no SPA redeploy / App.tsx**.

## UM ($UM-Radar)
- `@international-arctic/geo-filter` **0.1.4** left unchanged.
