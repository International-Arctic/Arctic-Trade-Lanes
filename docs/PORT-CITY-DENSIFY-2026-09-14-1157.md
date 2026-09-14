# Port↔city densify — 2026-09-14 (~11:57 MSK)

GIS Quality Loop cycle. Exact port↔city centroid stacks on live atlas: **12 → 9**.

## Densified (OSM-verified)

| Port ID | Name | Old WGS84 | New WGS84 | OSM |
|---------|------|-----------|-----------|-----|
| ARC-PORT-040 | Honningsvag Port | 70.9821, 25.9704 | 70.9813562, 25.9712896 | way/135566481 man_made=pier |
| ARC-PORT-106 | Alaska LNG Nikiski Marine Terminal | 60.6870, -151.3951 | 60.6875098, -151.3969088 | way/573884426 man_made=pier |
| ARC-PORT-124 | Effo Søldarfjørður Fuel Storage | 62.1683, -6.7840 | 62.1748622, -6.7763668 | way/1150270716 industrial=port |
| ARC-PORT-056 | Utqiagvik (Barrow) Port | 71.2906, -156.7887 | 71.3042960, -156.7568323 | node/846364136 Browerville Boat Launch (seamark slipway; best verifiable marine access in town bbox) |

Dataset: `International-Arctic/ArcticTradeLanes-Dataset` `ports.csv`. Live: https://arctictradelanes.com/atlas.geojson (generated `2026-09-14T08:58:51Z`, 1321 features, 156 ports). Also https://www.arctictradelanes.com/atlas.geojson.

## Skipped this cycle

- ARC-PORT-024 Prudhoe Bay — OSM industrial=oil/pipelines only; no pier/harbour
- ARC-PORT-034 Obskaya LNG — sparse OSM near Novy Urengoy centroid
- ARC-PORT-138 Koryak FSU Bechevinskaya — sparse OSM
- Proposed/planned (no pier): 052, 063, 069, 121, 123, 153

## Remaining exact stacks (help wanted)

Prudhoe Bay Oil Terminal, Obskaya LNG, Grays Bay (proposed), Ittoqqortoormiit (planned), Chevak (planned), DP World Vladivostok ACT (planned), Cape Blossom (proposed), Koryak FSU Bechevinskaya, Steensby Inlet (proposed).

Prefer pier/harbour/industrial=port OSM nodes; skip proposed sites where the city row *is* the port site unless a distinct quay exists.

## UM smoke

`filterPeoplePins` / `filterEventPins` present and healthy in unicornsmap-com; **no SPA redeploy**.
