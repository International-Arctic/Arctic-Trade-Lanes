# ARC-PORT-153 Steensby Inlet densify (2026-09-15 ~12:47 MSK)

## Change
- **ARC-PORT-153** Steensby Inlet Deep-Water Port (Baffinland Mary River Steensby Component)
- Old (centroid_clone of ARC-CITY-100): `71.9600, -79.6000`
- New: `70.3851175, -79.0793288`
- OSM: [relation/13745622](https://www.openstreetmap.org/relation/13745622) Steensby Inlet (`natural=bay`)
- Cross-check: Wikidata [Q7605890](https://www.wikidata.org/wiki/Q7605890) P625

## Why
Port↔city soft-stack on a rough north-Baffin pin. Same pattern as ARC-PORT-052 Grays Bay (OSM bay relation center). Unstacks PORT-153 from CITY-100 (~175 km).

## CI
- `scripts/check-port153-steensby-densify.mjs`
- `scripts/check-centroid-clone-remaining.mjs` — PORT-153 removed from expected remainder

## Remaining centroid_clone
ARC-PORT-034, ARC-PORT-069, ARC-SHIP-069

## UM
`filterPeoplePins` / `filterEventPins` smoke OK — no SPA redeploy.
