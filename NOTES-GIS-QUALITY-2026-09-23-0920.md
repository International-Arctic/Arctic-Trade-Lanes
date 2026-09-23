# GIS Quality Loop — 2026-09-23 ~09:20 MSK

## Outcome
- **Densified ARC-CITY-083 Sørkjosen (Norway / Troms / Nordreisa)** off soft `69.786,20.955` onto OSM **node/843983051** `place=village` `69.7860232,20.9502985` (name: Sørkjosen - Reaššegeahči - Rässikäinen; SSB tettsted 8181; population 826 @2025-01-01). Corroborated **Nominatim** village (Nordreisa), **Wikidata Q1019566 P625** area `69.789167/20.950833`, Wikipedia `69.78583/20.95028`. Distinct from already-dense **ARC-PORT-092** harbour node/5355495279.
- Tag `gis-densify-0920`. Softish shipyards blocked set unchanged (**13–14**). Quarantine + ARC-PORT-164 untouched.
- Preferred soft ports left soft (no new verified pier/harbour this cycle): Hoybukta-060, Wrangell-086, Nuupiluk-127, Indiga-128, Ura Guba-148, EMO-166 (route-pin). Soft cities left: 094 Pyramiden, 096 Colesbukta, 099 Bechevinskaya.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`.
- `generated` **2026-09-23T06:25:39Z**, **1321** features / **70** shipyards / **156** ports / **103** cities. CRS primary EPSG:3996.
- Synced root/www/public/dist/data + Dataset aliases + Zo space assets `/data/atlas*.geojson` — **no SPA redeploy / App.tsx**.

## UM
- No package bump this cycle; geo-filter left as prior **0.1.4** (ATL city densify shipped).

## OSS
- Dataset + Arctic-Trade-Lanes notes/data commits (see cycle report).

