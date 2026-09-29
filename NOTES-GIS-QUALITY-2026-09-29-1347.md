# GIS Quality Loop — 2026-09-29 ~13:47 MSK (gis-densify-1347)

## Outcome
- **Densified ARC-PORT-127 Nuupiluk Deep-Water Harbour & Ferry Port (planned — Qaqortoq district, South Greenland)** off soft `60.72,-46.15` onto planned ferry/harbour tip **~8.3 km west of Mittarfik Qaqortoq / Qaqortoq Airport** at **60.7658/-46.2170**.
- Soft→new ≈ **6.26 km** WNW.
- Method: average of (a) 8.3 km due west of OSM aerodrome way/1479504449 (60.7641866/-46.0707914) per sermitsiaq.ag distance, and (b) Kommune Kujalleq map georeference (orange Nuupiluk ferry marker on sermitsiaq article map).
- Corroboration: sermitsiaq.ag 2025-09-30 (8,3 km vest for lufthavnen; road Qaqortoq–Nuupiluk with airport midway; færge Nuupiluk–Narsaq ~20 km / GC ≈18.8 km); enwiki Qaqortoq Airport 60°45′57″N 046°03′54″W; OSM Mittarfik Qaqortoq.
- **DISTINCT**: ARC-PORT-053 Qaqortoq Port ~11.07 km E; ARC-PORT-091 Dual-Use ~11.07 km E; ARC-PORT-009 Nuuk Port ~472.5 km N; OSM cape Nuupiluk node/13267176632 at 65.90N/-52.49W is a different Qeqqata place name — not this site.
- Tag `gis-densify-1347` (~13:47 MSK). CI lock `check-port127-nuupiluk-densify.mjs`.
- Soft cities empty. Soft ports remaining: **none** (skip 166 EMO). Softish shipyards 022/027/029/034 DEFER/039/052 blocked; Vard-025 quarantine; Rosatom-075 planned empty; Sevgiprorybflot-069 Issue #34; quarantine + ARC-PORT-164 untouched. Soft industry still open: 006, 008, 317, 321, 322, 324, 352 (near-dup FAC-005), 353, 354, 356 Skaergaard WD-only optional (~3.67 km Q1970121).

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-29T10:56:22Z**, **1321** features / ports **156** / shipyards **70** / cities **103** / industry **110**. CRS primary EPSG:3996.
- Static atlas aliases synced (Dataset atlas/data + site root/www/public/dist + arctic-trade-lanes dist/public/www + `/data/arctictradelanes/`) — **no SPA redeploy / App.tsx**. Restarted `svc_UpoHDo9rDHs`.

## UM ($UM-Radar)
- `@international-arctic/geo-filter` **0.1.4** left unchanged (ATL densify win shipped; UM no bump).
