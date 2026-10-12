# ARC-PORT-034 Obskaya LNG Terminal moved to Sabetta seaport (gis-obsky-0947, 2026-10-12)

## Problem
`ARC-PORT-034` (Obskaya LNG Terminal, Novatek, Arc7, 14 m depth) was a `centroid_clone` of `ARC-CITY-047` Novy Urengoy at `66.0833, 76.6333`. That is an inland gas city about 580 km south of the Gulf of Ob shore, so the live map showed a deep-water LNG terminal in the middle of the tundra.

## Fix
| Field | Before | After |
|---|---|---|
| lat, lon | 66.0833, 76.6333 (Novy Urengoy city centroid) | 71.2733, 72.0725 |
| city_id | ARC-CITY-047 Novy Urengoy | ARC-CITY-005 Sabetta |
| confidence | (blank) | 60 |

Sources:
- Glavgosexpertiza approval, 10 March 2020, reported by [neftegaz.ru](https://neftegaz.ru/news/transport-and-storage/533065-odobren-proekt-stroitelstva-spg-terminala-obskiy-na-yamale/): the terminal is to be built in Sabetta seaport on the west shore of the Gulf of Ob.
- [GEM wiki: Obsky LNG Terminal](https://www.gem.wiki/Obsky_LNG_Terminal), approximate coordinates 71.2733, 72.0725 (about 1 km from the densified `ARC-PORT-004` Sabetta pin, OSM way/533105947).

Precision is site-level approximate (planned facility; GEM notes the project was reconfigured toward gas chemicals in 2021). Name and all other columns are unchanged.

## Live
- Atlas generation `2026-10-12T06:53:57Z`, 1319 features. Geometry changed for `ARC-PORT-034` only; `ARC-CITY-047` lost its now-empty co-site link. No lane ends at this port.
- `/atlas/*`, `/atlas.geojson` and `/data/*` verified on arctictradelanes.com and www. No SPA redeploy, no DNS change.
- Remaining `centroid_clone` pins: `ARC-PORT-069` Chevak barge landing (planned, no mapped landing in OSM) and `ARC-SHIP-069` Sevgiprorybflot (Issue #34, no OSM object found).

## Guard
`python3 scripts/check_port034_obsky.py atlas.wgs84.geojson` fails if the pin drifts more than 3 km from the Sabetta anchor, is stamped `centroid_clone` again, or returns to Novy Urengoy.
