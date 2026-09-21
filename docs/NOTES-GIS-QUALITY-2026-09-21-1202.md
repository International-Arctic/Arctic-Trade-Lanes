# GIS Quality Loop — 2026-09-21 ~12:02 MSK

## Win (ATL)
- Densified **ARC-SHIP-013** Damen Shipyard Galati off soft pin `45.4300,28.0500` onto Wikidata **Q4686063** Damen Shipyards Galați P625 `45.44375,28.085805555555556`.
- Cross-check OSM way/888306100 Șantierul Naval Damen Galați landuse=industrial industrial=factory Overpass center `45.4441528/28.0897162` Nominatim `45.4441736/28.0919041` (~2.8 km ENE of soft city pin onto yard). No P402; no OSM `industrial=shipyard` tag (WD place densify).

## Atlas
- Rebuilt via `ArcticTradeLanes.com/atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`; synced Dataset + public/dist/www + arctic-trade-lanes service static paths (no SPA redeploy / App.tsx).
- `generated` `2026-09-21T09:07:58Z`, 1321 features / 70 shipyards / 156 ports. CRS primary EPSG:3996.
- Live verified: https://arctictradelanes.com/atlas.geojson SHIP-013 `[28.085806, 45.44375]`.

## UM
- `filterPeoplePins` / `filterEventPins` smoke: accepted 5 dropped 6. No SPA redeploy / i18n untouched.

## Quarantine unchanged
- PORT-034/069, SHIP-069, Ulstein #37, Zvezda, Wrangell.
- Softish shipyards (no-sources) 24→23.
- Remaining soft preferred queue: Ulstein ARC-SHIP-024 leave #37 unless OSM industrial=shipyard found.
- CI: `check-ship013-damen-galati-densify.mjs`.
