# GIS Quality Loop — 2026-09-22 ~16:21 MSK

## Outcome
- **Densified ARC-PORT-142 Chaika Coal Terminal (Taymyr / Kara Sea)** off soft `73.51,80.81` onto OSM **way/1104012015** `man_made=pier` centroid `73.3779684,80.5176146` (Chaika Peninsula / Cape Severny construction cluster: OSM buildings + service roads ways/1104012016–2041). Corroborated **OurAirports RU-1018** *Chaika Coal Terminal Helipad* `73.379354,80.59003` (keywords Vostokugol-Dikson) + OVOS site note *мыс Северный полуострова Чайка*. Soft ~2dp pin sat ~17 km NE of the mapped pier/helipad complex; densify corrects onto verified harbour pier. **Distinct from ARC-PORT-007 Dikson Sea Port** (already on way/1080460349 `73.5043654,80.5151725`).
- Tag `gis-densify-1621`. Softish shipyards blocked set unchanged (**13–14**).
- Tried Hoybukta-060: Nominatim/Overpass hit airport + Kimek (not planned Vest site) — left soft. Wrangell-086: unnamed industrial only / City Dock ≠ 6-Mile Mill planned — left soft. Indiga-128: village + diesel industrials only / no Cape Rumyanichny harbour — left soft. Nuupiluk-127: Nominatim hit wrong North Greenland cape — left soft. Ura Guba-148 / EMO-166 skipped per standing guidance.
- Did **not** merge ARC-PORT-164; quarantine untouched.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`.
- `generated` **2026-09-22T13:33:54Z**, **1321** features / **70** shipyards / **156** ports. CRS primary EPSG:3996.
- Synced root/www/public/dist/data + Dataset aliases — **no SPA redeploy / App.tsx**.

## UM
- No package bump (geo-filter already **0.1.4**); ATL densify shipped this cycle.
