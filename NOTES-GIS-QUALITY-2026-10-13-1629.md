# GIS Quality — gis-port022-1629 (~16:29 MSK Europe/Moscow, 2026-10-13)

## Win
Densified **ARC-PORT-022** Tuktoyaktuk Port off soft 4-decimal `69.4457 / -133.0360`
(hamlet approx ~0.25 km from OSM place node/107350410 = WD Q719547; empty sources)
onto the **port land on the Tuktoyaktuk Harbour shore** south of Cache Point: OSM **way/513281075**
`landuse=industrial` + `industrial=port`, shoelace centroid `69.4281426 / -132.9885229`. Moved **~2.69 km** SE.

## Sources (neutral, public)
- OSM way/513281075 industrial=port (closed, 29 nodes, ~0.16 km2; contains a tank farm of ~21 man_made=storage_tank ways)
- OSM place node/107350410 Tuktoyaktuk = Wikidata **Q719547** (P625 69.4428/-133.031) ~2.4 km NW — the soft pin was this settlement approx
- Wikidata **Q116456484** Tuktoyaktuk Harbour (natural harbour, CGNDB LAYQW, P625 69.4333/-132.9694) ~1.0 km NE
- DFO/CHS tide station 6485 Tuktoyaktuk 69.438226/-132.994402 ~1.2 km NNW
- GNWT INF Marine Transportation Services: freight-handling terminal in Tuktoyaktuk (inf.gov.nt.ca/en/MTS)
- CMSN infrastructure profile: Tuktoyaktuk port = cargo pier (MTS freight terminal) + oil terminal
- UN/LOCODE CATUK; WPI 20491 (69.45/-133.033, 2-decimal, not used as anchor)
- Small hamlet piers (way/513281058, 737952630-632) ~2.5 km NW not used (community docks)
- No lanes end at ARC-PORT-022; no ATL co-site clash
- `position_quality=facility_site` (mapped port land polygon, not a surveyed berth line)

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-022 (schematic tags now 18)
- ports.csv: every copy (13) lat/lon + sources note, confidence=90, last_verified=2026-10-13
- Patch `atlas-proj/_patch_port022_1629.py`; lock check `atlas-proj/check_port022_tuktoyaktuk.py` (PORT-042/075 locks still OK)

## Live
- Atlas gen `2026-10-13T13:36:00.555629+00:00`, **1317** features (unchanged); EPSG:3996 atlas kept
- Diff vs previous build: ARC-PORT-022 only
- 10 alias dirs synced (bad=0) + extra served copies; 45 atlas.wgs84 copies at new md5, 0 left on previous gen
- Live https://arctictradelanes.com/atlas/atlas.wgs84.geojson, /atlas.wgs84.geojson, /data/atlas.wgs84.geojson, /atlas/atlas.3996.geojson verified
- No SPA redeploy / App.tsx / DNS / x402 change. UM: health check only

## Next candidates
- ARC-PORT-051 Nome Snake River Moorage, ARC-PORT-047 Nordvik (historic), ARC-PORT-171 Manorsky / Port Elga (Arctic-relevance check), ARC-PORT-150 Pyramiden
