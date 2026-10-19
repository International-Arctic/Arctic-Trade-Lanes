# GIS Quality — gis-loop-1019-1018 (~10:18 MSK Europe/Moscow, 2026-10-19)

## Site health
GET `/` → **200** (91208 B, md5 fdba64b6, v2 homepage); `/atlas.geojson` + `/atlas.3996.geojson` **200**
(1317 feats before rebuild gen 2026-10-19T06:56:21Z; after rebuild gen 2026-10-19T07:29:01Z). UM home 200 (8019 B),
bundle `index-CIQoD7he.js` + `index-DZdhQ1Nj.css`, hreflang 22, no Recovering/portfolioTree in HTML (bundle has defensive strings only),
DexScreener chip present in JS. Zo nested ATL == GitHub main **84b90fb04** (clean) before change.
Services not restarted. No DNS / x402 / SPA redeploy.

## Win
Densified **ARC-PORT-066** Vör — Reykjavík Cruise Terminal (Viðeyarsund; UN/LOCODE ISREY)
off soft 4-decimal `64.1680 / -21.8520` (~1.49 km NNE toward Viðey island picnic/viewpoint land, not on the Sundahöfn cruise quay)
onto the **Vör terminal building**: OpenStreetMap **way/1391146178** building=transportation
addr:housename=Vör addr:street=Skarfagarðar addr:housenumber=6 start_date=2026 (~3103 m² footprint),
shoelace centroid `64.1557650 / -21.8646994`. Moved **~1.49 km** SSW (bearing ~204°).

## Sources (neutral, public)
- OSM **way/1391146178** Vör transportation building — https://www.openstreetmap.org/way/1391146178
- OSM way/108336302 Skarfabakki quay service road (~542 m) adjacent
- Faxaflóahafnir / Faxaports; iceland-highlights.com Vör Cruise Terminal 2026 (Skarfabakki quay / Vör building)
- Wikidata **Q16427805** Sundahöfn P625 64.1494/-21.8565 (~0.81 km SE) — port-basin point, not reused as anchor
- No dedicated Vör Wikidata item yet
- ARC-PORT-012 Reykjavik Port remains on ferry_terminal node/694173331 (~0.12 km NW; distinct)
- Near-duplicate **ARC-PORT-079** (soft 64.1628/-21.8514, same Vör/Skarfabakki story) left untouched this cycle
- UN/LOCODE ISREY unchanged; `position_quality=facility_site` (building footprint, not a surveyed berth)

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-066 (parent + nested builder copies)
- ports.csv copies (13): lat/lon + densify sources note, confidence=95, last_verified=2026-10-19
- Patch `atlas-proj/_patch_port066_1018.py`; lock `atlas-proj/check_port066_vor_reykjavik.py`; PORT-065 lock still OK

## Live
- Atlas gen `2026-10-19T07:29:01.496988+00:00`, **1317** features (unchanged count); EPSG:3996 kept
- sync_atlas_aliases.sh 10 dirs bad=0 (ATL.com + Dataset copies)
- No App.tsx smash / SPA redeploy / DNS / x402 / restart.

## Next candidates
PORT-079 Vör near-duplicate (decide merge vs densify onto same way/1391146178), PORT-068 Whittier Delong Dock
(no OSM named Delong; City Dock way/397797323 ~0.88 km / Princess Pier way/232411495 ~1.66 km — needs ARRC/USACE source),
PORT-073 Arkhangelsk Deep-Water (planned greenfield), PORT-104 Narvik Dock 5 / LKAB shiploader.
