# GIS Quality — gis-port075-1525 (~15:25 MSK Europe/Moscow, 2026-10-13)

## Win
Densified **ARC-PORT-075** Nuuk Harbour Expansion — Qeqertat quay off soft approximate `64.1700 / -51.7100`
(2-decimal pin on Qeqertanut / Qeqertaq Avalleq) onto the **southern industrial port land** immediately
south of the 2017 container terminal: OSM **way/627906959** `landuse=industrial` + `industrial=port`,
shoelace centroid `64.1678488 / -51.7140694`. Moved **~0.31 km** WSW.

## Sources (neutral, public)
- Sikuki Nuuk Harbour A/S 2026-07-08: groundbreaking of harbour expansion on **Qeqertaq Avalleq (Fyroe)** —
  200 m trawler terminal + 150 m dual-use naval quay + 25,200 m2 harbour area; completion Nov 2028
  (contractor KJ Greenland A/S; tender Apr 2026)
- Naalakkersuisut VVM A246375-VVM-001 (public hearing 2024-07): new quay on the **west side of Qeqertaq Avalleq
  immediately south of the existing container terminal**; kajkant of the container terminal continues south;
  Figur 2-1 / 4-1 / 4-2 layout plans
- KNR: 350 m new quay in extension of the container terminal on Qeqertaq Avalleq
- OSM way/627906959 industrial=port covers that southern facility land (west face ~310 m N-S between
  nodes 2590218967 and 2590218977, matching planned quay length); container-terminal pier area
  way/257366762 ~0.45 km N; Qeqertanut road network names the peninsula
- Wikidata Q3398532 = Port of Nuuk (existing harbour; P625 64.1708/-51.7208) — related, not the expansion
- ARC-PORT-009 Nuuk Port stays on OSM harbour node/995384594 (~0.69 km NW) — not a co-site clash
- No OSM pier/quay way for the new berth yet (under construction through Nov 2028) →
  `position_quality=facility_site`

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-075 (schematic tags now 16)
- ports.csv: every copy (16) lat/lon + sources note append, confidence=90, last_verified=2026-10-13
- Patch `atlas-proj/_patch_port075_1525.py`; lock check `atlas-proj/check_port075_qeqertat.py` (prior port locks still OK)

## Live
- Atlas gen `2026-10-13T12:37:23.168090+00:00`, **1317** features (unchanged)
- Diff vs previous build: ARC-PORT-075 only (no lanes end at this port)
- 10 alias dirs synced (bad=0) + extra served copies; 59 copies at new md5, 0 left on previous gen
- Live https://arctictradelanes.com/atlas/atlas.wgs84.geojson, /atlas.wgs84.geojson, /data/atlas.wgs84.geojson, /atlas/atlas.3996.geojson verified
- No SPA redeploy / App.tsx / DNS change. UM: skipped (no patterned client-side geo-filter win this cycle)

## Next candidates
- Re-audit soft 4-decimal ports without OSM/WD refs in the sources field (last 2-decimal soft port densified)
