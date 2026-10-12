# River lane ordering + teleport endpoint quarantine (gis-riverlane-1346, 2026-10-12)

## Problem

The two river lanes in the atlas were drawn in raw CSV waypoint order, so they zig-zagged up and
down the river instead of following it:

| Lane | Before (vertex order) | Issue |
|---|---|---|
| ARC-LANE-014 Yenisei River Route | Dudinka -> Yenisei Gulf -> **Igarka** (back south) -> Dikson -> Cape Zhelaniya | 47.6% of the line on NE10m land, backtracks ~450 km |
| ARC-LANE-015 Lena River Route | Tiksi -> Lena delta -> **Yakutsk** (1,150 km south) -> Zhigansk -> **Franz Josef Land** | 62.4% on land; last leg 2,524 km across the Arctic Ocean because `end_port_id` = ARC-PORT-049 (FJL) |

## Fix (display-only, `atlas-proj/build_atlas.py`)

For lanes whose name contains "River":

1. **Quarantine teleport endpoints** — a start/end port farther than `RIVER_LANE_ENDPOINT_MAX_KM`
   (1,500 km) from every other vertex is dropped from the geometry and recorded in
   `endpoint_quarantined` (LANE-015: `ARC-PORT-049`).
2. **Order upstream -> mouth** — Arctic-draining rivers (Ob, Yenisei, Lena, Kolyma, Mackenzie) flow
   north, so vertices sort by ascending latitude. Vertices within `RIVER_MOUTH_PORT_KM` (150 km) of the
   `"<X> River"` mouth anchor (e.g. Tiksi next to the Lena delta) sort just after the mouth.
3. Feature gets `geometry_quality: river_ordered`, `route_order: upstream_to_mouth`,
   `route_vertices_before`.

After:

- Yenisei: Igarka -> Dudinka -> Yenisei Gulf -> Dikson -> Cape Zhelaniya
- Lena: Yakutsk -> Zhigansk -> Lena delta -> Tiksi

CSV rows are untouched (additive-only); `ATL_RIVER_LANE_ORDER=0` restores the old behaviour.
Only these two lane geometries changed; feature count 1318 unchanged. EPSG:3996 output and the
RFC 7946 WGS84 copies are regenerated from the same vertices.

## Lock

`python3 scripts/check_river_lane_order.py [atlas.wgs84.geojson | URL]` fails on any river-lane leg
> 1,500 km, a latitude drop > 0.5 deg before the mouth, a missing `river_ordered` tag, or LANE-015
touching Franz Josef Land. The pre-fix atlas fails it; the 2026-10-12T10:52:56Z atlas passes.

## Open (help wanted)

- River lanes are still straight chords between towns (Natural Earth 10m land includes river
  channels). Densifying them along a public-domain river centreline (Natural Earth
  `ne_10m_rivers_lake_centerlines` or OSM `waterway=river`) would make them follow the channel.
- `lanes.csv` LANE-015 `end_port_id` = ARC-PORT-049 (Franz Josef Land) looks like a data-entry error;
  a river-port row for Yakutsk would be the natural end port. Proposals welcome with a source.
