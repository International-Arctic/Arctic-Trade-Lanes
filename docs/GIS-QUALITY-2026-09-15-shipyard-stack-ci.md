# GIS Quality Loop — 2026-09-15 (~09:50+ MSK) shipyard stack CI

## Attempts

1. **ARC-SHIP-069 densify** — Overpass/Nominatim named Sevgiprorybflot **0**. Nearby Murmansk yards exist but are different operators → **skip** (no invented pin).
2. **ARC-PORT-034 / 069 / 153** — harbour/pier/industrial=port Overpass **0** → leave `centroid_clone`.
3. Fleet icebreakers/tankers — no null-island / exact dups; schematic stacks already unstacked.
4. UM `filterPeoplePins` / `filterEventPins` — existing smoke still green (null_island / OOB / swapped / aliases).

## Win shipped

Durable CI: `scripts/check-shipyard-city-stack.mjs` + [SHIPYARD-CITY-STACK.md](./SHIPYARD-CITY-STACK.md).

Live atlas unchanged: `generated` `2026-09-14T15:52:02Z`, **1321** features / **156** ports / **70** shipyards. Exact port↔city stacks **3**; exact shipyard↔city stacks **1** (SHIP-069).
