# GIS Quality Loop — 2026-09-23 ~09:48 MSK

## Outcome
- **Densified ARC-CITY-094 Pyramiden (Norway / Svalbard / Spitsbergen, Billefjorden)** off soft `78.655,16.333` onto OSM **node/273476498** `place=village` (abandoned:place=village; name Пирамида) `78.6558220,16.3228695`. Corroborated **Nominatim** village (Svalbard), **Wikidata Q845396 P625** `78.656111/16.325`. Distinct from already-present **ARC-PORT-150** Pyramiden Port ~`78.6567/16.3250` and peak node/9887055697 (Q31538635).
- Tag `gis-densify-0948`. Softish shipyards blocked set unchanged (**13–14**). Quarantine + ARC-PORT-164 untouched.
- Preferred soft ports left soft: Hoybukta-060, Wrangell-086, Nuupiluk-127, Indiga-128, Ura Guba-148, EMO-166 (route-pin). Soft cities left: 096 Colesbukta, 099 Bechevinskaya.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`.
- `generated` **2026-09-23T06:53:45Z**, **1321** features / **70** shipyards / **156** ports / **103** cities. CRS primary EPSG:3996.
- Synced root/www/public/dist/data + Dataset aliases + Zo space assets `/data/atlas*.geojson` — **no SPA redeploy / App.tsx**.

## UM
- No package bump this cycle; geo-filter left as prior **0.1.4** (ATL city densify shipped).

## OSS
- Dataset + Arctic-Trade-Lanes notes/data commits (see cycle report).
