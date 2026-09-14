# Port↔city densify — 2026-09-14 (~13:45 MSK)

GIS Quality Loop cycle. Exact port↔city centroid stacks on live atlas: **7 → 6** (only stamped `centroid_clone` proposed/planned remain).

## Densified (OSM-verified)

| Port ID | Name | Was (near city) | New WGS84 | OSM |
|---------|------|-----------------|-----------|-----|
| ARC-PORT-061 | Båtsfjord Port | 70.6344, 29.7182 | 70.6364025, 29.7287468 | node/5355453104 `harbour=yes` |
| ARC-PORT-032 | Vardo Harbor | 70.3705, 31.1107 | 70.374591, 31.104407 | node/269242524 Hurtigruten Vardø `amenity=ferry_terminal` |

Note: first attempt placed 032 on harbour node/5355495287 (already ARC-PORT-094 ytre molo) and soft-deduped 094 via `duplicate_unlocode_coord`. Corrected to Hurtigruten terminal; ports stay **156**, features **1321**.

## Remaining stacks (help wanted / client quarantine)

024 Prudhoe, 034 Obskaya, 052 Grays Bay, 063 Ittoqqortoormiit, 069 Chevak, 153 Steensby — all `geo_quality:centroid_clone`; filterGeoJson quarantines by default.

## Live

- https://arctictradelanes.com/atlas.geojson — generated `2026-09-14T10:52:31Z`, **1321** features, 156 ports
- Companion docs also in Arctic-Trade-Lanes `docs/PORT-CITY-DENSIFY-2026-09-14-1345.md`
