# GIS Quality — gis-port051-1700 (~17:00 MSK Europe/Moscow, 2026-10-13)

## Site health (PRIORITY 1)
Homepage was HTTP 500 (ENOENT `./dist/index.html`) while `/atlas/atlas.geojson` stayed 200.
SPA source on Zo was gutted (no `src/api/*`, no pre-built `dist/assets`); **did not restart** the live `bun run server.ts` process (pid still holding modules in memory).
Restored a self-contained `dist/index.html` + mirrored `public/index.html`, and restored `package.json`/`server.ts` from `_bak-mvp-20261006` for future restarts only.
After fix: apex/www/zo `/` → **200**; atlas still **200**. **Do not restart** arctic-trade-lanes until full SPA `src/` is restored — restart would crash.

## Win
Densified **ARC-PORT-051** Nome Snake River Moorage Facility off soft 4-decimal `64.4980 / -165.4200`
onto west-bank OSM **way/1268826085** `leisure=slipway` centroid `64.5014256 / -165.4286323`
in the City of Nome Snake River Floats / Moorage corridor (south of Satellite Drive, north of RO/RO).
Moved **~0.56 km**. Distinct from **ARC-PORT-026** Nome Harbor (~0.74 km SW).

## Sources (neutral, public)
- OSM way/1268826085 leisure=slipway (west bank Snake River)
- OSM way/8983909 Satellite Drive ~0.29 km N
- Wikidata **Q7547059** Snake River (Nome) P625 64.5044/-165.4242 ~0.39 km NE
- City of Nome Strategic Development Plan Phase B (Apr 2025): west shore Snake River, south of Satellite Drive, north of RO/RO
- MARAD FONSI Aug 2026 + RAISE $13.2M; 35% design; dredge bid early 2027 — floats not built
- `position_quality=facility_site` (planned facility; not a surveyed berth)

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-051 (schematic tags now 19)
- ports.csv: 13 copies lat/lon + sources note, confidence=90, last_verified=2026-10-13
- Patch `atlas-proj/_patch_port051_1700.py`; lock `atlas-proj/check_port051_snake_river.py`

## Live
- Atlas gen `2026-10-13T14:10:04.544559+00:00`, **1317** features; EPSG:3996 kept
- Alias sync bad=0
- No App.tsx smash / SPA redeploy / DNS / x402. UM skipped.

## Next candidates
- ARC-PORT-047 Nordvik (historic), ARC-PORT-171 Manorsky / Port Elga, ARC-PORT-150 Pyramiden
