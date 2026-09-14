# Port↔city centroid densify — 2026-09-14 ~11:08 MSK

## Win
Live atlas densified **4** exact port↔city stacks onto verifiable OSM pier/harbour/industrial=port coords.

| Port ID | Name | New lat/lon | OSM ref |
|---------|------|-------------|---------|
| ARC-PORT-030 | Kaliningrad Sea Port | 54.7023868, 20.4657734 | relation/21031711 (Калининградский морской торговый порт) |
| ARC-PORT-058 | Port MacKenzie Multimodal Port Expansion | 61.2689911, -149.9202949 | relation/16916230 (`industrial=port`) |
| ARC-PORT-151 | Kangerlussuaq Port | 66.9834732, -50.6887895 | way/80196513 (`man_made=pier`) |
| ARC-PORT-156 | Liinakhamari (Western Gate) | 69.6422303, 31.3600764 | way/85396490 (`man_made=pier` плавпричал №5) |

**Stacks:** live Zo atlas **16 → 12** exact port↔city (same lon/lat). Dataset OSS commit companion: `c6032d7`.

## Live verify
- https://arctictradelanes.com/atlas.geojson (+ `/data/`, www) — generated `2026-09-14T08:26:24Z`, features 1321, ports 156, EPSG:4326 alias.

## Skipped (no verifiable OSM pier this cycle)
Prudhoe Bay (024), Utqiagvik (056), Nikiski LNG (106), Effo Søldarfjørður (124) — Nominatim/Overpass lacked pier/harbour hits (Overpass often 504/429). Planned/proposed rows left on city site centroids by design.

## Remaining exact stacks (help wanted)
024 Prudhoe Bay · 034 Obskaya · 052 Grays Bay (proposed) · 056 Utqiagvik · 063 Ittoqqortoormiit (planned) · 069 Chevak (planned) · 106 Nikiski LNG · 121 DP World Vladivostok (planned) · 123 Cape Blossom (proposed) · 124 Effo Søldarfjørður · 138 Koryak FSU · 153 Steensby Inlet

## UM
`filterPeoplePins` / `filterEventPins` client-side bad-geo smoke OK (no SPA redeploy).
