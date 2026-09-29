# GIS Quality Loop — 2026-09-29 ~17:37 MSK (gis-densify-1737)

## Outcome
- **Densified ARC-FAC-374 Greenland Anorthosite Mining (GAM) — Majoqqap Qaava / Piiaaffik Itersarmiut Alliit** off soft `64.5500,-52.1500` (Qeqertarsuatsiaat settlement centroid) onto official GAM SIA 2019-162 §4.1 **63°13'N / 50°12'W = 63.216666666667/-50.2** (~176.31 km SE onto named mine/deposit place).
- Corroboration: GAM SIA PDF (EN 15.4.2025) + GAM Navigational Safety Investigation EIA Background X (same DMS); gam.gl/projects (~125–130 km SE of Nuuk; ~30 km NE of Fiskenæsset).
- **DISTINCT**: ARC-FAC-005 Buksefjord ~85.5 km; ARC-FAC-352 soft Buksefjord ~125.5 km; ARC-FAC-338 Royal Greenland Nuuk ~127.8 km.
- Tag `gis-densify-1737` (~17:37 MSK). CI lock `check-fac374-majoqqap-qaava-gam-densify.mjs`.
- Preferred FAC-324 Promstroyarktik Arkhangelsk: **BLOCKED** (no published site address/coords; city-only + SPb legal HQ). FAC-354 corridor-approx skip. FAC-352 near-dup skip. FAC-008 defer Sovinoye.
- Soft industry remaining after this cycle: **008 (defer), 324 (blocked no site pin), 352 (skip near-dup), 354 (corridor-approx)**; also softish corridor/multi-site: 365/369/370; FAC-398 Nscale Kvandal pending authoritative pin (third-party ~68.44/17.43 not used).

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-29T14:37:26Z**, **1321** features / ports **156** / shipyards **70** / cities **103** / industry **110**. CRS primary EPSG:3996.
- Static atlas aliases synced — **no SPA redeploy / App.tsx**.

## UM ($UM-Radar)
- No UM geo-filter change this cycle (ATL densify win shipped).
