# GIS Quality Loop — 2026-09-23 ~13:58 MSK (gis-densify-1358)

## Outcome
- **Densified ARC-CITY-009 Khatanga (Russia / Krasnoyarsk Krai)** off soft `71.9800,102.4700` onto OSM Nominatim **relation/18023381** `place=village` name=Хатанга / Khatanga `71.9819205/102.4714765` (wikidata=Q918830). Corroborated Wikidata **Q918830** P625 `71.983333333333/102.5` (precision ~1′ — coarser than OSM; OSM centroid preferred). **DISTINCT** from ARC-PORT-008 Khatanga River Port `71.9841653/102.4753286` ~0.28 km (city vs river-port pair; same pattern as Tiksi CITY-007 vs PORT-006).
- Tag `gis-densify-1358` (~13:58 MSK / fired ~11:01Z atlas gen).
- Soft cities remaining after this win: ARC-CITY-051 Grays Bay `67.87/-110.92`; ARC-CITY-100 Steensby Inlet `71.96/-79.6`.
- Softish ports left unchanged: Wrangell-086 / Nuupiluk-127 / Indiga-128 / Ura Guba-148 / EMO-166 (route-pin skip).
- Softish shipyards blocked set unchanged (**13–14**). Quarantine + ARC-PORT-164 untouched.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`.
- `generated` **2026-09-23T11:01:15Z**, **1321** features / **70** shipyards / **156** ports / **103** cities. CRS primary EPSG:3996.
- Synced root/www/public/dist/data + arctic-trade-lanes/{dist,public,data,atlas} + Dataset aliases + `/data/arctictradelanes/` + Zo space `/data/atlas*.{geojson,json}`; restarted `svc_UpoHDo9rDHs` (static atlas only — **no SPA redeploy / App.tsx**).

## Remaining soft preferred
- Cities: CITY-051 Grays Bay; CITY-100 Steensby
- Ports: 086 Wrangell; 127 Nuupiluk; 128 Indiga; 148 Ura Guba; 166 EMO (skip)

## UM
- Health check only; geo-filter left **0.1.4** (no bump).
