# GIS Quality Loop — 2026-09-23 ~12:54 MSK (gis-densify-1254)

## Outcome
- **Densified ARC-PORT-060 Kirkenes Hoybukta Vest New Transshipment Port (planned) (Norway / Sør-Varanger)** off soft `69.73,29.95` onto OSM **node/9880257803** `place=hamlet` name=Høybukta `69.7288566,29.8761941` (SSR stedsnr 982833; loc_name:se Nuovusgohppi). Corroborated **Nominatim** hamlet; Wikidata settlement **Q101110825** P625 `69.72886/29.87623`; nearby bay **Q101124669** Høybukta (Korsfjorden) P625 `69.73107/29.88016`. **No OSM pier/quay yet** for the planned Vest deep-water quay — pin = named Høybukta locality (planned site). **DISTINCT** from ARC-PORT-015 Kirkenes Port `[30.071781, 69.727887]` ~7.5 km; ARC-PORT-076 `[30.041701, 69.728621]` ~6.4 km; ARC-PORT-097 `[30.034853, 69.726774]` ~6.1 km.
- Tag `gis-densify-1254`. Softish shipyards blocked set unchanged (**13–14**). Quarantine + ARC-PORT-164 untouched.
- Soft cities queue still **empty**. Soft ports left: Wrangell-086, Nuupiluk-127, Indiga-128, Ura Guba-148, EMO-166 (route-pin).

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`.
- `generated` **2026-09-23T10:00:46Z**, **1321** features / **70** shipyards / **156** ports / **103** cities. CRS primary EPSG:3996.
- Synced root/www/public/dist/data + Dataset aliases + `/data/arctictradelanes/` + live `https://arctictradelanes.com/data/atlas.4326.geojson` verified ARC-PORT-060 `[29.876194, 69.728857]` — **no SPA redeploy / App.tsx**.

## UM
- No package bump this cycle; geo-filter left as prior **0.1.4** (ATL port densify shipped).
