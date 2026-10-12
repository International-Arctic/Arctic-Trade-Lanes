# GIS Quality Loop — gis-lane008-1843 (2026-10-12 ~18:43 MSK)

## Win: Norwegian Coastal Route follows the real coastal order (no Barents Sea basin detour)

`ARC-LANE-008` Norwegian Coastal Route (Tromsø start, 420 nm typical distance) had waypoints
`Tromso-Barents Sea-Soroya Island-Mageroya Island-Vardo-Honningsvag` and `end_port_id`
ARC-PORT-040 Honningsvåg. Two problems on the map:

1. The generic `Barents Sea` gazetteer anchor is the basin centroid 75.0N 40.0E. For a coastal
   lane it pulled the line ~1,000 km out to sea from Tromsø and ~900 km back to Sørøya.
2. Vardø (31.1E) was listed before Honningsvåg (26.0E), so the line ran east to Vardø and
   then back west to end at Honningsvåg.

Drawn length was **2,528 km** for a lane whose own CSV says 420 nm (~778 km).

## Fix (Dataset `lanes.csv`, one row)

| Field | Before | After |
|---|---|---|
| waypoints | Tromso-Barents Sea-Soroya Island-Mageroya Island-Vardo-Honningsvag | Tromso-Soroya Island-Mageroya Island-Honningsvag-Vardo |
| end_port_id | ARC-PORT-040 Honningsvåg | ARC-PORT-032 Vardø Harbor 70.374591/31.104407 |
| sources | (empty) | Hurtigruten northbound port order (en.wikipedia.org/wiki/Hurtigruten) |
| last_verified | (empty) | 2026-10-12 |

Source order (Hurtigruten northbound): Tromsø, Skjervøy, Øksfjord, Hammerfest, Havøysund,
**Honningsvåg**, Kjøllefjord, Mehamn, Berlevåg, Båtsfjord, **Vardø**, Vadsø, Kirkenes.
No geography is invented: every remaining waypoint already existed in the gazetteer/ports table.

## Measured
- Exactly 1 feature changed (ARC-LANE-008); the other 1,316 are byte-identical
- 23 → 21 vertices; drawn length 2,528 km → **750 km (~405 nm)**, now consistent with 420 nm
- Max vertex 75.0N/40.0E → 71.1N/31.1E (stays on the Finnmark coast)
- Ends at Vardø pin (waypoint snap `Vardo -> ARC-PORT-032`, 0.6 km)

## Live
- Atlas gen `2026-10-12T15:46:29.491557+00:00`, 1317 features, all 10 alias dirs synced (bad=0)
- Lock: `scripts/check_lane008_coastal_order.py` (OK against served atlas); prior locks
  `check_lane_endpoint_revisit.py`, `check_river_lane_order.py`, `check_wpport_endpoint_spur.py` still OK

## Open (help wanted)
- Basin-name waypoints (`Barents Sea`, `Kara Sea`, `Norwegian Sea`, …) resolve to one schematic
  centroid. `ARC-LANE-009` Svalbard Supply (`Tromso-Barents Sea-Bjornoya-…`) has the same
  out-to-40E detour. A generic builder rule (drop a basin waypoint when prev→wp→next is > 3× the
  direct leg) or per-lane sourced waypoints would fix it; contributions welcome.
- LANE-013 Ob Bay out-and-back and LANE-019 Provideniya/Wales coast vertices remain open (see 1743 notes).
