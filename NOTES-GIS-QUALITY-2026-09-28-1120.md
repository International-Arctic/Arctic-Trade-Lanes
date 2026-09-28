# GIS Quality Loop — 2026-09-28 ~11:20 MSK (gis-densify-1120)

## Outcome
- **Densified ARC-PORT-167 Petropavlovsk-Kamchatsky Commercial Sea Port (PKMTP)** off soft `53.0000,158.6500` onto OSM **way/106795429** Морской порт Петропавловск-Камчатский landuse=industrial industrial=port port:type=seaport Nominatim centroid `53.0099630/158.6510341`.
- OSM API tags confirmed (222 nodes). Secondary: warehouse way/128722287 `53.0109052/158.6504759` (~0.11 km); office way/442410115 `53.0118091/158.6499110` (~0.22 km).
- No Wikidata P625/P402 on the way (none found for ПКМТП in WD search).
- Soft→new ≈ **1.11 km**.
- Sibling DISTINCT: nearest ARC-PORT-138 Koryak FSU Bechevinskaya Bay ~**79.4 km** (no other ARC-* within 50 km).
- Tag `gis-densify-1120` (~11:20 MSK).
- Soft cities still empty preferred.
- Preferred soft ports left: Nuupiluk-127 / Indiga-128 / Ura Guba-148 / EMO-166 (skip) — not re-litigated.
- Softish shipyards remaining blocked: Vigor-021, VT Halter-022, Eastern-023, Greenland-027, Northern Marine-029, Sembcorp-033, Hyundai-034, Wuchang-039, Kolskaya-052, Zhatay-076, Zvezda-002 (+ Vard-025 quarantine, Rosatom-075 planned empty). Grovfjord-071 already densified (gis-densify-1312). Quarantine + ARC-PORT-164 untouched.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj` (Zo control plane).
- `generated` **2026-09-28T08:31:34Z**, **1321** features / **70** shipyards / **156** ports / **103** cities. CRS primary EPSG:3996.
- Synced Dataset atlas/data + site root/www/public/dist/data + arctic-trade-lanes mirrors + `/data/arctictradelanes/` (static atlas only — **no SPA redeploy / App.tsx**).
- Live target: https://arctictradelanes.com/atlas/atlas.manifest.json; ARC-PORT-167 at [158.651034, 53.009963] / EPSG:3996 [1529977.752, 3914302.403].

## Remaining soft preferred
- Cities: _(empty preferred)_
- Ports: 127 Nuupiluk; 128 Indiga; 148 Ura Guba; 166 EMO (skip)
- Softish shipyards: 021–023, 027, 029, 033–034, 039, 052, 076, Zvezda-002

## UM
- Health check only; geo-filter left **0.1.4** (no bump unless real filter improvement).
