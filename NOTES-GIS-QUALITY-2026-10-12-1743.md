# GIS Quality Loop — gis-endrevisit-1743 (2026-10-12 ~17:43 MSK)

## Win: lanes no longer retrace back to an endpoint port they already passed

Two lanes list their `end_port_id` as an INTERIOR waypoint and keep sailing:

- ARC-LANE-027 NSR China-Europe container service: waypoints `Ningbo-…-Kara Gates-Murmansk-Hamburg-Felixstowe`,
  `end_port_id` ARC-PORT-001 Murmansk.
- ARC-LANE-010 Greenland Coastal Route: waypoints `Nuuk-Disko Bay-Uummannaq-Ilulissat-Upernavik-Melville Bay`,
  `end_port_id` ARC-PORT-011 Ilulissat.

`build_atlas.py` appended the end port again after the last waypoint, so the map drew a duplicate
line straight back along the coast: LANE-027 Felixstowe → Norwegian coast → Murmansk (~6,500 km of
retrace, 35 extra vertices), LANE-010 Melville Bay → Ilulissat (~1,600 km).

`atlas-proj/build_atlas.py`: when a lane's start/end port is already an interior vertex (≤ 5 km,
`LANE_ENDPOINT_REVISIT_KM`) and is not the first/last waypoint, it is not prepended/appended again —
the CSV waypoint order is treated as the sailing order. Tag `endpoint_revisit_skipped`
(e.g. `end ARC-PORT-001 already waypoint #8`). Display-only; `lanes.csv` untouched.
Toggle `ATL_LANE_ENDPOINT_REVISIT=0`.

## Measured
- Exactly 2 lane geometries changed; every other feature byte-identical (1317 feats)
- LANE-027: 165 → 130 vertices, land-on-line (router metric) 735 → 595 km, now ends at Felixstowe (51.96N 1.35E)
- LANE-010: 49 → 39 vertices, land-on-line 141 → 127 km, now ends at Melville Bay (75.5N 62.0W)

## Live
- Atlas gen `2026-10-12T14:47:23.803810+00:00`, 1317 features, all 10 alias dirs synced (bad=0)
- Lock: `atlas-proj/check_lane_endpoint_revisit.py` (OK, 27 lanes, against served atlas)

## Open (help wanted)
- Dataset semantics: should LANE-027 `end_port_id` become Felixstowe/Hamburg (2025 test service called
  Felixstowe/Rotterdam/Hamburg/Gdansk) and LANE-010 end at Upernavik? Needs a sourced lanes.csv edit.
- LANE-008 Norwegian Coastal: CSV order `…Mageroya Island-Vardo-Honningsvag` hops Honningsvåg → Vardø →
  Honningsvåg (~440 km); likely should be `…Honningsvag-Vardo` with end port Vardø.
- LANE-013 Ob Bay Route ends at ARC-PORT-046 Zhelaniye (Cape Zhelaniya, N tip of Novaya Zemlya) after a
  Sabetta → Salekhard → back-up-the-bay out-and-back.
- LANE-019 Provideniya Bay / Wales coast vertices (router 10 km grid) still open.
