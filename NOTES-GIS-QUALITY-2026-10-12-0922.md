# GIS Quality Loop — 2026-10-12 ~09:22 MSK (gis-halter-0922)

## Prior run (Fri 2026-10-09 ~19:09 MSK)
Marked FAILED. This cycle: Zo MCP ready, `gh` as alexdolbun OK, live ATL atlas HTTP 200 (gen `2026-10-05T15:55:28Z`, 1320 feats), UM radar geo/geojson HTTP 200. No live-site / Zo-auth / git-auth breakage found. Automation `gis-quality-loop-um-atl-30m` last scheduled errors historically were `usage_limit` (Sep 17); Fri 19:09 is outside weekday 09–18 schedule — likely parent/manual fail, not infra down.

## Health
- ATL: 1320 features; 0 null-island; 0 OOB; 0 dup ids; layers ports 155 / shipyards 70 / programs 713 / lanes 27; projection note EPSG:4326 storage + EPSG:3996 companion; bathy gen `2026-10-05T15:56:06Z` (27 lanes).
- UM: geojson 834 (606 primary + 227 site + 1 corridor); geo.json 606 pins; 0 null-island/OOB; **countryIso2 missing on all Point features** (geo-filter 0.1.7 not applied server-side); 122 stacked locs / 724 stacked pins; 92 raw country strings.

## Wins
1. **ATL** — quarantined ARC-SHIP-022 VT Halter as duplicate of ARC-SHIP-068 (WD Q29093553). Atlas rebuild + alias sync.
2. **UM** — (see companion) emit `countryIso2`/`country_quality` on `/api/radar/geojson.json` if deployed this cycle.

## CI / docs
- `docs/GIS-QUALITY-2026-10-12-ship022-halter-quarantine.md`
- `scripts/check-ship022-halter-quarantine.mjs`
