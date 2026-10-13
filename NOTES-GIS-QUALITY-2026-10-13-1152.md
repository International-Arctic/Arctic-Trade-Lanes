# GIS Quality — gis-port045-1152 (~11:52 MSK Europe/Moscow, 2026-10-13)

## Win
Densified **ARC-PORT-045** Ambarchik Port off soft approximate `69.6500 / 162.3500` onto the
**Ambarchik** rural locality OSM **way/655223046** (place=hamlet; Nominatim `69.6252019 / 162.3024493`).
Moved **~3.3 km** SW toward Ambarchik Bay / Kolyma mouth settlement.

## Sources (neutral gazetteer)
- OSM way/655223046 Амбарчик place=hamlet; extratags wikidata=Q2629730, wikipedia=ru:Амбарчик_(село), population=4 (2010-10-14)
- en.wikipedia.org/wiki/Ambarchik 69.62611111 / 162.30388889 (~0.12 km from OSM)
- Wikidata Q2629730 P625 69.6167 / 162.2833 (~1.2 km; minute-rounded)
- UN/LOCODE RUABC 69.6167 / 162.3000 (bay/settlement corroboration; CSV still carries legacy RUAMB code)
- Historical East Siberian Sea / Ambarchik Bay port; shipping later transferred to Chersky — no dedicated modern pier OSM found
- DISTINCT: nearest sibling ports (Mys Shmidta PORT-041, Wrangel PORT-048, Anadyr PORT-044, Tiksi PORT-006) are hundreds of km away
- `position_quality=settlement_site`

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION allowlist + ARC-PORT-045 (schematic tags now 9)
- ports.csv: every copy (16) lat/lon + sources note, confidence=88, last_verified=2026-10-13
- Lock check `atlas-proj/check_port045_ambarchik.py`

## Live
- Atlas gen `2026-10-13T08:57:00.348201+00:00`, **1317** features (unchanged), alias dirs bad=0
- Live diff vs previous nested HEAD atlas: **ARC-PORT-045 geometry only**

## Next candidates
- ARC-PORT-041 Mys Shmidta 68.87/-179.40 (verify OSM way/93613726 ~2.7 km)
- ARC-PORT-136 Narvik Terminal Nord ~1.3 km (low value)
- UM: skipped (health check only)
