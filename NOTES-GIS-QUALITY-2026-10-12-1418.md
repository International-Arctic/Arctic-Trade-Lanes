# Landlocked lane waypoints -> open water (gis-lanewp-1418, 2026-10-12)

## Problem

Lane geometry is built from `lanes.csv` waypoint tokens resolved through the builder GAZETTEER. Five
tokens name a landmass or bay and resolved to a point **on Natural Earth 10m land with no water within
15 km**. The water router (gis-lanewater-1214) keeps every waypoint as a vertex, so those legs were
forced onto land:

| Lane | Token | Raw anchor | Symptom |
|---|---|---|---|
| ARC-LANE-025 Transpolar Route (Future) | `Alaska` | 68.0 / -152.0 (Brooks Range) | route ended ~270 km inland; 333 km of line on land |
| ARC-LANE-023 Kara Sea Oil Route | `Yamal Peninsula` | 71.0 / 70.0 (interior Yamal) | spur from Ob Bay across Yamal and back to Sabetta |
| ARC-LANE-006 Barents Sea Route | `Kolguev Island` | 69.0 / 49.0 (island centre) | detour onto Kolguev |
| ARC-LANE-010 Greenland Coastal Route | `Disko Bay` | 69.5 / -53.0 (on Disko Island) | vertex on the island, not the bay |
| ARC-LANE-017 Beaufort Sea Route | `Mackenzie Delta` | 69.0 / -135.0 (inland delta) | vertex ~30 km inland |

## Fix (display-only, `atlas-proj/build_atlas.py`)

A GAZETTEER waypoint (never a port, city, dataset/seed anchor or `<X> River` token; River lanes skipped)
that is on NE10m land with no water within `LANE_WP_KEEP_KM` = 15 km moves to an open-water slot
(>= ~1 km offshore). Candidates are ring-searched (3 km x 5 deg) up to 60 km beyond the nearest water
(max `LANE_WP_WATER_MAX_KM` = 350 km) and scored `2*offset + d(prev vertex) + d(next vertex)`, so the
slot sits on the lane's side of the landmass. The lane carries `waypoint_water_snap` with before->after.
CSV untouched; `ATL_LANE_WAYPOINT_WATER=0` restores the old behaviour. EPSG:3996 + RFC 7946 WGS84
outputs regenerate from the same vertices.

| Lane | After | Offset | Land km on line (before -> after) |
|---|---|---|---|
| ARC-LANE-025 | 70.444693 / -151.360895 (Beaufort coast off Harrison Bay) | 273 km | 333 -> 35 |
| ARC-LANE-023 | 71.307179 / 72.136672 (Ob Bay off Sabetta) | 84 km | 228 -> 39 |
| ARC-LANE-006 | 69.539593 / 49.000000 (north of Kolguev) | 60 km | 189 -> 138 |
| ARC-LANE-010 | 69.391120 / -52.560483 (Disko Bay) | 21 km | 169 -> 140 |
| ARC-LANE-017 | 69.338594 / -135.257271 (Mackenzie Bay) | 39 km | 158 -> 110 |

Total on these 5 lanes: 1,077 -> 462 land km. Only these 5 lane geometries changed; 1318 features.

## Lock

`python3 scripts/check_lane_waypoint_water.py [atlas.wgs84.geojson | URL]` fails if any non-river lane
vertex sits within 1 km of a landlocked raw anchor, the 5 lanes lose `waypoint_water_snap`, LANE-023/025
exceed 60 land km, or LANE-025 ends south of 70.2N. Pre-fix atlas fails (13 findings); live passes.
`check_river_lane_order.py` and `check_ship_single_water.py` still OK.

## Open (help wanted)

- `lanes.csv` LANE-025 / 005 / 016 / 018 reference `ARC-PORT-037`, which is not in `ports.csv`, so the
  Transpolar route has no Alaskan end port. A sourced port row (e.g. Utqiagvik or Prudhoe Bay / West Dock)
  would be the natural end.
- LANE-013 Ob Bay Route still visits Salekhard (Ob river port, ~240 km up-river) mid-route and returns;
  a river-aware ordering like gis-riverlane-1346 is a candidate.
- LANE-001/002/003 keep 1,150-1,520 km straight legs across the East Siberian / Laptev seas (New Siberian
  Islands, ~130-200 land km) where the A* margin seems to fail; worth a look.
