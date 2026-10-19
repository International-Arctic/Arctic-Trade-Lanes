# GIS Quality — gis-loop-1019-1119 (~11:19 MSK Europe/Moscow, 2026-10-19)

## Site health
GET `/` → **200** (91208 B, md5 fdba64b6); `/atlas.3996.geojson` 200 (1317 feats, gen 2026-10-19T07:57:32Z before rebuild,
EPSG:3996); `/api/health` ok, `/api/x402/schema` 200 2747 B, `/api/x402/status` 200 1363 B, `/api/alpha/status` 200 888 B,
`/pricing` 200. UM home 200 (8019 B, md5 83e8388a), bundle `index-CIQoD7he.js` (200, 957729 B) + `index-DZdhQ1Nj.css`;
person pages 200 (elon 26183, doug 23217, hi/doug 23781, olga 26475, durov 23232), no Recovering/portfolioTree in HTML.
Zo nested ATL == GitHub main **ec1099234** (clean apart from untracked builder output) before change.
Services not restarted. No DNS / x402 / SPA redeploy.

## Win
Densified **ARC-PORT-114** Port of Yeongilman (Pohang) — Northern Sea Route specialised hub feasibility study (UN/LOCODE KRKPO)
off soft 4-decimal `36.0194 / 129.4256` (inside POSCO Pohang Steelworks, Cheongnim-dong, Nam-gu — Nominatim reverse way/996515174;
not port infrastructure of Yeongilman) onto the **Pohang Yeongil New Port harbour area** (Heunghae-eup, Buk-gu):
OpenStreetMap **way/550199344** landuse=harbour name=포항영일신항만 (~136 ha, v7), shoelace centroid `36.1013341 / 129.4354711`
(inside the polygon). Moved **~9.15 km** N (bearing ~6°).

## Sources (neutral, public)
- OSM **way/550199344** 포항영일신항만 — https://www.openstreetmap.org/way/550199344
- Nearby OSM context: Yeongilmanhang station node/8310880353 (Q72246064), hinterland logistics warehouses (ways 1323889057/1323889058)
- No Wikidata item for the port itself (wbsearchentities ko/en: only Yeongilmanhang Station Q72246064, Yeongilman Bay Q11260549 — not reused)
- Row sources (bairdmaritime.com, portnews.ru, highnorthnews.com, korea.net, yna.co.kr) unchanged
- UN/LOCODE KRKPO unchanged; `position_quality=facility_site` (harbour-area polygon, not a surveyed berth)
- Note: the row's disambiguation text calls Yeongilman "Pohang New Port"; the older Pohang New Port (포항신항) beside POSCO is a
  different, southern port — the study subject is Yeongilman Port, so the pin now sits there

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-114 (parent + nested builder copies)
- ports.csv copies (13): lat/lon + densify sources note, confidence=92, last_verified=2026-10-19
- Patch `atlas-proj/_patch_port114_1119.py`; lock `atlas-proj/check_port114_yeongilman.py`; PORT-065/066/109 locks still OK

## Live
- Atlas gen `2026-10-19T08:26:33.732151+00:00`, **1317** features (unchanged count); EPSG:3996 kept; only ARC-PORT-114 changed
- old-gen sweep 70 copies / 14 dirs; sync_atlas_aliases.sh 10 dirs bad=0
- No App.tsx smash / SPA redeploy / DNS / x402 / restart.

## Next candidates
PORT-119 Blue Water Imeq Nuuk, PORT-129 Crémaillère Harbour, PORT-134 Argentia (Cooper Cove), PORT-135 Kalvåg,
PORT-139 Tromsø (multi-quay), PORT-140 Ísafjörður, PORT-158 Sortland, PORT-159 Hadsel.
