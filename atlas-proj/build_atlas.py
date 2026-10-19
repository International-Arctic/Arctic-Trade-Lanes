#!/usr/bin/env python3
"""build_atlas — Build the ArcticTradeLanes.com GIS OSINT atlas.

Reads the ArcticTradeLanes-Dataset CSVs (ports, cities, lanes, tankers,
icebreakers, shipyards) and emits two GeoJSON FeatureCollections:

  atlas.3996.geojson   — coordinates in EPSG:3996 (IBCAO Polar Stereographic,
                         metres E/N) with an explicit CRS declaration. This is
                         the machine-readable output consumed by the OSINT
                         pipeline (spec task T5: GeoJSON with EPSG:3996).
  atlas.wgs84.geojson  — RFC 7946 compliant copy (lon/lat) for web maps.

Plus atlas.manifest.json with layer counts and distortion KPIs.

Usage: python3 build_atlas.py [--dataset ../../ArcticTradeLanes-Dataset] [--out .]
"""

import argparse
import csv
import datetime
import json
import math
import os
import re as _re_iso2
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from atl_proj import get_crs  # noqa: E402

# --- Waypoint gazetteer (schematic WGS84 anchors for lane geometry) ----------
GAZETTEER = {
    "Kanin Nos": (68.65, 43.30), "Dikson": (73.51, 80.53), "Kara Gates": (70.45, 58.00),
    "Kara Sea": (75.00, 70.00), "Ayon": (69.90, 168.50), "Ayon Ice Edge": (69.90, 168.50),
    "Wrangel Island": (71.00, -178.00), "Bering Strait": (66.00, -169.00),
    "Hudson Bay": (60.00, -86.00), "Fury and Hecla Strait": (69.80, -83.00),
    "Bellot Strait": (72.00, -94.30), "Franklin Strait": (71.50, -96.50),
    "Victoria Strait": (69.50, -100.50), "Coronation Gulf": (68.00, -112.00),
    "Cambridge Bay": (69.12, -105.05), "Amundsen Gulf": (70.00, -118.00),
    "Beaufort Sea": (72.00, -135.00), "Davis Strait": (66.00, -58.00),
    "Baffin Bay": (74.00, -65.00), "Lancaster Sound": (74.20, -84.00),
    "Parry Channel": (74.50, -98.00), "Viscount Melville Sound": (74.50, -108.00),
    "McClure Strait": (74.50, -117.00), "Barents Sea": (75.00, 40.00),
    "Kolguev Island": (69.00, 49.00), "Novaya Zemlya": (74.50, 56.00),
    "White Sea": (65.50, 37.00), "Kandalaksha Gulf": (66.50, 33.50),
    "Norwegian Sea": (68.00, 5.00), "Baltic Sea": (58.00, 19.00),
    "Soroya Island": (70.50, 22.00), "Mageroya Island": (71.00, 25.80),
    "Bjornoya": (74.50, 19.00), "Spitsbergen": (78.20, 16.00),
    "Disko Bay": (69.50, -53.00), "Uummannaq": (70.68, -52.12),
    "Melville Bay": (75.50, -62.00), "Hudson Strait": (62.00, -70.00),
    "Greenland Sea": (76.00, -5.00), "Ob Bay": (69.50, 73.00),
    "Yenisei River": (71.50, 82.00), "Lena River": (72.40, 126.80),
    "Bothnian Bay": (64.50, 23.00), "Gulf of Finland": (60.00, 28.00),
    "Harrison Bay": (70.50, -151.00), "Mackenzie Delta": (69.00, -135.00),
    "Denmark Strait": (67.00, -27.00), "Scoresby Sund": (70.50, -25.00),
    "Hinlopen Strait": (79.60, 19.00), "Nordaustlandet": (79.80, 22.00),
    "Franz Josef Land": (80.80, 55.00), "North Pole": (90.00, 0.00),
    "Alaska": (68.00, -152.00), "Yamal Peninsula": (71.00, 70.00),
    "Ice Edge": None, "Novy Port": (67.70, 72.80), "Yamal": (71.26, 72.06),
    # 2026-09-07 GIS quality: resolve LANE-012/022/026/027 waypoint tokens (schematic WGS84)
    "North Sea": (56.00, 3.00),
    "Chukchi Sea": (69.00, -172.00), "East Siberian Sea": (72.00, 160.00),
    "Laptev Sea": (75.00, 125.00), "Kara seas": (75.00, 70.00),
    "Bergen": (60.39, 5.32), "Bergen (Fjord Line)": (60.39, 5.32),
    "Kristiansand": (58.15, 8.00),
    "Hurtigruten/Havila coastal route": (69.65, 18.96),
    "Ningbo": (29.9392024, 121.8373241), "Ningbo (CN)": (29.9392024, 121.8373241),  # gis-densify-1458 Beilun-2
    "Hamburg": (53.55, 9.99), "Felixstowe": (51.96, 1.35),
    "Hamburg/Felixstowe": (52.75, 5.67), "Hamburg/Felixstowe (EU)": (52.75, 5.67),
    "Kirkenes (35 ports)": (69.73, 30.05),
    "NSR 28 permit sections (Chukchi": (69.00, -172.00),
    "East Siberian": (72.00, 160.00), "Laptev": (75.00, 125.00),
}

# Port/city coords get merged in from the dataset; this map seeds known ones
# that do not appear as port rows but are lane waypoints.
EXTRA_ANCHORS = {
    "Churchill": (58.77, -94.17), "Kirkenes": (69.73, 30.05), "Tromso": (69.65, 18.96),
    "Vardo": (70.37, 31.11), "Honningsvag": (70.98, 25.97), "Longyearbyen": (78.22, 15.65),
    "Nuuk": (64.18, -51.72), "Ilulissat": (69.22, -51.10), "Upernavik": (72.79, -56.15),
    "Narvik": (68.44, 17.43), "Sabetta": (71.26, 72.06), "Kaliningrad": (54.71, 20.45),
    "Salekhard": (66.53, 66.60), "Dudinka": (69.40, 86.18), "Igarka": (67.47, 86.58),
    "Yakutsk": (62.03, 129.73), "Zhigansk": (66.77, 123.37), "Prudhoe Bay": (70.32, -148.70),
    "Point Barrow": (71.29, -156.79), "Wainwright": (70.64, -160.00), "Kotzebue": (66.90, -162.60),
    "Nome": (64.50, -165.44), "Tuktoyaktuk": (69.44, -133.03), "Provideniya": (64.43, -173.23),
    "Anadyr": (64.73, 177.51), "Wales": (65.61, -168.09), "Reykjavik": (64.15, -21.94),
    "Kangerlussuaq": (67.01, -50.69), "Oulu": (65.01, 25.47), "St. Petersburg": (59.93, 30.32),
    "Lavna Coal Terminal": (69.00, 33.50),
    "Kristiansand": (58.15, 8.00), "Bergen": (60.39, 5.32),
    "Ningbo": (29.87, 121.55), "Hamburg": (53.55, 9.99), "Felixstowe": (51.96, 1.35),
}


def _split_waypoints(raw):
    """Split lane waypoint chains on '-' outside parentheses; strip CSV quotes."""
    if raw is None:
        return []
    s = str(raw).strip().strip('"').strip("'")
    parts = []
    buf = []
    depth = 0
    for ch in s:
        if ch == '(':
            depth += 1
            buf.append(ch)
        elif ch == ')':
            depth = max(0, depth - 1)
            buf.append(ch)
        elif ch == '-' and depth == 0:
            tok = ''.join(buf).strip()
            if tok:
                parts.append(tok)
            buf = []
        else:
            buf.append(ch)
    tok = ''.join(buf).strip()
    if tok:
        parts.append(tok)
    return parts


def _haversine_km(lon1, lat1, lon2, lat2):
    """Great-circle distance (km) for lane start/end teleport QA."""
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlmb = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlmb / 2) ** 2
    return 2 * r * math.asin(min(1.0, math.sqrt(a)))


RIVER_LANE_ENDPOINT_MAX_KM = 1500.0  # gis-riverlane-1346: river lane endpoint farther than this from every other vertex is quarantined
RIVER_MOUTH_PORT_KM = 150.0  # gis-riverlane-1346: vertices this close to a "<X> River" mouth anchor sort after the mouth
LANE_ENDPOINT_REVISIT_KM = 5.0  # gis-endrevisit-1743: endpoint port already an interior waypoint
LANE_TELEPORT_MAX_KM = 5000.0  # drop only continent-scale mismatches (e.g. AK↔NO); keep long NSR ends


def _schematic_offset(lat, lon, index, total, radius_deg=0.28):
    """Golden-angle spiral so ships sharing a route anchor are not one pixel.

    Large co-route fleets expand the spiral radius so pins stay separable on
    the polar atlas (schematic positions, not AIS truth).
    """
    import math
    base = radius_deg * max(1.0, math.sqrt(max(total, 1) / 8.0))
    ang = index * 2.399963229728653
    r = base * math.sqrt((index + 1) / max(total, 1))
    dlat = r * math.cos(ang)
    dlon = (r * math.sin(ang)) / max(math.cos(math.radians(lat)), 0.2)
    return lat + dlat, lon + dlon


# --- 2026-10-05 gis-shipwater-1152: keep schematic ship fans off land ---------------
# Tankers/icebreakers have no AIS truth here; they are fanned around a route anchor
# (port or sea area). The legacy spiral put 53 of 107 ships on land (Yamal around
# Sabetta, Taymyr around the NSR default, Svalbard around Longyearbyen, Kola around
# Murmansk). This walks the same golden-angle spiral outward and keeps only candidates
# that are open water (Natural Earth 10m land, public domain, ref/ne_10m_land.geojson)
# at least ~1 km from shore. Display-only: route anchor kept in position_anchor.
# Anchors with no water inside max_r (river ports such as Dudinka) keep the legacy fan.
# Disable with ATL_SHIP_WATER_FAN=0.
_LAND_INDEX = None
_WATER_USED = set()


def _land_index():
    global _LAND_INDEX
    if _LAND_INDEX is None:
        _LAND_INDEX = False
        try:
            import json as _json, os as _os
            from shapely.geometry import shape as _shape
            from shapely.strtree import STRtree as _STRtree
            _p = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "ref", "ne_10m_land.geojson")
            with open(_p, encoding="utf-8") as fh:
                polys = []
                for f in _json.load(fh)["features"]:
                    g = _shape(f["geometry"])
                    polys.extend(list(g.geoms) if g.geom_type == "MultiPolygon" else [g])
            _LAND_INDEX = (_STRtree(polys), polys)
        except Exception as e:  # mask missing -> legacy behaviour, never break the build
            print(f"  ship water fan: land mask unavailable ({e}); legacy fan kept")
    return _LAND_INDEX


def _near_land(lat, lon, shore_deg=0.012):
    idx = _land_index()
    if not idx:
        return None
    from shapely.geometry import Point as _Point
    tree, polys = idx
    probe = _Point(lon, lat).buffer(shore_deg)
    return any(polys[i].intersects(probe) for i in tree.query(probe))


def _water_fan(lat, lon, total, step_deg=0.04, max_r_deg=2.5):
    """Return `total` open-water (lat, lon) points nearest the anchor, or None."""
    import math
    if not _land_index():
        return None
    out, k = [], 0
    while len(out) < total:
        r = step_deg * math.sqrt(k)
        if r > max_r_deg:
            return None
        ang = k * 2.399963229728653
        la = lat + r * math.cos(ang)
        lo = lon + (r * math.sin(ang)) / max(math.cos(math.radians(lat)), 0.2)
        lo = ((lo + 180.0) % 360.0) - 180.0
        _key = (round(la, 4), round(lo, 4))
        if -89.9 < la < 89.9 and _key not in _WATER_USED and not _near_land(la, lo):
            out.append((la, lo))
            _WATER_USED.add(_key)  # tankers + icebreakers on one anchor never share a point
        k += 1
    return out


# --- 2026-10-05 gis-seatland-1754: land-aware admin-seat fan for programs ---
# The 0.18 deg golden-angle seat fan put 169 program pins in open water around coastal
# seats (Helsinki, Reykjavik, Longyearbyen, Nuuk, Iqaluit, Nome, Utqiagvik; up to ~27 km
# offshore). Walk the SAME spiral at the same density but keep only candidates on land
# (Natural Earth 10m, ref/ne_10m_land.geojson). Falls back to the legacy fan when the mask
# is missing or a seat has too little land within max_r_deg. Disable: ATL_PROGRAMS_SEAT_LAND=0.
def _on_land(lat, lon):
    idx = _land_index()
    if not idx:
        return None
    from shapely.geometry import Point as _Point
    tree, polys = idx
    pt = _Point(lon, lat)
    return any(polys[i].contains(pt) for i in tree.query(pt))


# --- 2026-10-12 gis-shipland-1318: single-ship route anchors on land ---------------
# The water fan above only ran for anchors shared by >1 ship, so a lone tanker/icebreaker
# kept its raw route anchor even when that anchor is a town on land (Cambridge Bay for
# CCGS John A. Macdonald, Kirkenes for MS Stark, Dudinka for Taymyr, Cheboygan for USCGC
# Mackinaw). Lone ships whose anchor is on Natural Earth 10m land now get the nearest
# open-water slot (>=~1 km offshore) the same way; anchor kept in position_anchor.
# Lone ships only move if open water is within SINGLE_SHIP_WATER_MAX_R (~13 km), so river
# and narrow-fjord harbours (Dudinka on the Yenisei, Kirkenes) keep their raw port anchor
# instead of jumping 20-150 km to the nearest open sea.
# Disable with ATL_SHIP_SINGLE_WATER=0 (or ATL_SHIP_WATER_FAN=0 for all ship fans).
SINGLE_SHIP_WATER_MAX_R = 0.12


# --- 2026-10-12 gis-lanewp-1418: region/landmass lane waypoints on land ------------------
# Lane waypoints come from the GAZETTEER. A few tokens name a landmass or bay and resolve to a
# point ON Natural Earth 10m land with no water within ~15 km: "Alaska" (68N 152W, Brooks Range;
# LANE-025 Transpolar ended ~270 km inland), "Yamal Peninsula" (LANE-023 spur onto Yamal),
# "Kolguev Island" (LANE-006), "Disko Bay" (on Disko Island), "Mackenzie Delta". The water router
# keeps every waypoint as a vertex, so those legs were forced onto land. Such a waypoint now moves
# to open water (>= ~1 km offshore) chosen by 2*offset + d(prev) + d(next) among candidates within
# 60 km of the nearest water (max LANE_WP_WATER_MAX_KM). Ports, towns, dataset/seed anchors and
# "<X> River" tokens are never moved; River lanes untouched. Display-only; CSV untouched.
# Disable with ATL_LANE_WAYPOINT_WATER=0.
LANE_WP_KEEP_KM = 15.0

# --- 2026-10-12 gis-wpport-1636: redundant endpoint-town waypoints on land ------------------
# Several lanes repeat their own start/end port as a town GAZETTEER waypoint ("Prudhoe Bay",
# "Sabetta", "Barrow", "Murmansk" ...). The token resolves to a settlement centroid ON Natural
# Earth 10m land a few km from the OSM-densified harbour pin, and the router keeps every waypoint
# as a vertex, so the lane made a short inland spur (ARC-LANE-016/017: Prudhoe Bay port -> town
# centroid 9 km inland -> back out to sea). An on-land waypoint within LANE_WP_PORT_SNAP_KM of the
# lane's OWN start/end port now takes that port's pin; the consecutive-duplicate pass then removes
# the spur. Other ports are never substituted (that re-routes legs). River lanes untouched.
# Display-only; CSV untouched. Disable with ATL_LANE_WP_PORT_SNAP=0.
LANE_WP_PORT_SNAP_KM = 12.0
LANE_WP_WATER_MAX_KM = 350.0


def _dest_pt(lat, lon, km, brg):
    import math
    R = 6371.0
    d = km / R
    b = math.radians(brg)
    p1, l1 = math.radians(lat), math.radians(lon)
    p2 = math.asin(math.sin(p1) * math.cos(d) + math.cos(p1) * math.sin(d) * math.cos(b))
    l2 = l1 + math.atan2(math.sin(b) * math.sin(d) * math.cos(p1), math.cos(d) - math.sin(p1) * math.sin(p2))
    return math.degrees(p2), ((math.degrees(l2) + 540.0) % 360.0) - 180.0


def _water_within_km(lat, lon, km, step=2.0):
    r = step
    while r <= km:
        for b in range(0, 360, 10):
            if not _on_land(*_dest_pt(lat, lon, r, b)):
                return r
        r += step
    return None


def _lane_wp_water(lat, lon, prev_ll, next_ll, step=3.0):
    """(lat, lon, offset_km) for an open-water slot near a landlocked waypoint, or None."""
    def _hk(a, b):
        return _haversine_km(a[1], a[0], b[1], b[0])
    cands, first, r = [], None, step
    while r <= LANE_WP_WATER_MAX_KM:
        for b in range(0, 360, 5):
            la, lo = _dest_pt(lat, lon, r, b)
            if -89.9 < la < 89.9 and not _near_land(la, lo):
                cands.append((r, la, lo))
                if first is None:
                    first = r
        if first is not None and r > first + 60.0:
            break
        r += step
    if not cands:
        return None

    def _score(c):
        sc = 2.0 * c[0]
        if prev_ll:
            sc += _hk(prev_ll, (c[1], c[2]))
        if next_ll:
            sc += _hk((c[1], c[2]), next_ll)
        return sc
    best = min(cands, key=_score)
    return round(best[1], 6), round(best[2], 6), round(best[0], 1)


def _single_on_land(coord):
    import os as _os
    if _os.environ.get("ATL_SHIP_SINGLE_WATER", "1") == "0":
        return False
    return bool(_on_land(coord[0], coord[1]))


def _land_seat_slots(alat, alon, n, base_r=0.18, max_r_deg=0.45):
    import math, os as _os
    if _os.environ.get("ATL_PROGRAMS_SEAT_LAND", "1") == "0" or not _land_index():
        return None
    out, k = [], 0
    while len(out) < n:
        r = base_r * math.sqrt((k + 1) / n)
        if r > max_r_deg:
            return None
        ang = k * 2.399963229728653
        la = alat + r * math.cos(ang)
        lo = alon + (r * math.sin(ang)) / max(math.cos(math.radians(alat)), 0.2)
        if _on_land(la, lo):
            out.append((la, lo))
        k += 1
    return out


ROUTE_ANCHORS = {
    # Prefer longest substring match in _route_anchor (sorted by key length).
    "sabetta": (71.26, 72.06), "murmansk": (68.98, 33.06), "pevek": (69.70, 170.27),
    "nsr": (73.00, 90.00), "arctic bridge": (58.77, -94.17), "dudinka": (69.40, 86.18),
    "tiksi": (71.63, 128.87), "chukotka": (66.00, 175.00), "yamal": (71.26, 72.06),
    "svalbard": (78.22, 15.65), "greenland": (70.00, -45.00), "northwest": (68.00, -100.00),
    # Fleet densification (2026-09-07 GIS quality): Baltic / Nordic / Canada / Alaska
    "gulf of finland": (60.00, 28.00), "bothnia": (64.50, 23.00), "baltic": (58.00, 19.00),
    "kattegat": (57.50, 11.50), "north sea": (56.00, 3.00), "norwegian": (68.00, 5.00),
    "barents": (75.00, 40.00), "yenisei": (69.40, 86.18), "kirkenes": (69.73, 30.05),
    "st. lawrence": (48.50, -68.50), "newfoundland": (50.00, -55.00),
    "high arctic": (78.22, 15.65), "high latitudes": (78.22, 15.65),
    "research": (78.22, 15.65), "tourism": (78.22, 15.65), "expedition": (78.22, 15.65),
    "coastal": (68.98, 33.06), "river": (69.40, 86.18), "offshore": (71.00, 35.00),
    "container": (68.98, 33.06), "arctic lng": (71.26, 72.06), "lng 2": (71.26, 72.06),
    "alaska": (70.50, -150.00), "beaufort": (72.00, -135.00), "hudson": (60.00, -86.00),
    # 2026-10-05 gis-refring-1015: USCGC Mackinaw (WLBB-30) homeport Cheboygan, MI (USCG District 9)
    "great lakes": (45.65, -84.47),
}

# Generic "coastal" route text historically fell onto the Murmansk anchor for every flag
# (e.g. Swedish Ale). For non-Russian flags prefer a home-waters anchor; Russia keeps Murmansk.
# Sweden: state icebreakers are based in Lulea and work the Bay of Bothnia (Sjofartsverket).
COASTAL_BY_COUNTRY = {
    "sweden": (64.50, 23.00),
}

# When route text matches no ROUTE_ANCHORS key, fall back by flag/country so fleets
# do not collapse onto the default NSR centroid (73N, 90E).

# ISO 3166-1 alpha-2 for atlas props (join arctic_reference / client filters).
# Prefer UN/LOCODE prefix when present; else country-name map (neutral codes).
COUNTRY_TO_ISO2 = {
    "russia": "RU", "usa": "US", "united states": "US", "alaska": "US",
    "norway": "NO", "iceland": "IS", "greenland": "GL", "canada": "CA",
    "finland": "FI", "sweden": "SE", "faroe islands": "FO", "faroe": "FO",
    "svalbard": "SJ", "norway (svalbard)": "SJ", "south korea": "KR",
    "korea": "KR", "china": "CN", "japan": "JP", "germany": "DE",
    "greece": "GR", "switzerland": "CH", "denmark": "DK", "danish": "DK",
    "romania": "RO", "france": "FR", "netherlands": "NL", "turkey": "TR",
    "uk": "GB", "united kingdom": "GB", "great britain": "GB",
    "lithuania": "LT", "latvia": "LV", "estonia": "EE", "austria": "AT",
    "belgium": "BE", "poland": "PL", "portugal": "PT", "spain": "ES",
    "italy": "IT", "ireland": "IE", "aland": "AX", "åland": "AX",
}

# HQ / secretariat city → ISO2 for multi-country Nordic/EU/UArctic program pins.
CITY_TO_ISO2 = {
    "helsinki": "FI", "rovaniemi": "FI", "oulu": "FI", "tampere": "FI",
    "oslo": "NO", "tromsø": "NO", "tromso": "NO", "bergen": "NO", "kirkenes": "NO",
    "stockholm": "SE", "luleå": "SE", "lulea": "SE", "kiruna": "SE", "umeå": "SE", "umea": "SE",
    "copenhagen": "DK", "nuuk": "GL", "reykjavik": "IS", "reykjavík": "IS",
    "brussels": "BE", "brussel": "BE", "vienna": "AT", "wien": "AT",
    "klaipeda": "LT", "klaipėda": "LT", "riga": "LV", "tallinn": "EE",
    "ottawa": "CA", "anchorage": "US", "fairbanks": "US", "washington": "US",
    "moscow": "RU", "murmansk": "RU", "arkhangelsk": "RU",
}

def _iso2(country, unlocode=None, city=None):
    """Stamp ISO2 from UN/LOCODE, country name, embedded CC codes, or HQ city.

    Multi-country strings ("Nordic (NO/SE/FI)", "EU cross-border") resolve to the
    secretariat/HQ city when provided, else the first unambiguous ISO2 token.
    Neutral codes only — no editorial country ranking beyond HQ locality.
    """
    code = (unlocode or "").strip()
    if code.upper() in ("NULL", "NONE", "N/A", "NA", "-", "TODO"):
        code = ""
    # Real UN/LOCODE is typically 5 chars (CC + loc). Reject placeholders like NULL/CHV.
    if len(code) >= 5 and code[:2].isalpha():
        return code[:2].upper()

    key = (country or "").strip().lower()
    city_key = (city or "").strip().lower()

    # Swapped CSV cells: city holds a country name, country holds a locality.
    if city_key in COUNTRY_TO_ISO2 and (not key or key not in COUNTRY_TO_ISO2):
        if not any(name in key for name, _ in COUNTRY_TO_ISO2.items() if len(name) > 3):
            return COUNTRY_TO_ISO2[city_key]

    if key in COUNTRY_TO_ISO2:
        return COUNTRY_TO_ISO2[key]

    # HQ city first for multi-country / pan-regional rows.
    if city_key:
        # "Helsinki (NIB HQ; ...)" / "Oslo, Norway (Nordic Innovation HQ)"
        city_head = city_key.split(",")[0].split("(")[0].strip()
        if city_head in CITY_TO_ISO2:
            return CITY_TO_ISO2[city_head]
        for name, iso in sorted(CITY_TO_ISO2.items(), key=lambda kv: -len(kv[0])):
            if name in city_key:
                return iso

    # Embedded ISO2 tokens: "Nordic (NO/SE/FI/IS/DK)", "Aurora sub-area: NO/SE/FI"
    tokens = _re_iso2.findall(r"(?<![A-Za-z])([A-Z]{2})(?![A-Za-z])", country or "")
    # Prefer known Arctic/Nordic/Baltic codes; skip common false positives (OR, IN, AT as English).
    prefer = {"NO","SE","FI","IS","DK","GL","FO","AX","SJ","CA","US","RU","LT","LV","EE","KR","JP","CN"}
    for t in tokens:
        if t in prefer:
            return t

    if "/" in key:
        first = key.split("/")[0].strip()
        # strip leading labels like "nordic (no"
        first = first.split("(")[-1].strip()
        if first in COUNTRY_TO_ISO2:
            return COUNTRY_TO_ISO2[first]

    # Parenthetical / region strings: "USA (Alaska)", "Svalbard (Norway)", etc.
    for name, iso in sorted(COUNTRY_TO_ISO2.items(), key=lambda kv: -len(kv[0])):
        if name in key:
            return iso

    # Last resort: city string itself naming a country.
    if city_key in COUNTRY_TO_ISO2:
        return COUNTRY_TO_ISO2[city_key]
    for name, iso in sorted(COUNTRY_TO_ISO2.items(), key=lambda kv: -len(kv[0])):
        if name in city_key:
            return iso
    return ""


COUNTRY_ANCHORS = {
    "russia": (73.00, 90.00), "canada": (69.12, -105.05), "usa": (70.50, -150.00),
    "united states": (70.50, -150.00), "finland": (64.50, 25.00), "sweden": (64.00, 20.00),
    "norway": (69.65, 18.96), "denmark": (64.18, -51.72), "danish": (64.18, -51.72),
    "greenland": (70.00, -45.00), "china": (69.70, 170.27), "japan": (64.50, -165.44),
    "germany": (54.00, 10.00), "greece": (68.98, 33.06), "switzerland": (68.98, 33.06),
}


def _csv_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def _f64(row, key):
    try:
        return float(row[key])
    except (TypeError, ValueError):
        return None


def _feat(geom, props, fid=None):
    # Mirror stable ids into properties so client-side filterGeoJson / UI
    # can dedupe even when Feature.id is stripped by a downstream transform.
    if fid is not None and props is not None and props.get("id") in (None, ""):
        props = {**props, "id": fid}
    return {"type": "Feature", "id": fid, "properties": props, "geometry": geom}


def _point(lon, lat, crs):
    if crs == 4326:
        return {"type": "Point", "coordinates": [lon, lat]}
    e, n = get_crs(crs).forward(lon, lat)
    return {"type": "Point", "coordinates": [round(e, 3), round(n, 3)]}


def _polyline(lonlats, crs):
    coords = []
    for lon, lat in lonlats:
        if crs == 4326:
            coords.append([lon, lat])
        else:
            e, n = get_crs(crs).forward(lon, lat)
            coords.append([round(e, 3), round(n, 3)])
    return {"type": "LineString", "coordinates": coords}


def _ring(lats, crs, segments=128, lon0=0.0):
    """Polygon ring along a parallel (circle in stereographic = polar ring)."""
    # 2026-10-05 gis-refring-1015: project like _point/_polyline. Previously the ring stayed in
    # lon/lat degrees inside the EPSG:3996 atlas, and the WGS84 export then inverse-projected those
    # degrees as metres, collapsing Arctic Circle / 75N / 80N / target band onto ~89.999N.
    coords = []
    for i in range(segments + 1):
        lon = lon0 + i * (360.0 / segments)
        if crs == 4326:
            coords.append([lon, lats])
        else:
            e, n = get_crs(crs).forward(lon, lats)
            coords.append([round(e, 3), round(n, 3)])
    return {"type": "LineString", "coordinates": coords}


def _annulus(lat_inner, lat_outer, crs, segments=128):
    """Annulus polygon between two parallels (target-band overlay)."""
    inner = [c for c in _ring(lat_inner, crs, segments)["coordinates"]]
    outer = [c for c in _ring(lat_outer, crs, segments)["coordinates"]]
    return {"type": "Polygon", "coordinates": [outer + list(reversed(inner)) + [outer[0]]]}


def build_atlas(dataset_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)

    ports = {r["port_id"]: r for r in _csv_rows(os.path.join(dataset_dir, "ports.csv"))}
    cities = _csv_rows(os.path.join(dataset_dir, "cities.csv"))
    lanes = _csv_rows(os.path.join(dataset_dir, "lanes.csv"))
    tankers = _csv_rows(os.path.join(dataset_dir, "tankers.csv"))
    icebreakers = _csv_rows(os.path.join(dataset_dir, "icebreakers.csv"))
    shipyards = _csv_rows(os.path.join(dataset_dir, "shipbuilding_facilities.csv"))
    prog_path = os.path.join(dataset_dir, "entrepreneur_programs.csv")
    programs = _csv_rows(prog_path) if os.path.exists(prog_path) else []

    # Merge dataset coords into gazetteer lookups
    for p in ports.values():
        EXTRA_ANCHORS[p["port_name"].replace(" Commercial Sea Port", "").replace(" Sea Port", "")
                      .replace(" Commercial Port", "").replace(" East Port", "")] = \
            (float(p["latitude"]), float(p["longitude"]))
    for c in cities:
        EXTRA_ANCHORS[c["city_name"]] = (float(c["latitude"]), float(c["longitude"]))
    EXTRA_ANCHORS.update(GAZETTEER)

    def anchor(name):
        for key, coord in EXTRA_ANCHORS.items():
            if coord is None:
                continue
            if name and (name.lower() == key.lower() or name.lower().startswith(key.lower())
                         or key.lower() in name.lower()):
                return coord
        return None

    features = []
    counts = {}

    # Ports — sanitize UN/LOCODE; soft-dedupe exact unlocode+coord aliases (keep lowest port_id)
    def _clean_unlocode(raw):
        u = (raw or "").strip().upper()
        if not u or u in ("NULL", "NONE", "N/A", "-", "—"):
            return ""
        # common typo: USNOM (Nome TX) vs USOME (Nome AK)
        if u == "USNOM":
            u = "USOME"
        # Iqaluit pasted as city name (CAIqaluit) instead of UNECE CAIQL
        if u in ("CAIQALUIT", "CAIQAL", "CAIQA"):
            u = "CAIQL"
        # Vardø IATA VAW mistaken for UNECE LOCODE (real LOCODE is NOVAO)
        if u == "NOVAW":
            u = "NOVAO"
        if len(u) == 3 and u.isalpha():
            # incomplete code like CHV — reject
            return ""
        if len(u) != 5 or not u[:2].isalpha() or not u[2:].isalnum():
            return ""
        return u

    port_alias_drops = []
    _seen_port_loc_coord = {}
    _port_kept = 0
    # Index city WGS84 pins so ports that still share an exact city centroid
    # can be stamped geo_quality=centroid_clone for client quarantine (no invented offsets).
    _city_exact = {}
    for _c in cities:
        _clat, _clon = _f64(_c, "latitude"), _f64(_c, "longitude")
        if _clat is None or _clon is None:
            continue
        _city_exact[(round(_clat, 7), round(_clon, 7))] = _c.get("city_id") or _c.get("city_name")
    _centroid_clone_ids = []
    for p in sorted(ports.values(), key=lambda r: r.get("port_id") or ""):
        lat, lon = _f64(p, "latitude"), _f64(p, "longitude")
        if lat is None or lon is None:
            continue
        ul = _clean_unlocode(p.get("unlocode"))
        key = (ul, round(lon, 4), round(lat, 4)) if ul else None
        # Soft-dedupe: identical UNECE LOCODE + rounded WGS84 pin — keep lowest port_id
        if key is not None:
            if key in _seen_port_loc_coord:
                port_alias_drops.append({
                    "id": p.get("port_id"),
                    "name": p.get("port_name", ""),
                    "unlocode": ul,
                    "kept": _seen_port_loc_coord[key],
                    "reason": "duplicate_unlocode_coord",
                })
                continue
            _seen_port_loc_coord[key] = p.get("port_id")
        _props = {"layer": "ports", "name": p["port_name"], "country": p["country"],
             "iso2": _iso2(p["country"], ul or None),
             "unlocode": ul, "max_depth_m": p["max_depth_m"],
             "berths": p["berth_count"], "ice_class_support": p["ice_class_support"],
             "cargo_capacity_t": p["cargo_handling_capacity_tonnes"],
             "annual_vessel_calls": p["annual_vessel_calls"], "operator": p["operator"]}
        _ckey = (round(lat, 7), round(lon, 7))
        if _ckey in _city_exact:
            _props["geo_quality"] = "centroid_clone"
            _props["centroid_clone_of"] = _city_exact[_ckey]
            _centroid_clone_ids.append(p.get("port_id"))
        features.append(_feat(
            _point(lon, lat, 3996),
            _props,
            fid=p["port_id"]))
        _port_kept += 1
    counts["ports"] = _port_kept

    # Cities
    for c in cities:
        lat, lon = _f64(c, "latitude"), _f64(c, "longitude")
        if lat is None or lon is None:
            continue
        features.append(_feat(
            _point(lon, lat, 3996),
            {"layer": "cities", "name": c["city_name"], "country": c["country"],
             "iso2": _iso2(c["country"]),
             "region": c["region"], "population": c["population"], "gdp_usd": c["gdp_usd"]},
            fid=c["city_id"]))
    counts["cities"] = len(cities)

    # Shipyards (id-dedupe only — shared HQ coords can be distinct operators)
    shipyard_coord_drops = []
    _seen_ship_ids = set()
    _ship_kept = 0
    for s in shipyards:
        lat, lon = _f64(s, "latitude"), _f64(s, "longitude")
        if lat is None or lon is None:
            continue
        sid = s.get("shipyard_id") or ""
        if sid and sid in _seen_ship_ids:
            shipyard_coord_drops.append({"id": sid, "name": s.get("shipyard_name", ""), "reason": "duplicate_id"})
            continue
        if sid:
            _seen_ship_ids.add(sid)
        _sprops = {"layer": "shipyards", "name": s["shipyard_name"], "location": s["location"],
             "country": s["country"], "iso2": _iso2(s["country"]),
             "specialization": s["specialization"],
             "arctic_capable": s["arctic_vessel_capability"]}
        # stamp industry/shipyard centroid clones for client quarantine (no invented offsets)
        _sckey = (round(lat, 7), round(lon, 7))
        if _sckey in _city_exact:
            _sprops["geo_quality"] = "centroid_clone"
            _sprops["centroid_clone_of"] = _city_exact[_sckey]
            _centroid_clone_ids.append(sid or s.get("shipyard_name"))
        features.append(_feat(
            _point(lon, lat, 3996),
            _sprops,
            fid=s["shipyard_id"]))
        _ship_kept += 1
    counts["shipyards"] = _ship_kept

    # --- Optional extension layers (additive; missing file = layer skipped) ---
    EXTRA_POINT_LAYERS = [
        ("entrepreneur_programs.csv", "programs"),
        ("arctic_airports.csv", "airports"),
        ("arctic_industrial_facilities.csv", "industry"),
        ("rail_corridors.csv", "rail"),
        ("arctic_rescue_centers.csv", "rescue"),
    ]
    extra_id_drops = []
    program_name_coord_drops = []
    _seen_prog_name_coord = set()
    for _fname, _layer in EXTRA_POINT_LAYERS:
        _path = os.path.join(dataset_dir, _fname)
        if not os.path.exists(_path):
            continue
        _n_before = len(features)
        _seen_ids = set()
        for _r in _csv_rows(_path):
            _lat, _lon = _f64(_r, "latitude"), _f64(_r, "longitude")
            if _lat is None or _lon is None:
                continue
            _fid = _r.get("program_id")
            if _fid:
                if _fid in _seen_ids:
                    extra_id_drops.append({"layer": _layer, "id": _fid, "name": _r.get("program_name", "")})
                    continue
                _seen_ids.add(_fid)
            if _layer == "programs":
                _nk = (_r.get("program_name", "") or "").strip().lower()
                _ck = (_nk, round(_lon, 4), round(_lat, 4))
                if _nk and _ck in _seen_prog_name_coord:
                    program_name_coord_drops.append({"id": _fid, "name": _r.get("program_name", ""), "coord": (_lon, _lat)})
                    continue
                if _nk:
                    _seen_prog_name_coord.add(_ck)
            _iprops = {"layer": _layer, "name": _r.get("program_name", ""),
                 "country": _r.get("country", ""), "iso2": _iso2(_r.get("country", ""), city=_r.get("city", "")), "city": _r.get("city", ""),
                 "type": _r.get("program_type", ""), "benefits": _r.get("key_benefits", ""),
                 "eligibility": _r.get("eligibility", ""), "operator": _r.get("operator", ""),
                 "status": _r.get("status", ""), "url": _r.get("official_url", ""),
                 "sources": _r.get("sources", ""), "confidence": _r.get("confidence", ""),
                 "verified": _r.get("last_verified", "")}
            if _layer == "industry":
                _ickey = (round(_lat, 7), round(_lon, 7))
                if _ickey in _city_exact:
                    _iprops["geo_quality"] = "centroid_clone"
                    _iprops["centroid_clone_of"] = _city_exact[_ickey]
                    _centroid_clone_ids.append(_fid or _r.get("program_name"))
            features.append(_feat(
                _point(_lon, _lat, 3996),
                _iprops,
                fid=_fid))
        counts[_layer] = len(features) - _n_before

    # Lanes (schematic polylines via waypoint gazetteer)
    unresolved = set()
    teleport_drops = []
    _lane_pts_for_route = []
    for lane in lanes:
        start = ports.get(lane["start_port_id"])
        end = ports.get(lane["end_port_id"])
        pts = []
        wp_pts = []
        for wp in _split_waypoints(lane.get("waypoints", "")):
            coord = anchor(wp)
            if coord:
                wp_pts.append((coord[1], coord[0]))  # lon, lat
            elif wp not in ("Ice Edge",) and not any(wp.lower() == x for x in
                      (start["port_name"][:8].lower() if start else "",)):
                unresolved.add(wp)

        # 2026-10-12 gis-lanewp-1418: move landlocked region/landmass waypoints to open water
        _wp_snaps = []
        if (os.environ.get("ATL_LANE_WAYPOINT_WATER", "1") != "0" and wp_pts
                and "river" not in (lane.get("lane_name") or "").lower() and _land_index()):
            _region = {}
            for _gk, _gv in GAZETTEER.items():
                if _gv and not _gk.strip().lower().endswith(" river") and EXTRA_ANCHORS.get(_gk) == _gv:
                    _region.setdefault((round(_gv[1], 6), round(_gv[0], 6)), _gk)
            _port_ll = set()
            for _pr in ports.values():
                _la, _lo = _f64(_pr, "latitude"), _f64(_pr, "longitude")
                if _la is not None and _lo is not None:
                    _port_ll.add((round(_lo, 4), round(_la, 4)))

            def _ll(pr):
                if not pr:
                    return None
                _la, _lo = _f64(pr, "latitude"), _f64(pr, "longitude")
                return (_la, _lo) if _la is not None and _lo is not None else None
            for _i, (_lo, _la) in enumerate(list(wp_pts)):
                _tok = _region.get((round(_lo, 6), round(_la, 6)))
                if not _tok or (round(_lo, 4), round(_la, 4)) in _port_ll:
                    continue
                if not _on_land(_la, _lo) or _water_within_km(_la, _lo, LANE_WP_KEEP_KM) is not None:
                    continue
                _prev = (wp_pts[_i - 1][1], wp_pts[_i - 1][0]) if _i > 0 else _ll(start)
                _next = (wp_pts[_i + 1][1], wp_pts[_i + 1][0]) if _i + 1 < len(wp_pts) else _ll(end)
                _res = _lane_wp_water(_la, _lo, _prev, _next)
                if _res:
                    wp_pts[_i] = (_res[1], _res[0])
                    _wp_snaps.append(f"{_tok} {_la:.4f},{_lo:.4f}->{_res[0]:.6f},{_res[1]:.6f} ({_res[2]:.0f} km)")

        # 2026-10-12 gis-wpport-1636: on-land town waypoint -> nearby dataset harbour pin
        if (os.environ.get("ATL_LANE_WP_PORT_SNAP", "1") != "0" and wp_pts
                and "river" not in (lane.get("lane_name") or "").lower() and _land_index()):
            _pp = []
            for _pr in ports.values():
                _pla, _plo = _f64(_pr, "latitude"), _f64(_pr, "longitude")
                if _pla is not None and _plo is not None:
                    _pp.append((_plo, _pla, _pr.get("port_id", ""), _pr.get("port_name", "")))
            _wp_toks = [w for w in _split_waypoints(lane.get("waypoints", "")) if anchor(w)]
            _geo_words = ("cape", "kapp", "island", "peninsula", "strait", "gate", "sea", "bay",
                          "delta", "ice edge", "passage", "sound", "fjord", "alaska", "greenland")
            for _i, (_lo, _la) in enumerate(list(wp_pts)):
                _tk = (_wp_toks[_i] if len(_wp_toks) == len(wp_pts) else "").lower()
                if not _tk or not _on_land(_la, _lo):
                    continue
                _own = [_x for _x in _pp if _x[2] in (lane.get("start_port_id"), lane.get("end_port_id"))]
                _best = None
                for _plo, _pla, _pid, _pn in _own:
                    _dk = _haversine_km(_lo, _la, _plo, _pla)
                    if _best is None or _dk < _best[0]:
                        _best = (_dk, _plo, _pla, _pid, _pn)
                if _best and 0.05 < _best[0] <= LANE_WP_PORT_SNAP_KM:
                    wp_pts[_i] = (_best[1], _best[2])
                    _wp_snaps.append(f"port {_wp_toks[_i]}->{_best[3]} {_la:.4f},{_lo:.4f}->{_best[2]:.6f},{_best[1]:.6f} ({_best[0]:.1f} km)")

        def _near_ref(lon, lat, ref):
            if ref is None:
                return True
            return _haversine_km(lon, lat, ref[0], ref[1]) <= LANE_TELEPORT_MAX_KM

        first_wp = wp_pts[0] if wp_pts else None
        last_wp = wp_pts[-1] if wp_pts else None
        # 2026-10-12 gis-endrevisit-1743: some lanes list their end (or start) port as an INTERIOR
        # waypoint and then continue (LANE-027 Ningbo..Kara Gates-Murmansk-Hamburg-Felixstowe, end
        # PORT-001 Murmansk; LANE-010 Nuuk..Ilulissat-Upernavik-Melville Bay, end PORT-011 Ilulissat).
        # Appending the endpoint again after the last waypoint drew a full retrace back along the
        # coast (LANE-027 ~6,500 km Felixstowe->Norway->Murmansk). The CSV waypoint order is the
        # sailing order, so an endpoint already visited as an interior vertex (<= 5 km) is not
        # re-appended. Display-only; lanes.csv untouched. ATL_LANE_ENDPOINT_REVISIT=0 disables.
        _endpoint_skips = []
        _revisit_on = os.environ.get("ATL_LANE_ENDPOINT_REVISIT", "1") != "0"

        def _revisited(lon, lat, interior, terminal):
            if not _revisit_on or not interior or terminal is None:
                return None
            if _haversine_km(lon, lat, terminal[0], terminal[1]) <= LANE_ENDPOINT_REVISIT_KM:
                return None
            for _k, _q in interior:
                if _haversine_km(lon, lat, _q[0], _q[1]) <= LANE_ENDPOINT_REVISIT_KM:
                    return _k
            return None
        if start:
            s_lat, s_lon = _f64(start, "latitude"), _f64(start, "longitude")
            _sk = (_revisited(s_lon, s_lat, list(enumerate(wp_pts))[1:], first_wp)
                   if s_lat is not None and s_lon is not None else None)
            if _sk is not None:
                _endpoint_skips.append(f"start {lane.get('start_port_id')} already waypoint #{_sk + 1}")
            elif s_lat is not None and s_lon is not None:
                if _near_ref(s_lon, s_lat, first_wp):
                    pts.append((s_lon, s_lat))
                else:
                    teleport_drops.append((lane.get("lane_id"), "start", lane.get("start_port_id"), s_lon, s_lat))
        pts.extend(wp_pts)
        if end:
            e_lat, e_lon = _f64(end, "latitude"), _f64(end, "longitude")
            _ek = (_revisited(e_lon, e_lat, list(enumerate(wp_pts))[:-1], last_wp)
                   if e_lat is not None and e_lon is not None else None)
            if _ek is not None:
                _endpoint_skips.append(f"end {lane.get('end_port_id')} already waypoint #{_ek + 1}")
            elif e_lat is not None and e_lon is not None:
                if _near_ref(e_lon, e_lat, last_wp):
                    pts.append((e_lon, e_lat))
                else:
                    teleport_drops.append((lane.get("lane_id"), "end", lane.get("end_port_id"), e_lon, e_lat))
        # dedupe consecutive identical vertices
        deduped = []
        for p in pts:
            if not deduped or (abs(deduped[-1][0]-p[0]) > 1e-6 or abs(deduped[-1][1]-p[1]) > 1e-6):
                deduped.append(p)
        pts = deduped
        # 2026-10-12 gis-riverlane-1346: river lanes were drawn in CSV waypoint order, zig-zagging
        # up and down the river (Yenisei: Dudinka->Gulf->Igarka->Dikson; Lena: Tiksi->delta->Yakutsk->
        # Zhigansk) and LANE-015 Lena ended at ARC-PORT-049 Franz Josef Land, ~2,000 km off the river.
        # For "River" lanes: quarantine an endpoint port farther than RIVER_LANE_ENDPOINT_MAX_KM from
        # every other vertex, then order vertices upstream -> mouth (Arctic-draining rivers flow north,
        # so ascending latitude); vertices within RIVER_MOUTH_PORT_KM of the "<X> River" mouth anchor
        # (e.g. Tiksi) sort just after the mouth. Display-only; CSV untouched. ATL_RIVER_LANE_ORDER=0 disables.
        _river_props = None
        if (os.environ.get("ATL_RIVER_LANE_ORDER", "1") != "0"
                and "river" in (lane.get("lane_name") or "").lower() and len(pts) >= 3):
            _end_ports = {}
            for _pid in (lane.get("start_port_id"), lane.get("end_port_id")):
                _pr = ports.get(_pid)
                if _pr:
                    _la, _lo = _f64(_pr, "latitude"), _f64(_pr, "longitude")
                    if _la is not None and _lo is not None:
                        _end_ports[(round(_lo, 6), round(_la, 6))] = _pid
            _mouths = []
            for _wp in _split_waypoints(lane.get("waypoints", "")):
                if _wp.strip().lower().endswith(" river"):
                    _c = anchor(_wp)
                    if _c:
                        _mouths.append((_c[1], _c[0]))
            _kept = list(pts)
            _quar = []
            for _i in range(len(_kept) - 1, -1, -1):
                _p = _kept[_i]
                _pid = _end_ports.get((round(_p[0], 6), round(_p[1], 6)))
                if not _pid:
                    continue
                _others = [q for _j, q in enumerate(_kept) if _j != _i]
                if _others and min(_haversine_km(_p[0], _p[1], q[0], q[1]) for q in _others) > RIVER_LANE_ENDPOINT_MAX_KM:
                    _quar.append(_pid)
                    del _kept[_i]

            def _river_key(_p):
                for _m in _mouths:
                    if _p != _m and _haversine_km(_p[0], _p[1], _m[0], _m[1]) <= RIVER_MOUTH_PORT_KM:
                        return (1, _m[1], _p[1])
                return (0, _p[1], 0.0)
            _ordered = sorted(_kept, key=_river_key)
            if len(_ordered) >= 2 and (_ordered != pts or _quar):
                _river_props = {"geometry_quality": "river_ordered", "route_order": "upstream_to_mouth",
                                "route_vertices_before": len(pts)}
                if _quar:
                    _river_props["endpoint_quarantined"] = ",".join(sorted(_quar))
                pts = _ordered
        if len(pts) >= 2:
            _lane_pts_for_route.append((lane["lane_id"], lane["lane_name"], list(pts)))
            features.append(_feat(
                _polyline(pts, 3996),
                {"layer": "lanes", "name": lane["lane_name"],
                 "typical_distance_nm": lane["typical_distance_nm"],
                 "ice_conditions": lane["ice_conditions_seasonal"],
                 "difficulty": lane["navigational_difficulty"],
                 "transit_days": lane["average_transit_time_days"],
                 "icebreaker_required": lane["icebreaker_support_required"],
                 "transit_fee_usd": lane["transit_fee_range_usd"],
                 "volume_teu_per_year": lane["volume_estimate_teu_per_year"],
                 "operators": lane["primary_operators"]},
                fid=lane["lane_id"]))
            if _river_props:
                features[-1]["properties"].update(_river_props)
            if _endpoint_skips:
                features[-1]["properties"]["endpoint_revisit_skipped"] = "; ".join(_endpoint_skips)
                print(f"  lane endpoint revisit skipped {lane['lane_id']}: {'; '.join(_endpoint_skips)}")
            if _wp_snaps:
                features[-1]["properties"]["waypoint_water_snap"] = "; ".join(_wp_snaps)
                print(f"  lane waypoint water snap {lane['lane_id']}: {'; '.join(_wp_snaps)}")
    counts["lanes"] = sum(1 for f in features if f["properties"]["layer"] == "lanes")
    # 2026-10-05 gis-lanewater-1214: reroute only the lane legs that cross land onto water
    # (A* on a 10 km EPSG:3996 ocean raster from Natural Earth 10m, string-pulled).
    # Waypoints stay vertices; river lanes untouched; display-only. ATL_LANE_WATER_ROUTE=0 disables.
    lane_water_stats = {}
    if os.environ.get("ATL_LANE_WATER_ROUTE", "1") != "0" and _lane_pts_for_route:
        try:
            from lane_route import route_lanes_on_water
            _routed = route_lanes_on_water(_lane_pts_for_route, get_crs(3996))
            for f in features:
                if f["properties"].get("layer") == "lanes" and f.get("id") in _routed:
                    _npts, _st = _routed[f["id"]]
                    f["geometry"] = _polyline(_npts, 3996)
                    f["properties"]["geometry_quality"] = "water_routed"
                    f["properties"]["route_mask"] = "naturalearth_10m_land"
                    f["properties"]["route_land_km_before"] = _st["land_km_before"]
                    f["properties"]["route_land_km_after"] = _st["land_km_after"]
                    lane_water_stats[f["id"]] = _st
            print(f"  lane water route: {len(lane_water_stats)} lanes, land km "
                  f"{sum(v['land_km_before'] for v in lane_water_stats.values())} -> "
                  f"{sum(v['land_km_after'] for v in lane_water_stats.values())}")
        except Exception as e:  # never break the build; straight schematic lanes kept
            print(f"  lane water route skipped: {e}")

    # Tankers / icebreakers (anchored on primary route; spiral-unstack co-located anchors)
    def _route_anchor(route_text, country=None, default=(73.0, 90.0)):
        text = (route_text or "").lower()
        # Longest key first so "gulf of finland" wins over "finland".
        ckey = (country or "").strip().lower()
        for key, anchor_pt in sorted(ROUTE_ANCHORS.items(), key=lambda kv: -len(kv[0])):
            if key in text:
                if key == "coastal" and ckey and ckey != "russia":
                    return COASTAL_BY_COUNTRY.get(ckey) or COUNTRY_ANCHORS.get(ckey) or anchor_pt
                return anchor_pt
        if ckey in COUNTRY_ANCHORS:
            return COUNTRY_ANCHORS[ckey]
        return default

    # --- 2026-10-05 gis-seatfan-0948: display-only fan for programs on shared admin seats ---
    # Mirrors @international-arctic/geo-filter 0.1.5 unstackAdminSeats (golden-angle spiral,
    # radius 0.18 deg, stable id order). Coordinates are administrative seats (not sites), so
    # pins are fanned for clickability only; the true seat stays in position_anchor.
    # Disable with ATL_PROGRAMS_SEAT_FAN=0.
    _seat_fanned = 0
    _seat_land_groups = 0
    if os.environ.get("ATL_PROGRAMS_SEAT_FAN", "1") != "0":
        _seat_groups = {}
        for _f in features:
            if (_f.get("properties") or {}).get("layer") == "programs" and _f["geometry"]["type"] == "Point":
                _seat_groups.setdefault(tuple(_f["geometry"]["coordinates"]), []).append(_f)
        for _xy, _grp in _seat_groups.items():
            if len(_grp) < 2:
                continue
            _alon, _alat = get_crs(3996).inverse(_xy[0], _xy[1])
            _grp.sort(key=lambda f: str(f.get("id") or (f.get("properties") or {}).get("id") or ""))
            _n = len(_grp)
            _land_slots = _land_seat_slots(_alat, _alon, _n)
            if _land_slots:
                _seat_land_groups += 1
            for _i, _f in enumerate(_grp):
                if _land_slots:
                    _f["geometry"] = _point(_land_slots[_i][1], _land_slots[_i][0], 3996)
                    _f["properties"]["position_fan_mask"] = "ne_10m_land"
                else:
                    _ang = _i * 2.399963229728653
                    _r = 0.18 * math.sqrt((_i + 1) / _n)
                    _dlat = _r * math.cos(_ang)
                    _dlon = (_r * math.sin(_ang)) / max(math.cos(math.radians(_alat)), 0.2)
                    _f["geometry"] = _point(_alon + _dlon, _alat + _dlat, 3996)
                _f["properties"].update({
                    "position_quality": "admin_seat_fan",
                    "position_stack_size": _n,
                    "position_stack_index": _i,
                    "position_anchor": [round(_alon, 6), round(_alat, 6)],
                    "position_note": "Administered from this city; pin fanned for display, true seat in position_anchor",
                })
                _seat_fanned += 1
        print(f"  programs admin-seat fan: {_seat_fanned} pins on {sum(1 for g in _seat_groups.values() if len(g) > 1)} shared seats")
        print(f"  programs seat fan land mask: {_seat_land_groups} seats land-fanned")

    # --- 2026-10-05 gis-cosite-1045: display-only nudge for cross-layer co-sited pins ---
    # Different entities in different layers sometimes share one exact coordinate (port +
    # terminal operator, city + rescue centre, city centroid + program). Only the top pin is
    # clickable in the viewer. Keep the highest-priority layer on the true point and nudge the
    # rest ~2 km on a golden-angle spiral; true point kept in position_anchor, position_quality
    # untouched; geo_quality=centroid_clone pins always yield the true point. Disable with ATL_COSITE_NUDGE=0.
    _cosite_nudged = 0
    _cosite_groups_n = 0
    if os.environ.get("ATL_COSITE_NUDGE", "1") != "0":
        _prio = {"ports": 0, "industry": 1, "shipyards": 2, "airports": 3, "rescue": 4,
                 "rail": 5, "cities": 6, "programs": 7}
        _cs_groups = {}
        for _f in features:
            _p = _f.get("properties") or {}
            if _p.get("layer") in _prio and _f["geometry"]["type"] == "Point":
                _alon, _alat = get_crs(3996).inverse(*_f["geometry"]["coordinates"][:2])
                _cs_groups.setdefault((round(_alon, 5), round(_alat, 5)), []).append(_f)
        for _k, _grp in _cs_groups.items():
            if len(_grp) < 2 or len({(g["properties"] or {}).get("layer") for g in _grp}) < 2:
                continue
            _cosite_groups_n += 1
            _grp.sort(key=lambda f: (1 if f["properties"].get("geo_quality") == "centroid_clone" else 0, _prio[f["properties"]["layer"]], str(f.get("id") or f["properties"].get("id") or "")))
            _alon, _alat = get_crs(3996).inverse(*_grp[0]["geometry"]["coordinates"][:2])
            _ids = [str(g.get("id") or g["properties"].get("id") or "") for g in _grp]
            _n = len(_grp)
            for _i, _f in enumerate(_grp):
                _f["properties"]["co_site_ids"] = [x for x in _ids if x != _ids[_i]]
                if _i == 0:
                    continue
                _ang = _i * 2.399963229728653
                _r = 0.02 * math.sqrt(_i / max(_n - 1, 1))
                _dlat = _r * math.cos(_ang)
                _dlon = (_r * math.sin(_ang)) / max(math.cos(math.radians(_alat)), 0.2)
                _f["geometry"] = _point(_alon + _dlon, _alat + _dlat, 3996)
                _f["properties"].setdefault("position_anchor", [round(_alon, 6), round(_alat, 6)])
                _f["properties"]["display_offset"] = "co_site_nudge"
                _cosite_nudged += 1
        print(f"  co-site nudge: {_cosite_nudged} pins in {_cosite_groups_n} cross-layer groups")

    _ship_anchor = {}  # gis-shipwater-1152: id -> route anchor (lat, lon) for water-fanned ships        print(f"  co-site nudge: {_cosite_nudged} pins in {_cosite_groups_n} cross-layer groups")

    # --- 2026-10-12 gis-npra-1123 + 2026-10-13 gis-port048-wrangel: position_quality stamps ---
    # Soft-pin audits must not treat these as broken densify targets. Coords stay as CSV
    # (FAC-354 NSR corridor centre, FAC-370 North Pole drift-ice schematic; PROG-717 densified
    # onto NPR-A OSM area centroid). Disable with ATL_SCHEMATIC_POSITION=0.
    _schematic_stamped = 0
    if os.environ.get("ATL_SCHEMATIC_POSITION", "1") != "0":
        _SCHEMATIC_POSITION = {
            "ARC-FAC-354": {
                "position_quality": "schematic_corridor_center",
                "position_note": "NSR corridor-wide satellite coverage; approx. central-NSR schematic centre (not a ground HQ)",
            },
            "ARC-FAC-370": {
                "position_quality": "schematic_north_pole",
                "position_note": "North Pole drift-ice base schematic; intentional polar-region pin (not a densify target)",
            },
            "ARC-PROG-717": {
                "position_quality": "area_centroid",
                "position_note": "NPR-A protected_area OSM relation/8870643 Nominatim centroid; WD Q6974897 P625 70/-157 corroborates; DISTINCT from ARC-PROG-626 Anchorage admin seat and ARC-PROG-734 Deadhorse",
            },            "ARC-PORT-105": {
                "position_quality": "facility_site",
                "position_note": "Planned AMHS Cascade Point Ferry Terminal (Alaska DOT&PF, Mile 42 Glacier Highway, Goldbelt land): OSM node/2835378419 north terminus of Glacier Highway 58.7001371/-134.9378631 (way/217384152 + turnaround way/1033357934; DOT&PF 35% planset HSHWY00015 site map; KTOO 2013 Echo Cove-Cascade Point extension); was soft 58.8500/-135.0200 in upper Berners Bay water (~17.3 km); terminal not yet built - facility_site not a surveyed berth",
            },
            "ARC-PORT-099": {
                "position_quality": "facility_site",
                "position_note": "Baimskaya GOK marine terminal of Pevek seaport at Cape Nagleynyn, Chaunskaya Guba (RF govt order government.ru/news/48261 extended Pevek port borders there; Glavgosexpertiza gge.ru: 275 m berth, approach channel from Chaun Bay); anchor OSM way/1514011213 Naglyoygnyn Port landuse=industrial (Sentinel-2-mapped) centroid 69.0382643/169.3878168; cape OSM node/9513605008 = Wikidata Q37885662 ~5 km NNW; pier way/1514011280 ~1.0 km E; was soft 69.7200/170.2000 in Pevek Strait (~82 km NE); under construction - facility_site not a surveyed berth",
            },
            "ARC-PORT-089": {
                "position_quality": "facility_site",
                "position_note": "Grundarfjarðarhöfn / Grundarfjörður Harbour (Snæfellsnes, Iceland; UN/LOCODE ISGRU): OSM way/51858019 man_made=pier area=yes shoelace centroid 64.9231680/-23.2469906 = Norðurgarður main pier (maxspan ~319 m; grundport.is pier 365 m / 40 m, Berth 1 135 m @ 9.5 m + Berth 2 220 m); secondary pier way/51858020 ~0.92 km N unused; industrial hinterland way/203802229; town WD Q27014314 P625 64.92427/-23.26313 settlement only (~0.78 km WNW); soft 64.9183/-23.2503 matched harbour position DMS (~0.56 km); facility_site pier polygon, not a surveyed berth",
            },
            "ARC-PORT-039": {
                "position_quality": "facility_site",
                "position_note": "Rankin Inlet Port / Itivia barge dock (Kangiqiniq, Kivalliq, Nunavut; UN/LOCODE CARAN): OSM way/1537457615 man_made=pier area=yes concrete Itivia barge dock / sealift landing, shoelace centroid 62.7990461/-92.0920014 (mapped 2026); OSM way/1537459872 landuse=harbour industrial=port Itivia harbour yard ~0.30 km NW; Agnico Eagle Itivia Project laydown + fuel farm (OSM tanks way/762095264, way/762095265 ~0.38 km W) serving Meliadine; rankininlet.ca barge dock and FOL at Itivia; Wikimapia 5549311 Itivia ~0.11 km; no Wikidata harbour item (hamlet Q1021766 not reused); soft 62.8094/-92.0853 was ~1.20 km NNE on the hamlet core; distinct from Johnston Cove small craft harbour (OSM way/514257325 ~1.80 km NE); facility_site pier outline, not a surveyed berth",
            },
            "ARC-PORT-093": {
                "position_quality": "facility_site",
                "position_note": "Alta Urnesbukta Floating Quay / Molokaia (Alta Havn KF, Amtmannsnes, Altafjorden; UN/LOCODE NOALF): OSM way/795270408 man_made=pier floating=yes area=yes outer floating quay of Urnesbukta marina og fiskerihavn, shoelace centroid 69.9859524/23.3061572 (~142 m x 4 m outline mapped 2020); Alta Havn KF altahavn.no/kaier Kai 7 Molokaia 100 m x 6 m depth 5-15 m at 69.985979/23.306159 (~3 m); marinasolutions.no April 2026 new 100 m flytemolo; OSM node/1345229303 Urnesbukta Marina ~0.13 km W; Kystverket pile Innerberget ref 929503; no Wikidata harbour item (Alta municipality Q6535 not reused); soft 69.9686/23.2717 was ~2.33 km SW inland; distinct from Alta Havn Bukta main port (~1.25 km SE, no ATL port record); facility_site floating quay outline, not a surveyed berth",
            },
            "ARC-PORT-053": {
                "position_quality": "facility_site",
                "position_note": "Qaqortoq Port (Royal Arctic Line; South Greenland; UN/LOCODE GLJJU): OSM way/511853551 landuse=industrial harbourfront port yard shoelace centroid 60.7178523/-46.0365644 (11.4k m2 on coastline way/1476531377; shares nodes with piers way/598638435 + way/598638436 and Arctic Umiaq Line ferry route way/512918611); OSM building way/351129063 Royal Arctic Line (Torvevej B-163) inside yard ~33 m; Konge Bro pier way/378873667 + ferry_terminal node/3822342850 ~0.10 km E; town WD Q221203 P625 60.7167/-46.0333 settlement only; soft 60.7288/-46.0278 was ~1.31 km NNE in upper town; DISTINCT from ARC-PORT-091 dual-use expansion (60.7225/-46.0335, ~0.54 km N, untouched) and ARC-PORT-127 Nuupiluk (~11.2 km WNW); facility_site port yard polygon, not a surveyed berth",
            },
            "ARC-PORT-025": {
                "position_quality": "facility_site",
                "position_note": "Port of Anchorage / Port of Alaska (Knik Arm, Cook Inlet; UN/LOCODE USANC): OSM way/28577877 man_made=pier area=yes centroid 61.2408396/-149.8872591 = main cargo dock inside Port of Alaska OSM relation/10511522 (landuse=industrial, operator Municipality of Anchorage, wikidata Q3398440); Wikidata Q3398440 P625 61.2403/-149.886 ~0.09 km; Terminal Road way/28577529 and Alaska Railroad City Dock Track way/319205158 behind the dock; relation centroid 61.2446867/-149.8816953 kept for ARC-PORT-113 Terminal 1 replacement (~0.52 km NE); was soft 61.2387/-149.9076 (~1.11 km); facility_site cargo pier, not a surveyed berth",
            },
            "ARC-PORT-150": {
                "position_quality": "facility_site",
                "position_note": "Pyramiden Port quay (Billefjorden, Spitsbergen): OSM node/857534564 man_made=crane 78.654916/16.3553162 at the seaward end of concrete embankment quay road way/72761799; Kystverket leading beacons Pyramiden Ovre ref 991900 (OSM node/5323958065 ~0.16 km N) and Pyramiden Nedre ref 991800 (OSM node/5323958066 ~0.31 km E); settlement WD Q845396 P625 78.656111/16.325 ~0.67 km W; was soft 78.6567/16.3250 settlement centre (~0.69 km); local OSM coastline coarse (gadm); facility_site quay crane, not a surveyed berth",
            },
            "ARC-PORT-171": {
                "position_quality": "facility_site",
                "position_note": "Port Elga — Manorsky Cape Coal Marine Terminal (Sea of Okhotsk / Uda Bay, within Vanino seaport RUVNN): OSM way/1316635669 landuse=construction construction=industrial name=Порт Эльга (wikipedia=ru:Эльга (порт)) shoelace centroid 55.1173682/135.6970483; мыс Манорский OSM node/2643962546 55.1142092/135.6950826 ~0.37 km SW; Cape Manorsky WD Q37884830 P625 55.117222/135.6925 ~0.29 km W; WD Q115763861 Elga port soft P625 55.11667/135.7; was soft 55.1167/135.7000 (~0.20 km); facility_site construction area, not a surveyed berth",
            },
            "ARC-PORT-047": {
                "position_quality": "facility_site",
                "position_note": "Nordvik Port (historic) / former USSR port-settlement on Khatanga Gulf (Laptev Sea): Wikidata Q2364258 Nordvik P625 73.9975/111.463333 (founded ~1930, abolished 1956); OSM place=locality node/3290343023 Нордвик 73.9980/111.4693 ~0.19 km E; UN/LOCODE RUNVK; no OSM pier/harbour mapped; was soft 73.9980/111.4693 (and stale 74.5000/111.5000) - facility_site historic, not a surveyed berth",
            },
            "ARC-PORT-051": {
                "position_quality": "facility_site",
                "position_note": "Planned Nome Snake River Moorage Facility / Snake River Floats (City of Nome; MARAD FONSI Aug 2026; RAISE $13.2M): west shore of Snake River south of Satellite Drive and north of the RO/RO facility; anchor OSM way/1268826085 leisure=slipway 64.5014256/-165.4286323 (west-bank slipway in project corridor; Satellite Drive way/8983909 ~0.29 km N; Snake River WD Q7547059 P625 64.5044/-165.4242 ~0.39 km NE); ARC-PORT-026 Nome Harbor piers ~0.74 km SW; floats not yet built (35% design, dredge bid early 2027) - facility_site not a surveyed berth; was soft 64.4980/-165.4200 (~0.56 km)",
            },
            "ARC-PORT-022": {
                "position_quality": "facility_site",
                "position_note": "Tuktoyaktuk port land on the Tuktoyaktuk Harbour shore S of Cache Point: OSM way/513281075 landuse=industrial industrial=port (tank farm ~21 storage_tank ways) shoelace centroid 69.4281426/-132.9885229; Tuktoyaktuk Harbour WD Q116456484 (CGNDB LAYQW) ~1.0 km NE; DFO/CHS tide station 6485 ~1.2 km NNW; hamlet node/107350410 = WD Q719547 ~2.4 km NW; GNWT INF MTS Tuktoyaktuk freight terminal; UN/LOCODE CATUK; was soft 69.4457/-133.0360 in the hamlet (~2.69 km); facility_site not a surveyed berth",
            },
            "ARC-PORT-042": {
                "position_quality": "facility_site",
                "position_note": "Egvekinot seaport (RUEGV) main harbour pier on Kresta Bay: OSM way/721745076 man_made=pier shoelace centroid 66.3192251/-179.1095237; secondary pier way/721745075 ~0.6 km SSW; settlement node/2891542781 = WD Q1240765 ~0.62 km NW; Rosmorrechflot AD-378-r 24.12.2010 registry 66deg19N 179deg07W / ul. Portovaya 1; was soft 66.3167/-179.1167 (~0.43 km); facility_site",
            },
            "ARC-PORT-075": {
                "position_quality": "facility_site",
                "position_note": "Nuuk Harbour Expansion Qeqertat quay (Sikuki / KJ Greenland; 200 m trawler + 150 m dual-use naval; groundbreaking 2026-07-07; completion Nov 2028): on west side of Qeqertaq Avalleq (Fyroe) immediately south of the 2017 container terminal; anchor OSM way/627906959 landuse=industrial industrial=port shoelace centroid 64.1678488/-51.7140694 (west face ~310 m N-S); Naalakkersuisut VVM A246375-VVM-001 2024 + Sikuki 2026-07-08 + KNR; was soft 64.1700/-51.7100 (~0.31 km); ARC-PORT-009 on harbour node/995384594 ~0.69 km NW; no pier way yet - facility_site under construction",
            },
            "ARC-PORT-036": {
                "position_quality": "facility_site",
                "position_note": "Tiksi East Port read as the East piers of Tiksi seaport (west shore of Tiksi Bay): anchor OSM way/1081390287 man_made=pier Vostochny pirs I (East Pier No.1) vertex centroid 71.6448592/128.8963706 with seamark berths 11 + 12; Mintrans order No.50 of 14.02.2017 Annex 3: berths 11-12 on East Pier No.1 operating (157.5 m, 5.8 m), East Pier No.2 decommissioned; was soft 71.6800/128.9500 in Tiksi Bay anchorage water (~4.3 km NNE); no public source for a separate East Port entity - facility_site, identity inferred",
            },
            "ARC-PORT-136": {
                "position_quality": "facility_site",
                "position_note": "Planned Narvik Terminal Nord (Narvik Havn KF + Bane NOR; area plan Narvikterminalen med Terminal Nord PlanID 2021001 adopted 18.04.2024): between the RO-RO quay at Lillekleiva and Kleivhammaren with sea fill along Fagernesveien; anchor OSM node/6372382875 Kleivhammarn bus stop 68.4241270/17.4309920 (Lillekleiva stop node/6372384369 ~0.33 km S; Fagmobler node/7590047622 = access-north-of-furniture-store reference); was soft 68.4400/17.4200 in Narvik city/harbour (~1.8 km N); not built - facility_site not a surveyed berth",
            },
            "ARC-PORT-046": {
                "position_quality": "facility_site",
                "position_note": "Cape Zhelaniya (Mys Zhelaniya) / Rosmorport RUZHE area: OSM node/429774624 Nominatim 76.9542826/68.5639747 (WD Q2464613 cape; WD Q86004798 former polar station nearby); was soft 76.9500/68.5500 (~0.59 km); no OSM harbour/pier mapped - facility_site not a surveyed berth",
            },
            "ARC-PORT-045": {
                "position_quality": "settlement_site",
                "position_note": "Ambarchik rural locality / historic Kolyma-mouth port: OSM way/655223046 place=hamlet Nominatim 69.6252019/162.3024493 (WD Q2629730; enwiki Ambarchik 69.62611/162.30389); was soft 69.6500/162.3500 (~3.3 km); shipping later transferred to Chersky — settlement_site not a modern commercial terminal",
            },
            "ARC-PORT-041": {
                "position_quality": "settlement_site",
                "position_note": "Mys Shmidta urban-type settlement / Chukchi Sea coast port: OSM way/93613726 Nominatim 68.8928813/-179.4130958 (WD Q1020259); was soft 68.8700/-179.4000 on a road near the airport (~2.6 km); no OSM harbour/pier mapped - settlement_site not a surveyed berth",
            },
            "ARC-PORT-048": {
                "position_quality": "settlement_site",
                "position_note": "Ushakovskoye abandoned rural locality OSM node/1554927593; WP approx 70.98083N 178.49083W corroborates; historical Wrangel SE-coast settlement/port (not a modern commercial terminal)",
            },
            "ARC-PORT-074": {
                "position_quality": "facility_site",
                "position_note": "Planned Cape Blossom Regional Port site: Cape Blossom GNIS 1412717 / Wikidata Q5034592 / OSM node/5908987347 66.7341667/-162.495 (~11.7 mi S of Kotzebue, DOT&PF Cape Blossom Road terminus); was soft 66.85/-162.21 in Hotham Inlet (~17.9 km); planning stage, exact berth TBD (site re-study NCA1/ECA1)",
            },
            "ARC-PORT-078": {
                "position_quality": "facility_site",
                "position_note": "Planned Finnafjord Port (FFPD) harbour basin: Wikidata Q106075430 P625 66.1062/-15.1502 (= enwiki Finnafjord Port) inside Finnafjordur (OSM relation/8413765) between Gunnolfsvik industrial site (OSM node/1822239443, N shore) and Saurbaer (S shore); was soft 66.27/-15.25 in open sea (~18.8 km); planning stage, quay line TBD",
            },
            "ARC-PORT-110": {
                "position_quality": "facility_site",
                "position_note": "Planned Galtarhofn (GH Harbour) site in the land of Galtarlaekur, Hvalfjordur west of Grundartangi: Galtarlaekur farmstead OSM way/560639791 64.3470050/-21.8087513 (Hvalfjardarsveit notice: ~102 ha planning area below Route 1 in landi Galtarlaekjar; ghharbour.com); was soft 64.32/-21.85 (~3.6 km SW); planning/EIA stage, quay line TBD",
            },
            "ARC-PORT-157": {
                "position_quality": "settlement_site",
                "position_note": "Mishukovo hamlet OSM way/129872684 Nominatim 69.0451678/33.0406397; Arctic Gate Marine Terminal planned Kola Bay west shore near Mishukovo (pre-investment; no dedicated pier OSM yet)",
            },
        }
        for _f in features:
            _p = _f.get("properties") or {}
            _sid = str(_f.get("id") or _p.get("id") or "")
            if _sid in _SCHEMATIC_POSITION:
                _p.update(_SCHEMATIC_POSITION[_sid])
                if _f["geometry"]["type"] == "Point":
                    _alon, _alat = get_crs(3996).inverse(*_f["geometry"]["coordinates"][:2])
                    _p.setdefault("position_anchor", [round(_alon, 6), round(_alat, 6)])
                _schematic_stamped += 1
        print(f"  schematic position tags: {_schematic_stamped} pins")

    _ship_anchor = {}  # gis-shipwater-1152: id -> route anchor (lat, lon) for water-fanned ships
    tanker_groups = {}
    for t in tankers:
        coord = _route_anchor(t.get("typical_arctic_route"), t.get("country"))
        tanker_groups.setdefault(coord, []).append(t)
    for coord, group in tanker_groups.items():
        _wf = _water_fan(coord[0], coord[1], len(group), **({} if len(group) > 1 else {"max_r_deg": SINGLE_SHIP_WATER_MAX_R})) if ((len(group) > 1 or _single_on_land(coord)) and os.environ.get("ATL_SHIP_WATER_FAN", "1") != "0") else None
        for i, t in enumerate(group):
            lat, lon = _wf[i] if _wf else (_schematic_offset(coord[0], coord[1], i, len(group)) if len(group) > 1 else coord)
            if _wf:
                _ship_anchor[t["tanker_id"]] = coord
            features.append(_feat(
                _point(lon, lat, 3996),
                {"layer": "tankers", "name": t["vessel_name"], "country": t.get("country") or "",
                 "iso2": _iso2(t.get("country")),
                 "operator": t["owner_operator"],
                 "ice_class": t["ice_class"], "dwt": t["deadweight_tonnage"],
                 "cargo": t["cargo_type"], "route": t["typical_arctic_route"],
                 "year_built": t.get("year_built") or "",
                 "charter_usd_day": t["charter_rate_usd_per_day"],
                 "position_quality": "schematic_route_anchor" if len(group) > 1 else "route_anchor",
                 "position_stack_size": len(group), "position_stack_index": i},
                fid=t["tanker_id"]))
    counts["tankers"] = len(tankers)

    # gis-ice043-1535: drop icebreaker rows whose vessel_name declares "same as ARC-ICE-XXX"
    # (CSV provenance kept; ARC-ICE-043 Oden alias of ARC-ICE-033). Toggle ATL_ICE_SAME_AS_DROP=0.
    icebreaker_id_drops = []
    _ICE_SAME_RE = _re_iso2.compile(r"same as\s+(ARC-ICE-\d+)", _re_iso2.I)
    _ib_emit = []
    for ib in icebreakers:
        _m = _ICE_SAME_RE.search(ib.get("vessel_name") or "")
        if _m and os.environ.get("ATL_ICE_SAME_AS_DROP", "1") != "0":
            icebreaker_id_drops.append({
                "id": ib.get("icebreaker_id"), "name": ib.get("vessel_name", ""),
                "kept": _m.group(1), "reason": "duplicate_same_as_name",
            })
            continue
        _ib_emit.append(ib)
    if icebreaker_id_drops:
        print(f"  icebreaker same-as drops: {icebreaker_id_drops}")

    ib_groups = {}
    for ib in _ib_emit:
        coord = _route_anchor(ib.get("primary_service_route"), ib.get("country"))
        ib_groups.setdefault(coord, []).append(ib)
    for coord, group in ib_groups.items():
        _wf = _water_fan(coord[0], coord[1], len(group), **({} if len(group) > 1 else {"max_r_deg": SINGLE_SHIP_WATER_MAX_R})) if ((len(group) > 1 or _single_on_land(coord)) and os.environ.get("ATL_SHIP_WATER_FAN", "1") != "0") else None
        for i, ib in enumerate(group):
            lat, lon = _wf[i] if _wf else (_schematic_offset(coord[0], coord[1], i, len(group)) if len(group) > 1 else coord)
            if _wf:
                _ship_anchor[ib["icebreaker_id"]] = coord
            features.append(_feat(
                _point(lon, lat, 3996),
                {"layer": "icebreakers", "name": ib["vessel_name"], "country": ib.get("country") or "",
                 "iso2": _iso2(ib.get("country")),
                 "operator": ib["owner_operator"],
                 "ice_class": ib["ice_class"], "power_kw": ib["power_kw"],
                 "route": ib["primary_service_route"],
                 "year_built": ib.get("year_built") or "",
                 "charter_usd_day": ib["charter_rate_usd_per_day"],
                 "position_quality": "schematic_route_anchor" if len(group) > 1 else "route_anchor",
                 "position_stack_size": len(group), "position_stack_index": i},
                fid=ib["icebreaker_id"]))
    counts["icebreakers"] = len(_ib_emit)
    for _f in features:
        _p = _f.get("properties") or {}
        _sid = _f.get("id") or _p.get("id")
        if _p.get("layer") in ("tankers", "icebreakers") and _sid in _ship_anchor:
            _a = _ship_anchor[_sid]
            _p["position_anchor"] = [round(_a[1], 6), round(_a[0], 6)]
            _p["display_offset"] = "water_fan"
    print(f"  ship water fan: {len(_ship_anchor)} schematic ships moved to open water (anchor kept)")

    # Reference overlays: Arctic Circle ring + 75-80N target band annulus.
    # The annulus is layer="band", not "reference": the client styles layer==="band"
    # with a translucent gold fill and hides it until the "band" chip is toggled on,
    # while layer="reference" polygons fall through to an opaque slate fill.
    features.append(_feat(
        _ring(66.5, 3996),
        {"layer": "reference", "name": "Arctic Circle (66.5N)"},
        fid="REF-ARCTIC-CIRCLE"))
    features.append(_feat(
        _ring(75.0, 3996),
        {"layer": "reference", "name": "IBCAO true-scale parallel (75N)"},
        fid="REF-75N"))
    features.append(_feat(
        _ring(80.0, 3996),
        {"layer": "reference", "name": "Target band upper edge (80N)"},
        fid="REF-80N"))
    features.append(_feat(
        _annulus(75.0, 80.0, 3996),
        {"layer": "band", "name": "ATL target band 75-80N"},
        fid="REF-TARGET-BAND"))

    # --- Emit EPSG:3996 atlas ------------------------------------------------
    fc3996 = {
        "type": "FeatureCollection",
        "name": "ArcticTradeLanes GIS OSINT Atlas",
        "crs": {"type": "name", "properties": {"name": "EPSG:3996"}},
        "generated": __import__("datetime").datetime.now(datetime.timezone.utc).isoformat(),
        "projection": {
            "epsg": 3996, "name": "WGS 84 / IBCAO Polar Stereographic",
            "standard_parallel": 75.0, "central_meridian": 0.0,
            "scale_factor_at_pole": get_crs(3996).k0,
            "note": "Target band 75-80N; k range see manifest",
        },
        "features": features,
    }
    out3996 = os.path.join(out_dir, "atlas.3996.geojson")
    with open(out3996, "w", encoding="utf-8") as fh:
        json.dump(fc3996, fh)

    # --- Emit RFC 7946 (WGS84) copy ------------------------------------------
    wgs = json.loads(json.dumps(fc3996))
    wgs.pop("crs", None)
    for f in wgs["features"]:
        g = f["geometry"]
        if g["type"] == "Point":
            e, n = g["coordinates"]
            lon, lat = get_crs(3996).inverse(e, n)
            g["coordinates"] = [round(lon, 6), round(lat, 6)]
        elif g["type"] == "LineString":
            g["coordinates"] = [
                [round(x, 6) for x in get_crs(3996).inverse(e, n)]
                for e, n in g["coordinates"]]
        elif g["type"] == "Polygon":
            g["coordinates"] = [[
                [round(x, 6) for x in get_crs(3996).inverse(e, n)]
                for e, n in ring] for ring in g["coordinates"]]
    # RFC 7946 / EPSG:4326 — lon/lat degrees (must not keep the 3996 projection stamp)
    wgs["crs"] = {"type": "name", "properties": {"name": "EPSG:4326"}}
    wgs["projection"] = {
        "epsg": 4326,
        "name": "WGS 84",
        "note": "RFC 7946 lon/lat degrees; companion to EPSG:3996 polar stereographic atlas",
    }
    out4326 = os.path.join(out_dir, "atlas.wgs84.geojson")
    with open(out4326, "w", encoding="utf-8") as fh:
        json.dump(wgs, fh)
    # Explicit EPSG:4326 filename alias (byte-identical to wgs84)
    out_epsg4326 = os.path.join(out_dir, "atlas.4326.geojson")
    with open(out_epsg4326, "w", encoding="utf-8") as fh:
        json.dump(wgs, fh)
    # RFC7946 bare alias — SPA + CF proxy historically fetch /atlas.geojson
    out_alias = os.path.join(out_dir, "atlas.geojson")
    with open(out_alias, "w", encoding="utf-8") as fh:
        json.dump(wgs, fh)

    # Reconcile layer counts against actually-emitted features so the manifest
    # matches the geojson byte-for-byte on per-layer counts. A raw len(rows) count
    # over-reports when rows carry invalid/unparsable coords and are skipped by the
    # builder (e.g. shipbuilding_facilities cells mis-aligning latitude/longitude).
    counts = {l: sum(1 for f in features if f["properties"].get("layer") == l)
              for l in ("ports", "cities", "shipyards", "programs", "airports",
                        "industry", "rail", "lanes", "tankers", "icebreakers", "rescue")}

    # --- Manifest --------------------------------------------------------------
    proj = get_crs(3996)
    band_ks = [proj.scale_factor(lat) for lat in (75.0, 76.0, 77.0, 78.0, 79.0, 80.0)]
    ref_path = os.path.join(dataset_dir, "arctic_reference.csv")
    ref_by_country = {}
    if os.path.exists(ref_path):
        for r in _csv_rows(ref_path):
            ref_by_country[r.get("iso2") or r.get("country", "?")] = r
    manifest = {
        "atlas": "ArcticTradeLanes GIS OSINT Atlas",
        "generated": fc3996["generated"],
        "crs_primary": 3996,
        "crs_supported": [3996, 3995, 3411, 4326],
        "layer_counts": counts,
        "arctic_reference": ref_by_country,
        "unresolved_lane_waypoints": sorted(unresolved) if unresolved else [],
        "lane_water_route": lane_water_stats,
        "lane_teleport_drops": [
            {"lane_id": t[0], "end": t[1], "port_id": t[2], "lon": t[3], "lat": t[4]} for t in teleport_drops
        ],
        "extra_id_drops": extra_id_drops,
        "shipyard_coord_drops": shipyard_coord_drops,
        "port_alias_drops": port_alias_drops,
        "program_name_coord_drops": program_name_coord_drops,
        "icebreaker_id_drops": icebreaker_id_drops,
        "distortion_kpis": {
            "k_at_pole": round(proj.k0, 6),
            "k_true_scale_parallel": "75N (k=1.0)",
            "k_at_80N": round(proj.scale_factor(80.0), 4),
            "k_band_75_80N_range": [round(k, 4) for k in band_ks],
            "band_area_distortion_max_pct": round(max(abs(k * k - 1) for k in band_ks) * 100, 2),
        },
        "files": {
            "epsg3996": out3996,
            "wgs84": out4326,
            "epsg4326": out_epsg4326,
        },
    }
    with open(os.path.join(out_dir, "atlas.manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, indent=2)

    print(f"Atlas: {len(features)} features -> {out3996}")
    if _centroid_clone_ids:
        print(f"  centroid_clone stamped ({len(_centroid_clone_ids)}): {','.join(str(x) for x in _centroid_clone_ids)}")
    print(f"  layers: {counts}")
    if unresolved:
        print(f"  WARNING unresolved waypoints: {sorted(unresolved)}")
    if teleport_drops:
        print(f"  WARNING lane teleport drops: {teleport_drops}")
    if extra_id_drops:
        print(f"  WARNING duplicate program_id drops: {extra_id_drops}")
    if shipyard_coord_drops:
        print(f"  WARNING shipyard coord/id drops: {shipyard_coord_drops}")
    if program_name_coord_drops:
        print(f"  WARNING program name+coord drops: {program_name_coord_drops}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Build ArcticTradeLanes GeoJSON atlas")
    ap.add_argument("--dataset", default="../ArcticTradeLanes-Dataset")
    ap.add_argument("--out", default="out")
    args = ap.parse_args()
    sys.exit(build_atlas(args.dataset, args.out))
