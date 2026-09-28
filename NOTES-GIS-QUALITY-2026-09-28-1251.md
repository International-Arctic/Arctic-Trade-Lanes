# GIS Quality Loop — 2026-09-28 ~12:51 MSK (gis-densify-1251)

## Outcome
- **Densified ARC-SHIP-036 Shanghai Waigaoqiao (Arctic)** off soft `31.3667,121.5667` onto OSM **way/168992087** `landuse=industrial` 上海外高桥造船有限公司 / Shanghai Waigaoqiao Shipbuilding Co., Ltd. Nominatim centroid `31.3427375/121.6304940` (Overpass center ~`31.342622/121.6307173`).
- Corroboration: Wikidata **Q10867794** P159 HQ qualifier P625 `31.339166666666667/121.63333333333334` (~0.48 km from OSM).
- Soft→new ≈ **6.62 km**.
- Sibling DISTINCT: **ARC-SHIP-038 Hudong-Zhonghua** ~9.07 km; **ARC-SHIP-037 Jiangnan** ~10.65 km.
- Tag `gis-densify-1251` (~12:51 MSK).
- Preferred soft ports left soft (not re-litigated): Nuupiluk-127 / Indiga-128 / Ura Guba-148 / EMO-166 (skip).
- Softish shipyards remaining blocked: Vigor-021, VT Halter-022, Eastern-023, Greenland-027, Northern Marine-029, Sembcorp-033, Hyundai-034 (sibling ARC-SHIP-058 misplaced ~12 km W of Dong-gu yard — deferred), Wuchang-039, Kolskaya-052, Zhatay-076 (+ Vard-025 quarantine, Rosatom-075 planned empty). Quarantine + ARC-PORT-164 untouched.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-28T09:56:47Z**, **1321** features / **70** shipyards / **156** ports / **103** cities. CRS primary EPSG:3996.
- Synced Dataset atlas/data + site root/www/public/dist/data + arctic-trade-lanes dist/public (+ /atlas) + `/data/arctictradelanes/` + Zo space assets (static atlas only — **no SPA redeploy / App.tsx**). Restarted `svc_UpoHDo9rDHs`.
- Live target: https://arctictradelanes.com/atlas/atlas.manifest.json; ARC-SHIP-036 at [121.630494, 31.342738].

## Remaining soft preferred
- Cities: _(empty preferred)_
- Ports: 127 Nuupiluk; 128 Indiga; 148 Ura Guba; 166 EMO (skip)
- Softish shipyards: 021–023, 027, 029, 033–034, 039, 052, 076

## UM ($UM-Radar)
- `@international-arctic/geo-filter` **0.1.4** smoke left unchanged unless filter gap found.
