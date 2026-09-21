# GIS Quality Loop — 2026-09-21 ~16:25 MSK

## Win (ATL)
- Densified **ARC-SHIP-041** Kawasaki Heavy Industries (Arctic) off soft pin `34.6900,135.1900` (Kobe city) onto OSM **relation/6286362** Nominatim centroid `34.3341397,133.8321052`.
- OSM tags: `landuse=industrial` + `man_made=works`, name `川崎重工業 坂出造船工場` / Kawasaki Heavy Industries Sakaide Works (explicit 造船 = shipbuilding plant; no `industrial=shipyard` tag — same class as Galati factory densify).
- Bbox center ~`34.3341480/133.8355030`; WD **Q6379823** Ship & Offshore Structure Company (no P625; P159→Kobe Q48320 secondary); Kobe Works way/99284666 `industrial=factory` near soft noted secondary (not used — not named shipyard).
- Location label updated Kobe → Sakaide (Kawasaki-cho).

## Skips this loop
- Naval Group ARC-SHIP-015 / Issue #43 blocked; Ulstein #37 leave alone.
- Sembcorp ARC-SHIP-033: needs `industrial=shipyard`.
- Hyundai ARC-SHIP-034 soft: ARC-SHIP-058 already densified — avoid duplicate.
- Hudong / Wuchang: deferred (Kawasaki win shipped).

## Atlas
- Rebuilt via `build_atlas.py`; static aliases synced (no SPA redeploy / App.tsx).
- `generated` `2026-09-21T13:35:18Z`, 1321 features / 70 shipyards / 156 ports. CRS primary EPSG:3996.
- Softish shipyards 17→16.
- CI: `check-ship041-kawasaki-sakaide-densify.mjs`.

## Quarantine unchanged
- PORT-034/069, SHIP-069, Ulstein #37, Zvezda, Wrangell.
