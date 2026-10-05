# Lane depth screening: sample lanes as drawn in EPSG:3996 (2026-10-05, gis-lanedepth-1826)

**Live file:** https://arctictradelanes.com/bathy/lane-depth.json (read by the polar viewer's lane popups)

## Bug
`scripts/build_bathy.py` densified each lane in lon/lat degrees and measured segments with an
equirectangular formula. Five lanes cross the antimeridian (Bering Strait Transit, Chukchi Sea
Route, NSR Eastern Section, NSR Full Transit, NSR China-Europe container service). A leg from
179.9°E to 179.9°W was therefore sampled the long way round the planet, through Eurasia and
North America. The live file (generated 2026-09-13, also older than the 2026-10-05 water-routed
lanes) reported, for example:

| Lane | path_km before | after | ocean coverage before | after |
|---|---|---|---|---|
| ARC-LANE-019 Bering Strait Transit | 17,866 | 1,655 | 23.2% | 88.6% |
| ARC-LANE-018 Chukchi Sea Route | 18,283 | 2,132 | 26.9% | 94.2% |
| ARC-LANE-002 NSR Eastern Section | 25,631 | 3,737 | 43.6% | 96.2% |
| ARC-LANE-003 NSR Full Transit | 32,957 | 10,399 | 32.1% | 95.4% |
| ARC-LANE-027 NSR China-Europe container | 44,065 | 18,730 (lane) | 45.3% | 90.1% |

Depth statistics (p05, median, depth class, shallow-bank flags) for those lanes mixed in land
and unrelated ocean basins, so they were not meaningful.

## Fix (additive, build-time only, no SPA change)
- `densify_lane()` samples every 4 km along the lane's straight **EPSG:3996** segments (exactly
  what the polar viewer draws, and what `atlas-proj/lane_route.py` water-routes) and
  inverse-projects to lon/lat. Antimeridian-safe by construction; accepts LineString or an
  RFC 7946 antimeridian-split MultiLineString. Lon-unwrap fallback if pyproj is missing.
- `seg_km()` wraps Δlon into [-180, 180].
- Samples south of the cached 58–90°N ETOPO grid were silently edge-clamped by `bilinear()`;
  they are now excluded from depth stats and counted as `out_of_grid_samples`; `lane_km` is
  the full sampled length, `path_km` the in-grid part.
- Rebuilt from the cached grid against the current live atlas; all 27 lanes re-scored.
  Sea-lane ocean coverage is now 73–98% (was 5–87%).

## QA
`python3 scripts/check_lane_depth_antimeridian.py` compares each lane's `lane_km` with its
EPSG:3996 polyline length (±15%) and requires ≥60% ocean coverage for sea lanes.

## Open follow-ups (help wanted)
- Several lanes are much longer than their `typical_distance_nm` (e.g. NSR Western Section
  ~7,040 km vs 1,400 nm ≈ 2,590 km), which points at zig-zag waypoint chains. Good first
  issue: flag lanes where polyline length > 1.5× `typical_distance_nm`.
- Extend the bathy grid south (or add a second grid) so Baltic and East Asian legs get real
  depths instead of being excluded.

Scientific bathymetry screening only (NOAA NCEI ETOPO 2022 family). Not a nautical chart and not for navigation.
