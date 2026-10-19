# GIS Quality — gis-loop-1019-1048 (~10:48 MSK Europe/Moscow, 2026-10-19)

## Site health
GET `/` → **200** (91208 B, md5 fdba64b6); `/atlas.3996.geojson` + `/atlas.4326.geojson` **200** (1317 feats, gen
2026-10-19T07:29:01Z before rebuild, EPSG:3996 / EPSG:4326 stamps). `/api/x402/schema` 200 2747 B, `/api/x402/status` 200 1363 B,
`/api/alpha/status` 200 888 B keyConfigured=false. UM home 200 (8019 B, md5 83e8388a), bundle `index-CIQoD7he.js` +
`index-DZdhQ1Nj.css`, hreflang 22, no Recovering/portfolioTree in HTML, DexScreener string in bundle; person pages 200.
Zo nested ATL == GitHub main **8bdfa849e** (clean apart from untracked builder output dir) before change.
Services not restarted. No DNS / x402 / SPA redeploy.

## Win
Densified **ARC-PORT-109** Port of Reykjanes — Keflavík Harbour cruise upgrade programme (UN/LOCODE ISKEF)
off soft 4-decimal `63.9988 / -22.5550` (on residential Sólvallagata in Keflavík town, Nominatim way/496329734)
onto the **Keflavíkurhöfn port area**: OpenStreetMap **relation/19845360** landuse=industrial industrial=port
name=Keflavíkurhöfn (outer ways 1451071759 + 1451071766, ~1.39 ha), shoelace centroid `63.9983860 / -22.5443131`.
Moved **~0.52 km** E (bearing ~95°).

## Sources (neutral, public)
- OSM **relation/19845360** Keflavíkurhöfn — https://www.openstreetmap.org/relation/19845360
- OSM relation/19845279 Njarðvíkurhöfn (~1.6 km SSE) — distinct harbour, not merged
- ARC-PORT-111 Helguvík (~2.5 km N) left distinct
- reykjaneshofn.is (operator cruise page); icelandreview.com / ruv.is 2025 cruise-upgrade reporting (row sources unchanged)
- No Wikidata item for Keflavíkurhöfn found (wbsearchentities en/is empty)
- UN/LOCODE ISKEF unchanged; `position_quality=facility_site` (port-area polygon, not a surveyed berth)

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-109 (parent + nested builder copies)
- ports.csv copies (13): lat/lon + densify sources note, confidence=95, last_verified=2026-10-19
- Patch `atlas-proj/_patch_port109_1048.py`; lock `atlas-proj/check_port109_keflavik_harbour.py`; PORT-065/066 locks still OK

## Live
- Atlas gen `2026-10-19T07:57:32.640100+00:00`, **1317** features (unchanged count); EPSG:3996 kept
- sync_atlas_aliases.sh 10 dirs bad=0
- No App.tsx smash / SPA redeploy / DNS / x402 / restart.

## Next candidates
PORT-079 Vör near-duplicate (merge vs densify decision), PORT-068 Whittier Delong Dock (needs ARRC/USACE source),
PORT-101 Clyde River SCH (not yet mapped in OSM), PORT-102 Qikiqtarjuaq deep-sea port (planned; only small untagged piers in OSM),
PORT-107 Juneau USCG pier (site TBD), PORT-114 Yeongilman, PORT-134 Argentia, PORT-139 Tromsø.
