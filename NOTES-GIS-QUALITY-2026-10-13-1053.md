# GIS Quality — gis-port078-1053 (~10:53 MSK Europe/Moscow, 2026-10-13)

## Win
Densified **ARC-PORT-078** Finnafjörður Deep-Water Port (FFPD, planned greenfield) off soft `66.27 / -15.25`
(open sea off Langanes / Bakkaflói, no land within the reverse-geocode zoom) onto **Wikidata Q106075430 P625**
`66.1062 / -15.1502` (= en.wikipedia *Finnafjord Port* 66°06′22″N 15°09′01″W). Moved **~18.8 km**.

## Sources (neutral gazetteer / official planning)
- Wikidata Q106075430 Finnafjord Port P625 66.1062/-15.1502
- OSM relation/8413765 Finnafjörður (natural=bay); Wikidata Q16423834 fjord
- OSM node/1822239443 Gunnólfsvík (N shore, state-owned 167 ha industrial site) and Saurbær (S shore)
- Langanesbyggð / EFLA *The Finnafjord Harbour Project* (harbour dock area ~17 km² inside the fjord, ~6.3 km quays)
- Point sits in the planned harbour basin; quay line not yet fixed → `position_quality=facility_site` (planned)

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION allowlist + ARC-PORT-078 (schematic tags now 7)
- ports.csv: every copy (16) lat/lon + sources note, last_verified=2026-10-13 (confidence 85 kept)
- Lock check `atlas-proj/check_port078_finnafjord.py`

## Live
- Atlas gen `2026-10-13T07:59:24.930934+00:00`, **1317** features (unchanged), 10 alias dirs bad=0
- Live diff vs previous gen 07:23:15Z: **ARC-PORT-078 only**

## Checked / not taken this cycle
- ARC-PORT-110 Galtarhöfn 64.32/-21.85 → OSM Galtarvík way/249515549 ~2.5 km (candidate next)
- ARC-PORT-045 Ambarchik → OSM way/655223046 ~2.7 km; ARC-PORT-041 Mys Shmidta → OSM way/93613726 ~2.7 km
- ARC-PORT-136 Narvik Terminal Nord (Kleiva) → OSM node/9884377983 only ~1.3 km (low value)
- ARC-PORT-099 Pevek Cape Nagleynyn: Nominatim hit 69.08/169.33 ~70 km SW of Pevek, unverified — rejected
- UM: site 200, no cheap geo fix taken
