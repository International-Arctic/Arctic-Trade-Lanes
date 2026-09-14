# Centroid-clone quarantine — 2026-09-14 (~13:15 MSK)

GIS Quality Loop: stamp + client quarantine for the **6** remaining exact port↔city stacks (proposed/planned / no distinct OSM harbour). No invented offsets.

## Builder stamp (`atlas-proj/build_atlas.py`)

When a port WGS84 pin matches a city pin at 7 decimal places, emit:

- `properties.geo_quality: "centroid_clone"`
- `properties.centroid_clone_of: <city_id>`

Stamped this cycle:

| ID | Name | City |
|----|------|------|
| ARC-PORT-024 | Prudhoe Bay Oil Terminal | ARC-CITY-029 |
| ARC-PORT-034 | Obskaya LNG Terminal | ARC-CITY-047 |
| ARC-PORT-052 | Grays Bay Deep-Water Port (proposed) | ARC-CITY-051 |
| ARC-PORT-063 | Ittoqqortoormiit Port (planned) | ARC-CITY-069 |
| ARC-PORT-069 | Chevak Barge Landing (planned) | ARC-CITY-073 |
| ARC-PORT-153 | Steensby Inlet (proposed) | ARC-CITY-100 |

NEAR3 Båtsfjord (ARC-PORT-061) left alone (~7 m off city).

## Client filter (`src/lib/filterGeoJson.ts` + OSS `packages/geo-filter`)

Default-on `quarantineCentroidClones`:

1. Quarantine ports with `geo_quality=centroid_clone` / `centroidClone`.
2. Fallback: ports whose name/status contains `proposed`|`planned` and share a city pin at 3 decimal places.

Reason counter: `centroid_clone`. Cities remain visible; stacked port pin is dropped from the accepted FC.

## Live

- Rebuild via `python3 build_atlas.py --dataset ArcticTradeLanes-Dataset --out out`
- Sync `out/atlas*.geojson` → site `public/` (+ `public/data`, `dist`)
- PolarStereographicMap already calls `filterGeoJsonAccepted` (~L1684)
- Live atlas: https://arctictradelanes.com/atlas.geojson — generated `2026-09-14T10:13:49Z`, 1321 features, 156 ports, 6 stamped

## Help wanted

Prefer OSM pier/harbour densify for the six IDs above when geometry appears; until then keep quarantine. See GitHub good-first-issue on Arctic-Trade-Lanes.


## 2026-09-14 ~14:16 MSK extension

Stamp + quarantine also cover **industry** and **shipyards** (see `docs/INDUSTRY-CENTROID-DENSIFY-2026-09-14-1416.md`).
