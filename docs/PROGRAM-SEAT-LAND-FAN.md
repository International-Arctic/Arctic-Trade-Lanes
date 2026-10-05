# Land-aware program seat fan — gis-seatland-1754 (2026-10-05)

## Problem
`docs/PROGRAM-SEAT-FAN.md` fans the 563 program pins that share 65 administrative seats
(Luleå, Anchorage, Nuuk, Helsinki, Reykjavík, Longyearbyen, Iqaluit, Nome, Utqiaġvik …) on a
0.18° golden-angle spiral so each pin is clickable. Around coastal seats that spiral put
**169 pins in open water**, up to **27.3 km offshore** (Natural Earth 10m land mask). A funding
programme pin floating in the Gulf of Finland or Isfjorden reads as bad data.

## Fix (display-only, Zo `atlas-proj/build_atlas.py`)
`_land_seat_slots(lat, lon, n)` walks the **same** spiral at the same density
(`r = 0.18·√((k+1)/n)`, angle `k·2.39996`) and keeps only candidates inside a Natural Earth 10m
land polygon (`ref/ne_10m_land.geojson`, public domain — same mask as the ship water fan).
Search stops at 0.45°; if a seat cannot get `n` land slots, or the mask is missing, the legacy
fan is kept for that seat. Land-fanned pins carry `position_fan_mask: "ne_10m_land"`;
`position_anchor` still holds the true seat. Toggle off with `ATL_PROGRAMS_SEAT_LAND=0`.

## Result (live atlas generation 2026-10-05T14:57:50Z)
| metric | before | after |
|---|---|---|
| fanned program pins in water | 169 | **0** |
| max distance offshore | 27.3 km | 0 |
| seats land-fanned | – | 65 / 65 |
| median / max distance from seat | ≤20 km | 17.5 / 46.9 km |
| features changed | – | 372 program geometries only (ids, other layers, properties unchanged) |
| exact stacked points | 0 | 0 |

Regression: `python3 scripts/check_program_seat_land.py [atlas.4326.geojson|URL] [ne_10m_land.geojson]`.

## Client-side equivalent (help wanted)
Viewers that consume raw seats (no Zo build) can do the same with a land mask tiled as a
cheap static vector tile: walk the spiral, test point-in-polygon, keep land hits. A port of
this into `@international-arctic/geo-filter` (`unstackAdminSeats({ landMask })`) is open for
contributors — see Issue #51.

## Still open
- 34 non-fanned program pins and ~40 coastal city/industry pins sit 0–3 km "offshore" only
  because NE 10m coastlines are coarse (Maniitsoq, Tromsø, Tiksi); a finer OSM coastline
  check would separate real errors from mask noise.
- Intentional sea features (ARC-FAC-370 North Pole drift base, ARC-FAC-399 Polargrund offshore
  wind, ARC-FAC-369 Nordic Hydrogen Route) are correct in water and must stay allow-listed.
