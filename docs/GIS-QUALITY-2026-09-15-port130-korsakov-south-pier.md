# GIS Quality — ARC-PORT-130 Korsakov Commercial Sea Port densify (2026-09-15 ~15:51 MSK)

## Change
| Field | Before | After |
|-------|--------|-------|
| coords (WGS84) | `46.6347, 142.774` | `46.62028475714286, 142.75996909285715` |
| OSM | — | [way/104497425](https://www.openstreetmap.org/way/104497425) `man_made=pier` Южный пирс |

Broke soft-stack with **ARC-SHIP-065** (planned KMTP composite shipyard left at old coords — no separate OSM for planned yard).

## Quarantine unchanged
ARC-PORT-034 Obskaya, ARC-PORT-069 Chevak, ARC-SHIP-069 Sevgiprorybflot — no verifiable harbour/pier/shipyard OSM this pass.

## Live
- Atlas `generated` `2026-09-15T12:57:44.791596+00:00`, 1321 features / 156 ports, CRS primary EPSG:3996
- CI: `scripts/check-port130-korsakov-south-pier-densify.mjs`
