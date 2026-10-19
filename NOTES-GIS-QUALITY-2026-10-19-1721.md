# GIS Quality — gis-loop-1019-1721 (~17:21 MSK Europe/Moscow, 2026-10-19)

## Site health
ATL `/` **200** (91208 B, md5 fdba64b6); `/api/health` 200; `/api/x402/schema` 200 2747 B; `/api/x402/status` 200 1363 B;
`/api/alpha/status` 200 888 B. Atlas before change: gen 2026-10-19T13:47:29Z, 1317 feats, EPSG:3996, program-seat land-mask fan 563.
UM home 200 (8019 B); person pages 200 (elon 26183, doug 23217, /hi/ doug 23781, olga 26475, /hi/ olga 26887, olianayda 26475,
durov 23232); DexScreener chips present; hreflang 22; no Recovering/portfolioTree; UM x402 schema 2352, skill 14329, doug json 3433.

## Regression found + fixed: lane water routing
The 13:47:29Z generation (gis-loop-1019-1621) was built with the nested `arctic-trade-lanes/atlas-proj` copy, which has no
`ref/ne_10m_land.geojson`, so `lane_route.route_lanes_on_water` silently skipped: **0 of 25** lanes were `water_routed`
(12:50:43Z gen had 25). Only 14 of 65 atlas dirs got the 13:47 gen. This cycle rebuilt with the **parent** builder
(`ArcticTradeLanes.com/atlas-proj`, has ne_10m_land) and kept the live 13:47 versions of ARC-RAIL-008, ARC-RAIL-009,
ARC-SHIP-073 (neutral wording) and ARC-PORT-157 (overlay in `_sync_gen_1721.py`). Net diff vs 13:47 live =
ARC-PORT-132 + 25 lanes restored to the 12:50 water-routed geometry (byte-identical feature hashes to 12:50 gen).
Future builds: run the parent builder (or add the land ref to the nested copy) — do not build from nested atlas-proj.

## Win
Densified **ARC-PORT-132** Murmansk NSR Container Transshipment Terminal (NewNew Shipping container service; UN/LOCODE RUMMK)
off soft 4-decimal `68.9783 / 33.0680` (= OSM name node/4185004064 Murmansk Commercial Sea Port office / central gate, onshore)
onto **MCSP berth No. 15**: OSM **node/9910923976** `seamark:type=berth seamark:berth:name=15` min depth 10.47 m at
`68.9846667 / 33.0631667` (~0.73 km NNW, bearing ~345°), inside OSM **way/85150513** landuse=industrial
"Мурманский морской торговый порт". Berth 17 (potash return cargo) node/9910923973 ~0.29 km NNW.
Parent ARC-PORT-001 (MCSP yard centroid 68.98092/33.06345) ~0.42 km S, kept separate. Confidence 87→90; facility_site.

## Sources (neutral, public)
- OSM node/9910923976 https://www.openstreetmap.org/node/9910923976 ; way/85150513 ; node/9910923973 ; node/4185004064
- mvestnik.ru #233137 and murmansk.ru/55954 (first NewNew Shipping Line NSR container ship moored at berth 15, Aug 2026;
  container terminal set up in 2025 with Port Alliance support; return potash loading at berth 17)
- abnews.ru 2026-08-21 (specialised container terminal built at berth No. 15); portnews.ru/news/395720; morport.com news
- Row `max_depth_m` 14.5 left unchanged (additive-only); berth seamark depth 10.47 m recorded in note

## Builder / live
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-132 (parent + nested copies)
- ports.csv copies (13): lat/lon + densify note, confidence=90, last_verified=2026-10-19 (`_patch_port132_1721.py`)
- Lock `atlas-proj/check_port132_mcsp_berth15.py` OK; ARC-PORT-113 lock OK
- Atlas gen `2026-10-19T14:30:44.609344+00:00` (17:30:44 MSK), **1317** features, EPSG:3996; land-mask fan 563; 25 water-routed lanes;
  325 old-gen copies (12:50 + 13:47 gens) in 65 dirs replaced; sync_atlas_aliases 10 dirs bad=0;
  live md5 3996 7628d548 / 4326 8991b4ae / manifest 79d4e949
- Also commits nested data/ports.csv parity rows (PORT-035/048/147/157/166/169) that were live in every other copy but stale in git
- **ARC-PORT-157** parity restore (`_restore_port157_1721.py`): all 13 Zo ports.csv copies + 6 git copies had drifted back to the soft
  68.9800/33.0000 (conf 75) while the live atlas and GitHub Dataset carry the gis-port157-0943 Mishukovo densify
  69.0451678/33.0406397 (conf 88); the 0ac26d3 data/ports.csv parity sync briefly carried the stale row — fixed here.
  After restore the parent builder reproduces the live atlas except ARC-RAIL-008/009 + ARC-SHIP-073 wording
  (Dataset CSVs still hold the pre-neutral text; nested repo-root CSVs hold the neutral text) — next cycle: sync those 3 rows.
- No App.tsx smash / SPA redeploy / DNS / x402 / restart.

## Skipped
- ARC-PORT-148 Ura Guba Saam FSU: pin is AIS position of a permanently moored floating storage unit; OSM has no matching
  feature (vessel at anchor in open bay) — not densifiable from OSM; keep.
- PORT-166 (regime entity) / PORT-169 (planned) / PORT-101 previously skipped.

## Next candidates
Next soft 4-decimal ARC-PORT rows after 132/148 (scan ports.csv for 4-decimal lat/lon not yet tagged gis-loop-1019-*).
