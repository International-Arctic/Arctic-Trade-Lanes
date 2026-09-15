# GIS Quality — ARC-PORT-043 Provideniya Bay Port densify (2026-09-15 ~14:45 MSK)

## Change
| Field | Before | After |
|-------|--------|-------|
| coords (WGS84) | `64.3833, -173.3000` | `64.4211368, -173.2304897` |
| OSM | — | [way/129101713](https://www.openstreetmap.org/way/129101713) `landuse=harbour` Морской порт Провидения |

Broke soft-stack with **ARC-FAC-391** (NewNew/KRDV Provideniya concept pin left at old coords — no separate OSM for planned complex).

## Quarantine unchanged
ARC-PORT-034 Obskaya, ARC-PORT-069 Chevak, ARC-SHIP-069 Sevgiprorybflot — no verifiable harbour/pier/shipyard OSM this pass.

## Live
- Atlas `generated` `2026-09-15T11:43:39Z`, 1321 features / 156 ports, CRS primary EPSG:3996
- CI: `scripts/check-port043-provideniya-harbour-densify.mjs`
