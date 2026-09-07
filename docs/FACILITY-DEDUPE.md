# Facility / program pin dedupe (2026-09-07)

## Bugs fixed this cycle

1. **Duplicate Davie Defense Texas pin** — `ARC-SHIP-066` sat on the same lat/lon as `ARC-SHIP-056`.
2. **Duplicate CanNor NIEOP-ERS program pin** — `ARC-PROG-525` repeated `ARC-PROG-046` at the same Yellowknife point.
3. **Missing UN/LOCODE** — filled Skagway `USSGY`, Kirkenes `NOKKN`, Korsakov `RUKOR`, Ny-Ålesund `NONYK`, Hanko/Koverhar `FIHKO`, Vardø `NOVAD`.

## Fix

Dataset drops + `build_atlas.py` shipyard id dedupe and program name+coord soft-dedupe (`program_name_coord_drops` in manifest). Live atlas **1342** features (shipyards 71, programs 713), generated `2026-09-07T12:10:27Z`.

Do **not** coord-only-dedupe shipyards — distinct operators share city centroids.

## CI

```bash
node scripts/check-facility-dedupe.mjs path/to/atlas.4326.geojson
```

## UM

`filterPeoplePins` / `filterEventPins` healthy; no SPA redeploy this cycle.
