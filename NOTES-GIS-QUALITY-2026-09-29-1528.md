# GIS Quality Loop — 2026-09-29 ~15:28 MSK (gis-densify-1528)

## Outcome
- **Densified ARC-FAC-322 Plug Power Finland — Kristinestad green hydrogen plant + green DRI/HBI** off soft `62.2700,21.4400` onto OSM **way/40644756** Kristinestad kraftverk (Furuviken industrial landuse; former coal plant `end_date=2015`) **62.2570713/21.3234120** (~6.20 km W onto named plant pad).
- Corroboration: Wikidata **Q11873050** Kristiina power plant / Kristiinan voimalaitos P625 `62.25555556/21.32805556`; Plug Power / ArcticToday / STT: 1 GW electrolyzer "located close to a former coal plant" at Kristinestad; OSM tags `disused:power=plant`.
- **DISTINCT**: ARC-FAC-369 Nordic Hydrogen Route ~274.7 km; ARC-FAC-399 Polargrund ~362.9 km; ARC-FAC-320 Lulea Industripark ~370.1 km.
- Tag `gis-densify-1528` (~15:28 MSK). CI lock `check-fac322-kristinestad-kraftverk-densify.mjs`.
- Soft cities empty. Soft ports: none (skip 166 EMO). Soft industry remaining after this cycle: **008, 317, 321, 324, 352 (near-dup FAC-005), 353, 354**.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-29T12:35:53Z**, **1321** features / ports **156** / shipyards **70** / cities **103** / industry **110**. CRS primary EPSG:3996.
- Static atlas aliases synced — **no SPA redeploy / App.tsx**.

## UM ($UM-Radar)
- `@international-arctic/geo-filter` left unchanged pending sanity check (ATL densify win shipped).
