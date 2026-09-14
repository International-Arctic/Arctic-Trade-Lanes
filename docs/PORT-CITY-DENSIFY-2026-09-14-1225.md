# Port↔city densify — 2026-09-14 (~12:25 MSK)

GIS Quality Loop cycle. Exact port↔city centroid stacks on live atlas: **9 → 6**.

## Densified (OSM-verified)

| Port ID | Name | Was (city centroid) | New WGS84 | OSM |
|---------|------|---------------------|-----------|-----|
| ARC-PORT-121 | DP World Vladivostok ACT (planned) | 43.1155, 131.8855 | 43.0964571, 131.8717880 | relation/5160382 VMTP `landuse=industrial` |
| ARC-PORT-123 | Cape Blossom Deep-Water Port (proposed) | 66.8983, −162.5967 (Kotzebue) | 66.7341667, −162.4950000 | node/5908987347 Cape Blossom |
| ARC-PORT-138 | Koryak FSU / Bechevinskaya Bay | 53.60, 159.53 | 53.2491820, 159.7727540 | node/1972086501 бухта Бечевинская |

Also (shipyard soft-stack, alternate A): **ARC-SHIP-050** Kimek AS → way/231522562 Kimek verft `69.7276851, 30.0333955` (off Kirkenes town pin).

## Skipped (no distinct harbour/industrial/pier OSM)

| ID | Why |
|----|-----|
| ARC-PORT-024 Prudhoe | Sparse OSM; no pier/terminal distinct from city |
| ARC-PORT-034 Obskaya | Inland Novy Urengoy pin; Sabetta already ARC-PORT-004 — do not clone |
| ARC-PORT-052 Grays Bay | Proposed site = city row; bay natural only |
| ARC-PORT-063 Ittoqqortoormiit | Planned; no pier OSM |
| ARC-PORT-069 Chevak | Planned barge landing; no pier OSM |
| ARC-PORT-153 Steensby | Proposed Mary River site; no harbour OSM |

## Live

- https://arctictradelanes.com/atlas.geojson — generated `2026-09-14T09:24:52.855073+00:00`, **1321** features, 156 ports
- Dataset: `International-Arctic/ArcticTradeLanes-Dataset` `b8731e6`

## Remaining stacks (help wanted)

024 Prudhoe, 034 Obskaya, 052 Grays Bay (proposed), 063 Ittoqqortoormiit (planned), 069 Chevak (planned), 153 Steensby (proposed). Prefer pier/harbour/industrial OSM; skip inventing offsets for proposed-only sites. Optional follow-up: `geo_quality: centroid_clone` client quarantine for proposed ports that still share city 3-dp pins.
