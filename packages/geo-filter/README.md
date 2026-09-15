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

People/event filter covers null-island, OOB, swapped lat/lng, missing coords, duplicate slug, soft duplicate point, and `longitude`/`lon` aliases used by UnicornsMap pins.
