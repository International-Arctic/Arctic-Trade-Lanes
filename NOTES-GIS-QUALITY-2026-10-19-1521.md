# GIS Quality — gis-loop-1019-1521 (~15:21 MSK Europe/Moscow, 2026-10-19)

## Site health
ATL `/` **200** (91208 B, md5 fdba64b6); `/atlas.3996.geojson` 200 (1317 feats, gen 2026-10-19T11:52:01Z before rebuild, EPSG:3996);
`/api/health` 200 ok, `/api/x402/schema` 200 2747 B, `/api/x402/status` 200 1363 B, `/api/alpha/status` 200 888 B, `/data/ports.csv` 200.
UM home 200 (8019 B, md5 83e8388a), bundle `index-CIQoD7he.js` + `index-DZdhQ1Nj.css`; person pages 200 (elon 26183, doug 23217,
olga 26475, durov 23232; /hi/ doug 23781 Devanagari 293, /hi/ olga 26887 Devanagari 234); no Recovering/portfolioTree;
UM x402 schema 2352, status doug 2537, doug json 3433, skill 14329. Zo nested ATL == GitHub main **e6e170ccc** before change.

## Skipped
- ARC-PORT-166 Unified Northern-Supply Sea Route: regulated-tariff regime across Anadyr/Pevek/Tiksi, not a single facility.
- ARC-PORT-169 Korf Bay hub (VLT KORF): Phase 1 construction agreement only (Sep 2026); no built/mapped facility.
- ARC-PORT-101 Clyde River Small Craft Harbour: new basin not yet mapped in OSM (only town/tank-farm features within 2.5 km).
- PORT-129/135 parked, PORT-139 deferred (unchanged).

## Win
Densified **ARC-PORT-104** Narvik Port Dock 5 New Shiploader (LKAB, UN/LOCODE NONVK) off soft 4-decimal `68.4205 / 17.4332`
(onshore in Narvik town, ~0.4 km from ARC-PORT-136 Kleiva; not on the ore harbour). New anchor: shoelace centroid of OSM
`man_made=crane building=yes name=Malmuskippingsanlegg` **way/104708054** (~1500 m² loader footprint on LKAB quay 5 pier
way/1113478606, western tip of the LKAB ore harbour) at `68.4300757 / 17.3881101`. Moved **~2.13 km** WNW (bearing ~300°).
Quay 7 identification: OSM crane way/1113478612 on pier way/1113478609 (68.4304/17.3999) matches the public "LKAB Kai 7" place
68.430417/17.400040 within ~7 m, so the western loader is quay 5 (U5) by elimination (~0.48 km apart).

## Sources (neutral, public)
- OSM way/104708054, way/1113478606, way/1113478612, way/1113478609 (openstreetmap.org)
- LKAB news 2022-11-02 "New ship loader for continues stable deliveries" (quay 5 loader from 1977, SEK 500M replacement; quay 7 redundant loader 2016)
- LKAB news 2025-09-24 "Shift change after 50 years" (new U5 moored/assembled at quay 5; old slewing base kept and renovated, same place)
- LKAB press 2025-11-27 (inaugurated 27 Nov 2025; part of SEK 5B programme through 2029)
- Sarens 2026-01-15 install note (2,900 t old loader removed, 2,200 t new loader installed)
- DigitaltMuseum / Museum Nord photos of LKAB kai 5 + kai 7 (2016, 2017)
- Parent ARC-PORT-019 Narvik Port (68.4294644/17.4239955) ~1.47 km E kept separate; no Wikidata item for the loader
- `position_quality=facility_site`; confidence 95 → 96

## Builder / live
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-104 (parent + nested builder copies)
- ports.csv copies (15 incl. Dataset clone): lat/lon + densify note, confidence=96, last_verified=2026-10-19
- Patch `atlas-proj/_patch_port104_1521.py`; lock `atlas-proj/check_port104_narvik_lkab_quay5.py`; PORT-105…171 locks OK
- Built with the **parent** builder (has `ref/ne_10m_land.geojson`) to /tmp/atl_new_1521; diff vs 11:52:01Z = ARC-PORT-104 only;
  land-mask fan 563 intact, ship water fan 101
- Atlas gen `2026-10-19T12:30:44.007249+00:00`; 1317 features, EPSG:3996; sync_atlas_aliases.sh 10 dirs bad=0;
  260 old-gen copies in 52 dirs replaced; md5 3996 ec0d629e / wgs84 7adb4d69 (live verified)
- No App.tsx smash / SPA redeploy / DNS / x402 / restart.

## Next candidates
PORT-107 Juneau USCG homeport pier (58.3019/-134.4197), PORT-113 Port of Alaska Terminal 1 (61.2447/-149.8817),
PORT-132 Murmansk NSR container terminal (68.9783/33.0680), PORT-148 Ura Guba (69.3375/32.9273), PORT-101 Clyde River (when mapped).
