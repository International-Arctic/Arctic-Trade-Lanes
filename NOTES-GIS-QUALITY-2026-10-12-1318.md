# GIS Quality Loop — gis-shipland-1318 (2026-10-12 ~13:18 MSK)

## Win: lone ships no longer drawn on land anchors

The open-water ship fan (gis-shipwater-1152) only ran for route anchors shared by more than one
ship. A lone tanker or icebreaker kept its raw anchor even when that anchor is a town on land.
Land-mask audit of the live atlas (Natural Earth 10m land, public domain) found 4 lone icebreakers
on land; 0 fanned ships on land.

`atlas-proj/build_atlas.py` now gives a lone ship the nearest open-water slot (>= ~1 km offshore)
when its anchor is on land **and** open water exists within `SINGLE_SHIP_WATER_MAX_R = 0.12°`
(~13 km). Otherwise the raw port anchor is kept, so river / lake / narrow-fjord ports don't jump
20–150 km to open sea. Display-only: `position_anchor` keeps the anchor, `display_offset = water_fan`.
Toggle: `ATL_SHIP_SINGLE_WATER=0`.

| id | ship | before | after | note |
|---|---|---|---|---|
| ARC-ICE-022 | CCGS John A. Macdonald | 69.12 / -105.05 (Cambridge Bay hamlet) | 69.041223 / -105.089097 | ~8.9 km, Cambridge Bay water |
| ARC-ICE-006 | Taymyr | 69.40 / 86.18 (Dudinka) | unchanged | Yenisei river port; nearest NE10m sea ~153 km |
| ARC-ICE-052 | MS Stark | 69.73 / 30.05 (Kirkenes) | unchanged | harbour icebreaker; nearest open slot ~20 km |
| ARC-ICE-026 | USCGC Mackinaw | 45.65 / -84.47 (Cheboygan) | unchanged | Great Lakes (NE10m land includes lakes) |

## Live
- Atlas gen `2026-10-12T10:23:47Z`, **1318** features; baseline rebuild matched live with 0 diffs;
  after patch only ARC-ICE-022 changed (geometry + `position_anchor` / `display_offset`).
- Served aliases synced: `/atlas.*`, `/atlas/*`, `/data/*` on apex + www.
- Locks: `scripts/check_ship_single_water.py` (new), `scripts/check_ship_water.py` still OK
  (107 ships, 0 schematic on land, 3 allowlisted port anchors).

## Help wanted
A finer land mask (OSM water polygons, simplified) would let harbour pins like Kirkenes and river
ports like Dudinka sit on real water without a heavy server. See Issue #61.
