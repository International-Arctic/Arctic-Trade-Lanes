# GIS Quality Loop — gis-wpport-1636 (2026-10-12 ~16:36 MSK)

## Win: lanes no longer hop inland to their own port's town centroid

20 of 27 sea lanes listed their own start/end port again as a town waypoint (Prudhoe Bay, Sabetta,
Barrow, Murmansk, Pevek, Arkhangelsk, Nuuk, Reykjavik, Oulu, Kaliningrad, Kristiansand, Honningsvåg ...).
The GAZETTEER resolves those to settlement centroids on Natural Earth 10m land 0.2–9 km from the
OSM-densified harbour pin, and the water router keeps every waypoint as a vertex, so each lane began
or ended with a short inland spur (worst: ARC-LANE-016/017 Prudhoe Bay port -> town 9 km inland -> sea;
ARC-LANE-027 / 023 had backtrack spurs at Murmansk / Sabetta).

`atlas-proj/build_atlas.py`: an on-land waypoint within `LANE_WP_PORT_SNAP_KM` (12 km) of the lane's
OWN start/end port takes that port's pin; the consecutive-duplicate pass then drops it. Other ports are
never substituted (tested: that re-routes legs and adds land km). River lanes untouched. Display-only;
`lanes.csv` untouched. Tag in `waypoint_water_snap` (`port <token>-><port_id> ...`). Toggle
`ATL_LANE_WP_PORT_SNAP=0`.

## Measured (NE10m land, straight EPSG:3996 segments, 2 km sampling)
- 20 lane geometries changed, every other feature byte-identical (1317 feats)
- On-land vertices across changed lanes 91 -> 67; backtrack spurs removed on LANE-016/017/023/027
- Total lane land-on-line 7108 -> 7006 km (LANE-017 82->65, LANE-019 71->59, LANE-007 231->208, LANE-025 58->48)

## Live
- Atlas gen `2026-10-12T13:47:33.145637+00:00`, 1317 features, all 10 alias dirs synced (bad=0)
- Lock: `scripts/check_wpport_endpoint_spur.py` (OK, 19 lanes; LANE-008 Magerøya/Honningsvåg also snapped)
- Prior locks OK: port037 Utqiagvik, river lane order, ICE-043 quarantine

## Next / help wanted (Issue #61)
- LANE-019 Bering Strait still enters Provideniya Bay and touches Wales / Cape Lisburne coast vertices (router 10 km grid)
- LANE-027 lists Hamburg–Felixstowe waypoints after its Murmansk end port (endpoint order check)
