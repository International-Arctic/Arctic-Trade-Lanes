# GIS Quality — gis-port093-1020 (~10:20 MSK Europe/Moscow, 2026-10-14)

## Site health
GET `/` → **200**; atlas **200** (1317 feats, gen 2026-10-14T06:54:15Z before rebuild).
UM home **200**. **Did not restart** arctic-trade-lanes (full SPA `src/` still missing on Zo).

## Win
Densified **ARC-PORT-093** Alta Urnesbukta Floating Quay (Alta Havn KF, Amtmannsnes, Altafjorden, Finnmark)
off soft 4-decimal `69.9686 / 23.2717` (~2.3 km SW of Urnesbukta, inland on the Bossekop side)
onto the outer floating quay of Urnesbukta marina og fiskerihavn: OpenStreetMap **way/795270408**
man_made=pier floating=yes area=yes (~142 m x ~4 m outline, mapped 2020), shoelace centroid
`69.9859524 / 23.3061572`. Moved **~2.33 km** NE (bearing ~34°).

## Sources (neutral, public)
- OSM **way/795270408** man_made=pier floating=yes (outer floating quay / breakwater of the marina)
- Alta Havn KF quay list (altahavn.no/kaier): **Kai 7 Molokaia**, public fishery quay 100 m x 6 m, depth 5–15 m, 29 sheds, at `69.985979 / 23.306159` (**~3 m** from the OSM centroid)
- marinasolutions.no reference (April 2026): new 100 m two-unit floating molo in Urnesbukta for Alta Havn KF (6 m wide, 20-t bollards, crane-ready)
- OSM node/1345229303 Urnesbukta Marina (~0.13 km W); node/1376347030 natural=bay Urnesbukta (~0.39 km W); Fiskerihavna road way/123402386; Kystverket pile *Innerberget* ref 929503 (node/10813971232)
- Wikidata: no harbour item found; Alta municipality Q6535 not reused
- **UN/LOCODE corrected NOALT → NOALF**: NOALT is not in UN/LOCODE; NOALF = Alta (function 1-34, 6958N 02314E); Alta Havn ISPS facility codes are NOALF-00xx
- `position_quality=facility_site` (floating quay outline; OSM outline predates the 2026 molo, not a surveyed berth)
- Distinct from the Alta Havn **Bukta** main port (Bukta flytekai 69.978171/23.330122, ~1.25 km SE); there is no ATL port record there, so nothing collapsed. ARC-PROG-597 (Innsatssona, 69.9689/23.2717) untouched.

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-093 (both builder copies; schematic tags now 26)
- ports.csv: 13 copies lat/lon + unlocode + densify sources note, confidence=90, last_verified=2026-10-14
- Patch `atlas-proj/_patch_port093_1020.py`; lock `atlas-proj/check_port093_alta_urnesbukta.py`; all prior port locks OK

## Live
- Atlas gen `2026-10-14T07:26:36.374680+00:00`, **1317** features (unchanged); EPSG:3996 kept; diff = ARC-PORT-093 only (coords, position_anchor/quality/note, unlocode)
- Alias sync bad=0 (10 dirs) + 38 extra served dirs (ATL.com) + 3 Dataset dirs; 0 stale manifests left
- No App.tsx smash / SPA redeploy / DNS / x402 / restart.

## Next candidates
PORT-039 Rankin Inlet (CARAN), PORT-034 Obskaya LNG (RUOBS), PORT-065 Kokkola (FIKOK), PORT-139 Tromsø Havn (NOTRO), PORT-160 Mjóeyrarhöfn (ISRFJ).
