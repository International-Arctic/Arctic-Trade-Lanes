# GIS Quality Loop — 2026-09-22 ~12:47 MSK

## Outcome
- **Densified ARC-SHIP-055 Sata Shipbuilding (Mantyluoto)** off soft `61.5992,21.4100` onto OSM **way/39584327** Nominatim centroid `61.5967316,21.5097519` (named *Mäntyluodon telakka*, `landuse=industrial`, operator Enersense Offshore).
- Tag `gis-densify-1247`. Softish preferred blocked set unchanged (**13**); open softish **Sata densified** — remaining open softish: **Grovfjord-071** only (Overpass flaky on kumi; lz4 returned Mantyluoto).
- Did **not** merge ARC-PORT-164 Lavna/MTU soft; quarantine untouched.

## Soft shipyards (still blocked / quarantine)
Vigor-021, VT Halter-022, Eastern-023, Ulstein-024 (#37), Greenland-027, Northern Marine-029, Sembcorp-033, Hyundai-034, Wuchang-039, Kolskaya-052, Zhatay-076, Zvezda-002, Naval Group-015 (#43). Also Waigaoqiao-036 (tag bar).

Open softish remaining: ARC-SHIP-071 Grovfjord.

## Quarantine untouched
PORT-034/069, SHIP-069, ARC-PORT-164 (community review before merge).

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`.
- `generated` **2026-09-22T09:48:57Z**, **1321** features / **70** shipyards / **156** ports. CRS primary EPSG:3996.
- Live verified: https://arctictradelanes.com/data/atlas.geojson ARC-SHIP-055 `[21.509752, 61.596732]`.
- Synced root/www/public/dist/data + arctic-trade-lanes aliases — **no SPA redeploy / App.tsx**.

## UM
- No package bump (geo-filter already **0.1.4**).

## Note on OSM operator
Way name *Mäntyluodon telakka* matches the Mantyluoto shipyard site used by Sata/Inocea block construction; OSM `operator=Enersense Offshore` recorded in sources for transparency (facility polygon, not corporate ownership claim).
