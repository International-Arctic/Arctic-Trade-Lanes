# GIS Quality Loop — 2026-09-23 ~13:25 MSK (gis-densify-1325)

## Outcome
- **Densified ARC-CITY-007 Tiksi (Russia / Sakha Republic)** off soft `71.64,128.86` onto Wikidata **Q500895** P625 `71.636836111111/128.86793333333` (Тикси urban-type settlement). Corroborated OSM Nominatim **relation/3971161** `place=town` name=Тикси `71.6366294/128.8682510` (wikidata=Q500895). **DISTINCT** from ARC-PORT-006 Tiksi Sea Port `[128.890727, 71.645377]` ~1.25 km and ARC-PORT-036 Tiksi East Port `[128.95, 71.68]` ~5.6 km.
- Tag `gis-densify-1325` (~13:25 MSK / fired ~10:25Z).
- **Indiga ARC-PORT-128 left soft**: Cape Bolshoy Rumyanichny (мыс Большой Румяничный) has ru.wikipedia DMS `67°32′59″N 47°51′08″E` (~67.5497/47.8522) and project sources place the planned harbour ~50 km west of village Indiga — but **no OSM/Nominatim feature and Wikidata port Q86679105 has no P625**. Village Indiga (Q3798263 / OSM node/1731320627 `67.655231/49.037071`) ≠ Cape site. Hard rule: densify only with verifiable OSM/Nominatim/Wikidata geo.
- **Ura Guba ARC-PORT-148 left soft**: village Ура-Губа OSM way/83361500 `69.291389/32.793522` (Q4411417) ≠ FSU terminal soft `69.16/33.42`; Overpass pier/FSU hunt timed out / no harbour geometry found.
- Softish shipyards blocked set unchanged (**13–14**). Quarantine + ARC-PORT-164 untouched. Wrangell-086 / Nuupiluk-127 / EMO-166 skipped per cycle rules.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`.
- `generated` **2026-09-23T10:36:17Z**, **1321** features / **70** shipyards / **156** ports / **103** cities. CRS primary EPSG:3996.
- Synced root/www/public/dist/data + arctic-trade-lanes/{dist,public,data} + Dataset aliases + `/data/arctictradelanes/` + Zo space assets; restarted `svc_UpoHDo9rDHs` (static atlas only — **no SPA redeploy / App.tsx**).

## Remaining soft preferred ports
- Wrangell-086 (6-Mile Mill — no pier OSM)
- Nuupiluk-127 (planned; Nominatim cape risk)
- Indiga-128 (Cape Rumyanichny — needs OSM cape/harbour node or Wikidata P625)
- Ura Guba-148 (needs FSU/pier OSM, not village)
- EMO-166 (route-pin — skip)

## Remaining soft cities (live ≤2dp after this win)
- ARC-CITY-009 Khatanga `71.98/102.47` (OSM relation/18023381 available)
- ARC-CITY-051 Grays Bay (port site) `67.87/-110.92`
- ARC-CITY-100 Steensby Inlet `71.96/-79.6`

## UM
- Health check only; geo-filter left **0.1.4** (no bump).
