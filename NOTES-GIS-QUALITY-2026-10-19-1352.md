# GIS Quality — gis-loop-1019-1352 (~13:52 MSK Europe/Moscow, 2026-10-19)

## Site health
ATL `/` **200** (91208 B, md5 fdba64b6); `/atlas.3996.geojson` 200 (1317 feats, gen 2026-10-19T10:26:57Z before rebuild,
EPSG:3996); `/api/health` 200 (47 B), `/api/x402/schema` 200 2747 B, `/api/alpha/status` 200 888 B keyConfigured=false.
UM home 200 (8019 B, md5 83e8388a), bundle `index-CIQoD7he.js` + `index-DZdhQ1Nj.css`; hreflang 22; DexScreener API present in bundle;
no Recovering/portfolioTree as active UI error on home. Zo nested ATL == GitHub main **7740513da** before change.
Services not restarted. No DNS / x402 / SPA redeploy.

## Win
Densified **ARC-PORT-159** Hadsel Havn KF (Stokmarknes, Vesterålen; UN/LOCODE NOSKN) off soft 4-decimal `68.5648 / 15.2207`.
That pin was ~12.56 km ESE of the real harbour on the wrong longitude (toward Sortlandssundet rather than Hadseløya).
New anchor: OSM `amenity=ferry_terminal` **node/75102834** Hurtigruten Stokmarknes with `ref:LOCODE=NOSKN` at
`68.5710140 / 14.9117250` (~12.57 km WNW). Official Kystdatahuset/Allemannsdata NOSKN harbour `68.57093 / 14.91198`
lies ~14 m away. hadselhavn.no: Nordnes kai I is the Kystruten + container/cargo quay.

## Sources (neutral, public)
- OSM node/75102834 https://www.openstreetmap.org/node/75102834 (Hurtigruten Stokmarknes, ref:LOCODE=NOSKN)
- OSM node/9512006003 https://www.openstreetmap.org/node/9512006003 (Stokmarknes hurtigbåtkai, also NOSKN)
- allemannsdata.com / Kystdatahuset havn 2328291 Stokmarknes NOSKN 68.57093/14.91198
- hadselhavn.no/virksomheter/havneanlegg/ (Nordnes kai I/II; Melbu/Børøya/Miljøhavn are separate Hadsel sites)
- No Wikidata port item
- `position_quality=facility_site` (Stokmarknes instrumental port, not a single berth); confidence 75 → 90

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-159 (parent + nested builder copies)
- ports.csv copies (13): lat/lon + densify sources note, confidence=90, last_verified=2026-10-19
- Patch `atlas-proj/_patch_port159_1352.py`; lock `atlas-proj/check_port159_hadsel_stokmarknes.py`; PORT-114/119/134/140/158 locks still OK

## Live
- Built to staging first; 1317 features, EPSG:3996 kept
- Atlas gen `2026-10-19T10:58:50.651276+00:00`; sync_atlas_aliases.sh 10 dirs bad=0 (nested + parent);
  extra/old-gen sweep → 0 stale left; live nested wgs84 md5 bd699a39 (3996 c93b90e9)
- No App.tsx smash / SPA redeploy / DNS / x402 / restart.

## Next candidates
PORT-160 Mjóeyrarhöfn (Reyðarfjörður), PORT-139 Tromsø (only with one named quay).
Parked: PORT-129 Crémaillère and PORT-135 Kalvåg (planned/unbuilt).
