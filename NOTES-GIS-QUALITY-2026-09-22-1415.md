# GIS Quality Loop — 2026-09-22 ~14:15 MSK

## Outcome
- **Densified ARC-PORT-143 NorSea Polarbase Hammerfest (Rypefjord)** off soft `70.66,23.6` onto OSM **relation/8520723** Nominatim `70.6309365,23.6456644` (named *Polarbase*, `landuse=industrial`).
- **Densified ARC-PORT-161 Koverhar Harbour (Hanko)** off soft `59.868,22.992` onto OSM **way/22798026** Nominatim `59.8784323,23.2158120` (named *Koverhar*, `landuse=industrial`). Soft lon was ~12 km west of named industrial polygon; densify corrects onto OSM site.
- Tag `gis-densify-1415`. Softish shipyards blocked set unchanged (**13–14**); open softish preferred shipyards still **none**.
- Tried Piteå/Haraholmen, Ura Guba LNG, Evenes: no verified port/wharf polygon this cycle (Overpass 504 / Nominatim miss). Left soft.
- Did **not** merge ARC-PORT-164 Lavna/MTU soft; quarantine untouched.

## Soft shipyards (still blocked / quarantine)
Vigor-021, VT Halter-022, Eastern-023, Ulstein-024, Greenland-027, Northern Marine-029, Sembcorp-033, Hyundai-034, Wuchang-039, Kolskaya-052, Zhatay-076, Zvezda-002, Naval Group-015, Waigaoqiao-036.

## Quarantine untouched
PORT-034/069, SHIP-069, ARC-PORT-164 (community review before merge).

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset` (Zo).
- `generated` **2026-09-22T11:22:34Z**, **1321** features / **70** shipyards / **156** ports. CRS primary EPSG:3996.
- Live verified: https://arctictradelanes.com/data/atlas.geojson ARC-PORT-143 `[23.645664, 70.630937]`, ARC-PORT-161 `[23.215812, 59.878432]`.
- Synced root/www/public/dist/data + Dataset aliases — **no SPA redeploy / App.tsx**.

## UM
- No package bump (geo-filter already **0.1.4**); no new sentinel evidence this cycle.
