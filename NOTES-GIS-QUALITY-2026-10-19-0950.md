# GIS Quality — gis-loop-1019-0950 (~09:50 MSK Europe/Moscow, 2026-10-19)

## Site health
GET `/` → **200** (91208 B, md5 fdba64b6, v2 homepage); `/atlas.3996.geojson` + `/atlas.4326.geojson` **200**
(1317 feats, gen 2026-10-19T06:23:15Z before rebuild, CRS EPSG:3996 / EPSG:4326). `/api/health` ok, `/api/x402/status` 200,
`/api/alpha/status` 200 (keyConfigured=false). UM home 200 (8019 B), radar/doug-leone, radar/elon-musk, hi/radar/doug-leone 200;
UM `/api/x402/status?slug=doug-leone` 200 2537 B with locales + geo (Menlo Park). Zo nested ATL == GitHub main 75ff0b63d (clean) before change.
Services not restarted.

## Win
Densified **ARC-PORT-065** Port of Kokkola (Deep Port + Silverstone; Ykspihlaja, Kokkola, Finland; UN/LOCODE FIKOK)
off soft 4-decimal `63.8472 / 23.1133` (Kokkola town east of the harbour, ~1.3 km from ARC-CITY-071; not port infrastructure)
onto the **Deep Port** basin: OpenStreetMap **relation/11003166** landuse=industrial industrial=port name=Kokkolan syväsatama,
operator=Kokkolan satama, wikidata=Q10543787, website=portofkokkola.fi. Net shoelace centroid (outer way/792462335 minus
inner ways 506266877, 506266875; 0.43 km²) `63.865509 / 23.0312818`, point-in-polygon verified. Moved **~4.50 km** WNW (bearing ~297°).

## Sources (neutral, public)
- OSM **relation/11003166** Kokkolan syväsatama (Deep Port) — https://www.openstreetmap.org/relation/11003166
- portofkokkola.fi/en/ports/deep-port (7 Mt/yr dark bulk, 14 m fairway, quays 10–12 14.2 m) and /silverstone-port
  ("Silverstone Port … shares the same basin with the Deep Port")
- Wikidata **Q10543787** Port of Kokkola: P1937 UN/LOCODE FIKOK (matches record), P625 63.844439/23.022219 = port-wide point
  on General Port / Kokkolan kantasatama (OSM way/759190646, also wikidata=Q10543787) ~2.38 km SSW — not used as anchor
  because the record is Deep Port + Silverstone
- OSM way/519261340 Suurteollisuusalue (KIP industrial park, industrial=port) adjacent S
- UN/LOCODE FIKOK unchanged; `position_quality=facility_site` (port-area polygon, not a surveyed berth)
- No other ATL point feature within 3 km of the new position

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-065 (both builder copies)
- ports.csv copies (13): lat/lon + densify sources note, confidence=95, last_verified=2026-10-19
- Patch `atlas-proj/_patch_port065_0950.py`; lock `atlas-proj/check_port065_kokkola_deep_port.py`; all prior port locks OK

## Live
- Atlas gen `2026-10-19T06:56:21.759701+00:00`, **1317** features (unchanged); EPSG:3996 kept; diff vs previous live = ARC-PORT-065 only
- Pre-patch baseline rebuild reproduced the live atlas exactly (0 feature diffs) before the change
- sync_atlas_aliases.sh 10 dirs bad=0 + swept 205 old-generation copies (41 dirs, ATL.com + Dataset); 0 stale left
- live `/atlas.3996.geojson` md5 a764ef64, `/atlas.4326.geojson` md5 59bbba5c
- No App.tsx smash / SPA redeploy / DNS / x402 / restart.

## Next candidates
PORT-139 Tromsø Havn (NOTRO; multi-quay, needs anchor choice), PORT-160 Mjóeyrarhöfn (ISRFJ; soft pin already ~= OSM relation/2819859
centroid, harbour node/626578135 only ~0.21 km — low value), PORT-140 Ísafjörður pier extension, PORT-158 Sortland, PORT-159 Hadsel.
