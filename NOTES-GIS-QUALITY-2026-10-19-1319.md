# GIS Quality — gis-loop-1019-1319 (~13:19 MSK Europe/Moscow, 2026-10-19)

## Site health
ATL `/` **200** (91208 B, md5 fdba64b6); `/atlas.3996.geojson` 200 (1317 feats, gen 2026-10-19T09:51:56Z before rebuild,
EPSG:3996); `/api/health` 200 (47 B), `/api/x402/schema` 200 2747 B, `/api/x402/status` 200 1363 B, `/api/alpha/status` 200 888 B,
`/pricing` 200 8673 B, `/ports` 200 27302 B.
UM home 200 (8019 B, md5 83e8388a), bundle `index-CIQoD7he.js` + `index-DZdhQ1Nj.css`; radar pages 200 (elon 26183,
doug 23217, olga 26475, durov 23232), hi/radar doug 23781 (Devanagari 293), hi/radar olga 26887 (Devanagari 234),
doug_json 3433, x402 status doug 2537, skill 14329; no Recovering/portfolioTree. Identical to the 1245 baseline.
Zo nested ATL == GitHub main **d9530c8b1** before change. Services not restarted. No DNS / x402 / SPA redeploy.

## Win
Densified **ARC-PORT-158** Sortland Havn KF (Vesterålen; row UN/LOCODE NOSLD) off soft 4-decimal `68.6964 / 15.4145`.
That pin was on land in Sortland town centre (Strandgata / Gårdsalléen shops), ~0.44 km SSW of the port.
New anchor: the main quay **Terminalkaia**. OSM has no harbour or quay polygon here, but the `natural=coastline` ways
**way/552701435** (v2) + **way/552701437** (v1) form one straight quay face of **434 m** at bearing **348.9°**
(node/5335888572 68.6978898/15.4209075 → node/5335888593 68.7017107/15.4188371), passing the Hurtigrute
`amenity=ferry_terminal` node/279276240. New pin = geodesic midpoint of that face `68.6998001 / 15.4198705`.
Moved **~0.44 km** NNE (bearing ~30°).

## Sources (neutral, public)
- OSM way/552701435 https://www.openstreetmap.org/way/552701435 , way/552701437 https://www.openstreetmap.org/way/552701437 ,
  node/279276240 https://www.openstreetmap.org/node/279276240 (Sortland Hurtigrutekai)
- sortland-havn.no/terminalkaia: Terminalkaia length 438 m, heading 348/168°, 10,500 m² quay area, depth 10 m (N) to 7.5 m (S),
  EU control port + ISPS terminal (matches the 434 m / 348.9° OSM face)
- sortland-havn.no/navigasjon: official harbour position UTM33 E517007 N7620922 = 68.69957/15.41952, ~29 m from the new pin
- No Wikidata port item. OSM ferry node carries `ref:LOCODE=NOSLX` while the row has NOSLD: left unchanged, flagged for review
- `position_quality=facility_site` (main quay, not a single berth); confidence 80 → 88

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-158 (parent + nested builder copies)
- ports.csv copies (13): lat/lon + densify sources note, confidence=88, last_verified=2026-10-19
- Patch `atlas-proj/_patch_port158_1319.py`; lock `atlas-proj/check_port158_sortland_terminalkaia.py`; PORT-114/119/134/140 locks still OK

## Live
- Built to staging first; diff vs previous live: only ARC-PORT-158 changed, 1317 features, EPSG:3996 kept
- Atlas gen `2026-10-19T10:26:57.629075+00:00`; sync_atlas_aliases.sh 10 dirs bad=0; old-gen sweep 15 files in 3 Dataset dirs;
  0 old-gen copies left; live /, /data, /atlas aliases md5 38c9aea6 (3996 76ac52f1)
- No App.tsx smash / SPA redeploy / DNS / x402 / restart.

## Next candidates
PORT-159 Hadsel Havn (Stokmarknes), PORT-160 Mjóeyrarhöfn (Reyðarfjörður), PORT-139 Tromsø (only with one named quay).
Parked: PORT-129 Crémaillère and PORT-135 Kalvåg, both planned sites with no built or mapped facility yet.
