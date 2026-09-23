# GIS Quality Loop — 2026-09-23 ~14:27 MSK (gis-densify-1427)

## Outcome
- **Densified ARC-CITY-051 Grays Bay (port site)** off soft `67.8700,-110.9200` onto Wikidata **Q5598339** P625 `67.8167/-111.0000` (bay in Nunavut). OSM Nominatim **relation/13884530** `natural=bay` Grays Bay `67.7938459/-111.0127848` corroborates the feature; **ARC-PORT-052** already densified on that OSM center — city uses WD to stay **DISTINCT ~2.60 km** (city vs proposed-port pair).
- **Densified ARC-CITY-100 Steensby Inlet (Mary River mineral port site)** off soft `71.9600,-79.6000` (~176 km error) onto Wikidata **Q7605890** P625 `70.1667/-78.4167`. OSM **relation/13745622** Steensby Inlet center `70.3851175/-79.0793288` is the **ARC-PORT-153** pin — city stays **DISTINCT ~34.8 km** on coarser WD bay coordinate (inlet-scale).
- Tag `gis-densify-1427` (~14:27 MSK).
- Soft cities remaining after this win: **none** (Issue #49 queue cleared).
- Softish ports left unchanged: Wrangell-086 / Nuupiluk-127 / Indiga-128 / Ura Guba-148 / EMO-166 (route-pin skip).
- Softish shipyards blocked set unchanged (**13–14**). Quarantine + ARC-PORT-164 untouched.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`.
- `generated` **2026-09-23T11:33:08Z**, **1321** features / **70** shipyards / **156** ports / **103** cities. CRS primary EPSG:3996.
- Synced root/www/public/dist/data + arctic-trade-lanes/{dist,public,data,atlas} + Dataset aliases + `/data/arctictradelanes/` + Zo space `/data/atlas*.{geojson,json}`; restarted `svc_UpoHDo9rDHs` (static atlas only — **no SPA redeploy / App.tsx**).

## Remaining soft preferred
- Cities: _(empty)_
- Ports: 086 Wrangell; 127 Nuupiluk; 128 Indiga; 148 Ura Guba; 166 EMO (skip)

## UM
- Health check only; geo-filter left **0.1.4** (no bump).
