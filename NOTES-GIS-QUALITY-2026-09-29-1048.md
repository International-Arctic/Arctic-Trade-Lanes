# GIS Quality Loop — 2026-09-29 ~10:48 MSK (gis-densify-1048)

## Outcome
- **Densified ARC-PORT-148 Ura Guba (Ura Bay) - Murmansk LNG Reloading Terminal (Arctic LNG 2 OTC)** off soft `69.16,33.42` (misplaced toward Murmansk/Kola Bay approaches) onto permanently moored **Saam FSU** (IMO **9915090** / MMSI 273256300) AIS at-anchor **69.3375/32.9273** (fleetleaks.com/vessels/imo-9915090; BarentsObserver + PortNews: FSU permanently based in Ura Guba for Novatek Arctic LNG reloading).
- Soft→new ≈ **27.68 km**.
- Corroboration: OSM **way/83361500** `place=village` Ура-Губа Nominatim centroid `69.2913890/32.7935220` (~7.34 km); WD **Q4411417** Ura-Guba P625 `69.2894/32.8006`; OSM **relation/1426500** Видяево `69.3180/32.8067` (~5.21 km).
- **DISTINCT**: nearest same-class ARC-PORT-031 Lavna ~33.95 km (soft pin had been only ~19 km from Kola Bay Fuel — wrongly clustered with Murmansk).
- Tag `gis-densify-1048` (~10:48 MSK).
- Soft cities empty. Remaining soft ports: **127 Nuupiluk** (planned; no named OSM site; airport-west estimate only), **128 Indiga** (Cape Rumyanichny ~50 km west of Indiga Bay — cape not in OSM/WD; village/bay ≠ cape). Skip EMO-166. Softish shipyards 022/027/029/034 DEFER/039/052 blocked; Vard-025 quarantine; Rosatom-075 planned empty; Sevgiprorybflot-069 Issue #34; quarantine + ARC-PORT-164 untouched. FAC-368 left soft (Stegra=FAC-319); FAC-308/333/344/398 no site OSM; FAC-356 Skaergaard WD-only deferred again; Sakatti FAC-394 still approx (WD P625 ~1 km only; office≠deposit).

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-29T07:56:28Z**, **1321** features / ports **156** / shipyards **70** / cities **103** / industry **110**. CRS primary EPSG:3996.
- Static atlas aliases synced (Dataset atlas/data + site root/www/public/dist + arctic-trade-lanes dist/public/www + `/data/arctictradelanes/`) — **no SPA redeploy / App.tsx**. Restarted `svc_UpoHDo9rDHs`.

## UM ($UM-Radar)
- `@international-arctic/geo-filter` **0.1.4** left unchanged (no pin-filter defect this cycle).
