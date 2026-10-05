# @international-arctic/geo-filter

Pure client-side GeoJSON filter used by ArcticTradeLanes.com:

- null island / OOB / NaN quarantine
- duplicate id / point dedupe
- optional schematic unstack for stacked tanker/icebreaker pins
- near-zero serving cost (runs in browser)

See also `docs/CLIENT-GEO-FILTER.md` and Issue #1.


## UnicornsMap events

Use `filterEventPins` (alias of `filterPeoplePins`) on event collage / speaker venue pins before merging into the map pin list. Always run a final `filterPeoplePins` pass on the assembled array so toggles cannot re-introduce null-island / swapped / OOB pins.


## CI smoke (2026-09-15)

```bash
bun scripts/check-people-event-pin-filter.mjs
node scripts/check-centroid-clone-remaining.mjs dataset/atlas.4326.geojson
```

People/event filter covers null-island, OOB, swapped lat/lng, sentinel `(1,1)`/`999`, missing coords, duplicate slug, soft duplicate point, GeoJSON Point geometry, nested `location`, and `longitude`/`lon`/`x`/`y` aliases used by UnicornsMap pins.

## 0.1.5 — admin-seat unstack for `programs` (2026-10-05)

The live atlas has 713 entrepreneur-program pins, and 563 of them sit on just 65 shared
city/capital coordinates (up to 49 on one Luleå pin, 42 on Anchorage, 41 on Nuuk). Those are
honest administrative seats, not bad coordinates, but on the map only the top dot is clickable.

```ts
filterGeoJson(fc, { unstackSchematic: true, unstackAdminSeats: true });
```

- Opt-in (default `false`), so existing callers see identical output.
- Fans each co-located stack into a small golden-angle spiral (`adminSeatRadiusDeg`, default 0.18°),
  ordered by feature id so the layout is stable between builds.
- Display-only: the source coordinate stays in `position_anchor`, and fanned pins are tagged
  `position_quality: 'admin_seat_fan'` plus `position_stack_size` / `position_stack_index`, so popups
  can say "program administered from <city>" instead of implying a site location.
- Layers: `adminSeatLayers` (default `['programs','program']`). Also usable on UnicornsMap
  people/event pins that fall back to a city centroid.

CI smoke: `bun scripts/check-program-seat-stack.mjs atlas.4326.geojson`.


## 0.1.6 — people/org/event pins (UnicornsMap)

- `filterPeoplePins(pins, { siteAware: true })`: primary+site GeoJSON feeds keep real multi-site
  locations; a site on its own primary point is dropped as `site_coincident_with_primary`.
- `unstackSharedPoints(pins, { radiusDeg })`: display-only fan for pins sharing one exact point
  (city centroid / HQ approx / venue fallback); true point kept in `position_anchor`.
- Smoke: `bun scripts/check-um-geo-quality.mjs [--live]`. Notes: `docs/UM-GEO-QUALITY-2026-10-05.md`.
