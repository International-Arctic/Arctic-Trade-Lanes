# GIS Quality — gis-port046-1247 (~12:47 MSK Europe/Moscow, 2026-10-13)

## Win
Densified **ARC-PORT-046** Zhelaniye Port off soft approximate `76.9500 / 68.5500` onto
**Мыс Желания / Cape Zhelaniya** OSM **node/429774624** (natural=cape; Nominatim `76.9542826 / 68.5639747`).
Moved **~0.59 km** NE; the old pin was a 0.05-step soft coordinate near the cape / former polar station.

## Sources (neutral gazetteer)
- OSM node/429774624 Мыс Желания; extratags wikidata=Q2464613, wikipedia=ru:Мыс Желания
- Wikidata Q2464613 Cape Zhelaniya P625 76.9546 / 68.57589 (~0.83 km E of soft)
- Wikidata Q86004798 former polar station P625 76.95056 / 68.54194 (~0.21 km from soft; not used as pin — station remnant, not a berth)
- UN/LOCODE RUZHE; operator Rosmorport (CSV)
- Nominatim/Overpass: no harbour / pier / quay mapped near the cape — no surveyed berth
- `position_quality=facility_site`

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-046 (schematic tags now 11)
- ports.csv: every copy (16) lat/lon + sources note, confidence=88, last_verified=2026-10-13
- Lock check `atlas-proj/check_port046_zhelaniye.py`

## Live
- Atlas gen `2026-10-13T09:52:51.582729+00:00`, **1317** features (unchanged), alias dirs bad=0
- Live https://arctictradelanes.com/atlas/atlas.wgs84.geojson verified PORT-046 at cape + facility_site
- No SPA redeploy / App.tsx / DNS change

## Next candidates
- ARC-PORT-136 Narvik Terminal Nord ~1.3 km (low value; last coarse ≥0.05 soft port was PORT-046)
- UM: skipped (time / health-only)
