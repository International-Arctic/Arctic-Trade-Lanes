# GIS Quality Loop — 2026-09-22 ~11:43 MSK

## Outcome
- **Densified ARC-PORT-031 Lavna Coal Terminal** off soft `69.1500,33.4500` onto OSM **way/1300372902** Nominatim centroid `69.0341207,33.0244586` (named *Морской торговый порт «Лавна»*, `landuse=industrial`).
- Tag `gis-densify-1143`. Softish shipyards unchanged (**13**); this is a **port** soft-pin win.
- Note: `ARC-PORT-164` remains a separate narrative Lavna/MTU soft pin (`69.0000,32.7900`) — do not merge without community review (possible near-duplicate).

## Soft shipyards (still blocked / quarantine)
Vigor-021, VT Halter-022, Eastern-023, Ulstein-024 (#37), Greenland-027, Northern Marine-029, Sembcorp-033, Hyundai-034, Wuchang-039, Kolskaya-052, Zhatay-076, Zvezda-002, Naval Group-015 (#43).

## Quarantine untouched
PORT-034/069, SHIP-069, Zvezda, Wrangell, Ulstein #37, Naval Group #43.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`.
- `generated` **2026-09-22T08:53:21Z**, **1321** features / **70** shipyards / **156** ports. CRS primary EPSG:3996.
- Live verified: https://arctictradelanes.com/data/atlas.geojson ARC-PORT-031 `[33.024459, 69.034121]`.
- Synced static Dataset + www/public/data/dist aliases — **no SPA redeploy / App.tsx**.

## UM
- No new package bump this cycle (geo-filter already **0.1.4** from ~11:20 MSK).

## OSS
- Dataset `92b951c` (densify + sources dedupe).
- Arctic-Trade-Lanes `1148b59` + Issue #32 comment.
