# GIS Quality — gis-port047-1735 (~17:35 MSK Europe/Moscow, 2026-10-13)

## Site health
GET apex/www/zo `/` → **200** (self-contained `dist/index.html`); HEAD `/` → 404 (server SPA fallback is GET-only — not a content outage). Atlas GET **200**. **Did not restart** arctic-trade-lanes (full SPA `src/` still missing on Zo).

## Win
Densified **ARC-PORT-047** Nordvik Port (historic) off soft 4-decimal `73.9980 / 111.4693`
(= OSM place=locality **node/3290343023** Нордвик; empty sources; some stale copies still `74.5000/111.5000`)
onto Wikidata **Q2364258** Nordvik (former port and settlement, Krasnoyarsk Krai / Taymyr;
founded ~1930, abolished 1956) P625 `73.9975 / 111.463333`. Moved **~0.19 km** W.
No OSM pier/harbour mapped nearby on Khatanga Gulf / Laptev Sea shore.

## Sources (neutral, public)
- Wikidata **Q2364258** Nordvik — former port and settlement; P625 73.9975/111.463333; P576 1956; P571 1930
- OSM node/3290343023 place=locality Нордвик 73.9980/111.4693 (~0.19 km E of WD)
- UN/LOCODE RUNVK
- `position_quality=facility_site` (historic port site; not a surveyed berth)

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-047 (schematic tags now 20)
- ports.csv: 13 copies lat/lon + sources note, confidence=90, last_verified=2026-10-13
- Patch `atlas-proj/_patch_port047_1735.py`; lock `atlas-proj/check_port047_nordvik.py`

## Live
- Atlas gen `2026-10-13T14:42:59.279687+00:00`, **1317** features; EPSG:3996 kept
- Alias sync bad=0 + extra served copies
- No App.tsx smash / SPA redeploy / DNS / x402. UM health check only.

## Next candidates
- ARC-PORT-171 Manorsky / Port Elga, ARC-PORT-150 Pyramiden
