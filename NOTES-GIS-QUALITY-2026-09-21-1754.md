# GIS Quality Loop — 2026-09-21 ~17:54 MSK

## Win (ATL)
- Densified **ARC-SHIP-038** Hudong-Zhonghua (Arctic) off soft pin `31.2700,121.5400` (Shanghai city) onto OSM **way/165711825** Nominatim centroid `31.2797045,121.5698527`.
- OSM tags: `landuse=industrial` + `description=shipyard`, name `沪东中华造船` / Hudong–Zhonghua Shipbuilding (WD Q15411288 linked).
- Overpass center ~`31.2791378/121.5682657`; WD **Q15411288** (P31 shipyard/shipbuilding company; no P625; P159→Shanghai Q8686).
- Location label updated Shanghai → Shanghai (Pudong / Zhujiamen).

## Skips this loop
- Naval Group ARC-SHIP-015 / Issue #43 blocked; Ulstein #37 leave alone.
- Sembcorp ARC-SHIP-033: needs `industrial=shipyard`.
- Hyundai ARC-SHIP-034 soft: ARC-SHIP-058 already densified — avoid duplicate.
- Wuchang ARC-SHIP-039: deferred (Hudong win shipped).

## Atlas
- Rebuilt via `build_atlas.py`; static aliases synced (no SPA redeploy / App.tsx).
- `generated` `2026-09-21T15:01:48Z`, 1321 features / 70 shipyards / 156 ports. CRS primary EPSG:3996.
- Softish shipyards 15→14.
- CI: `check-ship038-hudong-densify.mjs`.

## Quarantine unchanged
- PORT-034/069, SHIP-069, Ulstein #37, Zvezda, Wrangell.
