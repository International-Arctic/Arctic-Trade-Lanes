# Vardø city diacritic + port/airport densify (2026-09-08)

## Bugs

1. **`ARC-CITY-042` Vardo** (ASCII) soft-stacked on **`ARC-CITY-084` Vardø** (~34 m / same 3-dp cell as harbour pins). Same Finnmark gateway town; ASCII twin mirrored the Honningsvag pattern already fixed earlier today.
2. **`ARC-PORT-094`** (Vardø Fishing Harbour — External Breakwater) sat ~34 m from **`ARC-PORT-032`** Vardo Harbor — users saw a soft commercial/fishing stack.
3. **`ARC-PORT-076`** (Kirkenes Havn KF → Sør-Varanger kommune integration) sat ~62 m from **`ARC-PORT-015`** Kirkenes Port — municipal-governance pin looked like a duplicate harbour.
4. **`ARC-AIR-010`** (Kalaallit Airports International A/S Nuuk & Ilulissat development) sat on **Nuuk city centroid** (`-51.6941 / 64.1814`), not the aerodrome.

## Fix (Zo control plane)

| ID | Action | Result |
|---|---|---|
| `ARC-CITY-042` | drop | keep sourced `ARC-CITY-084` |
| `ARC-PORT-032` | city_id retarget | `ARC-CITY-084` |
| `ARC-PORT-094` | densify | Kystverket/OSM fishing harbour node `70.3759328, 31.1072193` (~618 m from 032) |
| `ARC-PORT-076` | densify | OSM Nominatim Sør-Varanger rådhus `69.7286210, 30.0417013` (~243 m from 015) |
| `ARC-PORT-166` | city_id fix | was wrongly `ARC-CITY-042`; now `ARC-CITY-006` (same as Anadyr Port sibling until an Anadyr city row exists) |
| `ARC-AIR-010` | densify | OSM Mittarfik Nuuk / BGGH `64.1906162, -51.6763924` |

Live apex+www+Zo atlas generated `2026-09-08T11:41:49Z`, features **1321**, cities **103**, airports **10**, city 3-dp stacks **0**. Projection stamp EPSG:4326 unchanged; `/data/atlas.geojson` remains 4326 alias. www CNAME to Zo left grey-cloud.

## CI

```bash
node scripts/check-vardo-city-port-dedupe.mjs path/to/atlas.4326.geojson
node scripts/check-vardo-city-port-dedupe.mjs --csv-cities path/to/cities.csv --csv-ports path/to/ports.csv --csv-airports path/to/arctic_airports.csv
```

## UM

`filterPeoplePins` / `filterEventPins` smoke OK (null-island + OOB quarantine); no SPA redeploy this cycle.

## Notes

Do **not** mass-offset entrepreneur program HQ stacks. City diacritic twins and soft harbour/municipal restates are fair game for drop+densify.
