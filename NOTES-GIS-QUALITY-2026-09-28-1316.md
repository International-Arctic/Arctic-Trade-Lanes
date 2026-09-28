# GIS Quality Loop — 2026-09-28 ~13:16 MSK (gis-densify-1316)

## Outcome
- **Densified ARC-SHIP-033 Sembcorp Marine (Arctic Capabilities)** off soft `1.2600,103.8300` onto OSM **way/1004233134** `landuse=industrial` Sembcorp Marine Tuas Boulevard Yard (alt_name Sembcorp Marine Tuas Shipyard; old_name Sembcorp Marine Integrated Yard). Nominatim centroid `1.2543436/103.6130677`.
- Corroboration: official yard page https://www.sembmarine.com/our-global-network/singapore-hub/sembcorp-marine-tuas-boulevard-yard; Seatrium Limited WD **Q7449144** (corporate entity; no yard-level P625).
- Soft→new ≈ **24.12 km**.
- Sibling DISTINCT: no other ARC-SHIP within 50 km.
- Tag `gis-densify-1316` (~13:16 MSK).
- Preferred soft ports left soft (not re-litigated): Nuupiluk-127 / Indiga-128 / Ura Guba-148 / EMO-166 (skip).
- Softish shipyards remaining blocked: Vigor-021, VT Halter-022, Eastern-023, Greenland-027, Northern Marine-029, Hyundai-034 (sibling ARC-SHIP-058 misplaced — deferred), Wuchang-039, Kolskaya-052, Zhatay-076 (+ Vard-025 quarantine, Rosatom-075 planned empty). Quarantine + ARC-PORT-164 untouched.
- Alternate Nominatim probes this cycle (empty / blocked): Vigor Seattle, Wuchang Wuhan, Eastern Panama City, VT Halter Pascagoula, Zhatay Yakutsk, Kolskaya Murmansk, Northern Marine Anchorage.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-28T10:21:55Z**, **1321** features / **70** shipyards / **156** ports / **103** cities. CRS primary EPSG:3996.
- Synced Dataset atlas/data + site root/www/public/dist/data + arctic-trade-lanes dist/public (+ /atlas) + `/data/arctictradelanes/` + Zo space assets (static atlas only — **no SPA redeploy / App.tsx**). Restarted `svc_UpoHDo9rDHs`.
- Live target: https://arctictradelanes.com/atlas/atlas.manifest.json; ARC-SHIP-033 at [103.613068, 1.254344].

## Remaining soft preferred
- Cities: _(empty preferred)_
- Ports: 127 Nuupiluk; 128 Indiga; 148 Ura Guba; 166 EMO (skip)
- Softish shipyards: 021–023, 027, 029, 034, 039, 052, 076

## UM ($UM-Radar)
- `@international-arctic/geo-filter` **0.1.4** smoke left unchanged (no filter gap found).
