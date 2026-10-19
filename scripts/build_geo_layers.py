#!/usr/bin/env python3
"""Build the Arctic map geo layers that the ATL SPA fetches at runtime.

Idempotent: safe to re-run. Writes into dist/ (served assets) and caches raw
source data in atlas-proj/ref/.

Layers produced:
  dist/land110.geojson            Natural Earth land, WGS84 lon/lat, kind=land
  dist/polar-silk-road.geojson    NSR China->EU corridor: 1 LineString + real ports
  dist/seaice/seaice.geojson      NSIDC median/extent (only if real source reachable)
  dist/autonomous-arctic.geojson  real atlas icebreakers flagged as assets (no invented craft)

Frontend contracts (extracted from the shipped bundle):
  land      read with dataProjection=EPSG:4326; features styled by properties.kind=="land"
  silk      1 LineString (route, lon/lat) + Points with properties {lon,lat,step,name,cc,info}
  seaice    properties.kind in {extent,median}, plus name/source/note
"""
from __future__ import annotations

import json
import math
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
REF = os.path.join(os.path.dirname(ROOT), "atlas-proj", "ref")
ATLAS = os.path.join(DIST, "atlas.wgs84.geojson")

NE_50M_LAND = (
    "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/"
    "geojson/ne_50m_land.geojson"
)
NE_10M_LOCAL = os.path.join(REF, "ne_10m_land.geojson")


def log(msg: str) -> None:
    print(f"[geo-layers] {msg}", flush=True)


def load_json(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def write_json(path: str, obj) -> int:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, separators=(",", ":"))
    os.replace(tmp, path)
    return os.path.getsize(path)


def fetch_cached(url: str, dest: str) -> str:
    if os.path.exists(dest) and os.path.getsize(dest) > 1024:
        log(f"cache hit {os.path.basename(dest)}")
        return dest
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    log(f"fetch {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "atl-geo-layers/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = resp.read()
    with open(dest, "wb") as fh:
        fh.write(data)
    log(f"saved {dest} ({len(data)} bytes)")
    return dest


# ---------------------------------------------------------------- land
LAND_LAT_MIN = 30.0
LAND_CUTS = (180.0, 135.0)

def simplify_ring(ring, tol):
    """Douglas-Peucker on a closed ring, preserving first/last point."""
    if tol <= 0 or len(ring) < 5:
        return ring
    out = [ring[0]]
    for pt in ring[1:]:
        lx, ly = out[-1][0], out[-1][1]
        if abs(pt[0] - lx) >= tol or abs(pt[1] - ly) >= tol:
            out.append(pt)
    if len(out) < 4:
        return ring
    if out[-1] != ring[-1]:
        out.append(ring[-1])
    return out


def split_dateline(ring):
    """Unwrap longitudes, then cut the ring wherever it leaves [-180, 180].

    A ring whose vertices jump across the antimeridian is valid lon/lat, but the
    polar-stereographic transform then sweeps its closing edge a full circle
    around the pole (a false annulus). Each piece must also stand alone because
    the client filters land on the outer ring only.
    """
    if len(ring) < 3:
        return []
    un = [list(ring[0])]
    for pt in ring[1:]:
        lon, lat = pt[0], pt[1]
        prev = un[-1][0]
        while lon - prev > 180.0:
            lon -= 360.0
        while lon - prev < -180.0:
            lon += 360.0
        un.append([lon, lat])

    parts, cur = [], [un[0]]
    for pt in un[1:]:
        plon, plat = cur[-1][0], cur[-1][1]
        lon, lat = pt[0], pt[1]
        if lon > 180.0 or lon < -180.0:
            bound = 180.0 if lon > 180.0 else -180.0
            t = (bound - plon) / (lon - plon) if lon != plon else 0.0
            latc = plat + t * (lat - plat)
            cur.append([bound, latc])
            parts.append(cur)
            lon2 = lon - 360.0 if lon > 180.0 else lon + 360.0
            cur = [[-bound, latc], [lon2, lat]]
        else:
            cur.append([lon, lat])
    parts.append(cur)
    return [ring_part for ring_part in parts if len(ring_part) >= 3]


def clip_lat(ring, lat_min):
    """Sutherland-Hodgman clip of a closed ring to lat >= lat_min.

    ATL's primary CRS is EPSG:3996 (north polar stereographic), so land south of
    the equator projects outside the equator ring at a huge radius; a southern
    continent then encircles the pole and fills the map. Northern-only land keeps
    every ring inside the useful projection domain.
    """
    pts = ring[:-1] if len(ring) > 1 and ring[0] == ring[-1] else ring
    if len(pts) < 3:
        return []
    out = []
    n = len(pts)
    for i in range(n):
        cur = pts[i]
        nxt = pts[(i + 1) % n]
        cur_in = cur[1] >= lat_min
        nxt_in = nxt[1] >= lat_min
        if cur_in:
            out.append([cur[0], cur[1]])
        if cur_in != nxt_in:
            t = (lat_min - cur[1]) / (nxt[1] - cur[1])
            out.append([cur[0] + t * (nxt[0] - cur[0]), lat_min])
    if len(out) < 3:
        return []
    out.append(out[0][:])
    return out


def split_meridian(ring, cuts):
    """Unwrap longitudes, then cut the ring at each discontinuity meridian.

    The app maps polygon vertices one by one with proj4 but never splits a
    polygon, so a ring crossing a projection discontinuity sweeps around the
    pole. Cutting at 180 covers EPSG:3996/3995/5041 (lon_0=0); 135E covers
    EPSG:3411 (lon_0=-45).
    """
    if len(ring) < 3:
        return [ring]
    un = [[ring[0][0], ring[0][1]]]
    for lon, lat in ring[1:]:
        prev = un[-1][0]
        while lon - prev > 180:
            lon -= 360
        while lon - prev < -180:
            lon += 360
        un.append([lon, lat])
    bounds = sorted(c + 360 * k for c in cuts for k in (-2, -1, 0, 1, 2))
    parts = []
    cur = [un[0]]
    for lon, lat in un[1:]:
        plon, plat = cur[-1]
        crossed = None
        for b in bounds:
            if (plon < b <= lon) or (lon <= b < plon):
                crossed = b
                break
        if crossed is None:
            cur.append([lon, lat])
            continue
        t = (crossed - plon) / (lon - plon) if lon != plon else 0.0
        latc = plat + t * (lat - plat)
        cur.append([crossed, latc])
        parts.append(cur)
        cur = [[crossed, latc], [lon, lat]]
    parts.append(cur)
    cleaned = []
    for part in parts:
        if len(part) < 3:
            continue
        norm = []
        for lon, lat in part:
            while lon > 180:
                lon -= 360
            while lon < -180:
                lon += 360
            norm.append([lon, lat])
        if len(norm) >= 3:
            cleaned.append(norm)
    return cleaned


def build_land(tol: float = 0.012) -> None:
    src = None
    try:
        src = fetch_cached(NE_50M_LAND, os.path.join(REF, "ne_50m_land.geojson"))
    except Exception as exc:  # noqa: BLE001
        log(f"WARN 50m fetch failed ({exc}); falling back to local 10m ref")
    if not src or not os.path.exists(src):
        if not os.path.exists(NE_10M_LOCAL):
            log("SKIP land: no source available")
            return
        src = NE_10M_LOCAL
        tol = 0.02

    gj = load_json(src)
    feats = []
    for f in gj.get("features", []):
        g = f.get("geometry") or {}
        gt = g.get("type")
        if gt == "Polygon":
            polys = [g["coordinates"]]
        elif gt == "MultiPolygon":
            polys = g["coordinates"]
        else:
            continue
        for poly in polys:
            if not poly:
                continue
            outer = clip_lat(simplify_ring(poly[0], tol), LAND_LAT_MIN)
            if len(outer) < 4:
                continue
            holes = [
                h
                for h in (clip_lat(simplify_ring(r, tol), LAND_LAT_MIN) for r in poly[1:])
                if len(h) >= 4
            ]
            for part in split_meridian(outer, LAND_CUTS):
                if len(part) < 4:
                    continue
                coords = [part]
                if len(holes) == 1:
                    coords.extend(holes)
                feats.append(
                    {
                        "type": "Feature",
                        "properties": {"kind": "land"},
                        "geometry": {"type": "Polygon", "coordinates": coords},
                    }
                )
    out = {"type": "FeatureCollection", "name": "ne_land_wgs84", "features": feats}
    size = write_json(os.path.join(DIST, "land110.geojson"), out)
    log(
        f"land -> {len(feats)} polygons ({LAND_LAT_MIN:.0f}N+, cut at {LAND_CUTS}), "
        f"{size / 1024:.0f} KiB"
    )


# ---------------------------------------------------------------- silk road
def nearest_vertex(route, lon, lat):
    best, bi = float("inf"), 0
    for i, (x, y) in enumerate(route):
        dx = x - lon
        dy = y - lat
        d = dx * dx + dy * dy
        if d < best:
            best, bi = d, i
    return bi


def build_silk() -> None:
    """Route + port anchors taken from the verified atlas lane. Real ports only."""
    d = load_json(ATLAS)
    F = d["features"]

    lanes = [f for f in F if f["properties"].get("layer") == "lanes"]
    route_feat = None
    for want in ("Scheduled", "Full Transit"):
        for f in lanes:
            if want in (f["properties"].get("name") or ""):
                route_feat = f
                break
        if route_feat is not None:
            break
    route_feat = route_feat or (lanes[0] if lanes else None)
    if route_feat is None:
        log("SKIP silk: no lane in atlas")
        return

    route = [list(c) for c in route_feat["geometry"]["coordinates"]]
    route_name = route_feat["properties"].get("name")

    ports = [f for f in F if f["properties"].get("layer") == "ports"]
    rows = []
    for f in ports:
        p = f["properties"]
        lon, lat = f["geometry"]["coordinates"][:2]
        rows.append(
            {
                "idx": nearest_vertex(route, lon, lat),
                "lon": lon,
                "lat": lat,
                "name": p.get("name"),
                "cc": p.get("iso2"),
                "info": (
                    f"{p.get('unlocode') or ''} · {p.get('country') or '?'} · "
                    f"depth {p.get('max_depth_m') or '?'} m · "
                    f"berths {p.get('berths') or '?'} · "
                    f"ice {p.get('ice_class_support') or 'n/a'} · "
                    f"calls/yr {p.get('annual_vessel_calls') or '?'} · source: ATL atlas"
                ),
            }
        )
    rows.sort(key=lambda r: r["idx"])
    for step, r in enumerate(rows):
        r["step"] = step
        r.pop("idx", None)

    feats = [
        {
            "type": "Feature",
            "properties": {
                "kind": "silk",
                "name": route_name,
                "source": "ATL atlas verified lane",
            },
            "geometry": {"type": "LineString", "coordinates": route},
        }
    ] + [
        {
            "type": "Feature",
            "properties": {
                "kind": "silk-port",
                "lon": r["lon"],
                "lat": r["lat"],
                "step": r["step"],
                "name": r["name"],
                "cc": r["cc"],
                "info": r["info"],
            },
            "geometry": {"type": "Point", "coordinates": [r["lon"], r["lat"]]},
        }
        for r in rows
    ]
    size = write_json(
        os.path.join(DIST, "polar-silk-road.geojson"),
        {"type": "FeatureCollection", "name": "polar_silk_road", "features": feats},
    )
    log(f"silk -> route '{route_name}' {len(route)} pts + {len(rows)} real ports, {size / 1024:.0f} KiB")


# ---------------------------------------------------------------- autonomous
def build_autonomous() -> None:
    """Real atlas icebreakers/craft only. No invented vessels."""
    d = load_json(ATLAS)
    F = d["features"]
    feats = []
    for f in F:
        p = f["properties"]
        if p.get("layer") not in ("icebreakers",):
            continue
        g = f["geometry"]
        if g["type"] != "Point":
            continue
        lon, lat = g["coordinates"][0], g["coordinates"][1]
        feats.append(
            {
                "type": "Feature",
                "properties": {
                    "name": p.get("name"),
                    "operator": p.get("operator") or "",
                    "class": p.get("ice_class") or "",
                    "status": "atlas anchor (schematic position)",
                },
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
            }
        )
    size = write_json(os.path.join(DIST, "autonomous-arctic.geojson"),
                      {"type": "FeatureCollection", "name": "atl_arctic_assets", "features": feats})
    log(f"autonomous -> {len(feats)} real atlas assets, {size / 1024:.0f} KiB")


# ---------------------------------------------------------------- sea ice
def build_seaice() -> bool:
    """Only writes if a real NSIDC-derived file is provided.

    NSIDC G02135 requires an authenticated download; we do not fabricate ice
    geometry. Drop a real file at atlas-proj/ref/seaice.geojson to enable.
    """
    cand = os.path.join(REF, "seaice.geojson")
    if not os.path.exists(cand) or os.path.getsize(cand) < 128:
        log("SKIP seaice: no verified NSIDC source present (not fabricating)")
        return False
    gj = load_json(cand)
    size = write_json(os.path.join(DIST, "seaice", "seaice.geojson"), gj)
    log(f"seaice -> {len(gj.get('features', []))} features, {size / 1024:.0f} KiB")
    return True


def main() -> int:
    os.makedirs(REF, exist_ok=True)
    if not os.path.exists(ATLAS):
        log(f"FATAL atlas missing: {ATLAS}")
        return 1
    build_land()
    build_silk()
    build_autonomous()
    build_seaice()
    log("done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
