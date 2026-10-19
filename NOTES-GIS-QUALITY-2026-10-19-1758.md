# GIS Quality Loop gis-loop-1019-1758 (2026-10-19 ~17:58-18:15 MSK)

## Health (before)
- ATL: home 200 91208; /api/health ok; x402 status 1363 / schema 2747; alpha 888 keyConfigured=false.
  Live atlas gen `2026-10-19T14:30:44.609344+00:00`, 1317 feats, EPSG:3996, md5 3996 7628d548 / 4326 8991b4ae
  (byte-identical to the gis-loop-1019-1721 output); 25/25 route-masked lanes water_routed; land-mask fan 563.
  PORT-104/107/113/119/132/157/159/160/165 at their densified coordinates.
- UM: home 200 8019 md5 83e8388a, bundle index-CIQoD7he.js + index-DZdhQ1Nj.css, hreflang 22; elon 26183, doug 23217,
  hi/doug 23781 (Devanagari 293), olga 26475 (= olianayda), hi/olga 26887 (Devanagari 234), durov 23232, schema 2352,
  st_doug 2537 vs st_ma 2317, doug_json 3433 (only `generated` changed), skill 14329; no Recovering/portfolioTree.
- Zo nested ATL HEAD d0395481f == GitHub International-Arctic/Arctic-Trade-Lanes main.

## Win: ARC-PORT-079 Reykjavík Vör Cruise Terminal (Skarfabakki 312, Viðeyjarsund; ISREK)
- Soft `64.1628 / -21.8514` (4-decimal) sat **on Viðey island** (OSM relation/8385552), ~0.27 km NE of the Viðey ferry
  landing node/4451609056, across Viðeyjarsund from the cruise quay.
- New `64.1550151 / -21.8620629` (~1.01 km SSW): length-weighted midpoint of OSM [way/108336302](https://www.openstreetmap.org/way/108336302)
  `highway=service access=no name=Skarfabakki` (542 m quay-apron road along the Skarfabakki berth face, Sundahöfn).
- Corroboration: Faxaports Port Information Guide: Skarfabakki 650 m, 12.0 m MLWS, cruise/general cargo/bulk/trawlers, ISPS;
  iceland-highlights.com: Skarfabakki 312 = main cruise berth with the Vör terminal (64°09.0'N 021°51.7'W, ~0.55 km).
- Sibling ARC-PORT-066 (Vör terminal building, OSM way/1391146178) ~0.15 km NW kept separate (near-duplicate entity; 079 = berth).
- position_quality=facility_site; confidence 80 -> 85; max_depth left empty.
- `atlas-proj/_patch_port079_1758.py`: 13 ports.csv copies + 2 builders.

## Atlas regression gate (`atlas-proj/_sync_gen_1758.py`)
- Built ONLY from parent `ArcticTradeLanes.com/atlas-proj` (ref/ne_10m_land.geojson present): 25 lanes water-routed
  (land km 30601 -> 3774), admin-seat fan 563 / 65 seats land-fanned, ship water fan 101.
- Raw build vs live: ARC-PORT-079 + the known ARC-RAIL-008/009 + ARC-SHIP-073 wording drift (Dataset CSVs hold the
  pre-neutral text). Overlaid those 3 from live (as in 1721).
- Post-overlay gate PASS on 3996/4326/wgs84/geojson: only ARC-PORT-079 differs; ids + order identical; top-level identical
  except `generated`; 1317 feats; water_routed 25; position_fan_mask 563; display_offset 131 == live; PORT-066/104/107/113/114/
  119/132/134/140/157/158/159/160/165 identical.
- Live gen `2026-10-19T15:03:53.217382+00:00` (18:03:53 MSK), 1317 feats, EPSG:3996; md5 3996 f8447f78 / 4326 e56790f4;
  320 old-gen copies in 64 dirs replaced; sync_atlas_aliases 10 dirs bad=0. Box-side diff of old vs new live: only ARC-PORT-079.
- No App.tsx smash / SPA redeploy / DNS / x402 / restart.

## Open
- Input drift: ARC-RAIL-008/009 + ARC-SHIP-073 text in Dataset CSVs != live neutral wording (needs a canonical-wording
  decision; until then every build needs the overlay).

## Next candidates
ARC-PORT-068 Whittier Delong Dock, 082 Whittier ARRC, 083 Lumina White Mountain (Qartorqsuaq), 139 Tromsø (one named quay),
091 Qaqortoq expansion, 073 Arkhangelsk deep-water, 128 Indiga (planned). Parked: 129, 135, 148, 166, 169, 101.
