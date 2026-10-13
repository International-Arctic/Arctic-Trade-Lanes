# GIS Quality — gis-port048-wrangel (~09:27 MSK Europe/Moscow, 2026-10-13)

## Win
Densified **ARC-PORT-048 Wrangel Island Port** off soft round `71.0167 / -178.5000` (~4.1 km) onto OpenStreetMap **node/1554927593** Ushakovskoye abandoned rural locality `70.98046 / -178.48159` (SE Wrangel coast historical settlement/port site).

## Sources (politically neutral gazetteer)
- OSM node/1554927593 (mapcarta.com/N1554927593)
- Wikipedia *Ushakovskoye, Chukotka Autonomous Okrug*: 70°58′51″N 178°29′27″W ≈ 70.98083 / -178.49083 (~0.4 km from OSM)
- Not a modern commercial terminal — Wrangel Island Reserve historical SE-coast settlement/port

## Builder
- `atlas-proj/build_atlas.py` stamps `position_quality=settlement_site` + `position_anchor` (ATL_SCHEMATIC_POSITION allowlist; schematic tags now 4)
- Dataset `ports.csv`: lat/lon/sources/confidence=88/last_verified=2026-10-13

## Live
- Atlas gen `2026-10-13T06:27:11Z`, **1317** features (count unchanged)
- Geometry change: **ARC-PORT-048 only**
- Lock: `scripts/check_port048_wrangel.py`

## Skipped this cycle
- LANE-019 already water_routed 604→47 land km — leave
- FAC-324/365 / PORT-157 / RSC-006 — next soft densify candidates
- UM — no cheap second win
