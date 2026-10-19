# GIS Quality — gis-loop-1019-1146 (~11:46 MSK Europe/Moscow, 2026-10-19)

## Site health
GET `/` → **200** (91208 B, md5 fdba64b6); `/atlas.3996.geojson` 200 (1317 feats, gen 2026-10-19T08:26:33Z before rebuild,
EPSG:3996); `/api/health` 200, `/api/x402/schema` 200 2747 B, `/api/x402/status` 200 1363 B, `/api/alpha/status` 200 888 B,
`/pricing` 200. UM home 200 (8019 B, md5 83e8388a), bundle `index-CIQoD7he.js` + `index-DZdhQ1Nj.css`;
person pages 200 (elon 26183, doug 23217, hi/doug 23781, olga 26475, durov 23232), no Recovering/portfolioTree in HTML.
Zo nested ATL == GitHub main **372f0f954** before change. Services not restarted. No DNS / x402 / SPA redeploy.

## Win
Densified **ARC-PORT-119** Blue Water Blue Imeq — Greenland logistics hub (Nuuk) (UN/LOCODE GLGOH)
off soft 4-decimal `64.1835 / -51.7216` (~0.28 km W of Blue Water's legacy Industrivej 22 office, OSM node/5130345724;
not the Blue Imeq hub) onto the **former Nuuk Imeq bottling plant** that Blue Water bought in 2024 and opened as Blue Imeq
in Mar 2026: OpenStreetMap **way/257366763** building=industrial name=Nuuk Imeq A/S, addr Qeqertanut 2, 3905 Nuussuaq
(~8,400 m², v3), shoelace centroid `64.1765970 / -51.7059645` (inside the polygon). Moved **~1.08 km** SE (bearing ~135°).

## Sources (neutral, public)
- OSM **way/257366763** — https://www.openstreetmap.org/way/257366763
- bws.net news 26 Jul 2024 "Blue Water opens new facilities in the former bottling plant in Nuuk" (bought Nuuk Imeq buildings, ~9,800 m²)
- sermitsiaq.ag "Shipping-selskab køber Nuuk Imeq-bygninger" / "Blue Water satser stort i Grønland"
- bws.net/contact/greenland/nuuk: Blue Water Greenland A/S, Qeqertanut 2, 3905 Nuussuaq (matches OSM addr)
- heavyliftpfi.com 10 Mar 2026 (row source, opening of Blue Imeq) unchanged
- No Wikidata facility item (operator Blue Water Shipping Q12303853 not reused). UN/LOCODE GLGOH unchanged
- `position_quality=facility_site` (warehouse/terminal building, not a quay); confidence 74 → 90

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-119 (parent + nested builder copies)
- ports.csv copies (13): lat/lon + densify sources note, confidence=90, last_verified=2026-10-19
- Patch `atlas-proj/_patch_port119_1146.py`; lock `atlas-proj/check_port119_blue_imeq.py`; PORT-065/066/114 locks still OK

## Live
- Atlas gen `2026-10-19T08:53:03.904784+00:00`, **1317** features (unchanged count); EPSG:3996 kept; only ARC-PORT-119 changed
- old-gen sweep 70 copies / 14 dirs; sync_atlas_aliases.sh 10 dirs bad=0; live /, /data, /atlas aliases md5 79c8e3a3
- No App.tsx smash / SPA redeploy / DNS / x402 / restart.

## Next candidates
PORT-129 Crémaillère Harbour (planned, EA registration coords), PORT-134 Argentia (Cooper Cove), PORT-135 Kalvåg,
PORT-139 Tromsø (multi-quay), PORT-140 Ísafjörður, PORT-158 Sortland, PORT-159 Hadsel, PORT-160 Mjóeyrarhöfn.
