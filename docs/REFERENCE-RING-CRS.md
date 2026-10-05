# Reference overlays and generic fleet anchors (gis-refring-1015, 2026-10-05)

## 1. Reference rings were collapsing onto the North Pole

The atlas ships four reference overlays: `REF-ARCTIC-CIRCLE` (66.5°N), `REF-75N` (IBCAO
true-scale parallel), `REF-80N` and the `REF-TARGET-BAND` annulus (75–80°N).

`_ring()` in `atlas-proj/build_atlas.py` ignored its `crs` argument, so:

- in `atlas.3996.geojson` the rings were stored as **lon/lat degrees** inside an EPSG:3996 (metres) file,
  which renders as a speck a few metres from the pole;
- the WGS84 export then inverse-projected those degree values as if they were metres, which put every
  vertex at **~89.997–89.999°N** in `atlas.wgs84.geojson` / `atlas.4326.geojson` / `atlas.geojson`.

Fix: `_ring()` now projects like `_point()` / `_polyline()`.

```diff
 def _ring(lats, crs, segments=128, lon0=0.0):
     coords = []
     for i in range(segments + 1):
         lon = lon0 + i * (360.0 / segments)
-        coords.append([lon, lats])
+        if crs == 4326:
+            coords.append([lon, lats])
+        else:
+            e, n = get_crs(crs).forward(lon, lats)
+            coords.append([round(e, 3), round(n, 3)])
     return {"type": "LineString", "coordinates": coords}
```

CI guard: `node scripts/check-reference-rings.mjs atlas.wgs84.geojson atlas.3996.geojson`
(the pre-fix atlas fails with 8 errors; the live atlas passes).

## 2. Generic "coastal" route text pinned foreign icebreakers at Murmansk

Fleet pins are schematic: `_route_anchor()` matches the longest `ROUTE_ANCHORS` key in the route text.
The generic key `coastal` maps to Murmansk, which is right for Russian Northern Fleet units but wrong for:

| id | vessel | flag | route text | before | after |
|----|--------|------|------------|--------|-------|
| ARC-ICE-026 | USCGC Mackinaw (WLBB-30) | USA | Great Lakes and Coastal | Murmansk spiral | Great Lakes anchor 45.65, −84.47 (homeport Cheboygan, MI — USCG District 9) |
| ARC-ICE-036 | Ale | Sweden | Coastal and Port Operations | Murmansk spiral | Bay of Bothnia anchor 64.50, 23.00 (Sjöfartsverket state icebreakers are based in Luleå; Ale also serves Lake Vänern) |

Changes: new `"great lakes"` route key, and for `coastal` matches on non-Russian flags the builder now
prefers `COASTAL_BY_COUNTRY`, then `COUNTRY_ANCHORS`, then the old anchor. Russian units keep Murmansk.

Side effect: the Murmansk icebreaker spiral shrank 4→2, so the exact tanker/icebreaker coincidences
there (TNK-022/ICE-014, TNK-023/ICE-015, TNK-049/ICE-026, TNK-050/ICE-036) are gone; the Bothnia spiral
(ICE-027/031/032/053 + Ale) re-spaced. Live atlas coincident point pins: 68 → 60.

Sources: [USCG Cutter Mackinaw](https://www.atlanticarea.uscg.mil/Our-Organization/Great-Lakes-District/Staff/Prevention-Division/Cutters/MACKINAW/),
[Sjöfartsverket — Våra isbrytare](https://www.sjofartsverket.se/sv/tjanster/isbrytning/vara-isbrytare/).

Diff vs previous live atlas: exactly 12 features changed (8 icebreakers, 4 reference overlays); no CSV edits.
