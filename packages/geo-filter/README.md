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


## 0.1.7 — country normalisation for people/org/event pins (UnicornsMap)

The live `/api/radar/geojson.json` feed derives `country` from the last comma part of `city`, so
`Seoul` becomes country `Seoul`, `San Francisco, CA` becomes `CA` (California, which a naive reader
takes as Canada), and free-text notes leak in (`USA — Hugging Face HQ (...)`). On 2026-10-05 that was
92 distinct country strings for 49 real countries, and 198 of 600 primaries had `country === locality`,
so any country toggle / filter / legend was broken.

```ts
import { normalizePinCountries } from '@international-arctic/geo-filter/country';
const { pins, stats } = normalizePinCountries(fc.features);
// each pin gains properties.countryIso2 ('KR', 'US', ...) + properties.country_quality
const label = new Intl.DisplayNames([locale], { type: 'region' }).of(pin.properties.countryIso2);
```

- Additive: raw `country` is never overwritten; output is shallow copies.
- `country_quality`: `iso_or_name`, `us_state_tail` (`City, ST` / full state name), `city_gazetteer`
  (city or city-state tail), `multi_city_first` (`A / B` or `A · B` multi-seat strings resolve from the first
  seat, which is where the pin sits), `unresolved`.
- Neutral by construction: output is an ISO 3166-1 alpha-2 code only; display names come from the
  viewer's own locale via `Intl.DisplayNames`, so no editorial country label is baked into data.
- Extend the small city table with `{ extraCities: { 'Busan': 'KR' } }`.
- Live result: 827/827 Point features resolved, 92 raw strings to 49 ISO codes.
- Smoke: `bun scripts/check-um-geo-quality.mjs [--live]`. Notes: `docs/UM-COUNTRY-NORMALIZE-2026-10-05.md`.


## 0.1.8 — spiderfy-on-click + "approximate location" flag (UnicornsMap shared points)

For viewers that prefer **not** to move pins (the 0.1.6 `unstackSharedPoints` fan moves them up to
about 4.5 km). Nothing here rewrites coordinates; output is shallow copies.

```ts
import { flagApproximateLocations, groupSharedPoints, spiderfyStackGeoJson } from '@international-arctic/geo-filter/spiderfy';
const { pins, stacks } = flagApproximateLocations(geo.pins);          // + location_precision / approximate_location / shared_point_size
// on click of a stacked marker at the current zoom:
const fc = spiderfyStackGeoJson(pins, stacks[0], { zoom: map.getZoom() }); // leg_end points + leg_line LineStrings
map.getSource('spider').setData(fc);                                   // clear it on zoom / click-away
```

- `groupSharedPoints(pins, { eps = 1e-5, minSize = 2 })`: exact shared points, members sorted by slug.
- `flagApproximateLocations(pins, { minStack = 3 })`: members of stacks of 3+ get
  `location_precision: 'shared_point'`, `approximate_location: true`; everything else `'point'`.
  Two pins at one office are not flagged. Suggested UI text: "Approximate location (shared city point)".
- `spiderfyOffsetsPx(n)` / `spiderfyLegs(anchor, n, { zoom })`: circle for n ≤ 9, Archimedean spiral
  above, in screen pixels at the current zoom (512 px tiles), so legs keep ≥ 27 px spacing at any zoom
  (defaults `legPx = 28`, spiral pitch 30 px). Max radius: 9 → 40 px, 34 → 99 px, 74 → 143 px, 129 → 188 px.
- Works with MapLibre, Leaflet, OpenLayers or a plain canvas; no dependencies.
- Smoke: `bun scripts/check-um-stack-spiderfy.mjs [--live | --file geo.json]`. Notes: `docs/UM-STACK-SPIDERFY-2026-10-20.md`.
