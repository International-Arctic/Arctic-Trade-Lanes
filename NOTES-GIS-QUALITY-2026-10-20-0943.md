# GIS Quality Loop gis-loop-1020-0943 (2026-10-20 ~09:43 MSK)

## Health (before)
- ATL: home 200 91208 (md5 fdba64b6); /api/health ok; x402 status 1363 / schema 2747; alpha 888 keyConfigured=false.
  Live atlas gen 2026-10-20T06:18:42Z, 1317 feats, EPSG:3996, md5 3996 2a2ccabe / 4326 907cfbc2; 25/25 lanes water_routed; fan mask 563; display_offset 131.
- UM: home 200 8019 md5 83e8388a, hreflang 22; no Recovering/portfolioTree; DexScreener chips on radar/person pages; all key pages byte-identical to 09:13.
- Zo nested ATL HEAD b957b5a7a == GitHub main.

## Win: ARC-PORT-083 Lumina White Mountain Mine Port (Qartorqsuaq)
- Soft 66.5369/-52.3091 == OSM node/12615395211 natural=peak name=Qaqortorsuaq (summit), ~10.9 km WSW of the port.
- New 66.5576559/-52.0679314: length-weighted midpoint of OSM way/1362676696 man_made=quay (76 m), beside way/1362676698 industrial=port,
  way/1362676699 pier, way/1362676697 warehouse, node/12615366365 man_made=mine operator=Lumina.
- Corroboration: DCE/GINR TR353 (plant close to the coast and the harbour, shipped through Kangerlussuaq Fjord); Hudson White Mountain EIA 2015 (~66 33N 52 10W, incl. port).
- facility_site; confidence 85 unchanged; last_verified 2026-10-20; 13 ports.csv copies + 2 builders (_patch_port083_0943.py).

## Gate (_sync_gen_0943.py)
- Parent atlas-proj (ref/ne_10m_land present). 25 lanes water-routed (land km 30601 -> 3774), fan 563 / 65 seats, ship water fan 101.
- PASS on 3996/4326/wgs84/geojson: only ARC-PORT-083 differs (geometry + position_quality/note/anchor); ids/order/top-level identical; 1317; display_offset 131;
  fixed ports (039/113/132/157 Mishukovo 69.0451678/33.0406397, 079 Skarfabakki 64.1550151/-21.8620629, 066, 068 ...) unchanged.
- Live gen 2026-10-20T06:55:31.792422Z, md5 3996 44198823 / 4326 87d25a26 / manifest 4a39a9a5; 320 copies in 64 dirs; aliases 10 dirs bad=0.
- No App.tsx smash / SPA redeploy / DNS / x402 / restart.
