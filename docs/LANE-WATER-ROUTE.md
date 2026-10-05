# Lane water routing (gis-lanewater-1214, 2026-10-05)

## Problem
ATL trade lanes are built from a few gazetteer waypoints (`lanes.csv` `waypoints`) and drawn
as straight segments in EPSG:3996. In the live atlas, 28.3% of sea-lane length
(33,628 km of 119,029 km) ran across land on Natural Earth 10m: the Northern Sea Route
cut over Taymyr and Yamal, the White Sea–Baltic and Baltic–Barents routes over
Scandinavia, the Northwest Passage over the Canadian archipelago, and so on.

## Fix (display-only, builder-side)
`scripts/lane_route.py` (same module as the Zo builder `atlas-proj/lane_route.py`):

1. Rasterize Natural Earth 10m land (public domain) into a 10 km grid in EPSG:3996.
2. For each lane leg whose straight segment touches land, run 8-connected A* on that grid.
   Land costs 40x water instead of being forbidden, so ports on land cells, canals and
   straits narrower than the grid still connect with the shortest possible land hop.
3. String-pull the cell path (Douglas–Peucker style): a shortcut is kept only if it adds no land.
4. Every original waypoint stays a vertex. Only legs between waypoints change.
5. River lanes (name contains "River": Yenisei, Lena) are left unchanged.

Each routed lane carries `geometry_quality: water_routed`, `route_mask: naturalearth_10m_land`,
`route_land_km_before` and `route_land_km_after`. The manifest has `lane_water_route` per lane.
Turn it off with `ATL_LANE_WATER_ROUTE=0`. It runs at build time in about 8 s, and the output is static GeoJSON, so there's no server GIS cost.

## Result (live atlas generated 2026-10-05T09:18:55Z)
| Check (`scripts/check_lane_water.py`, vector intersection in EPSG:3996) | Before | After |
|---|---|---|
| Sea-lane length on land | 33,628 km (28.3%) | 5,669 km (4.1%) |

Only the 25 sea-lane geometries changed. All other 1,296 features are byte-identical.

## Known leftovers (help wanted)
The remaining land length mostly comes from waypoints or end ports that sit inland
(e.g. Ob Bay route to Salekhard/Obskaya, Iceland–Greenland, Transpolar, Kristiansand–Kirkenes)
and from straits narrower than 10 km. Fixing waypoint coordinates in the gazetteer is the real cure.
Also note that the drawn lengths are often far longer than `typical_distance_nm` in `lanes.csv`,
which points to waypoint ordering problems worth auditing.

CI: `python3 scripts/check_lane_water.py atlas.wgs84.geojson` fails above 8% (`MAX_LAND_PCT`).
