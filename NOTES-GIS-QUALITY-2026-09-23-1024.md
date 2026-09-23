# GIS Quality Loop — 2026-09-23 ~10:24–10:31 MSK (gis-densify-1024)

## Outcome
- **Densified ARC-CITY-096 Colesbukta (incl. Grumant) (Norway / Svalbard / Spitsbergen, Isfjorden south shore)** off soft `78.120,15.150` onto OSM **node/10253369144** `place=hamlet` (abandoned:place=village; name Colesbukta; alt_name Colesdalen) `78.1165817,15.0225494`. Corroborated **Nominatim** hamlet + **way/501142759** center `78.1166315/15.0222348`; Wikidata settlement **Q2982452** P625 area `78.08476/14.86333` (NPDC placename; OSM hamlet currently tags bay Q1108175 — noted, not edited upstream). No separate ARC-PORT Colesbukta/Grumant row; distinct from ARC-PORT-017 Longyearbyen.
- Tag `gis-densify-1024`. Softish shipyards blocked set unchanged (**13–14**). Quarantine + ARC-PORT-164 untouched.
- Preferred soft ports left soft: Hoybukta-060, Wrangell-086, Nuupiluk-127, Indiga-128, Ura Guba-148, EMO-166 (route-pin). Soft cities left: **099 Bechevinskaya** only.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`.
- `generated` **2026-09-23T07:30:45Z**, **1321** features / **70** shipyards / **156** ports / **103** cities. CRS primary EPSG:3996.
- Synced root/www/public/dist/data + Dataset aliases + live `https://arctictradelanes.com/data/atlas.geojson` verified ARC-CITY-096 `[15.022549, 78.116582]` — **no SPA redeploy / App.tsx**.

## UM
- No package bump this cycle; geo-filter left as prior **0.1.4** (ATL city densify shipped).

