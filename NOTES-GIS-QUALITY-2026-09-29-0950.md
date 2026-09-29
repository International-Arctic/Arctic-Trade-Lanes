# GIS Quality Loop — 2026-09-29 ~09:50 MSK (gis-densify-0950)

## Outcome
- **Densified ARC-FAC-004 Grangex Sydvaranger Mine Restart** off soft `69.6830,30.0500` (approx Kirkenes S/SE pin) onto **GEM exact** `69.655768/30.014566` (Sydvaranger Mining Bjørnevatn Mine; gem.wiki; WGS84 exact).
- OSM corroboration: **relation/15301891** `landuse=quarry` `resource=iron_ore` (Overpass center `69.65174/30.0124012`, ~0.46 km from GEM; historic OSM operator tag Tacora — site now Grangex/Sydvaranger).
- Soft→new ≈ **3.32 km**.
- Independent: Wikipedia Sydvaranger (open-pit mine in Bjørnevatn); grangex.se ESIA (mine at Bjørnevatn ~7 km south of Kirkenes).
- **DISTINCT**: nearest same-class ARC-FAC-314 KILA ~7.53 km; nearest ARC-PORT-015 Kirkenes ~8.32 km.
- Tag `gis-densify-0950` (~09:50 MSK).
- Soft cities empty. Preferred soft ports 127/128/148 still unverifiable; EMO-166 skip; softish shipyards 022/027/029/034 DEFER/039/052 blocked; Vard-025 quarantine; Rosatom-075 planned empty; Sevgiprorybflot-069 Issue #34; quarantine + ARC-PORT-164 untouched. FAC-368 left soft (Stegra=FAC-319); FAC-308/333/344/398 no new site OSM this cycle; Sakatti FAC-394 still approx (WD Q11891986 ~1 km / office OSM ≠ deposit; Viiankiaapa wetland only).

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-29T06:59:56Z**, **1321** features / ports **156** / shipyards **70** / cities **103** / industry **110**. CRS primary EPSG:3996.
- Static atlas aliases synced only — **no SPA redeploy / App.tsx**.

## UM ($UM-Radar)
- `@international-arctic/geo-filter` **0.1.4** left unchanged.
