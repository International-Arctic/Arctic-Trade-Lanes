# GIS Quality Loop — 2026-10-05 ~09:48 MSK (gis-seatfan-0948)

## Win: co-located program pins are now clickable on the live atlas
- Follow-up to gis-seatfan-0922 (geo-filter 0.1.5 `unstackAdminSeats`, Issue #51).
- Instead of waiting for an SPA change, the atlas **builder** now applies the same display-only fan to the
  `programs` layer (golden-angle spiral, radius 0.18°, stable id order). Spec: `docs/PROGRAM-SEAT-FAN.md`.
- Result on the live atlas (generated `2026-10-05T06:53:46Z`, apex + www, root and `/atlas/` aliases):
  **563 pins on 65 shared seats → 0 stacked**; max display offset ~20.1 km from the seat.
- Every fanned pin carries `position_quality: "admin_seat_fan"`, `position_stack_size`, `position_stack_index`,
  `position_anchor: [lon, lat]` (the true administrative seat) and a `position_note`.
- Regression check vs previous live build: same 1321 ids; **only 563 program geometries changed**; zero property
  changes outside `position_*`; no null-island / out-of-bounds points; EPSG:4326 stamp intact; layer counts unchanged
  (ports 156, cities 103, shipyards 70, programs 713, industry 110, tankers 51, icebreakers 56).
- `scripts/check-program-seat-stack.mjs atlas.4326.geojson` → raw stacks 0, anchors OK.

## Not touched
- No dataset coordinate edits, no SPA rebuild/redeploy, no App.tsx, no DNS, x402/pricing or ads changes.
- City pins stay exactly on the seat; programs ring around them.

## Still open (Issue #51)
- Low-zoom count badge / OL `Cluster` so the fan only appears when zoomed in; popup wording “administered from <city>”.

## UM ($UM-Radar)
- unicornsmap.com and /radar return 200; no change this cycle.
