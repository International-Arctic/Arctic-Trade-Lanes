# GIS Quality Loop — 2026-09-22 ~09:20 MSK

## Outcome
- **Densified ARC-SHIP-037 Jiangnan Shipyard (Arctic)** off soft `31.3533,121.6917` (Shanghai) onto OSM **way/145733398** Nominatim centroid `31.3557037,121.7415905` (`industrial=shipyard` 江南造船厂; operator 江南造船（集团）有限责任公司; website jnshipyard.cssc.net.cn; WD **Q81472** P31 shipyard, no P625).
- Location → **Shanghai (Changxing / Chongming)**.
- Tag `gis-densify-0920`. Softish (4-dec `.xx00`) shipyards **14→14** (Jiangnan was empty-source coarse, not in the `.xx00` softish set).

## Skips / blocked (unchanged)
- Wuchang ARC-SHIP-039 — need Yangluo/Shuangliu `industrial=shipyard`.
- Sembcorp ARC-SHIP-033 — way/1004233134 missing `industrial=shipyard`.
- Hyundai ARC-SHIP-034 — avoid dup vs ARC-SHIP-058 HD HHI Ulsan.
- Quarantine: PORT-034/069, SHIP-069, Zvezda, Wrangell, Ulstein #37, Naval Group #43.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`.
- `generated` **2026-09-22T06:23:44Z**, 1321 features / 70 shipyards / 156 ports. CRS primary EPSG:3996.
- Synced Dataset + atlas/ + www/public/dist/arctic-trade-lanes data paths — **no SPA redeploy / App.tsx / vite build**.

## Next preferred
- BAE ARC-SHIP-016 Glasgow, Vigor ARC-SHIP-021 Seattle, VT Halter ARC-SHIP-022, Eastern ARC-SHIP-023, Waigaoqiao ARC-SHIP-036 (Nominatim way/168992087 needs tag check), Wuchang/Sembcorp if OSM tags appear.
