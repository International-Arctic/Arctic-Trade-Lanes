# GIS Quality Loop — 2026-09-29 ~14:21 MSK (gis-densify-1421)

## Outcome
- **Densified ARC-FAC-356 Greenland Mines (Nasdaq: GRML) — Skaergaard 2026 Field Program** off soft `68.1800,-31.8000` onto Wikidata **Q1970121** P625 **68.1683/-31.7169** (~3.67 km WNW onto intrusion centroid).
- Corroboration: enwiki Skaergaard intrusion 68°10′06″N 31°43′01″W; Commons Category:Skaergaard_intrusion; greenlandmines.com/projects/skaergaard-site (MEL 2007-01 hosts intrusion).
- **DISTINCT**: ARC-FAC-343 Tasiilaq ~383.5 km; ARC-FAC-331 Malmbjerg ~506.5 km; ARC-FAC-330 Sarfartoq ~853.4 km.
- Tag `gis-densify-1421` (~14:21 MSK). CI lock `check-fac356-skaergaard-densify.mjs`.
- Soft cities empty. Soft ports remaining: **none** (skip 166 EMO). Softish shipyards blocked as prior. Soft industry remaining after this cycle: 006, 008, 317, 321, 322, 324, 352 (near-dup FAC-005), 353, 354.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-29T11:27:32Z**, **1321** features / ports **156** / shipyards **70** / cities **103** / industry **110**. CRS primary EPSG:3996.
- Static atlas aliases synced — **no SPA redeploy / App.tsx**.

## UM ($UM-Radar)
- `@international-arctic/geo-filter` left unchanged pending sanity check (ATL densify win shipped).
