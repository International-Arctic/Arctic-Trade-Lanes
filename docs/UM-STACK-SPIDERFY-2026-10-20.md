# UnicornsMap shared-point pins: spiderfy-on-click + "approximate location" flag (geo-filter 0.1.8)

Follow-up to `docs/UM-GEO-QUALITY-2026-10-05.md` and issue #53 ("ways to help" item 2). Display-only,
client-side, additive. Nothing in the UnicornsMap production frontend or worker is changed by this.

## Why

Read-only audit of the public feeds on 2026-10-20 at about 14:50 MSK
(`bun scripts/check-um-stack-spiderfy.mjs --live`, exact match within 1e-5°):

| Feed | Pins | Shared points | Pins on shared points | Pins on points with 3+ |
|---|---|---|---|---|
| `GET /api/radar/geo.json` (one pin per entity) | 631 | 87 | 498 (79%) | 392 on 34 points |
| `GET /api/radar/geojson.json` (primary + site) | 859 | 122 | 726 | 604 on 61 points |

Largest stacks in `geo.json`: New York centroid (-74.006, 40.7128) 74, Seoul venue fallback
(126.92663, 37.52539) 65, Singapore centroid (103.85, 1.28) 34, Paris 22, Dubai 18, Singapore CBD 17.
No null-island, NaN or out-of-range coordinates were found.

These points are city centroids or venue fallbacks, not real addresses. On a clustered MapLibre
source the cluster never splits at max zoom, so most of those profiles can't be clicked, and a
single precise-looking pin overstates how well the location is known.

## Two display options (pick one per viewer)

1. **Fan** (`unstackSharedPoints`, 0.1.6): always-visible golden-angle fan, max about 4.5 km, moves
   the drawn pin, keeps the true point in `position_anchor`. Best for static maps and screenshots.
2. **Spiderfy-on-click** (`spiderfyStackGeoJson`, new in 0.1.8): pins stay on the true point; a click
   on a stacked marker draws legs on a circle (n ≤ 9) or Archimedean spiral (n > 9) in screen pixels at
   the current zoom. Legs collapse on zoom or click-away. Best for interactive maps where pins must not move.

Both can be combined with `flagApproximateLocations` (new in 0.1.8): members of a stack of 3 or more
pins get `approximate_location: true`, `location_precision: 'shared_point'` and `shared_point_size`,
so a popup can say "Approximate location (shared city point)". Coordinates are never rewritten.

## Spec

- Grouping: exact match after rounding to `eps = 1e-5°` (about 1 m). Members sorted by `slug`, so the
  layout is stable between refreshes.
- Approximate flag threshold `minStack = 3`: two people at one office can share a real address;
  three or more on one 4–5 decimal point almost never do. Tunable.
- Leg geometry: Web Mercator pixel space, 512 px tiles (MapLibre convention). Circle radius
  `max(legPx, legPx·n/2π)`, first leg due north; spiral radius grows 30 px per turn with an arc step of
  `legPx = 28`. Checked on every live stack at zoom 4–18: minimum neighbour spacing 27.1 px.
  Max radius 40 px (n = 9), 99 px (34), 143 px (74), 188 px (129).
- Output of `spiderfyStackGeoJson`: one `leg_end` Point per member (its properties plus
  `spider_anchor`, `spider_index`, `spider_size`) and one `leg_line` LineString per member, ready for a
  GeoJSON source with a circle layer and a line layer.

## Suggested data-side follow-up (not shipped here)

If the feed itself carried `location_precision` (`address` / `venue` / `city`), the client would not
need to infer it from stack size. That is a server-side change and is out of scope for this module.
