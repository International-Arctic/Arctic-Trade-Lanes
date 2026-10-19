# GIS Quality Loop gis-loop-1019-1837 (2026-10-19 ~18:37-18:55 MSK)

## Health (before)
- ATL: home 200 91208 (md5 fdba64b6); /api/health ok; x402 status 1363 / schema 2747; alpha 888 keyConfigured=false.
  Live atlas gen `2026-10-19T15:03:53.217382+00:00`, 1317 feats, EPSG:3996, md5 3996 f8447f78 / 4326 e56790f4
  (= gis-loop-1019-1758 output); 25/25 lanes water_routed; land-mask fan 563; display_offset 131.
- UM: home 200 8019 md5 83e8388a, bundle index-CIQoD7he.js + index-DZdhQ1Nj.css, hreflang 22; elon 26183, doug 23217,
  hi/doug 23781, olga 26475 (= olianayda), hi/olga 26887, durov 23232, schema 2352, st_doug 2537 vs st_ma 2317,
  doug_json 3433 (only `generated` changed), skill 14329; no Recovering/portfolioTree. All md5-identical to 1758.
- Zo nested ATL HEAD dd99be1c4 == GitHub International-Arctic/Arctic-Trade-Lanes main.

## Win: Dataset neutral-text sync + ARC-PORT-079/066 cross-reference (owner decisions 2026-10-19)
- Live neutral wording is the official text for ARC-RAIL-008, ARC-RAIL-009, ARC-SHIP-073. Dataset CSVs synced to it:
  - ARC-RAIL-008 `key_benefits` (Zo Dataset rail_corridors.csv; GitHub Dataset already in sync).
  - ARC-RAIL-009 `status` + `sources` text from live (Zo Dataset); latitude/longitude 62.8981/135.3215, confidence 93 and
    last_verified 2026-09-06 kept from the Zo Dataset (owner decision). GitHub Dataset already had the live text but
    conf 92 / 2026-09-05; set to 93 / 2026-09-06 for parity.
  - ARC-SHIP-073 `arctic_vessel_capability` (Zo Dataset + ArcticTradeLanes.com/data copies; nested ATL + GitHub Dataset already in sync).
- ARC-PORT-079 (Skarfabakki berth/quay) and ARC-PORT-066 (Vör terminal building) cross-referenced as the same Reykjavík
  cruise terminal; kept as SEPARATE features (not merged). Note appended to both builder `position_note` entries and to
  the ports.csv `sources` cell of both rows. No coordinate changes.
- Script: `atlas-proj/_patch_neutral_xref_1837.py` (line-level edits, idempotent; 17 CSV + 2 builder files on Zo).

## Atlas regression gate (`atlas-proj/_sync_gen_1837.py`)
- Built ONLY from parent `ArcticTradeLanes.com/atlas-proj` (ref/ne_10m_land.geojson present). **No live overlay needed
  any more**: raw build reproduces live RAIL-008 + SHIP-073 byte-for-byte.
- 25 lanes water-routed (land km 30601 -> 3774), admin-seat fan 563 / 65 seats land-fanned, ship water fan 101.
- Gate PASS on 3996/4326/wgs84/geojson: ids + order identical; top-level identical except `generated`; 1317 feats;
  diffs ONLY ARC-PORT-066 + ARC-PORT-079 (`position_note`) and ARC-RAIL-009 (`confidence` 92->93, `verified`
  2026-09-05 -> 2026-09-06); display_offset 131 == live; geometry of ports 012/025/039/065/066/079/104/107/109/113/114/
  119/132/134/140/157/158/159/160/165 unchanged.
- Live gen `2026-10-19T15:43:15.601866+00:00` (18:43:15 MSK), 1317 feats, EPSG:3996; md5 3996 b47b27ce / 4326 fec5483a;
  320 old-gen copies in 64 dirs replaced; sync_atlas_aliases 10 dirs bad=0. Box diff old vs new live: only 066/079/RAIL-009.
- No App.tsx smash / SPA redeploy / DNS / x402 / restart.

## Next candidates
ARC-PORT-068 Whittier Delong Dock, 082 Whittier ARRC, 083 Lumina White Mountain (Qartorqsuaq), 139 Tromsø (one named quay),
091 Qaqortoq expansion, 073 Arkhangelsk deep-water, 128 Indiga (planned). Parked: 129, 135, 148, 166, 169, 101.
Observation: 066 carries UN/LOCODE ISREY, 079 ISREK (both Reykjavík codes) - left as-is, worth an owner check.
