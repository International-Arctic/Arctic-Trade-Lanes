# GIS Quality Loop — 2026-09-28 ~09:26 MSK (gis-densify-0926)

## Outcome
- **Densified ARC-PORT-086 Wrangell Deepwater Port (6-Mile Mill site)** off soft `56.3850,-132.3550` onto OSM **way/240047996** `landuse=industrial` (unnamed industrial polygon on Zimovia Highway / former Alaska Pulp–Silver Bay mill site) centroid `56.3961351/-132.3404270`.
- City of Wrangell Reliant appraisal **22-0340** Mile 6 Zimovia Highway geo coords `56.395815/-132.337955` corroborates (~0.16 km; wrangell.com PDF). Soft→new ≈ **1.53 km**.
- Sibling **ARC-CITY-079 Wrangell** `56.4708/-132.3767` DISTINCT ~8.6 km; downtown Wrangell Harbor marina OSM way/1163706231 ~8.0 km — not conflated.
- Tag `gis-densify-0926` (~09:26 MSK).
- Preferred soft ports left: Nuupiluk-127 / Indiga-128 / Ura Guba-148 / EMO-166 (skip). Indiga Cape Rumyanichny still lacks named OSM/WD cape geometry (settlement ≠ cape; GEM: cape ~50 km west of Indiga Bay).
- Softish shipyards blocked set unchanged (13–14). Quarantine + ARC-PORT-164 untouched.
- Prior 2026-09-25 routine failure: live atlas/dataset verified healthy before edit (manifest gen was 2026-09-23T12:12:31Z; ports.csv + atlas consistent).

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`.
- `generated` **2026-09-28T06:27:01Z**, **1321** features / **70** shipyards / **156** ports / **103** cities. CRS primary EPSG:3996.
- Synced Dataset atlas/data + site root/www/public/dist/data + arctic-trade-lanes mirrors + `/data/arctictradelanes/` + `/www/atlas` (static atlas only — **no SPA redeploy / App.tsx**).

## Remaining soft preferred
- Cities: _(empty)_
- Ports: 127 Nuupiluk; 128 Indiga; 148 Ura Guba; 166 EMO (skip)

## UM
- Health check only; geo-filter left **0.1.4** (no bump).
