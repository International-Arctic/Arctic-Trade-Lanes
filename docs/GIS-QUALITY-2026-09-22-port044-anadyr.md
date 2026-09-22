# GIS Quality Loop — 2026-09-22 ~12:10 MSK

## Outcome
- **Densified ARC-PORT-044 Anadyr Port** off soft `64.7333,177.5000` onto OSM **way/685797435** Nominatim centroid `64.7399757,177.5074775` (named *Анадырский морской порт, ММПП «Анадырь»*, `landuse=harbour`, `industrial=port`, wikipedia `ru:Анадырь (порт)`).
- Tag `gis-densify-1206`. Softish shipyards unchanged (**13**); this is a **port** soft-pin win.
- Did **not** merge ARC-PORT-164 Lavna/MTU soft pin (community review first).

## Soft shipyards (still blocked / quarantine)
Vigor-021, VT Halter-022, Eastern-023, Ulstein-024 (#37), Greenland-027, Northern Marine-029, Sembcorp-033, Hyundai-034, Wuchang-039, Kolskaya-052, Zhatay-076, Zvezda-002, Naval Group-015 (#43). Also Waigaoqiao-036.

## Quarantine untouched
PORT-034/069, SHIP-069, ARC-PORT-164.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`.
- `generated` **2026-09-22T09:13:48Z**, **1321** features / **70** shipyards / **156** ports. CRS primary EPSG:3996.
- Live verified: https://arctictradelanes.com/data/atlas.geojson ARC-PORT-044 `[177.507478, 64.739976]`.
- Synced static aliases — **no SPA redeploy / App.tsx**.

## UM
- No package bump (geo-filter already **0.1.4**).
