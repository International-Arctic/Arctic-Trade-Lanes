# Lane waypoint gazetteer QA

Schematic trade-lane polylines on ArcticTradeLanes.com are built from `lanes.csv` waypoint chains plus a WGS84 gazetteer in Zo `atlas-proj/build_atlas.py`.

## Problem (2026-09-07)

`atlas.manifest.json` listed **8 unresolved lane waypoints**, so Kristiansand–Kirkenes and Ningbo–Europe lanes skipped intermediate vertices:

- `Bergen (Fjord Line)`, `Hurtigruten/Havila coastal route`
- `Ningbo (CN)`, `Hamburg/Felixstowe (EU)`, `North Sea`
- Broken paren splits: `NSR 28 permit sections (Chukchi`, `East Siberian`, `Laptev`

Root causes:

1. Naive `waypoints.split("-")` sliced tokens **inside** parentheses.
2. Missing schematic gazetteer anchors for North Sea / Bergen / Ningbo / Hamburg / Laptev / East Siberian / Chukchi seas.
3. CSV rows for ARC-LANE-026/027 used nested hyphens and quoted blobs.

## Fix (live)

1. Paren-safe `_split_waypoints()` (split on `-` only when paren depth is 0; strip CSV quotes).
2. Gazetteer + EXTRA_ANCHORS densified with verifiable schematic WGS84 (ports/cities/seas — not AIS tracks).
3. Cleaned ARC-LANE-026/027 waypoint strings in `ArcticTradeLanes-Dataset/lanes.csv`.

**Result:** `unresolved_lane_waypoints: []` on apex + www  
`https://arctictradelanes.com/data/atlas.manifest.json` (generated `2026-09-07T10:18:39Z`).

Vertex densify examples:

| Lane | Vertices after fix |
|------|-------------------|
| Kristiansand–Kirkenes coastal freight | 7 |
| NSR China–Europe container (Sea Legend) | 12 |
| Yamal LNG export | 8 |
| Northeast Passage container | 9 |

## How to help (good first issue)

- Add missing sea/strait anchors with ≥1 institutional source (IHO / nautical chart gazetteer / port authority).
- Unit-test `_split_waypoints` for nested parentheses and slash aliases (`Hamburg/Felixstowe`).
- Optional CI: fail if `unresolved_lane_waypoints` is non-empty after `build_atlas.py`.

Stay politically neutral in labels; schematic only — no fake AIS precision.

## Follow-up (same day) — start_port teleport

Even with resolved waypoints, a mismatched `start_port_id` can still prepend a continent jump. See [LANE-TELEPORT.md](./LANE-TELEPORT.md) (Homer AK tip on Kristiansand–Kirkenes; fixed live).
