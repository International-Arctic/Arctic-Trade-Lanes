# GIS Quality Loop — 2026-09-15 (~09:45 MSK)

## Hard port re-check (Issue #32)

Overpass + Nominatim re-verification — **no densify** (no invented offsets):

| ID | Result | Evidence |
|----|--------|----------|
| ARC-PORT-034 Obskaya LNG | Skip | Named Obskaya harbour/pier/terminal Overpass bbox (60.5–70N, 65–85E) → **0**. Do **not** clone Sabetta; do **not** use railway Q4330011. |
| ARC-PORT-069 Chevak (planned) | Skip | Overpass 12 km around `61.5278,-165.5864` harbour/pier/ferry_terminal/industrial=port → **0**. Nominatim hit is admin boundary only ([relation/16770756](https://www.openstreetmap.org/relation/16770756)). |
| ARC-PORT-153 Steensby (proposed) | Skip | OSM [relation/13745622](https://www.openstreetmap.org/relation/13745622) Steensby Inlet **bay** center `70.3851175,-79.0793288` (~177 km from synthetic site `71.96,-79.6`). Wikidata [Q7605890](https://www.wikidata.org/wiki/Q7605890) is the inlet, not the mineral port. Skip without published site plan. |

Exact 3-dp port↔city stacks remain **3** (034/069/153). Client `filterGeoJson` continues to quarantine `geo_quality=centroid_clone` (cities stay).

Also stamped: **ARC-SHIP-069** Sevgiprorybflot on Murmansk city centroid — Nominatim/Photon/Wikidata named facility **0**; keep quarantine (do not invent yard pin).

Live atlas unchanged this cycle: `generated` `2026-09-14T15:52:02Z`, **1321** features / **156** ports, CRS primary EPSG:3996.

## Concrete win shipped (UM + ATL OSS)

Additive CI smokes (no SPA redeploy, no App.tsx, static/edge-cheap):

1. `bun scripts/check-people-event-pin-filter.mjs` — UnicornsMap people/event pin QA (`filterPeoplePins` / `filterEventPins`): null-island, OOB, swapped lat/lng, missing, slug dupe, soft point dupe, `longitude` alias.
2. `node scripts/check-centroid-clone-remaining.mjs [atlas.4326.geojson]` — locks remaining quarantine set to the four known IDs above.

Politically neutral OSINT hygiene; commercial rails untouched; no orange-cloud DNS.


## Update 2026-09-15 ~12:47 MSK
ARC-PORT-153 densified off CITY-100 onto OSM R13745622; remaining centroid_clone: 034, 069, SHIP-069.
