# GIS Quality Loop — 2026-09-29 ~13:20 MSK (gis-densify-1320)

## Outcome
- **Densified ARC-PORT-128 Indiga Deep-Water Arctic Port (Cape Rumyanichny, Nenets AO)** off soft `67.6,49.0` (Indiga *village* / UNLOCODE RUIDG centroid; WD Q3798263 P625 ~67.6583/49.0164) onto **ruwiki Порт Индига** site — southern side of **мыс Большой Румяничный (Cape Bolshoy Rumyanichny)** **67°32′59″N 47°51′08″E = 67.5497/47.8522**.
- Soft→new ≈ **49.01 km** west (village≠port site; name already said Cape Rumyanichny).
- Corroboration: GEM Port of Indiga (Cape Rumyanichny ~50 km W of Indiga Bay/village); Kremlin/Gov Gekht ice-free deep-water bay notes already in sources.
- **DISTINCT**: WD Q3798263 Indiga settlement ~49 km E (soft pin was that conflation); nearest other ATL port ARC-PORT-073 Arkhangelsk ~456.5 km. No second Indiga port row.
- Tag `gis-densify-1320` (~13:20 MSK). CI lock `check-port128-indiga-densify.mjs`.
- Soft cities empty. Soft ports remaining: **127 Nuupiluk**; skip 166 EMO. Softish shipyards 022/027/029/034 DEFER/039/052 blocked; Vard-025 quarantine; Rosatom-075 planned empty; Sevgiprorybflot-069 Issue #34; quarantine + ARC-PORT-164 untouched. Soft industry still open: 006, 008, 317, 321, 322, 324, 352 (near-dup FAC-005), 353, 354, 356 Skaergaard WD-only optional (~3.67 km Q1970121).

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-29T10:18:50Z**, **1321** features / ports **156** / shipyards **70** / cities **103** / industry **110**. CRS primary EPSG:3996.
- Static atlas aliases synced (Dataset atlas/data + site root/www/public/dist + arctic-trade-lanes dist/public/www + `/data/arctictradelanes/`) — **no SPA redeploy / App.tsx**. Restarted `svc_UpoHDo9rDHs`.

## UM ($UM-Radar)
- `@international-arctic/geo-filter` **0.1.4** left unchanged (ATL densify win shipped; UM no bump).
