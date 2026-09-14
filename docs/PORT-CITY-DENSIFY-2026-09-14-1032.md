# Port↔city densify — 2026-09-14 (~10:32 MSK)

GIS Quality Loop cycle. Exact port↔city centroid stacks on live atlas: **23 → 16**.

## Densified (OSM-verified)

| Port ID | Name | New WGS84 | OSM |
|---------|------|-----------|-----|
| ARC-PORT-149 | Barentsburg Port | 78.0637890, 14.2011382 | way/25712063 Ferry Pier |
| ARC-PORT-115 | Port of Adak | 51.8540255, -176.6537206 | way/8901402 Adak Fuel Pier |
| ARC-PORT-085 | Metlakatla Port Improvements | 55.1276713, -131.5701576 | way/137311089 pier |
| ARC-PORT-084 | Cold Bay Dock Replacement | 55.2071566, -162.6958899 | way/551383874 Dock Road |
| ARC-PORT-155 | Vopnafjörður Deep-Water Port | 65.7575271, -14.8183391 | way/220753605 pier |

Dataset: `International-Arctic/ArcticTradeLanes-Dataset` `ports.csv`. Live: https://arctictradelanes.com/atlas.4326.geojson (generated `2026-09-14T07:42:00Z`, 1321 features, 156 ports).

## Remaining stacks (help wanted)

Prudhoe Bay, Kaliningrad, Obskaya/Novy Urengoy, Grays Bay (proposed site), Utqiagvik, Port MacKenzie, Ittoqqortoormiit (planned), Chevak (planned), Nikiski LNG, Vladivostok ACT (planned), Cape Blossom (proposed), Søldarfjørður/Runavík, Koryak FSU, Kangerlussuaq, Steensby Inlet (site), Liinakhamari.

Prefer pier/harbour/industrial=port OSM nodes; skip proposed sites where the city row *is* the port site unless a distinct quay exists.
