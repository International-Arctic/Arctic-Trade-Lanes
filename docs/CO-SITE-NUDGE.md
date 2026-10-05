# Cross-layer co-site nudge (gis-cosite-1045, 2026-10-05)

## Problem
After the programs admin-seat fan (see `PROGRAM-SEAT-FAN.md`), the live atlas still had
**30 cross-layer pairs (60 pins)** sharing one exact coordinate, for example:

- `ARC-PORT-002` Arkhangelsk Sea Port and `ARC-FAC-342` Severny Proekt
- `ARC-PORT-004` Sabetta LNG Terminal and `ARC-FAC-315` Arctic LNG 1 Sabetta cargo terminal
- `ARC-CITY-005` Sabetta and `ARC-RSC-001` Yamal (Sabetta) emergency rescue centre
- `ARC-CITY-001` Murmansk and `ARC-SHIP-069` (centroid clone, quarantined)

In the OpenLayers viewer only the top pin of a stack receives the click, so the second
entity was effectively invisible.

## Fix (builder-side, display-only)
`atlas-proj/build_atlas.py` (Zo control plane) now runs a pass after the program seat fan:

1. Group point features of the layers `ports, industry, shipyards, airports, rescue, rail,
   cities, programs` by WGS84 coordinate rounded to 1e-5 deg.
2. Only groups with **two or more different layers** are touched (same-layer stacks are
   handled by the seat fan / schematic offsets).
3. Sort: `geo_quality == centroid_clone` last, then layer priority
   `ports > industry > shipyards > airports > rescue > rail > cities > programs`, then id.
4. The first feature keeps the true point. Each other feature `i` moves on a golden-angle
   spiral, radius `0.02 deg * sqrt(i / (n-1))` (about 2.2 km), longitude scaled by
   `1/cos(lat)`.
5. Moved features get `display_offset: "co_site_nudge"` and `position_anchor: [lon, lat]`
   (the true point); every grouped feature gets `co_site_ids` listing its partners.
   `position_quality` / `geo_quality` are **not** changed, so source accuracy flags survive.

Toggle off with `ATL_COSITE_NUDGE=0`.

## Result
Live atlas generated `2026-10-05T07:48:15Z`: 1321 features, 30 geometries changed
(21 programs, 5 cities, 4 industry), max shift 2.23 km, no ports moved except the two
quarantined centroid clones (`ARC-PORT-034`, `ARC-PORT-069`), cross-layer stacks 30 -> 0,
no null-island / out-of-bounds / duplicate ids.

## Client guidance
Viewers that want true positions (measurement, routing, export) should read
`position_anchor` when present. `scripts/check-cosite-stack.mjs` is the CI guard.
