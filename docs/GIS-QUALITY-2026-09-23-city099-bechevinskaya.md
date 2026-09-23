# GIS Quality Loop — 2026-09-23 ~11:19 MSK (gis-densify-1119)

## Outcome
- **Densified ARC-CITY-099 Bechevinskaya Bay (Petropavlovsk-Kamchatskiy) (Russia / Kamchatka Krai, SE coast)** off soft `53.60,159.53` onto OSM **node/2409941325** `place=locality` (name Бечевинка; alt_name Финвал) `53.273373,159.782166`. Corroborated **Nominatim** locality (Yelizovsky District); Wikidata settlement **Q2412038** P625 `53.2725/159.7844444`; en.wikipedia Bechevinka. **DISTINCT** from ARC-PORT-138 Koryak FSU osm:node/1972086501 `53.249182/159.772754` (~2.8 km).
- Tag `gis-densify-1119`. Softish shipyards blocked set unchanged (**13–14**). Quarantine + ARC-PORT-164 untouched.
- Preferred soft ports left soft: Hoybukta-060, Wrangell-086, Nuupiluk-127, Indiga-128, Ura Guba-148, EMO-166 (route-pin). Soft cities queue **empty** (099 done).

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset` (prior local densify; this cycle sync-only).
- `generated` **2026-09-23T08:26:40Z**, **1321** features / **70** shipyards / **156** ports / **103** cities. CRS primary EPSG:3996.
- Synced root/www/public/dist/data + Dataset aliases + Zo space assets `/data/atlas*.geojson` — **no SPA redeploy / App.tsx**.

## UM
- No package bump this cycle; geo-filter left as prior **0.1.4** (ATL city densify shipped).

## OSS
- Dataset + Arctic-Trade-Lanes notes/data commits (see cycle report).
