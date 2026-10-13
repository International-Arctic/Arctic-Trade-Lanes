# GIS Quality — gis-port136-1346 (~13:46 MSK Europe/Moscow, 2026-10-13)

## Win
Densified **ARC-PORT-136** Narvik Terminal Nord (Kleiva), the planned Narvik Havn KF + Bane NOR rail/port terminal,
off soft approximate `68.4400 / 17.4200` onto **Kleivhammaren on Fagernesveien**, OSM **node/6372382875**
(bus stop "Kleivhammarn", NSR quay 85150) `68.4241270 / 17.4309920`.
Moved **~1.82 km** S/SE. The old 2-decimal pin sat in Narvik city/harbour, north of the planned terminal area.

## Sources (neutral, public)
- Narvik kommune, kunngjøring av planvedtak: områderegulering "Narvikterminalen med Terminal Nord", PlanID 2021001,
  kommunestyret 18.04.2024 sak 040/24 (pkt. 7.3 not yet legally binding pending the Bane NOR objection)
- Planbeskrivelse (Rambøll for Narvik Havn KF; statsforvalteren.no copy): "En ny Terminal nord mellom RO-RO-kaia og
  Kleivhammaren"; sea fill along Fagernesveien; Fagernesveien moved east ~500 m past Kleivhammaren; access to
  Terminal nord "nord for eksisterende møbelforretning"; ro-ro terminal "ved Lillekleiva"
- Logistikk Inside (trade press): "Terminal nord ... som ligger langs Kleiva", about NOK 1 billion, national (NTP) funding sought
- OSM API: Kleivhammarn stop node/6372382875 (+ opposite platform node/6372382883); Lillekleiva stop node/6372384369
  (~0.33 km S, ro-ro end); Fagmøbler Narvik node/7590047622 (the furniture store, ~0.08 km N); Kleiva place node/9884377983 (~0.5 km N)
- Terminal not built and no quay mapped yet, so `position_quality=facility_site`

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-136 (schematic tags now 13)
- ports.csv: every copy (16) lat/lon + sources note appended (inside the quoted sources field), confidence=90, last_verified=2026-10-13
- Patch `atlas-proj/_patch_port136_1346.py`; lock check `atlas-proj/check_port136_narvik_terminal_nord.py`
  (prior PORT-105/046/041/045/110/078 locks still OK)

## Live
- Atlas gen `2026-10-13T10:52:57.222487+00:00`, **1317** features (unchanged); diff vs previous build: **ARC-PORT-136 geometry/props only** (wgs84 + 3996)
- 10 alias dirs synced (bad=0) + 10 extra served copies (20 verified md5)
- Live https://arctictradelanes.com/atlas/atlas.wgs84.geojson, /atlas.wgs84.geojson, /data/atlas.wgs84.geojson, /atlas/atlas.3996.geojson verified
- No SPA redeploy / App.tsx / DNS change

## Help wanted
When Bane NOR's detailed plan for the rail terminal or the new quay on the outer side of the Kleiva fill is published,
or the fill gets mapped in OSM, a PR moving this pin onto the quay (with the source cited) would upgrade it to a surveyed berth.

## Next candidates
- ARC-PORT-036 Tiksi East Port (71.68/128.95; need a source that "East Port" is the mapped Tiksi seaport harbour way/233652114, not a separate site)
- ARC-PORT-075 Nuuk Qeqertat quay (64.17/-51.71; need the Qeqertat quay site from a public Sikuki / Nuuk harbour source)
- UM: health OK (838 pins + 1 corridor line, 0 bad geo); no change
