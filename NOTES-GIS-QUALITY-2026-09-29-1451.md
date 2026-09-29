# GIS Quality Loop — 2026-09-29 ~14:51 MSK (gis-densify-1451)

## Outcome
- **Densified ARC-FAC-006 Nukissiorfiit/NunaGreen Disko Bay Hydropower Plant (21 MW at Kangersuneq)** off soft `68.7500,-51.3000` onto OSM **node/14155973775** Kangersuneq bay (Qeqertalik) **68.7612/-50.9377** (~14.65 km E onto named fjord).
- Corroboration: KNR 2025-06-24 (Kangersuneq SE of Qasigiannguit); hydropower-dams.com (power station at Kangersuneq fjord + Kuussuup Tasia reservoir); NunaGreen Disko Bay (>6 km transfer tunnel, no dam); OSM Kuussuup Tasia way/833124366 + Qinngap Ilulialeeraa relation/20142362 (~6.1 km lake-to-lake matches tunnel).
- **DISTINCT**: ARC-FAC-330 Sarfartoq ~251.8 km; ARC-FAC-374 Piiaaffik ~471.3 km; ARC-FAC-340 Eimskip Nuuk ~511.5 km.
- Tag `gis-densify-1451` (~14:51 MSK). CI lock `check-fac006-kangersuneq-densify.mjs`.
- Soft cities empty. Soft ports remaining: **none** (skip 166 EMO). Softish shipyards blocked as prior. Soft industry remaining after this cycle: 008, 317, 321, 322, 324, 352 (near-dup FAC-005), 353, 354.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-29T11:58:06Z**, **1321** features / ports **156** / shipyards **70** / cities **103** / industry **110**. CRS primary EPSG:3996.
- Static atlas aliases synced — **no SPA redeploy / App.tsx**.

## UM ($UM-Radar)
- `@international-arctic/geo-filter` left unchanged pending sanity check (ATL densify win shipped).
