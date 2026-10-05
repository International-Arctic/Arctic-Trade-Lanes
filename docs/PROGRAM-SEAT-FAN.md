# Program admin-seat fan (builder-side, display-only)

Entrepreneur programs are geocoded to the city that administers them, so many share one coordinate
(Luleå 49, Anchorage 42, Nuuk 41, …). Only the top dot of a stack is clickable. Since 2026-10-05 the
atlas builder fans each stack so every program is reachable. The data is not "moved": the true seat is
kept in `position_anchor`.

Algorithm (identical to `@international-arctic/geo-filter` 0.1.5 `unstackAdminSeats`):

```python
# group programs Point features by exact coordinate; for stacks of n >= 2, sorted by id:
ang = i * 2.399963229728653            # golden angle
r   = 0.18 * sqrt((i + 1) / n)         # degrees, max ~20 km
dlat = r * cos(ang)
dlon = r * sin(ang) / max(cos(radians(seat_lat)), 0.2)
props.update(position_quality="admin_seat_fan", position_stack_size=n,
             position_stack_index=i, position_anchor=[seat_lon, seat_lat],
             position_note="Administered from this city; pin fanned for display, true seat in position_anchor")
```

- Toggle: `ATL_PROGRAMS_SEAT_FAN=0` disables it in the builder.
- Consumers that need the administrative seat (analytics, joins) should read `position_anchor`
  when `position_quality == "admin_seat_fan"`.
- Ships/icebreakers keep their own `schematic_route_anchor` fan; ports, cities, shipyards and industry are never fanned.
- CI: `node scripts/check-program-seat-stack.mjs atlas.4326.geojson` must report 0 stacked seats and anchors OK.
