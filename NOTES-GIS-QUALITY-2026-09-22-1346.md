# GIS Quality Loop — 2026-09-22 ~13:46 MSK

## Outcome
- **Densified ARC-PORT-088 Port of Skellefteå (Skelleftehamn)** off soft `64.684,21.32` onto OSM **way/171489289** Nominatim `64.6784456,21.2485262` (named *Skellefteå hamn*, `landuse=wharf`, website portofskelleftea.se).
- **Densified ARC-PORT-064 Port of Tornio (Röyttä)** off soft `65.7530,24.1570` onto OSM **way/1335385483** Nominatim `65.7598189,24.1574679` (named *Tornion satama*, `landuse=industrial`).
- Tag `gis-densify-1346`. Softish shipyards blocked set unchanged (**13–14**); open softish preferred shipyards still **none**.
- Ulstein-024 re-checked: Nominatim only bus_stop/defibrillator named Ulstein Verft (~62.3408,5.8225); no industrial=shipyard polygon (Overpass 504). Kept blocked.
- Did **not** merge ARC-PORT-164 Lavna/MTU soft; quarantine untouched.

## Soft shipyards (still blocked / quarantine)
Vigor-021, VT Halter-022, Eastern-023, Ulstein-024, Greenland-027, Northern Marine-029, Sembcorp-033, Hyundai-034, Wuchang-039, Kolskaya-052, Zhatay-076, Zvezda-002, Naval Group-015, Waigaoqiao-036.

## Quarantine untouched
PORT-034/069, SHIP-069, ARC-PORT-164 (community review before merge).

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`.
- `generated` **2026-09-22T10:53:20Z**, **1321** features / **70** shipyards / **156** ports. CRS primary EPSG:3996.
- Live verified: https://arctictradelanes.com/data/atlas.geojson ARC-PORT-088 `[21.248526, 64.678446]`, ARC-PORT-064 `[24.157468, 65.759819]`.
- Synced root/www/public/dist/data + Dataset aliases — **no SPA redeploy / App.tsx**.

## UM
- No package bump (geo-filter already **0.1.4**); no new sentinel evidence this cycle.
