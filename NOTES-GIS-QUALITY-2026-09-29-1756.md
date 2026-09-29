# GIS Quality Loop — 2026-09-29 ~17:56 MSK (gis-densify-1756)

## Outcome
- **Densified ARC-FAC-398 Nscale Narvik AI Data Center Campus (Kvandal / Kvanndalen)** off soft `68.4500,16.5800` (Evenes-area approximate) onto OSM house **Nordmoveien 281, Bjerkvik** `68.5756900/17.5800710` (node 13377571111; Google Maps "Kvandal Datasenter (Stargate)" / Campus Kvandal) — **~43.06 km NE** onto named campus address in Narvik kommune.
- Corroboration: OSM Kvanndalen hamlet node 9884377673 `68.5760610/17.6216335`; TU.no 2026-07-03 (Nscale DC in Kvanndalen ~3.5 km N of Bjerkvik); Fremover Kvandal Nord/Kvanndalen; HENT Kvandal North Campus KNB4–6. Rejected third-party Narvik-town centroid ~68.44/17.43 (DC Atlas / AI Data Center Index approximate).
- **DISTINCT**: ARC-FAC-366 NGA Bjerkvik ~3.09 km; ARC-PORT-136 Narvik Terminal Nord ~16.44 km; ARC-FAC-327 Narvik Bulk ~16.46 km.
- Tag `gis-densify-1756` (~17:56 MSK). CI lock `check-fac398-kvandal-nordmoveien-densify.mjs`.
- Softish corridor/multi-site skipped this cycle (no single verifiable pin): FAC-365 Port Alliance multi-terminal; FAC-369 Nordic Hydrogen Route network; FAC-370 North Pole drift-ice (no fixed pin).
- Soft industry remaining: **008 (defer Sovinoye), 324 (blocked no site pin), 352 (skip near-dup FAC-005), 354 (corridor-approx)**; softish 365/369/370; shipyard blocks unchanged.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- Static atlas aliases synced — **no SPA redeploy / App.tsx**.

## UM ($UM-Radar)
- No UM geo-filter change this cycle (ATL densify win shipped).
