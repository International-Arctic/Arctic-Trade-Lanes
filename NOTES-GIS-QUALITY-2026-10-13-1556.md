# GIS Quality — gis-port042-1556 (~15:56 MSK Europe/Moscow, 2026-10-13)

## Win
Densified **ARC-PORT-042** Egvekinot Port off soft 4-decimal `66.3167 / -179.1167`
(Rosmorrechflot registry AD-378-r / WD Q1240765 settlement P625 approx; empty sources)
onto the **main harbour pier** on Kresta Bay: OSM **way/721745076** `man_made=pier`,
shoelace centroid `66.3192251 / -179.1095237`. Moved **~0.43 km** ENE.

## Sources (neutral, public)
- OSM way/721745076 man_made=pier (larger harbour pier area; shoelace centroid 66.3192251/-179.1095237)
- OSM way/721745075 man_made=pier secondary ~0.6 km SSW (centroid ~66.3140/-179.1114)
- OSM place node/2891542781 Эгвекинот = Wikidata **Q1240765** (~0.62 km NW of pier)
- Rosmorrechflot disposition AD-378-r of 24.12.2010: морской порт Эгвекинот in Registry
  (66°19′ N, 179°07′ W; ул. Портовая, д. 1; UN/LOCODE RUEGV)
- Soft pin matched registry/WD settlement approx — not a pier; densify fills empty sources
- No nearby ATL port clash within tens of km
- `position_quality=facility_site` (mapped pier polygon, not a surveyed berth line)

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-042 (schematic tags now 17)
- ports.csv: every copy (16) lat/lon + sources note, confidence=90, last_verified=2026-10-13
- Patch `atlas-proj/_patch_port042_1556.py`; lock check `atlas-proj/check_port042_egvekinot.py` (prior port locks still OK)

## Live
- Atlas gen `2026-10-13T13:03:22.899995+00:00`, **1317** features (unchanged)
- Diff vs previous build: ARC-PORT-042 only
- 10 alias dirs synced (bad=0) + extra served copies; all ATL atlas.wgs84 copies at new md5
- Live https://arctictradelanes.com/atlas/atlas.wgs84.geojson, /atlas.wgs84.geojson, /data/atlas.wgs84.geojson, /atlas/atlas.3996.geojson verified
- No SPA redeploy / App.tsx / DNS change. UM: skipped (no patterned client-side geo-filter win this cycle)

## Next candidates
- Soft 4-decimal / softish ports still without OSM/WD in sources: ARC-PORT-022 Tuktoyaktuk, ARC-PORT-051 Nome Snake River Moorage, ARC-PORT-047 Nordvik (historic), ARC-PORT-150 Pyramiden, ARC-PORT-171 Port Elga (Arctic-relevance check)
