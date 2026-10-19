# GIS Quality — gis-loop-1019-1414 (~14:14 MSK Europe/Moscow, 2026-10-19)

## Site health
ATL `/` **200** (91208 B, md5 fdba64b6); `/atlas.3996.geojson` 200 (1317 feats, gen 2026-10-19T10:58:50Z before rebuild,
EPSG:3996); `/api/health` 200 ok, `/api/x402/schema` 200 2747 B, `/api/x402/status` 200 1363 B, `/api/alpha/status` 200 888 B keyConfigured=false.
UM home 200 (8019 B, md5 83e8388a), bundle `index-CIQoD7he.js` + `index-DZdhQ1Nj.css`; hreflang 22; person pages 200
(elon 26183, doug 23217, olga 26475, durov 23232; /hi/ doug 23781 lang=hi Devanagari 293, /hi/ olga 26887 Devanagari 234);
no Recovering/portfolioTree in any fetched page. Zo nested ATL == GitHub main **ac6261c1d** before change.
Services not restarted. No DNS / x402 / SPA redeploy.

## Win
Densified **ARC-PORT-160** Mjóeyrarhöfn (Reyðarfjörður, East Iceland; UN/LOCODE ISRFJ) off soft 4-decimal `65.0284 / -14.1121`
(on the harbour backland ~0.13 km NNE of the berth). New anchor: midpoint of the 384 m quay face — OSM `natural=coastline`
**way/210145938** (bearing 80/260°), outer member of OSM **relation/2819859** `landuse=industrial industrial=port` Mjóeyrarhöfn
(~7.1 ha, centroid 65.0282174/-14.1133016) — at `65.0273990 / -14.1134659` (~0.13 km SSW).
Official fjardabyggdarhafnir.is: Mjóeyrarbryggja 383 m, 14.2 m depth, steel sheet pile; port position 65°01.66'N 014°06.80'W (~30 m away).

## Sources (neutral, public)
- OSM way/210145938 https://www.openstreetmap.org/way/210145938 (quay-face coastline, 384 m)
- OSM relation/2819859 https://www.openstreetmap.org/relation/2819859 (Mjóeyrarhöfn port area)
- OSM node/626578135 https://www.openstreetmap.org/node/626578135 (seamark harbour Mjóeyrarhöfn, ~0.13 km W)
- https://www.fjardabyggdarhafnir.is/is/fjardabyggdarhafnir/mjoeyrarhofn (official port authority page)
- No Wikidata port item
- `position_quality=facility_site` (single-quay bulk harbour next to Alcoa Fjarðaál; planned extension not built); confidence 86 → 92

## Builder / live
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-160 (parent + nested builder copies)
- ports.csv copies (13): lat/lon + densify sources note, confidence=92, last_verified=2026-10-19
- Patch `atlas-proj/_patch_port160_1414.py`; lock `atlas-proj/check_port160_mjoeyrarhofn.py`; PORT-114/119/134/140/158/159 locks still OK
- Built with the **parent** builder (`ArcticTradeLanes.com/atlas-proj`, which has `ref/ne_10m_land.geojson` + `atl_proj.py`) to staging.
  Staged build vs the 09:51:56Z generation differs only in ARC-PORT-158/159/160 (geometry + position_anchor/note/quality).
- **Restored land-mask fans:** the 10:58:50Z generation (gis-loop-1019-1352) had been built from the nested atlas-proj copy,
  where `ref/ne_10m_land.geojson` is absent, so it shipped without the program seat land-mask fan (563 tagged) and the
  ship water fan (101) and with slightly different lane water routing. This build brings them back.
- Atlas gen `2026-10-19T11:20:15.068171+00:00`; 1317 features, EPSG:3996 kept; 325 old-gen copies in 65 dirs replaced;
  sync_atlas_aliases.sh 10 dirs bad=0; md5 3996 0bb847d6 / wgs84 5ee6e455
- No App.tsx smash / SPA redeploy / DNS / x402 / restart.

## Next candidates
PORT-139 Tromsø (only with one named quay). Parked: PORT-129 Crémaillère and PORT-135 Kalvåg (planned/unbuilt).
Next pass: rescan ports.csv for remaining 4-decimal soft pins (e.g. PORT-165 Vardø 70.3740/31.1019, PORT-166/169 Russian Far East 4-decimal pins).
Process: build only from `ArcticTradeLanes.com/atlas-proj` (parent) — not the nested copy.
