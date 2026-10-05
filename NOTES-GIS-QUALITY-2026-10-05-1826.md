# GIS Quality Loop 2026-10-05 18:26 MSK (gis-lanedepth-1826)

**ATL win:** live lane depth screening (`/bathy/lane-depth.json`, shown in polar-viewer lane popups) now samples each lane exactly as drawn in EPSG:3996.

- Bug: lon/lat densify + equirectangular length sent antimeridian legs (179.9E to 179.9W) the long way round the globe. Bering Strait Transit scored 17,866 km at 23% ocean; NSR Full Transit 32,957 km at 32%.
- Fix: `scripts/build_bathy.py` `densify_lane()` (4 km steps on EPSG:3996 segments, inverse-projected; MultiLineString-ready), antimeridian-safe `seg_km()`, out-of-grid (<58N) samples excluded instead of edge-clamped.
- Result: all 27 lanes re-scored against the current water-routed atlas; 5 antimeridian lanes fixed (Bering Strait Transit 1,655 km / 88.6% ocean); sea-lane ocean coverage 73-98%.
- QA: `python3 scripts/check_lane_depth_antimeridian.py` (27/27 OK, lane_km within 0.94-1.01 of EPSG:3996 length).
- Live file gen 2026-10-05T15:33:09Z; snapshot in `data/arctictradelanes/bathy/`. No SPA redeploy.
- Details: docs/LANE-DEPTH-ANTIMERIDIAN-2026-10-05.md
