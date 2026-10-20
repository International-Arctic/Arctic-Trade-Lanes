# GIS Quality Loop gis-loop-1020-0913 (2026-10-20 ~09:13 MSK)

## Health (before)
- ATL: home 200 91208 (md5 fdba64b6, = baseline); /api/health ok; x402 status 1363 / schema 2747 (= baseline); alpha 888 keyConfigured=false.
  Live atlas gen `2026-10-19T15:43:15.601866+00:00`, 1317 feats, EPSG:3996, md5 3996 b47b27ce / 4326 fec5483a (= gis-loop-1019-1837);
  25/25 lanes water_routed; land-mask fan 563; display_offset 131.
- UM: home 200 8019 md5 83e8388a (= baseline), hreflang 22; schema 2352, st_doug 2537 vs st_ma 2317, doug_json 3433, skill 14329 (= baseline);
  no Recovering/portfolioTree; DexScreener present. Person/radar pages +1684 B each vs 1019-1837 = additive "Affiliate & Partner Links"
  section (#um-affiliates; already present at the 07:04 MSK watchdog) - not a breakage.

## Win: Reykjavík UN/LOCODE (owner decision 2026-10-19)
- Official UNECE UN/LOCODE list for Iceland, https://service.unece.org/trade/locode/is.htm :
  `IS REY | Reykjavík | Function 1------- (port) | Status AC | Date 0212 | IATA REK | 6409N 02157W`.
  There is NO `IS REK` entry (REK is Reykjavík's IATA city code). Official Reykjavík code = **ISREY**.
- ARC-PORT-079 (Skarfabakki berth/quay) `unlocode` ISREK -> ISREY; ARC-PORT-066 (Vör terminal building) already ISREY (confirmed).
  Both stay SEPARATE features, cross-referenced as the same Reykjavík cruise terminal. No coordinate / confidence / last_verified change.
- ports.csv (13 copies on Zo incl. Dataset): 079 unlocode cell + UNECE verification note appended to `sources` of 066 and 079.
  builder `position_note` of 079: "UN/LOCODE ISREK" -> "UN/LOCODE ISREY" + correction note. Script `atlas-proj/_patch_unlocode_0913.py`.

## Atlas regression gate (`atlas-proj/_sync_gen_0913.py`)
- Built only from parent `ArcticTradeLanes.com/atlas-proj` (ref/ne_10m_land.geojson present), no overlay.
- 25 lanes water-routed (land km 30601 -> 3774), admin-seat fan 563 / 65 seats land-fanned, ship water fan 101.
- Gate PASS on 3996/4326/wgs84/geojson: ids + order identical; top-level identical except `generated`; 1317 feats; the ONLY diff is
  ARC-PORT-079 (`unlocode`, `position_note`); ARC-PORT-066, RAIL-008/009, SHIP-073 equal to live; display_offset 131 == live; geometry of
  ports 012/025/039/053/065/066/079/089/093/104/107/109/113/114/119/132/134/140/157/158/159/160/165 unchanged.
- Live gen `2026-10-20T06:18:42.855823+00:00` (09:18:42 MSK), 1317 feats, EPSG:3996; md5 3996 2a2ccabe / 4326 907cfbc2 / manifest 703c927c;
  320 old-gen copies in 64 dirs replaced; sync_atlas_aliases 10 dirs bad=0. Box diff old vs new live: only ARC-PORT-079.
- Live /data/ports.csv serves ISREY for both rows.
- No App.tsx smash / SPA redeploy / DNS / x402 / restart.

## Not changed (observation)
- Static factpages `arctic-trade-lanes/factpages/*/port/reykjavik-vor-cruise-terminal.html` still show ISREK and the pre-1758 soft coords
  64.1628/-21.8514; they are not served live (404) and were left untouched.
