# Port↔city densify — 2026-09-14 (~16:37 MSK)

GIS Quality Loop cycle. Verified OSM pier densify for **1** remaining proposed/planned stack (no invented offsets).

## Densified (OSM-verified)

| Port ID | Name | Was (city centroid) | New WGS84 | OSM |
|---------|------|---------------------|-----------|-----|
| ARC-PORT-063 | Ittoqqortoormiit Port (planned — EM2026 design) | 70.4845, -21.9666 | 70.4836789, -21.9625036 | way/1089665745 `man_made=pier` (wood; foot=yes) |

Exact 3-dp port↔city stacks among the tracked six: **6 → 5**. PORT-063 no longer stamped `centroid_clone`.

## Still centroid_clone / help wanted

| ID | Name | Overpass note this cycle |
|----|------|--------------------------|
| ARC-PORT-024 | Prudhoe Bay Oil Terminal | industrial=oil landuse only; no pier/harbour/quay |
| ARC-PORT-034 | Obskaya LNG Terminal | 0 harbour/pier hits near Novy Urengoy pin |
| ARC-PORT-052 | Grays Bay Deep-Water Port (proposed) | proposed site = city row; no pier |
| ARC-PORT-069 | Chevak Barge Landing (planned) | 0 pier hits |
| ARC-PORT-153 | Steensby Inlet (proposed) | proposed mineral port; no pier in bbox |

Client `filterGeoJson` continues to quarantine remaining `geo_quality=centroid_clone` ports (cities stay visible).

## Live

- https://arctictradelanes.com/atlas.geojson — generated `2026-09-14T13:48:39.600767+00:00`, **1321** features, 156 ports
- Backup: `ports.csv.bak-gis-1637`
- No SPA redeploy; static atlas sync only
