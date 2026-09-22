# GIS Quality Loop — 2026-09-22 ~11:20 MSK

## Outcome
- **No ATL soft-pin densify** (softish stays **13**). Preferred candidates checked; none clear the `industrial=shipyard` / named-polygon bar.
- **UM win:** `@international-arctic/geo-filter` **0.1.3 → 0.1.4** — `filterPeoplePins` / `filterEventPins` now accept GeoJSON Point `geometry`, nested `location.{lat,lng|lon|longitude}`, `x`/`y` aliases, and quarantine `sentinel_coords` (`999`/`9999`, exact `(1,1)` / axis-unit junk). CI: `bun scripts/check-people-event-pin-filter.mjs`.

## Soft candidates checked (no densify)
| ID | Finding | Blocker |
|----|---------|---------|
| ARC-SHIP-027 Greenland Dockyards | No Nominatim/Overpass `industrial=shipyard` near Nuuk | Need OSM yard polygon |
| ARC-SHIP-029 Northern Marine Repair | No shipyard within ~60 km of Anchorage soft pin | Need named OSM yard |
| ARC-SHIP-052 Kolskaya (planned workshop) | Nearby way/676358072 is **CSKMS** (wrong company) | Do not densify onto CSKMS |
| ARC-SHIP-076 Zhatay | Named building [way/161547566](https://www.openstreetmap.org/way/161547566) @ 62.15967,129.83239 | `building=industrial` only (no `industrial=shipyard`); nearby way/467028290 `landuse=industrial` unnamed |
| ARC-SHIP-055 / 071 | Mantyluoto / Grovfjord | Overpass flaky; Nominatim no shipyard hit — leave soft |

## Still blocked (prior)
Vigor-021, VT Halter-022, Eastern-023, Waigaoqiao-036, Wuchang-039, Sembcorp-033, Hyundai-034.

## Quarantine untouched
PORT-034/069, SHIP-069, Zvezda, Wrangell, Ulstein #37, Naval Group #43.

## Atlas
- Live `/data/atlas.geojson` healthy: `generated` **2026-09-22T06:51:31Z**, **1321** features / **70** shipyards / **156** ports. No rebuild this cycle (no densify).

## OSS
- Arctic-Trade-Lanes: geo-filter 0.1.4 + NOTES + Issue refresh (#45/#46).
- Dataset: no CSV change.
