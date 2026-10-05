# GIS Quality Loop — 2026-10-05 ~09:22 MSK (gis-seatfan-0922)

## Finding
- Live atlas (`/atlas/atlas.geojson`, generated 2026-09-29T15:42:55Z, 1321 features) is healthy:
  no null-island / OOB / duplicate ids. EPSG:3996 companion intact.
- But **654 point features share 97 coordinates**; the programs layer is the bulk:
  **563 of 713 program pins on 65 shared admin seats** (Luleå 49, Anchorage 42, Nuuk 41,
  Reykjavík 37, Yellowknife 35, Helsinki 34, Moscow 32, Iqaluit 25, Longyearbyen 23, Tromsø 21).
  Only the top dot of each stack is clickable, so most programs are unreachable from the map.
- Soft-pin densify queue is effectively exhausted (remaining targets blocked/deferred; see 2026-09-29 notes).

## Win (OSS, additive)
- `@international-arctic/geo-filter` **0.1.5**: opt-in `unstackAdminSeats` fans co-located
  `programs` pins into a stable golden-angle spiral (display-only, anchor preserved,
  `position_quality: 'admin_seat_fan'`). Default output unchanged (regression: 1318 accepted /
  `centroid_clone: 3` with and without the new code path off).
- New CI smoke `scripts/check-program-seat-stack.mjs`: 65 stacked seats → 0 after fan; anchors OK.
- **Not live yet**: the atlas SPA bundles geo-filter, and this loop does not redeploy the SPA.
  Wiring it in (or an OpenLayers Cluster + spiderfy on the programs layer) is the community ask.

## UM ($UM-Radar)
- unicornsmap.com and /radar return 200. Same 0.1.5 option applies to people/event pins on city centroid fallback; no SPA change.

## Not touched
- No dataset coordinate edits (seat pins are correct administrative locations). No DNS, x402, ads, or SPA changes.
