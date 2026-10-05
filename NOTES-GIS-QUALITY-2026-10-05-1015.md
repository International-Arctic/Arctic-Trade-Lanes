# GIS Quality Loop — 2026-10-05 ~10:15 MSK (gis-refring-1015)

- Live atlas before: generated 2026-10-05T06:53:46Z, 1321 features, programs seat fan live.
- Found: reference overlays (Arctic Circle / 75N / 80N / 75–80N band) collapsed to ~89.999N in the WGS84
  atlas and stored as degrees inside the EPSG:3996 atlas. Fixed in the builder (`_ring` now projects).
- Found: USCGC Mackinaw (Great Lakes) and Swedish Ale pinned in the Murmansk "coastal" spiral. Fixed with a
  `great lakes` anchor and flag-aware `coastal` fallback.
- Rebuilt and synced static atlas aliases (apex + www, `/atlas.*`, `/data/atlas.*`, `/atlas/atlas.*`).
  Live generated 2026-10-05T07:21:35Z, 1321 features; only 12 features changed. No SPA redeploy.
- CI: `scripts/check-reference-rings.mjs`. Docs: `docs/REFERENCE-RING-CRS.md`.
- Follow-up ask: audit other generic route keys (`container`, `research`, `tourism`, `river`) for
  foreign-flag or non-Arctic vessels landing on Murmansk / Svalbard anchors.
