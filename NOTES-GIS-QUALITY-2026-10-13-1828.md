# GIS Quality — gis-port150-1828 (~18:28 MSK Europe/Moscow, 2026-10-13)

## Site health
GET apex `/` and `www` → **200**; atlas GET **200** (1317 feats, gen 2026-10-13T15:13:10Z before rebuild). **Did not restart** arctic-trade-lanes (full SPA `src/` still missing on Zo).

## Win
Densified **ARC-PORT-150** Pyramiden Port (Billefjorden, Spitsbergen) off soft 4-decimal `78.6567 / 16.3250`
(= settlement centre, Wikidata **Q845396** P625 78.656111/16.325, ~0.07 km) onto the harbour quay crane:
OpenStreetMap **node/857534564** man_made=crane `78.654916 / 16.3553162`, at the seaward end of the concrete
embankment quay road **way/72761799**. Moved **~0.69 km** ESE.

## Sources (neutral, public)
- OSM **node/857534564** man_made=crane 78.654916/16.3553162 (harbour coal-loading crane)
- OSM **way/72761799** highway=service surface=concrete embankment=yes (quay road; ends ~0.02 km from crane)
- Kystverket leading beacons: **Pyramiden, Øvre** ref:kystverket 991900 (OSM node/5323958065, ~0.16 km N); **Pyramiden, Nedre** ref:kystverket 991800 (OSM node/5323958066, ~0.31 km E)
- OSM weather station node/6955534667 (~0.09 km N)
- Wikidata **Q845396** Pyramiden (settlement; soft pin source) ~0.67 km W; OSM place node/273476498
- harbourmaps.com Pyramiden natural harbour 78.6528/16.3822 (~0.6 km E; anchorage, not used as anchor)
- No Wikidata harbour item; UN/LOCODE for Pyramiden not confirmed (unece.org blocked fetch) — not claimed
- Caveat: local OSM coastline way/323883492 is coarse (source gadm/yahoo, fixme=update); crane plots ~0.17 km inside it
- `position_quality=facility_site` (quay crane; not a surveyed berth)

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-150 (schematic tags now 22)
- ports.csv: 13 copies lat/lon + densify sources note, confidence=92, last_verified=2026-10-13
- Patch `atlas-proj/_patch_port150_1828.py`; lock `atlas-proj/check_port150_pyramiden.py` (PORT-171/047/051/022/042 locks OK)

## Live
- Atlas gen `2026-10-13T15:35:13.097946+00:00`, **1317** features (unchanged); EPSG:3996 kept; diff = ARC-PORT-150 only
- Alias sync bad=0 + 50 extra served copies; 0 left on previous gen
- No App.tsx smash / SPA redeploy / DNS / x402 / restart.

## Next candidates
- Remaining soft 4-decimal ports lacking OSM/WD in sources (re-scan ports.csv)
