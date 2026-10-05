# Ship pins stay in open water (gis-shipwater-1152, 2026-10-05)

## Problem

Tankers and icebreakers in the ATL atlas have no AIS truth. Each ship is placed on a
route anchor (a port or sea area named in its route text) and fanned on a golden-angle
spiral so pins sharing an anchor stay clickable. The legacy fan ignored the coastline.
Checked against Natural Earth 10m land (public domain), **53 of 107 ship pins were on land**
in the live atlas generated 2026-10-05T07:48Z:

| Anchor | What happened |
|---|---|
| Sabetta / Yamal / Arctic LNG (71.26N 72.06E) | 12 LNG carriers fanned west onto the Yamal peninsula (up to ~110 km inland) |
| NSR default (73N 90E) | 6 icebreakers + 3 carriers on the Taymyr peninsula (~180–300 km inland) |
| Svalbard / research / tourism (78.22N 15.65E) | 13 icebreakers and research vessels on Spitsbergen around Isfjorden |
| Murmansk / coastal / container (68.98N 33.06E) | 6 ships on the Kola peninsula around the narrow Kola Bay |
| Dudinka / Yenisei / river (69.40N 86.18E) | 4 Norilsk Nickel carriers on the Yenisei banks |
| Others | Nuuk, Baltic (Gotland), St. Lawrence, Alaska North Slope, Northwest Passage |

## Fix (builder-side, display-only)

`atlas-proj/build_atlas.py` (Zo control plane) now walks the same golden-angle spiral
outward from the anchor (step 0.04 deg) and keeps only candidates in open water at least
~1 km (0.012 deg) from any land polygon, up to 2.5 deg from the anchor. Tankers and
icebreakers on the same anchor share one used-point set, so they never stack.

- Moved pins keep the route anchor in `position_anchor` ([lon, lat]) and get
  `display_offset: "water_fan"`; `position_quality` stays `schematic_route_anchor`.
- Single-ship `route_anchor` pins are untouched: they sit on their real port, which can be a
  river or lake port the 10m land mask does not cut out (Dudinka on the Yenisei, Cheboygan on
  Lake Huron, Cambridge Bay, Kirkenes).
- No water within 2.5 deg means the legacy fan is kept (none today).
- Toggle: `ATL_SHIP_WATER_FAN=0`. Mask file: `atlas-proj/ref/ne_10m_land.geojson`
  (Natural Earth 10m land, ~10 MB, static, no paid GIS service).

Live result (atlas generated 2026-10-05T08:59:34Z): 1321 features, ids unchanged, only 101
ship geometries changed, 0 schematic ships on land, 0 exact point stacks, cross-layer
co-site check still OK.

## Known trade-off

The Dudinka river fleet now sits in the first open water the 10m mask knows about, down the
Yenisei about 140–150 km north of Dudinka (still on its Dudinka–Murmansk route). The NSR
default fleet sits on the nearest Kara Sea water off Taymyr (~120–140 km from 73N 90E).
A river- and lake-aware water mask (Natural Earth lakes + river centrelines, or OSM water
polygons clipped to the Arctic) would let these stay closer. See Issue #52.

## QA

```bash
python3 scripts/check_ship_water.py atlas.wgs84.geojson   # needs shapely>=2; fetches NE land if missing
```
