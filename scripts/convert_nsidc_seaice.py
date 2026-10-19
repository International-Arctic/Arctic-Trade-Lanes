#!/usr/bin/env python3
"""NSIDC G02135 sea-ice shapefile -> dist/seaice/seaice.geojson (WGS84 lon/lat).

Source of truth: NSIDC Sea Ice Index v4.0 (G02135), public no-auth mirror.
  https://noaadata.apps.nsidc.org/NOAA/G02135/north/monthly/shapefiles/shp_median/

Emits the contract the ATL SPA expects:
  kind="median"  -> dashed median ice-edge polyline
  kind="extent"  -> ice polygon
  plus name / source / note

Never fabricates geometry: with no local shapefile it exits non-zero and writes
nothing, so the layer simply stays absent (matching prior behaviour).
"""

import json
import os
import sys

import re

import shapefile  # pyshp
from pyproj import CRS, Transformer

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REF = os.path.join(os.path.dirname(ROOT), "atlas-proj", "ref")
NSIDC = os.path.join(REF, "nsidc")
DIST = os.path.join(ROOT, "dist")
OUT = os.path.join(DIST, "seaice", "seaice.geojson")

SOURCE = "NSIDC Sea Ice Index v4.0 (G02135)"
SOURCE_URL = "https://noaadata.apps.nsidc.org/NOAA/G02135/north/monthly/shapefiles/shp_median/"

MONTHS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def log(msg: str) -> None:
    print(f"[nsidc-seaice] {msg}", flush=True)


def crs_from_prj(shp_path: str) -> CRS:
    prj = os.path.splitext(shp_path)[0] + ".prj"
    if os.path.exists(prj):
        with open(prj, encoding="utf-8", errors="replace") as fh:
            return CRS.from_wkt(fh.read())
    log("WARN no .prj; assuming EPSG:3413 (NSIDC polar stereographic north)")
    return CRS.from_epsg(3413)


def ym_from_name(name: str) -> tuple[int, int] | None:
    """Year+month from an NSIDC YYYYMM token (e.g. extent_N_202510_polygon)."""
    match = re.search(r"(?<!\d)(\d{4})(0[1-9]|1[0-2])(?!\d)", name)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def month_from_name(name: str) -> int | None:
    for i, m in enumerate(MONTHS, start=1):
        if f"_{i:02d}_" in name or f"_{m}_" in name:
            return i
    return None


def ring_to_wgs84(coords, tf) -> list:
    out = []
    for x, y in coords:
        lon, lat = tf.transform(x, y)
        out.append([round(lon, 4), round(lat, 4)])
    return out


def main() -> int:
    if not os.path.isdir(NSIDC):
        log("SKIP: no NSIDC shapefile directory present")
        return 1

    shps = sorted(f for f in os.listdir(NSIDC) if f.endswith(".shp"))
    if not shps:
        log("SKIP: no .shp present")
        return 1

    features = []
    for shp_name in shps:
        path = os.path.join(NSIDC, shp_name)
        crs = crs_from_prj(path)
        tf = Transformer.from_crs(crs, CRS.from_epsg(4326), always_xy=True)
        reader = shapefile.Reader(path)
        kind_label = "median" if "median" in shp_name.lower() else "extent"
        month = month_from_name(shp_name)
        ym = ym_from_name(shp_name)
        if kind_label == "median" and month:
            label = f"NSIDC Sea Ice Index 1981-2010 median ice edge ({MONTHS[month - 1]})"
        elif ym:
            label = f"NSIDC Sea Ice Index monthly {kind_label} ({MONTHS[ym[1] - 1]} {ym[0]})"
        else:
            label = f"NSIDC Sea Ice Index ice {kind_label}"
        count = 0
        for shape in reader.shapes():
            pts = shape.points
            parts = list(shape.parts) + [len(pts)]
            for i in range(len(parts) - 1):
                seg = pts[parts[i]:parts[i + 1]]
                if len(seg) < 2:
                    continue
                coords = ring_to_wgs84(seg, tf)
                closed = coords[0] == coords[-1] and len(coords) >= 4
                if kind_label == "median":
                    geom = {"type": "LineString", "coordinates": coords}
                elif closed and len(coords) >= 4:
                    geom = {"type": "Polygon", "coordinates": [coords]}
                else:
                    geom = {"type": "LineString", "coordinates": coords}
                features.append(
                    {
                        "type": "Feature",
                        "properties": {
                            "kind": kind_label,
                            "name": label,
                            "source": SOURCE,
                            "source_url": SOURCE_URL,
                            "file": shp_name,
                            "note": "Official NSIDC G02135 product, reprojected to WGS84.",
                        },
                        "geometry": geom,
                    }
                )
                count += 1
        log(f"{shp_name} -> {count} feature(s) [{kind_label}]")

    if not features:
        log("SKIP: shapefile yielded no geometry")
        return 1

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    tmp = OUT + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(
            {
                "type": "FeatureCollection",
                "name": "nsidc_sea_ice_g02135",
                "source": SOURCE,
                "source_url": SOURCE_URL,
                "features": features,
            },
            fh,
            ensure_ascii=False,
            separators=(",", ":"),
        )
    os.replace(tmp, OUT)
    log(f"wrote {OUT} ({os.path.getsize(OUT)} bytes, {len(features)} features)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
