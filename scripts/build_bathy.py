#!/usr/bin/env python3
"""Build the Arctic bathymetry (depth) OSINT layer + lane draft screening.

Source: NOAA NCEI global DEM mosaic ImageServer (ETOPO 2022 family, 60 arc-second,
float32 elevation = +land / -ocean depth). Scientific bathymetry, NOT a nautical
chart and NOT for navigation: official ENCs (S-57 today, S-101 next) come from IHO
RENCs (PRIMAR / IC-ENC) under licence.

Pipeline (rerunnable, CI-friendly, offline-cacheable):
  1. Fetch + cache the Arctic elevation grid (58-90N) at --step degrees.
  2. Marching-squares depth contours at 50/200/500/1000/2500/4000 m, stitched and
     simplified, written as WGS84 GeoJSON.
  3. Sample every atlas shipping lane on a densified path -> shallowest depth,
     percentile depths, shallow-bank flags, land-intersection QA counter.
  4. Write public/bathy/{depth-contours.geojson,lane-depth.json,bathy.manifest.json}.

Usage: python3 scripts/build_bathy.py [--out public] [--refresh] [--step 0.1]
"""

import io
import json
import os
import sys
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone

import math

import numpy as np
from PIL import Image

DEM_URL = (
    "https://gis.ngdc.noaa.gov/arcgis/rest/services/DEM_mosaics/"
    "DEM_global_mosaic/ImageServer/exportImage"
)
DEM_ATTRIB = (
    "NOAA NCEI global DEM mosaic (ETOPO 2022 family, 60 arc-second float32 "
    "elevation/bathymetry) via ArcGIS ImageServer exportImage"
)
GEBCO_WMS = (
    "https://wms.gebco.net/mapserv?service=WMS&version=1.3.0&request=GetMap"
    "&layers=GEBCO_LATEST_3&styles=default&crs=EPSG:4326"
)
DISCLAIMER = (
    "Scientific bathymetry - NOT for navigation. Gridded models are not official "
    "nautical charts; official ENCs (S-57 / S-101) come from IHO RENCs "
    "(PRIMAR / IC-ENC) under licence."
)
LAT_N, LAT_S = 90.0, 58.0
LEVELS = [-50, -200, -500, -1000, -2500, -4000]
CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", ".cache", "bathy")

# 16-case marching-squares edge pairs (edges: 0=top 1=right 2=bottom 3=left)
CASES = {
    1: [(3, 0)], 2: [(0, 1)], 3: [(3, 1)], 4: [(1, 2)], 6: [(0, 2)], 7: [(3, 2)],
    8: [(2, 3)], 9: [(0, 2)], 11: [(1, 2)], 12: [(3, 1)], 13: [(0, 1)], 14: [(3, 0)],
}


def fetch_grid(step, refresh=False):
    """Fetch (and cache) the F32 Arctic elevation grid. Returns (Z, lons, lats)."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache = os.path.abspath(os.path.join(CACHE_DIR, f"etopo_arctic_{step:.3f}.tif"))
    if refresh or not os.path.exists(cache) or os.path.getsize(cache) < 10_000:
        nx = int(round(360.0 / step))
        ny = int(round((LAT_N - LAT_S) / step))
        url = (
            f"{DEM_URL}?bbox=-180,{LAT_S},180,{LAT_N}&bboxSR=4326&imageSR=4326"
            f"&size={nx},{ny}&format=tiff&f=image"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "ArcticTradeLanes-OSINT/1.0"})
        with urllib.request.urlopen(req, timeout=300) as r:
            data = r.read()
        if not data[:2] in (b"II", b"MM"):
            raise SystemExit(f"[bathy] DEM server did not return a TIFF: {data[:120]!r}")
        with open(cache, "wb") as f:
            f.write(data)
        print(f"[bathy] fetched {url} -> {cache} ({len(data)} bytes)")
    else:
        print(f"[bathy] cache hit {cache}")

    Z = np.asarray(Image.open(cache), dtype=np.float64)
    ny, nx = Z.shape
    lons = -180.0 + step * np.arange(nx)
    lats = LAT_N - step * np.arange(ny)
    pole = Z[0, nx // 2]
    print(f"[bathy] grid {nx}x{ny} step {step} deg | pole sample {pole:.1f} m")
    if pole > -2500:
        raise SystemExit("[bathy] sanity check failed: north-pole cell is not abyssal")
    return Z, lons, lats


def bilinear(Z, lons, lats, lon, lat):
    step_lon = lons[1] - lons[0]
    step_lat = lats[1] - lats[0]
    fi = (np.asarray(lon, dtype=float) - lons[0]) / step_lon
    fj = (np.asarray(lat, dtype=float) - lats[0]) / step_lat
    i0 = np.clip(np.floor(fi).astype(int), 0, len(lons) - 2)
    j0 = np.clip(np.floor(fj).astype(int), 0, len(lats) - 2)
    di = np.clip(fi - i0, 0.0, 1.0)
    dj = np.clip(fj - j0, 0.0, 1.0)
    z00 = Z[j0, i0]
    z01 = Z[j0, i0 + 1]
    z10 = Z[j0 + 1, i0]
    z11 = Z[j0 + 1, i0 + 1]
    top = z00 * (1 - di) + z01 * di
    bot = z10 * (1 - di) + z11 * di
    return top * (1 - dj) + bot * dj


def _edge_points(g, level, lons, lats):
    """Interpolated crossing points for all four cell edges (flat arrays)."""
    a, b = g[:-1, :-1], g[:-1, 1:]
    c, d = g[1:, 1:], g[1:, :-1]
    X = lons[:-1][None, :] * np.ones((g.shape[0] - 1, 1))
    Y = lats[:-1][:, None] * np.ones((1, g.shape[1] - 1))
    dlon = lons[1] - lons[0]
    dlat = lats[1] - lats[0]

    def t(va, vb):
        den = vb - va
        with np.errstate(divide="ignore", invalid="ignore"):
            out = np.where(den != 0, -va / den, 0.5)
        return np.clip(np.nan_to_num(out, nan=0.5), 0.0, 1.0)

    tt, tr, tb, tl = t(a, b), t(b, c), t(d, c), t(a, d)
    top = (X + tt * dlon, Y)
    right = (X + dlon, Y + tr * dlat)
    bottom = (X + tb * dlon, Y + dlat)
    left = (X, Y + tl * dlat)
    return {"a": a, "b": b, "c": c, "d": d,
            "edges": {0: top, 1: right, 2: bottom, 3: left},
            "center": (a + b + c + d) / 4.0, "level": level}


def contour_segments(Z, lons, lats, level):
    g = Z - level
    ep = _edge_points(g, level, lons, lats)
    a, b, c, d = ep["a"], ep["b"], ep["c"], ep["d"]
    edges = ep["edges"]
    idx = ((a > 0).astype(np.uint8) | ((b > 0).astype(np.uint8) << 1)
           | ((c > 0).astype(np.uint8) << 2) | ((d > 0).astype(np.uint8) << 3))
    out = []
    ny, nx = idx.shape
    flat = idx.ravel()
    for case, pairs in CASES.items():
        pos = np.flatnonzero(flat == case)
        if pos.size == 0:
            continue
        for (e1, e2) in pairs:
            x1 = edges[e1][0].ravel()[pos]
            y1 = edges[e1][1].ravel()[pos]
            x2 = edges[e2][0].ravel()[pos]
            y2 = edges[e2][1].ravel()[pos]
            out.append(np.stack([x1, y1, x2, y2], axis=1))
    # saddle cases 5 / 10 resolved by the cell-centre value
    for case, (pair_in, pair_out) in ((5, (((3, 0), (1, 2)), ((3, 2), (0, 1)))),
                                      (10, (((0, 1), (2, 3)), ((3, 0), (1, 2))))):
        pos = np.flatnonzero(flat == case)
        if pos.size == 0:
            continue
        ctr = ep["center"].ravel()[pos] > 0
        for inside, pairs in ((True, pair_in), (False, pair_out)):
            sel = pos[ctr] if inside else pos[~ctr]
            if sel.size == 0:
                continue
            for (e1, e2) in pairs:
                x1 = edges[e1][0].ravel()[sel]
                y1 = edges[e1][1].ravel()[sel]
                x2 = edges[e2][0].ravel()[sel]
                y2 = edges[e2][1].ravel()[sel]
                out.append(np.stack([x1, y1, x2, y2], axis=1))
    if not out:
        return np.zeros((0, 4))
    return np.concatenate(out, axis=0)


def stitch(segments, q=2e-4):
    """Join marching-squares segments into polylines."""
    if len(segments) == 0:
        return []
    key = lambda x, y: (int(round(x / q)), int(round(y / q)))
    lookup = defaultdict(list)
    for i, (x1, y1, x2, y2) in enumerate(segments):
        lookup[key(x1, y1)].append((i, 0))
        lookup[key(x2, y2)].append((i, 1))
    used = np.zeros(len(segments), dtype=bool)
    chains = []
    for start in range(len(segments)):
        if used[start]:
            continue
        used[start] = True
        x1, y1, x2, y2 = segments[start]
        chain = [(x1, y1), (x2, y2)]
        extended = True
        while extended:
            extended = False
            for endpt, forward in ((chain[-1], True), (chain[0], False)):
                for i, which in lookup[key(*endpt)]:
                    if used[i]:
                        continue
                    sx1, sy1, sx2, sy2 = segments[i]
                    other = (sx2, sy2) if which == 0 else (sx1, sy1)
                    used[i] = True
                    if forward:
                        chain.append(other)
                    else:
                        chain.insert(0, other)
                    extended = True
                    break
                if extended:
                    break
        chains.append(chain)
    return chains


def rdp(points, tol):
    """Ramer-Douglas-Peucker simplification (iterative)."""
    if len(points) < 3:
        return points[:]
    pts = np.asarray(points, dtype=float)
    keep = np.zeros(len(pts), dtype=bool)
    keep[0] = keep[-1] = True
    stack = [(0, len(pts) - 1)]
    while stack:
        i0, i1 = stack.pop()
        if i1 <= i0 + 1:
            continue
        p0, p1 = pts[i0], pts[i1]
        seg = p1 - p0
        seglen = np.hypot(*seg)
        if seglen == 0:
            dist = np.hypot(*(pts[i0 + 1:i1] - p0).T)
        else:
            rel = pts[i0 + 1:i1] - p0
            dist = np.abs(seg[0] * rel[:, 1] - seg[1] * rel[:, 0]) / seglen
        k = int(np.argmax(dist))
        if dist[k] > tol:
            j = i0 + 1 + k
            keep[j] = True
            stack.extend([(i0, j), (j, i1)])
    return [tuple(p) for p in pts[keep]]


def densify(coords, step_deg):
    out = []
    for i in range(len(coords) - 1):
        lon1, lat1 = coords[i]
        lon2, lat2 = coords[i + 1]
        n = max(1, int(np.ceil(max(abs(lon2 - lon1), abs(lat2 - lat1)) / step_deg)))
        for t in np.linspace(0.0, 1.0, n, endpoint=False):
            out.append((lon1 + t * (lon2 - lon1), lat1 + t * (lat2 - lat1)))
    out.append(tuple(coords[-1]))
    return out


def densify_lane(geom, step_km=4.0):
    """Densify a lane exactly as the polar viewer draws it (gis-lanedepth-1826).

    Lanes are straight segments in EPSG:3996 (lane_route.py water-routes them there), so
    sample along 3996 segments and inverse-project to lon/lat. This is antimeridian-safe:
    the old lon/lat densify sent a 179.9E -> 179.9W leg the long way round the globe
    (Bering Strait Transit scored 17,866 km / 23% ocean). Accepts LineString or
    MultiLineString (RFC 7946 antimeridian split). Falls back to a lon-unwrapped
    lon/lat densify when pyproj is unavailable.
    """
    parts = geom["coordinates"] if geom.get("type") == "MultiLineString" else [geom["coordinates"]]
    try:
        from pyproj import Transformer
        fwd = Transformer.from_crs(4326, 3996, always_xy=True)
        inv = Transformer.from_crs(3996, 4326, always_xy=True)
    except Exception:  # pragma: no cover - fallback path
        fwd = inv = None
    out = []
    for part in parts:
        pts = [(float(c[0]), float(c[1])) for c in part]
        if len(pts) < 2:
            continue
        if fwd is not None:
            xy = [fwd.transform(lo, la) for lo, la in pts]
            for (x1, y1), (x2, y2) in zip(xy, xy[1:]):
                n = max(1, int(math.ceil(math.hypot(x2 - x1, y2 - y1) / (step_km * 1000.0))))
                for t in np.linspace(0.0, 1.0, n, endpoint=False):
                    out.append(tuple(inv.transform(x1 + t * (x2 - x1), y1 + t * (y2 - y1))))
            out.append(pts[-1])
        else:
            un = [pts[0]]
            for lo, la in pts[1:]:
                plo = un[-1][0]
                while lo - plo > 180:
                    lo -= 360
                while lo - plo < -180:
                    lo += 360
                un.append((lo, la))
            out.extend(((lo + 180) % 360 - 180, la) for lo, la in densify(un, step_deg=0.05))
    return out


def classify(median_m, p05_m):
    if median_m < 50:
        return "very_shallow_shelf"
    if median_m < 200:
        return "shelf"
    if median_m < 1000:
        return "slope"
    return "deep_basin"


def seg_km(lon1, lat1, lon2, lat2):
    """Cheap equirectangular segment length in km (sampling QA only)."""
    dlat = (lat2 - lat1) * 111.32
    dl = (lon2 - lon1 + 180.0) % 360.0 - 180.0  # antimeridian-safe (gis-lanedepth-1826)
    dlon = dl * 111.32 * math.cos(math.radians((lat1 + lat2) / 2))
    return math.hypot(dlat, dlon)


def longest_run_km(path, mask):
    """Longest contiguous run of mask==True samples -> (km, pct of total path)."""
    best, cur = 0.0, 0.0
    for i, m in enumerate(mask):
        if m:
            if i > 0:
                a, b = path[i - 1], path[i]
                cur += seg_km(a[0], a[1], b[0], b[1])
            best = max(best, cur)
        else:
            cur = 0.0
    span = sum(seg_km(path[i - 1][0], path[i - 1][1], path[i][0], path[i][1])
               for i in range(1, len(path)))
    return round(best, 1), (round(best / span * 100, 1) if span > 0 else 0.0)


def count_runs(mask, min_len=3):
    """Count contiguous True runs of at least min_len samples."""
    runs, cur = 0, 0
    for m in mask:
        if m:
            cur += 1
        else:
            if cur >= min_len:
                runs += 1
            cur = 0
    return runs + (1 if cur >= min_len else 0)


def main():
    argv = sys.argv
    out_dir = argv[argv.index("--out") + 1] if "--out" in argv else "public"
    step = float(argv[argv.index("--step") + 1]) if "--step" in argv else 0.1
    refresh = "--refresh" in argv
    now = datetime.now(timezone.utc)

    Z, lons, lats = fetch_grid(step, refresh)

    # ---- depth contours -------------------------------------------------
    feats = []
    stats = {}
    for level in LEVELS:
        segs = contour_segments(Z, lons, lats, float(level))
        chains = stitch(segs)
        kept = 0
        pts_total = 0
        for ch in chains:
            if len(ch) < 3:
                continue
            span = max(max(p[0] for p in ch) - min(p[0] for p in ch),
                       max(p[1] for p in ch) - min(p[1] for p in ch))
            if span < 0.4:
                continue
            simp = rdp(ch, tol=0.02)
            if len(simp) < 2:
                continue
            kept += 1
            pts_total += len(simp)
            feats.append({
                "type": "Feature",
                "properties": {"kind": "depth_contour", "layer": "contour",
                               "depth_m": level, "source": DEM_ATTRIB},
                "geometry": {"type": "LineString",
                             "coordinates": [[round(x, 3), round(y, 3)] for x, y in simp]},
            })
        stats[str(level)] = {"polylines": kept, "points": pts_total}
        print(f"[bathy] contour {level} m: {kept} polylines / {pts_total} points")

    os.makedirs(os.path.join(out_dir, "bathy"), exist_ok=True)
    fc = {
        "type": "FeatureCollection",
        "name": "atl_arctic_depth_contours",
        "metadata": {
            "title": "Arctic depth contours (shelf break, slope, basins)",
            "source": DEM_ATTRIB,
            "levels_m": LEVELS,
            "crs": "EPSG:4326",
            "retrieved_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "disclaimer": DISCLAIMER,
        },
        "features": feats,
    }
    contour_path = os.path.join(out_dir, "bathy", "depth-contours.geojson")
    with open(contour_path, "w") as f:
        json.dump(fc, f, separators=(",", ":"))

    # ---- lane draft screening ------------------------------------------
    atlas_path = os.path.join(out_dir, "atlas.wgs84.geojson")
    if not os.path.exists(atlas_path):
        atlas_path = os.path.join(out_dir, "atlas.4326.geojson")
    atlas = json.load(open(atlas_path))
    lanes = [f for f in atlas["features"] if f["properties"].get("layer") == "lanes"]
    lane_out = {}
    for lane in lanes:
        prop = lane["properties"]
        full_path = densify_lane(lane["geometry"])
        if len(full_path) < 2:
            continue
        # samples south of the cached grid (e.g. China/Baltic legs) were edge-clamped
        # by bilinear(); exclude them from depth stats instead of inventing depths
        lat_min, lat_max = float(min(lats[0], lats[-1])), float(max(lats[0], lats[-1]))
        path = [p for p in full_path if lat_min <= p[1] <= lat_max]
        out_of_grid = len(full_path) - len(path)
        full_km = round(sum(seg_km(full_path[i - 1][0], full_path[i - 1][1], full_path[i][0], full_path[i][1])
                            for i in range(1, len(full_path))), 1)
        if len(path) < 2:
            lane_out[prop.get("id")] = {
                "name": prop.get("name"), "samples": 0, "out_of_grid_samples": out_of_grid,
                "lane_km": full_km, "status": "outside_bathy_grid", "source": DEM_ATTRIB,
            }
            continue
        lons_s = np.array([p[0] for p in path])
        lats_s = np.array([p[1] for p in path])
        elev = bilinear(Z, lons, lats, lons_s, lats_s)
        depth = -elev
        land = int((elev > 0).sum())
        if land == len(depth):
            lane_out[prop.get("id")] = {
                "name": prop.get("name"), "samples": int(len(depth)),
                "status": "no_ocean_samples", "source": DEM_ATTRIB,
            }
            continue
        sea = depth[elev <= 0]
        p05 = float(np.percentile(sea, 5))
        over_water = elev <= 0
        land_runs = count_runs(~over_water, min_len=3)
        shallow_mask = list(over_water & (depth < 25))
        run_km, run_pct = longest_run_km(path, shallow_mask)
        span_km = round(sum(seg_km(path[i - 1][0], path[i - 1][1], path[i][0], path[i][1])
                             for i in range(1, len(path))), 1)
        lane_out[prop.get("id")] = {
            "name": prop.get("name"),
            "samples": int(len(depth)),
            "ocean_samples": int(len(sea)),
            "land_samples": land,
            "ocean_coverage_pct": round(float(over_water.mean() * 100), 1),
            "land_runs_ge_3_samples": land_runs,
            "path_km": span_km,
            "lane_km": full_km,
            "out_of_grid_samples": out_of_grid,
            "sampling": "epsg3996_straight_segments_4km",
            "shallowest_depth_m": int(round(float(sea.min()))),
            "p05_depth_m": int(round(p05)),
            "median_depth_m": int(round(float(np.median(sea)))),
            "deepest_depth_m": int(round(float(sea.max()))),
            "samples_lt_25m": int((sea < 25).sum()),
            "samples_lt_50m": int((sea < 50).sum()),
            "samples_lt_100m": int((sea < 100).sum()),
            "samples_lt_200m": int((sea < 200).sum()),
            "pct_lt_50m": round(float((sea < 50).mean() * 100), 1),
            "longest_run_lt_25m_km": run_km,
            "longest_run_lt_25m_pct": run_pct,
            "depth_class": classify(float(np.median(sea)), p05),
            "shallow_bank_flag": bool(run_km >= 10.0),
            "scientific_draft_screen_m": round(max(0.0, p05 - 1.0), 1),
            "geometry_qa": ("synthetic straight-line apex crosses land "
                            f"({land_runs} land runs) - coastal depth stats unreliable")
            if land_runs else "clean_over_water",
            "source": DEM_ATTRIB,
            "disclaimer": DISCLAIMER,
        }
    lane_path = os.path.join(out_dir, "bathy", "lane-depth.json")
    with open(lane_path, "w") as f:
        json.dump({
            "generated": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source": DEM_ATTRIB,
            "grid_deg": step,
            "method": ("lane polyline densified every 4 km along its EPSG:3996 segments (as drawn; "
                       "antimeridian-safe; samples outside the grid excluded), bilinear-sampled on the "
                       "elevation grid; depth = -elevation, land samples excluded from "
                       "statistics but counted; p05 = 5th percentile of ocean depth, "
                       "i.e. available keel depth along 95% of the corridor"),
            "disclaimer": DISCLAIMER,
            "lanes": lane_out,
        }, f, indent=1)

    manifest = {
        "generated": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": DEM_ATTRIB,
        "source_endpoint": DEM_URL,
        "gebco_wms_relief": GEBCO_WMS,
        "grid_deg": step,
        "levels_m": LEVELS,
        "contour_polylines": stats,
        "contour_features": len(feats),
        "contour_bytes": os.path.getsize(contour_path),
        "lane_depth_bytes": os.path.getsize(lane_path),
        "lanes_scored": len(lane_out),
        "shallow_bank_lanes": sorted(k for k, v in lane_out.items() if v.get("shallow_bank_flag")),
        "disclaimer": DISCLAIMER,
    }
    man_path = os.path.join(out_dir, "bathy", "bathy.manifest.json")
    with open(man_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"[bathy] wrote {contour_path} ({manifest['contour_bytes']} bytes), "
          f"{lane_path}, {man_path}")
    print(f"[bathy] shallow-bank lanes: {manifest['shallow_bank_lanes']}")


if __name__ == "__main__":
    main()
