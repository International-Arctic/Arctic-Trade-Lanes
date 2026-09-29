# GIS Quality Loop — 2026-09-29 ~11:47 MSK (gis-densify-1147)

## Outcome
- **Densified ARC-FAC-379 Afrikanda perovskite rare-earth & titanium complex (JSC Arkmineral-Resurs)** off soft `67.2500,33.5200` (coarse Kola pin ~38 km SE of locality) onto OSM **node/303015821** `place=village` Африканда Nominatim **67.4416890/32.7769090**.
- Soft→new ≈ **38.30 km**.
- Corroboration: Wikidata **Q1987760** Afrikanda P625 67.441666666667/32.781666666667 (~0.20 km); ru.wikipedia Африканда 67.44167/32.78167; station WD **Q111372418** 67.442545/32.778071 (~0.11 km). Deposit massif described ~1 km from station SE of Lake Imandra (ke-culture.gov-murman.ru slovnik ELEMENT_ID=92699). No named OSM perovskite quarry geometry.
- **DISTINCT**: OSM way/47293064 песчаный карьер ~3.2 km (sand pit ≠ deposit); air base WD Q2027349 ~1.7 km; nearest same-class ARC-FAC-304 Sokli ~153 km; Murmansk cluster ARC-FAC-316 ~170 km. No conflation.
- Tag `gis-densify-1147` (~11:47 MSK). CI lock `check-fac379-afrikanda-densify.mjs`.
- Soft cities empty. Soft ports 127 Nuupiluk (planned; no named OSM) / 128 Indiga (Cape Rumyanichny — not village) skip; EMO-166 skip. Softish shipyards 022/027/029/034 DEFER/039/052 blocked; Vard-025 quarantine; Rosatom-075 planned empty; Sevgiprorybflot-069 Issue #34; quarantine + ARC-PORT-164 untouched. FAC-352 duplicate of densified FAC-005 Buksefjord (left soft). FAC-356 Skaergaard WD-only deferred; Sakatti FAC-394 still approx (WD P625 deposit-grade ~1 km from soft; office OSM way/397619252 ~17 km DISTINCT — micro-move deferred this cycle in favour of Afrikanda).

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-29T08:55:51Z**, **1321** features / ports **156** / shipyards **70** / cities **103** / industry **110**. CRS primary EPSG:3996.
- Static atlas aliases synced (Dataset atlas/data + site root/www/public/dist + arctic-trade-lanes dist/public/www + `/data/arctictradelanes/`) — **no SPA redeploy / App.tsx**. Restarted `svc_UpoHDo9rDHs`.

## UM ($UM-Radar)
- `@international-arctic/geo-filter` **0.1.4** left unchanged (UM no bump).
