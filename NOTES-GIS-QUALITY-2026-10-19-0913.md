# GIS Quality — gis-loop-1019-0913 (~09:13 MSK Europe/Moscow, 2026-10-19)

## Site health
GET `/` → **200** (91208 B, v2 homepage layer from 2026-10-18); `/atlas.3996.geojson` + `/atlas.4326.geojson` **200**
(1317 feats, gen 2026-10-14T07:26:36Z before rebuild). `/api/health` ok. UM home + radar pages **200**.
Service `arctic-trade-lanes` (bun run cluster.ts) up; **not restarted**.

## Win
Densified **ARC-PORT-039** Rankin Inlet Port (Kangiqiniq, Kivalliq, Nunavut; UN/LOCODE CARAN)
off soft 4-decimal `62.8094 / -92.0853` (hamlet core, not port infrastructure) onto the **Itivia barge dock**
(sealift landing): OpenStreetMap **way/1537457615** man_made=pier area=yes floating=no surface=concrete
(mapped 2026-07-11), shoelace centroid `62.7990461 / -92.0920014`. Moved **~1.20 km** SSW (bearing ~196°).

## Sources (neutral, public)
- OSM **way/1537457615** man_made=pier concrete (Itivia barge dock)
- OSM **way/1537459872** landuse=harbour industrial=port (Itivia harbour yard), centroid 62.8009827/-92.0959941 (~0.30 km NW)
- Agnico Eagle Nunavut — Itivia Project (aemnunavut.ca/community/itivia-project): Itivia Harbour laydown, fuel farm, bypass road to Meliadine; OSM storage tanks way/762095264, way/762095265 (~0.38 km W)
- rankininlet.ca/tourism: "barge dock and FOL" at Itivia; Johnston's Cove small craft harbour is separate
- Wikimapia 5549311 Itivia 62.79944/-92.09000 (~0.11 km)
- Nunatsiaq News (2022, syndicated): new boat launch ~152 m from the Itivia barge where sealift and Agnico offload
- Wikidata: no harbour item; hamlet Q1021766 not reused
- UN/LOCODE CARAN left unchanged (not re-verified this cycle)
- `position_quality=facility_site` (pier outline, not a surveyed berth)
- Distinct from Johnston Cove small craft harbour (OSM way/514257325 landuse=harbour, ~1.80 km NE); no other ATL record within 1.2 km

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-039
- ports.csv copies: lat/lon + densify sources note, confidence=90, last_verified=2026-10-19
- Patch `atlas-proj/_patch_port039_0913.py`; lock `atlas-proj/check_port039_rankin_itivia.py`; all prior port locks OK

## Live
- Atlas gen `2026-10-19T06:23:15.177259+00:00`, **1317** features (unchanged); EPSG:3996 kept; diff vs previous live = ARC-PORT-039 only
- Pre-patch baseline rebuild reproduced the live atlas exactly (0 feature diffs) before the change
- Synced 260 old-generation copies (52 dirs, ATL.com + Dataset); live `/atlas.3996.geojson` md5 4d53c0da, `/atlas.4326.geojson` md5 65e525bc
- No App.tsx smash / SPA redeploy / DNS / x402 / restart.

## Next candidates
PORT-065 Kokkola (FIKOK), PORT-139 Tromsø Havn (NOTRO), PORT-160 Mjóeyrarhöfn (ISRFJ).
