# GIS Quality — gis-loop-1019-1446 (~14:46 MSK Europe/Moscow, 2026-10-19)

## Site health
ATL `/` **200** (91208 B, md5 fdba64b6); `/atlas.3996.geojson` 200 (1317 feats, gen 2026-10-19T11:20:15Z before rebuild, EPSG:3996;
program seat land-mask fan 563 `position_fan_mask=ne_10m_land`, ship water fan 101, 25 water-routed lanes); `/api/health` 200 ok,
`/api/x402/schema` 200 2747 B, `/api/x402/status` 200 1363 B, `/api/alpha/status` 200 888 B keyConfigured=false, `/pricing` 200 (x402/USDC).
UM home 200 (8019 B, md5 83e8388a), bundle `index-CIQoD7he.js` + `index-DZdhQ1Nj.css`; hreflang 22; person pages 200
(elon 26183, doug 23217, olga 26475, durov 23232; /hi/ doug 23781 Devanagari 293, /hi/ olga 26887 Devanagari 234); DexScreener chips present;
no Recovering/portfolioTree; UM x402 schema 2352, status doug 2537 (locales+geo) vs machine-age 2317; skill 14329.
Zo nested ATL == GitHub main **d7c17d1fb** before change (HEAD). Working-tree drift found: the 1352/1414 commits carried only
scripts/notes, so PORT-159/160 ports.csv + atlas copies were live but uncommitted; this commit includes them.

## Win
Densified **ARC-PORT-165** Vardø fiskerihavn (Vardøya, Finnmark; UN/LOCODE NOVAO) off soft 4-decimal `70.3740 / 31.1019`
(= the onshore OSM `Vardø havn` name node/6372262628 on Kaigata street). New anchor: shoelace centroid of OSM
`man_made=pier area=yes floating=no ref:LOCODE=NOVAO` **way/987326753** (~1260 m² fishing pier, inner harbour inside indre molo)
at `70.3760571 / 31.1021737` (~0.23 km N). Twin NOVAO pier way/987326754 ~45 m NW; Vestre molo flytebrygge way/1526392564 ~0.10 km N;
OSM seamark harbour node/5355495287 (category=fishing, Vardø) ~0.19 km E. Kept distinct from parent ARC-PORT-032 (Hurtigruten
terminal node/269242524, ~0.18 km SSE).

## Sources (neutral, public)
- OSM way/987326753 https://www.openstreetmap.org/way/987326753 ; way/987326754 ; node/5355495287
- Kystverket project page https://www.kystverket.no/utbygging/farleds--og-fiskerihavnprosjekt/store-prosjekt/vardo-fiskerihavn/
  (planned 595 m outer molo 300 m N of existing molo across Sandvikflua; Hasselneset dredging — not yet built)
- Menon/Kystverket samfunnsøkonomisk analyse av Vardø (indre havn liggeplasser, fiskemottak east side)
- vardohavn.no Vardø Port (port position 70°22'N 031°06'E, coarse); no Wikidata port item
- `position_quality=facility_site` (existing fishing-harbour pier, not the future molo); confidence 94 unchanged

## Builder / live
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-165 (parent + nested builder copies)
- ports.csv copies (13): lat/lon + densify sources note, last_verified=2026-10-19
- Patch `atlas-proj/_patch_port165_1446.py`; lock `atlas-proj/check_port165_vardo_fiskerihavn.py`; PORT-105…171 locks OK
- Built with the **parent** builder (`ArcticTradeLanes.com/atlas-proj`, has `ref/ne_10m_land.geojson`) to /tmp/atl_new_1446;
  diff vs 11:20:15Z generation = ARC-PORT-165 only (geometry + position_anchor/note/quality); fan 563 / water_fan 101 intact
- Atlas gen `2026-10-19T11:52:01.127468+00:00`; 1317 features, EPSG:3996; 325 old-gen copies in 65 dirs replaced;
  sync_atlas_aliases.sh 10 dirs bad=0; md5 3996 1676d201 / wgs84 e769034b (live verified)
- No App.tsx smash / SPA redeploy / DNS / x402 / restart.

## Next candidates
PORT-166 Unified Northern-Supply Sea Route (64.7333/177.5042, Anadyr — regime entity, needs one named terminal) and
PORT-169 Korf Bay hub (60.0333/165.7333, project — likely planned/unbuilt). PORT-139 Tromsø deferred; PORT-129/135 parked.
