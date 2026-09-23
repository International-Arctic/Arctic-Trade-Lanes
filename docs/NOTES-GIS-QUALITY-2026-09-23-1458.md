# GIS Quality Loop — 2026-09-23 ~14:58 MSK (gis-densify-1458)

## Outcome
- **Densified ARC-PORT-173 Ningbo-Zhoushan Port (NSR China–Europe container gateway)** off soft `29.8700,121.5500` onto OSM **way/172381552** `landuse=industrial` `industrial=port` (name 宁波舟山港股份有限公司北仑第二集装箱码头分公司 / Ningbo-Zhoushan Port Co. Beilun Second Container Terminal) `29.9392024/121.8373241`.
- Wikidata **Q1703245** Port of Ningbo-Zhoushan P625 `29.93333333/121.83333333` corroborates (~0.7 km). Soft→new ≈ **28.7 km**.
- Sole China ATL port row — no sibling conflation.
- Tag `gis-densify-1458` (~14:58 MSK).
- Preferred soft ports left unchanged (no new named 6-Mile / cape / FSU / Nuupiluk geometry): Wrangell-086 / Nuupiluk-127 / Indiga-128 / Ura Guba-148 / EMO-166 (skip).
- Softish shipyards blocked set unchanged (**13–14**; Ulstein #37 still needs OSM `industrial=shipyard`). Quarantine + ARC-PORT-164 untouched.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`.
- `generated` **2026-09-23T12:12:31Z**, **1321** features / **70** shipyards / **156** ports / **103** cities. CRS primary EPSG:3996.
- Synced root/www/public/dist/data + arctic-trade-lanes/{dist,public,data,atlas} + Dataset aliases + `/data/arctictradelanes/` + Zo space `/data/atlas*.{geojson,json}`; restarted `svc_UpoHDo9rDHs` (static atlas only — **no SPA redeploy / App.tsx**).

## Remaining soft preferred
- Cities: _(empty)_
- Ports: 086 Wrangell; 127 Nuupiluk; 128 Indiga; 148 Ura Guba; 166 EMO (skip)

## UM
- Health check only; geo-filter left **0.1.4** (no bump).
