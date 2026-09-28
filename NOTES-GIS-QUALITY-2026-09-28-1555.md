# GIS Quality Loop — 2026-09-28 ~15:55 MSK (gis-densify-1555)

## Outcome
- **Densified ARC-PORT-111 Helguvik NATO Fuel Depot Expansion + New 390m Quay** off soft `63.9900,-22.4000` onto OSM **way/1454401176** `landuse=construction` `construction=quay` name="Nýr viðlegukantur í Helguvíkurhöfn" (New berth at Helguvík Harbour). Nominatim centroid `64.0200664/-22.5583966` (extratags `opening_date=2029`).
- Soft→new ≈ **8.41 km** (soft was near Vogar/Hafnargata, not Helguvík cove).
- Corroboration: government.is 2025-11-27 Helguvík NATO fuel depot expansion; arctictoday.com / grapevine.is 390 m quay + 25,000 m³ fuel storage; OSM construction quay named Helguvíkurhöfn matches project.
- Sibling **DISTINCT**: ARC-PORT-109 Port of Reykjanes Keflavik cruise upgrade ~**2.37 km** (Keflavíkurhöfn `industrial=port` relation/19845360) — same Reykjanes Harbour operator, different berth/project (cruise upgrade vs NATO fuel quay).
- Tag `gis-densify-1555` (~15:55 MSK / fire 2026-09-28T12:55Z).
- Not touched: quarantine + ARC-PORT-164; soft ports Nuupiluk-127 / Indiga-128 / Ura Guba-148 / EMO-166 skip; softish shipyards 022/027/029/034/039/052 blockers unchanged; Vard-025 quarantine; Rosatom-075 planned empty.

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-28T13:06:37Z**, **1321** features / **70** shipyards / **156** ports / **103** cities. CRS primary EPSG:3996.
- Synced Dataset atlas/data + site root/www/public/dist/data + arctic-trade-lanes mirrors + `/data/arctictradelanes/` + `/www/atlas` (static atlas only — **no SPA redeploy / App.tsx**).
- Live target: https://arctictradelanes.com/atlas/atlas.manifest.json; ARC-PORT-111 at [-22.558397, 64.020066].

## Tried / deferred this cycle
- Preferred softish shipyards 022/027/029/039/052: prior blockers hold (022 alias of 068 + no named OSM at Bayou Casotte; 027/029 Nominatim empty; 039 wrong subsidiary; 052 planned-only; 034 DEFER).
- Soft ports 127/128/148: still unverifiable / planned-only.
- ARC-PORT-171 Port Elga: named OSM way/1316635669 Порт Эльга already ~0.14 km from soft — skipped (marginal); Helguvik was the material pin error.
- ARC-PORT-041 Mys Shmidta: hamlet/airport only, no harbour geometry.

## Remaining soft preferred
- Cities: _(empty)_
- Ports: 127 Nuupiluk; 128 Indiga; 148 Ura Guba; 166 EMO (skip)
- Softish shipyards: 022, 027, 029, 034 (DEFER), 039, 052; Vard-025 quarantine; Rosatom-075 planned empty

## UM ($UM-Radar)
- `@international-arctic/geo-filter` **0.1.4** left unchanged (no cheap client-side filter win this cycle).
