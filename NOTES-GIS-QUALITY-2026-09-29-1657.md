# GIS Quality Loop — 2026-09-29 ~16:57 MSK (gis-densify-1657)

## Outcome
- **Densified ARC-FAC-321 ETFuels Finland — Ranua Näätäaapa e-methanol plant** off soft `65.9300,26.5100` onto Wikidata **Q24322521** Näätäaapa P625 **65.933333333333/26.2** (~14.06 km west onto named peatland/swamp place).
- Corroboration: WD Q24322521 + cebwiki Näätäaapa; Geonames **645185**; Ranua municipal planning (~11 km west of Ranua keskustaajama; https://ranua.fi/naataaavan-hanke/; kaavoitusaloite 2024-05-03 + Hankealuerajaus Liite 1); soft pin was Ranua parish/town centroid (WD Q11890090 / Nominatim Ranua).
- **DISTINCT**: ARC-FAC-002 Norsk e-Fuel Tornio ~94.9 km; ARC-FAC-001 Norwegian Hydrogen Tornio ~94.9 km; ARC-FAC-003 Oulun Energia Laanila ~104.8 km.
- Tag `gis-densify-1657` (~16:57 MSK). CI lock `check-fac321-naataaapa-wd-densify.mjs`.
- Soft cities empty. Soft ports: none (skip 166 EMO). Soft industry remaining after this cycle: **008 (defer Sovinoye), 324, 352 (near-dup FAC-005 — skip), 354 (corridor-approx)**.
- OSS: Dataset / ATL SHAs filled after push; Issue #48 comment posted.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-29T14:05:10Z**, **1321** features / ports **156** / shipyards **70** / cities **103** / industry **110**. CRS primary EPSG:3996.
- Static atlas aliases synced — **no SPA redeploy / App.tsx**.

## UM ($UM-Radar)
- `@international-arctic/geo-filter` **0.1.4 stay** (confirmed Zo ATL `packages/geo-filter/package.json`). No i18n churn.
