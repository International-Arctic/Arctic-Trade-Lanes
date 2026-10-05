"""lane_route — keep schematic ATL lane polylines on water (2026-10-05 gis-lanewater-1214).

Lanes are built from a handful of gazetteer waypoints and drawn as straight segments in
EPSG:3996. Across the Arctic that cut straight over Taymyr, Yamal, Novaya Zemlya,
Scandinavia and the Canadian archipelago (~29% of sea-lane length on land vs Natural
Earth 10m). This module reroutes ONLY the segments that cross land with an A* search on
a coarse ocean raster in EPSG:3996 (polar stereographic, never Mercator), then
string-pulls the path back to a few clean vertices.

Rules (display-only, additive):
- Every original waypoint stays a vertex; only the leg between two waypoints changes.
- Land is expensive, not forbidden, so ports on land cells, canals and narrow straits
  below grid resolution still connect with the shortest possible land hop.
- River lanes (name contains "River") are left as-is.
- Public-domain mask: Natural Earth 10m land (ref/ne_10m_land.geojson).
- Toggle off with ATL_LANE_WATER_ROUTE=0. Cheap: pure numpy/heapq, runs at build time,
  output is static GeoJSON (no server GIS).
"""

import heapq
import json
import math
import os

import numpy as np

CELL_M = 10_000.0
LAND_COST = 40.0
_GRID = None


def _fwd_arrays(proj, lons, lats):
    out = [proj.forward(lo, la) for lo, la in zip(lons, lats)]
    return [o[0] for o in out], [o[1] for o in out]


def _build_grid(proj, extent):
    """Rasterize Natural Earth land into an EPSG:3996 grid covering extent (minx,miny,maxx,maxy)."""
    from rasterio import features as rfeat
    from rasterio.transform import from_origin
    from shapely.geometry import shape, box, mapping
    from shapely.ops import transform as stransform

    minx, miny, maxx, maxy = extent
    w = int(math.ceil((maxx - minx) / CELL_M))
    h = int(math.ceil((maxy - miny) / CELL_M))
    tr = from_origin(minx, maxy, CELL_M, CELL_M)
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ref", "ne_10m_land.geojson")
    with open(p, encoding="utf-8") as fh:
        land = json.load(fh)["features"]
    clip = box(-180, 15, 180, 90)

    def _f(x, y, z=None):
        xs, ys = _fwd_arrays(proj, list(np.atleast_1d(x)), list(np.atleast_1d(y)))
        return (xs, ys)

    shapes = []
    for f in land:
        g = shape(f["geometry"])
        if not g.intersects(clip):
            continue
        g = g.intersection(clip)
        if g.is_empty:
            continue
        g = g.simplify(0.02)
        if g.is_empty:
            continue
        shapes.append((mapping(stransform(_f, g)), 1))
    mask = rfeat.rasterize(shapes, out_shape=(h, w), transform=tr, fill=0, dtype="uint8")
    return {"mask": mask.astype(bool), "minx": minx, "maxy": maxy, "w": w, "h": h}


def _cell(g, x, y):
    c = int((x - g["minx"]) // CELL_M)
    r = int((g["maxy"] - y) // CELL_M)
    return min(max(r, 0), g["h"] - 1), min(max(c, 0), g["w"] - 1)


def _center(g, r, c):
    return g["minx"] + (c + 0.5) * CELL_M, g["maxy"] - (r + 0.5) * CELL_M


def _land_samples(g, a, b):
    """Number of land samples along straight segment a->b (projected metres)."""
    d = math.hypot(b[0] - a[0], b[1] - a[1])
    n = max(2, int(d / (CELL_M * 0.5)) + 1)
    xs = np.linspace(a[0], b[0], n)
    ys = np.linspace(a[1], b[1], n)
    cs = np.clip(((xs - g["minx"]) // CELL_M).astype(int), 0, g["w"] - 1)
    rs = np.clip(((g["maxy"] - ys) // CELL_M).astype(int), 0, g["h"] - 1)
    return int(g["mask"][rs, cs].sum()), n


def _astar(g, s, t, margin_cells):
    (r0, c0), (r1, c1) = s, t
    rmin = max(0, min(r0, r1) - margin_cells); rmax = min(g["h"] - 1, max(r0, r1) + margin_cells)
    cmin = max(0, min(c0, c1) - margin_cells); cmax = min(g["w"] - 1, max(c0, c1) + margin_cells)
    mask = g["mask"][rmin:rmax + 1, cmin:cmax + 1]
    H, W = mask.shape
    cost = np.where(mask, LAND_COST, 1.0)
    INF = float("inf")
    dist = np.full((H, W), INF)
    prev = np.full((H, W), -1, dtype=np.int64)
    sr, sc, tr_, tc = r0 - rmin, c0 - cmin, r1 - rmin, c1 - cmin
    dist[sr, sc] = 0.0
    pq = [(math.hypot(sr - tr_, sc - tc), 0.0, sr, sc)]
    nbrs = [(-1, 0, 1.0), (1, 0, 1.0), (0, -1, 1.0), (0, 1, 1.0),
            (-1, -1, 1.4142), (-1, 1, 1.4142), (1, -1, 1.4142), (1, 1, 1.4142)]
    while pq:
        _, d, r, c = heapq.heappop(pq)
        if d > dist[r, c]:
            continue
        if r == tr_ and c == tc:
            break
        cc = cost[r, c]
        for dr, dc, w in nbrs:
            rr, c2 = r + dr, c + dc
            if 0 <= rr < H and 0 <= c2 < W:
                nd = d + w * 0.5 * (cc + cost[rr, c2])
                if nd < dist[rr, c2]:
                    dist[rr, c2] = nd
                    prev[rr, c2] = r * W + c
                    heapq.heappush(pq, (nd + math.hypot(rr - tr_, c2 - tc), nd, rr, c2))
    if not math.isfinite(dist[tr_, tc]):
        return None
    path, k = [], tr_ * W + tc
    while k != -1:
        r, c = divmod(int(k), W)
        path.append((r + rmin, c + cmin))
        if r == sr and c == sc:
            break
        k = prev[r, c]
    return path[::-1]


def _pull(g, pts):
    """Douglas-Peucker style string pulling: keep a shortcut only if it adds no land."""
    land_path = [0] * len(pts)
    for i in range(1, len(pts)):
        land_path[i] = land_path[i - 1] + (1 if g["mask"][_cell(g, *pts[i])] else 0)
    keep = {0, len(pts) - 1}
    stack = [(0, len(pts) - 1)]
    while stack:
        i, j = stack.pop()
        if j - i < 2:
            continue
        ls, n = _land_samples(g, pts[i], pts[j])
        # convert path land cells to comparable sample count (2 samples per cell)
        if ls <= 2 * (land_path[j] - land_path[i]) + 2:
            continue
        m = (i + j) // 2
        keep.add(m)
        stack.append((i, m)); stack.append((m, j))
    return [pts[k] for k in sorted(keep)]


def route_lanes_on_water(lanes, proj):
    """lanes: list of (lane_id, name, [(lon,lat),...]). Returns {lane_id: (new_pts, stats)}."""
    global _GRID
    xy_all = []
    for _, _, pts in lanes:
        xy_all.extend(proj.forward(lo, la) for lo, la in pts)
    if not xy_all:
        return {}
    xs = [p[0] for p in xy_all]; ys = [p[1] for p in xy_all]
    pad = 1_200_000.0
    extent = (min(xs) - pad, min(ys) - pad, max(xs) + pad, max(ys) + pad)
    if _GRID is None:
        _GRID = _build_grid(proj, extent)
    g = _GRID
    out = {}
    for lid, name, pts in lanes:
        if "river" in (name or "").lower() or len(pts) < 2:
            continue
        xy = [proj.forward(lo, la) for lo, la in pts]
        new_xy = [xy[0]]
        legs_routed = 0
        before = after = 0.0
        for a, b in zip(xy, xy[1:]):
            ls, n = _land_samples(g, a, b)
            seg = math.hypot(b[0] - a[0], b[1] - a[1])
            before += seg * ls / n
            if ls == 0:
                new_xy.append(b); after += 0.0
                continue
            sa, sb = _cell(g, *a), _cell(g, *b)
            margin = max(60, int(0.7 * seg / CELL_M))
            path = _astar(g, sa, sb, margin)
            if not path:
                new_xy.append(b)
                after += seg * ls / n
                continue
            cpts = [a] + [_center(g, r, c) for r, c in path[1:-1]] + [b]
            cpts = _pull(g, cpts)
            for p, q in zip(cpts, cpts[1:]):
                l2, n2 = _land_samples(g, p, q)
                after += math.hypot(q[0] - p[0], q[1] - p[1]) * l2 / n2
            new_xy.extend(cpts[1:])
            legs_routed += 1
        if legs_routed:
            new_pts = [proj.inverse(x, y) for x, y in new_xy]
            # keep original waypoint lon/lat exactly
            out[lid] = (new_pts, {"legs_routed": legs_routed,
                                  "land_km_before": round(before / 1000.0),
                                  "land_km_after": round(after / 1000.0)})
    return out
