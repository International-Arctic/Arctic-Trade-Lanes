# GIS Quality Loop — 2026-09-29 ~11:19 MSK (gis-densify-1119)

## Outcome
- **Densified ARC-FAC-390 Pavlovskoye Pb-Zn GOK (Rosatom/PGRK)** off soft `72.12,53.42` (coarse Novaya Zemlya / Bezymyannaya Bay-region pin ~80+ km south of deposit) onto Wikidata **Q4341836** Павловское месторождение P625 **72.8521/53.7067**.
- Soft→new ≈ **81.97 km**.
- Corroboration: ru.wikipedia Павловское месторождение (Новая Земля) **72°51′08″N 53°42′24″E** (dual with WD); OSM **node/1903379280** `natural=bay` губа Безымянная `72.9018168/53.1741024` (~17.6 km W — bay/port approach; deposit inland per project docs 16–18 km from bay).
- **DISTINCT**: nearest same-class next ARC-FAC-315 Sabetta ~649 km; nearest port ARC-PORT-050 Novaya Zemlya Ports ~83 km (coarse). No conflation.
- Tag `gis-densify-1119` (~11:19 MSK). CI lock `check-fac390-pavlovskoye-densify.mjs`.
- Soft cities empty. Soft ports 127 Nuupiluk (planned; no named OSM) / 128 Indiga (Cape Rumyanichny — not village; WD village ≠ cape) skip; EMO-166 skip. Softish shipyards 022/027/029/034 DEFER/039/052 blocked; Vard-025 quarantine; Rosatom-075 planned empty; Sevgiprorybflot-069 Issue #34; quarantine + ARC-PORT-164 untouched. FAC-352 duplicate of densified FAC-005 Buksefjord (left soft; do not conflate onto FAC-005). FAC-368 left soft (Stegra=FAC-319); FAC-308/333/344/398 no site OSM; FAC-356 Skaergaard WD-only deferred; Sakatti FAC-394 still approx (WD P625 ~1 km only; office≠deposit).

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-29T08:28:49Z**, **1321** features / ports **156** / shipyards **70** / cities **103** / industry **110**. CRS primary EPSG:3996.
- Static atlas aliases synced (Dataset atlas/data + site root/www/public/dist + arctic-trade-lanes dist/public/www + `/data/arctictradelanes/`) — **no SPA redeploy / App.tsx**. Restarted `svc_UpoHDo9rDHs`.

## UM ($UM-Radar)
- `@international-arctic/geo-filter` **0.1.4** left unchanged (UM no bump).
