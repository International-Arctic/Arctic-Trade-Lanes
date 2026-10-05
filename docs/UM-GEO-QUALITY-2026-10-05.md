# UnicornsMap $UM-Radar pin quality — 2026-10-05 (geo-filter 0.1.6)

Live audit of the public UnicornsMap GIS feeds at about 11:30 MSK on 2026-10-05
(`bun scripts/check-um-geo-quality.mjs --live`).

## What we found

| Feed | Finding |
|---|---|
| `GET /api/radar/geo.json` (600 pins, one per entity) | No null-island, out-of-bounds, NaN or duplicate slugs. But **489 of 600 pins (81%) sit on 83 exact shared points**: New York city centroid 74, Seoul Conrad/Yeouido venue fallback 65, Singapore centroid 34, Paris 22, Dubai 17. On a clustered MapLibre source those never split at max zoom, so most profiles can't be clicked. |
| `GET /api/radar/geojson.json` (827 points: 600 `kind=primary` + 227 `kind=site`) | The 0.1.5 `filterPeoplePins` dedupes by slug only, so it **drops all 227 site pins**, including 78 real second locations. 148 of the site pins sit exactly on their own primary (redundant). |
| same feed, `properties.country` | 198 primary rows have `country === locality` (e.g. `"Seoul"`, `"NY"`), because the worker takes the last comma part of `city` as the country. |

## What 0.1.6 adds (opt-in, back-compatible)

- `filterPeoplePins(pins, { siteAware: true })` dedupes slugs per `kind`, keeps real multi-site
  locations, and drops only a site that sits on its own primary (`site_coincident_with_primary`).
  Live: 673 kept (was 595), 148 redundant sites dropped, 78 real sites recovered.
- `unstackSharedPoints(pins, { radiusDeg = 0.04 })` is a display-only golden-angle fan (max about
  4.5 km, stays inside the city). The true point stays in `position_anchor`; flat pins get
  `display_lat` / `display_lng` (their `lat` / `lng` are not rewritten), GeoJSON features get a moved
  geometry plus anchor in `properties`. Tagged `position_quality: 'shared_point_fan'`, stable order by slug.
  Live: 83 stacks / 489 stacked pins become 0.

Same idea as the ATL builder-side program seat fan (`docs/PROGRAM-SEAT-FAN.md`) and co-site nudge
(`docs/CO-SITE-NUDGE.md`), packaged for people/org/event pins.

## Suggested server-side follow-up (not shipped here)

In the UM worker `radarGeojson()`, `country` should only be filled when `city` has two or more
comma parts and the tail is a country (not a US state code); otherwise leave it empty or use the
node's own country field. Kept out of this change because that worker is edited hourly by the
UM-Radar pipeline.

## Viewer wiring

```ts
import { filterPeoplePins, unstackSharedPoints } from '@international-arctic/geo-filter/people';
const { accepted } = filterPeoplePins(fc.features, { siteAware: true });
const display = unstackSharedPoints(accepted); // render geometry; show position_anchor in the popup
```
