# GIS Quality — gis-loop-1019-1245 (~12:45 MSK Europe/Moscow, 2026-10-19)

## Site health
ATL `/` **200** (91208 B, md5 fdba64b6); `/atlas.3996.geojson` 200 (1317 feats, gen 2026-10-19T09:29:57Z before rebuild,
EPSG:3996); `/api/health` 200 (47 B), `/api/x402/schema` 200 2747 B, `/api/x402/status` 200 1363 B, `/api/alpha/status` 200 888 B,
`/pricing` 200 8673 B, `/ports` 200 27302 B, `/icebreakers` 200 11480 B, `/lanes` 200, `/shipyards` 200, `/data/ports.csv` 200.
(`/api/ships`, `/api/ports`, `/ships` are 404 and were never part of the baseline. Ships are served as atlas layers plus `/icebreakers`.)
UM home 200 (8019 B, md5 83e8388a), bundle `index-CIQoD7he.js` + `index-DZdhQ1Nj.css`; radar/person pages 200 (elon 26183,
doug 23217, olga 26475, durov 23232), hi/radar doug 23781 (Devanagari 293), hi/radar olga 26887 (Devanagari 234),
doug_json 3433, x402 status doug 2537, skill 14329; no Recovering/portfolioTree. All identical to the 1222 baseline.
Zo nested ATL == GitHub main **2f8302956** before change. Services not restarted. No DNS / x402 / SPA redeploy.

## Skipped
- ARC-PORT-135 Kalvåg New Fishing Harbour (NOKVG): planned Kystverket project that has not been built yet. fjt.no and Bremanger kommune (2026)
  report the tender had not yet been issued, and OSM has no facility polygon for the new basin. The official application (Norconsult
  for Kystverket, statsforvalteren søknad) only has survey points. The 2019 sediment stations at UTM32 E282643–282939 / N6854445–6854671,
  i.e. 61.7610–61.7632 N / 4.8802–4.8858 E, and the current meters S1 61.761526/4.883464 and S2 61.763307/4.887927 lie south of Kalvøya
  near Høgholmen, 0.2–0.6 km from the current pin. That defines an area, not a facility. Pin left unchanged. Revisit when the moloer are built or mapped.
- ARC-PORT-139 Tromsø Havn: the row is a port-authority aggregate across several quays (Breivika, Prostneset, Grøtsund). No single
  verifiable facility, so it was not attempted this cycle.

## Win
Densified **ARC-PORT-140** Ísafjörður Pier Extension (Sundabakki, Sundahöfn; UN/LOCODE ISISA) off soft 4-decimal
`66.0755 / -23.1080`. That pin was a schematic offset from the ISISA parent ARC-PORT-077, ~1.2 km NNE of the pier and not on a quay.
New anchor: OpenStreetMap **way/1294792142** `man_made=quay mooring=cruise name=Cruise Port`
(~16,400 m², ~509 m long, v5), shoelace centroid `66.0657813 / -23.1204589` (inside the polygon). Moved **~1.22 km** SSW (bearing ~207°).

## Sources (neutral, public)
- OSM **way/1294792142**: https://www.openstreetmap.org/way/1294792142 ; Cruise Port Information Center node/13048366035 adjacent
- vegagerdin.is/verkefnin/framkvaemdir/sundabakki: ~300 m steel-sheet quay extension south of the older addition, dredged to 11 m,
  ~6,000 m² concrete deck, ships up to 330 m / 9.5 m draught
- cruisemapper.com news 12408: pier 190 m → 500 m, ISK 1B / EUR 8M, 10 m alongside (row sources unchanged)
- No Wikidata item. UN/LOCODE ISISA unchanged. Parent ARC-PORT-077 (66.0708207/-23.1241308, OSM harbour node/1852758904) untouched, ~0.6 km N
- `position_quality=facility_site` (cruise quay, not a single berth); confidence 84 → 90

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-140 (parent + nested builder copies)
- ports.csv copies (13): lat/lon + densify sources note, confidence=90, last_verified=2026-10-19
- Patch `atlas-proj/_patch_port140_1245.py`; lock `atlas-proj/check_port140_isafjordur_sundabakki.py`; PORT-114/119/134 locks still OK

## Live
- Atlas gen `2026-10-19T09:51:56.963382+00:00`, **1317** features (count unchanged); EPSG:3996 kept; only ARC-PORT-140 changed
- old-gen sweep 70 copies / 14 dirs; sync_atlas_aliases.sh 10 dirs bad=0; live /, /data, /atlas aliases md5 5987c96a (3996 9088082f)
- No App.tsx smash / SPA redeploy / DNS / x402 / restart.

## Next candidates
PORT-158 Sortland, PORT-159 Hadsel (Stokmarknes), PORT-160 Mjóeyrarhöfn (Reyðarfjörður), PORT-139 Tromsø (needs one named quay).
Parked: PORT-129 Crémaillère and PORT-135 Kalvåg, both planned sites with no built or mapped facility yet.
