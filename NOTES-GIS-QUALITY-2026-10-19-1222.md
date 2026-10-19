# GIS Quality — gis-loop-1019-1222 (~12:22 MSK Europe/Moscow, 2026-10-19)

## Site health
GET `/` → **200** (91208 B, md5 fdba64b6); `/atlas.3996.geojson` 200 (1317 feats, gen 2026-10-19T08:53:03Z before rebuild,
EPSG:3996); `/api/health` 200 ok, `/api/x402/schema` 200 2747 B, `/api/x402/status` 200 1363 B, `/api/alpha/status` 200 888 B,
`/pricing` 200 8673 B. UM home 200 (8019 B, md5 83e8388a), bundle `index-CIQoD7he.js` (957729 B) + `index-DZdhQ1Nj.css`;
person pages 200 (elon 26183, doug 23217, olga 26475, durov 23232), hi/radar doug 23781 (Devanagari 293), hi/radar olga 26887
(Devanagari 234), doug_json 3433, x402 status doug 2537; no Recovering/portfolioTree in HTML.
Zo nested ATL == GitHub main **198d8958b** before change. Services not restarted. No DNS / x402 / SPA redeploy.

## Skipped
- ARC-PORT-129 Crémaillère Harbour (GNP, planned greenfield): no OSM/Wikidata facility exists yet. Only OSM relation/13625890
  `natural=bay` Crémaillère Harbour (centroid 51.3372352/-55.6051772, ~0.79 km from the EA-registration pin, in water) and an
  OSM track way/1392421233 "Crémaillère Harbour Road". Bay-level only, no gain over the EA registration coords → left unchanged.

## Win
Densified **ARC-PORT-134** Port of Argentia / Cooper Cove Marine Terminal (UN/LOCODE CANWP) off soft 4-decimal
`47.2953 / -53.9858` (~0.21 km SW of the terminal, just outside the harbour lands) onto OpenStreetMap **way/845500563**
`landuse=harbour` (~4.0 ha, v1, along Waterfront Drive, bordering Cooper Cove OSM relation/13574863), shoelace centroid
`47.2968528 / -53.9842123` (inside the polygon). Moved **~0.21 km** NE (bearing ~35°).

## Sources (neutral, public)
- OSM **way/845500563** — https://www.openstreetmap.org/way/845500563 ; Cooper Cove relation/13574863
- NL EA Reg. 2279 project summary (Oct 2023, gov.nl.ca/eccc/files/env_assessment_y2023_2279_summary.pdf): wharf-face start
  UTM 22N N5242739.41 E274633.14 → 47.299333/-53.981152 (~0.36 km NE of the centroid, at the polygon NE edge), the existing
  fleet dock extended into Cooper Cove; IAAC 86128 (no further assessment, 2 Aug 2024). Row sources unchanged
- No Wikidata port item (Argentia settlement Q2860953 not reused). UN/LOCODE CANWP unchanged
- `position_quality=facility_site` (terminal harbour lands, not a single berth); confidence 90 (unchanged)

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-134 (parent + nested builder copies)
- ports.csv copies (13): lat/lon + densify sources note, confidence=90, last_verified=2026-10-19
- Patch `atlas-proj/_patch_port134_1222.py`; lock `atlas-proj/check_port134_argentia.py`; PORT-114/119 locks still OK

## Live
- Atlas gen `2026-10-19T09:29:57.704068+00:00`, **1317** features (unchanged count); EPSG:3996 kept; only ARC-PORT-134 changed
- old-gen sweep 70 copies / 14 dirs; sync_atlas_aliases.sh 10 dirs bad=0; live /, /data, /atlas aliases md5 af0252bc (3996 a9133dcd)
- No App.tsx smash / SPA redeploy / DNS / x402 / restart.

## Next candidates
PORT-135 Kalvåg, PORT-139 Tromsø (multi-quay), PORT-140 Ísafjörður pier extension, PORT-158 Sortland, PORT-159 Hadsel,
PORT-160 Mjóeyrarhöfn. PORT-129 Crémaillère parked until GNP publishes a site plan / OSM facility appears.
