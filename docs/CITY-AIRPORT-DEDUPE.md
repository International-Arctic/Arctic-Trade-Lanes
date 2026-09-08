# City diacritic + airport near-dup densify (2026-09-08)

## Bugs

1. **`ARC-CITY-043` Honningsvag** (ASCII) stacked on **`ARC-CITY-086` Honningsvåg** at `25.970 / 70.982` (3-dp). Same Nordkapp gateway town; the ASCII row had empty sources/confidence.
2. **`ARC-AIR-011`** restated the same Transport Canada / AIF first-project Inuvik (Mike Zubko / YEV) modernization as **`ARC-AIR-005`**, pinned within ~30 m — map users saw a soft-stacked airport twin.

## Fix (Zo control plane)

| ID | Action | Result |
|---|---|---|
| `ARC-CITY-043` | drop | keep sourced `ARC-CITY-086` |
| `ARC-AIR-011` | drop | near-dup of AIF first project |
| `ARC-AIR-005` | densify | OSM Nominatim `Inuvik Airport` / CYEV aerodrome `68.3060612, -133.4822581` |

Live apex+www atlas generated `2026-09-08T11:14:21Z`, features **1322**, cities **104**, airports **10**, city 3-dp stacks **0**. Projection stamp EPSG:4326 unchanged; `/data/atlas.geojson` remains 4326 alias.

## CI

```bash
node scripts/check-city-airport-dedupe.mjs path/to/atlas.4326.geojson
node scripts/check-city-airport-dedupe.mjs --csv-cities path/to/cities.csv --csv-airports path/to/arctic_airports.csv
```

## UM

`filterPeoplePins` / `filterEventPins` smoke OK (null-island + OOB + duplicate quarantine); no SPA redeploy this cycle.

## Notes

Do **not** mass-offset entrepreneur program HQ stacks (Luleå / Anchorage / Nuuk / …) — those are intentional secretariat pins. City diacritic twins and same-announcement airport restates are fair game for drop+densify.
