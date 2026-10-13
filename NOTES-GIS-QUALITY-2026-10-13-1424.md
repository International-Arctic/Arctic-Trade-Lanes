# GIS Quality — gis-port099-1424 (~14:24 MSK Europe/Moscow, 2026-10-13)

## Win
Densified **ARC-PORT-099** Pevek Cape Nagleynyn Marine Terminal (Baimskaya GOK gateway of Pevek seaport)
off soft approximate `69.7200 / 170.2000`, which sat in Pevek Strait water off Pevek town, onto the terminal site
mapped in OSM: **way/1514011213** `landuse=industrial` "Naglyoygnyn Port" (мыс Наглёйгнын порт), vertex centroid
`69.0382643 / 169.3878168`, on the Chaunskaya Guba (Chaun Bay) shore.
Moved **~82.2 km** SW. The old sources note ("Cape Nagleynyn adjacent NW of existing Pevek quays") was wrong;
a correction note is appended in the sources field.

## Sources (neutral, public)
- government.ru/news/48261: RF government order adding land and water "у мыса Наглёйнын" to Pevek seaport for the Baimskaya GOK terminal (~2 Mt/yr)
- gge.ru (Glavgosexpertiza positive conclusion): terminal "у мыса Наглёйнын в заливе Чаунская Губа", 275 m berth, approach channel sited for the shortest run from Chaun Bay to the cape, territory 224.86 ha
- OSM node/9513605008 `natural=cape` мыс Наглёйнын `69.0792927 / 169.3310737`; Wikidata **Q37885662** (instance of cape, GeoNames 2123047) P625 `69.0772 / 169.3269` (~0.28 km apart)
- OSM changeset 182704371 (2026-05-15, iD, source Sentinel-2 / Esri imagery): port area way/1514011213, pier way/1514011280 (~1.0 km E of anchor),
  breakwaters way/1514011278 + way/1514011279, fuel depot way/1514011277, floating nuclear unit node/13831051695 (ref Cape Nagloynyn-2)
- Earlier cycle (gis-port078-1053) rejected the 69.08/169.33 cape hit as "unverified, ~70 km SW of Pevek"; the government order + Glavgosexpertiza text + imagery-mapped terminal now verify it
- Terminal under construction, so `position_quality=facility_site`

## Data QA flag (not changed by us, OSM side)
- Same changeset tags way/1471454224 near the port as `landuse=quarry name="Baimskaya copper and gold mine"`; the Baimskaya (Peschanka) deposit is ~400 km inland by road, so that label looks wrong. Worth a polite OSM note by a local mapper; ATL does not ingest it.

## Builder
- `atlas-proj/build_atlas.py` ATL_SCHEMATIC_POSITION + ARC-PORT-099 (schematic tags now 14)
- ports.csv: every copy (16) lat/lon + sources note appended (inside the quoted sources field), confidence=90, last_verified=2026-10-13
- Patch `atlas-proj/_patch_port099_1424.py`; lock check `atlas-proj/check_port099_nagleynyn.py`
  (prior PORT-136/105/046/041/045/110/078 locks still OK)

## Live
- Atlas gen `2026-10-13T11:30:10.794285+00:00`, **1317** features (unchanged); diff vs previous build: **ARC-PORT-099 geometry/props only** (wgs84 + 3996)
- 10 alias dirs synced (bad=0) + 7 extra served copies (18 verified md5, 0 stale)
- Live https://arctictradelanes.com/atlas/atlas.wgs84.geojson, /atlas.wgs84.geojson, /data/atlas.wgs84.geojson, /atlas/atlas.3996.geojson verified
- No SPA redeploy / App.tsx / DNS change

## Help wanted
When the 275 m berth is visible on fresh imagery or the port's own docs publish berth coordinates, a PR moving this pin from the port-area centroid onto the berth (with the source cited) would make it a surveyed berth.

## Next candidates (soft 2-decimal ports left: 036, 075)
- ARC-PORT-036 Tiksi East Port (71.68/128.95; need a source that "East Port" is a distinct site from ARC-PORT-006 Tiksi Sea Port)
- ARC-PORT-075 Nuuk Qeqertat quay (64.17/-51.71; already ~0.3 km from OSM way/627906959 industrial=port at the Qeqertat container port; need the new quay site at Qeqertaq Avalleq from a public source)
