# GIS Quality — ARC-PORT-001 Murmansk Commercial Sea Port densify (2026-09-15 ~16:38 MSK)

## Change
| Field | Before | After |
|-------|--------|-------|
| coords (WGS84) | `68.9841, 33.0610` | `68.98092036962025, 33.06344651139241` |
| OSM | — | [way/85150513](https://www.openstreetmap.org/way/85150513) `landuse=industrial` Мурманский морской торговый порт |

Broke soft-stack with **ARC-FAC-336** (Kola Farwater Ltd ship agency left at old coords — no separate OSM office).

Cross-check: [node/4185004064](https://www.openstreetmap.org/node/4185004064) ПАО ММТП office.

## Wrangell (deferred)
ARC-PORT-086↔ARC-SHIP-051 6-Mile Mill soft-stack skipped — planned-only; no pier/harbour OSM at mill site (way/240047996 industrial ~1.5 km; downtown piers ~3.5 km = wrong target).

## Quarantine unchanged
ARC-PORT-034 Obskaya, ARC-PORT-069 Chevak, ARC-SHIP-069 Sevgiprorybflot.

## Live
- Atlas `generated` `2026-09-15T13:48:48.021251+00:00`, 1321 features / 156 ports, CRS primary EPSG:3996
- CI: `scripts/check-port001-murmansk-mmtp-densify.mjs`
