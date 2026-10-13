# GIS Quality — gis-port041-1216 (~12:16 MSK Europe/Moscow, 2026-10-13)

## Win
Densified **ARC-PORT-041** Mys Shmidta Port off soft approximate `68.8700 / -179.4000` onto the
**Mys Shmidta** settlement OSM **way/93613726** (place=hamlet, official_status urban-type settlement; Nominatim `68.8928813 / -179.4130958`).
Moved **~2.6 km** N; the old pin sat on a tertiary road (OSM way/93603325) south of the settlement near the airport.

## Sources (neutral gazetteer)
- OSM way/93613726 Мыс Шмидта; extratags wikidata=Q1020259, wikipedia=ru:Мыс Шмидта (посёлок городского типа), population=140 (2018-01-01)
- Wikidata Q1020259 P625 68.91056 / -179.45889 (~2.7 km NW, toward the cape; outside OSM settlement bbox)
- Wikidata Q2603783 Cape Schmidt 68.92056 / -179.45333 (~3.5 km)
- Overpass: no harbour / pier / quay / landuse=port mapped in 68.85–68.95 N, 179.30–179.55 W — no surveyed berth
- `position_quality=settlement_site`

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-041 (schematic tags now 10)
- ports.csv: every copy (16) lat/lon + sources note, confidence=88, last_verified=2026-10-13
- Lock check `atlas-proj/check_port041_mys_shmidta.py`

## Live
- Atlas gen `2026-10-13T09:19:07.781826+00:00`, **1317** features (unchanged), alias dirs bad=0, stale copies 0
- Live diff vs previous atlas: **ARC-PORT-041 geometry only**; live https://arctictradelanes.com/atlas/atlas.wgs84.geojson verified

## Next candidates
- ARC-PORT-136 Narvik Terminal Nord ~1.3 km (low value)
- UM: skipped (health check only)
