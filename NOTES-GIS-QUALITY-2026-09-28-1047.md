# GIS Quality Loop — 2026-09-28 ~10:47 MSK (gis-densify-1047)

## Outcome
- **Densified ARC-SHIP-015 Naval Group (Arctic Capabilities)** off soft `49.6400,-1.6200` onto OSM **way/984780193** Naval Group landuse=industrial Overpass center `49.6496403/-1.6342186`.
- Official address corroboration: annuaire-entreprises.data.gouv.fr établissement 44113380800028 **PL BRUAT 50100 CHERBOURG-EN-COTENTIN**; nae.fr Place Bruat.
- Adjacent Arsenal: Wikidata **Q3398673** Cherbourg Naval Base P625 `49.6525/-1.63416667` (~0.32 km) + OSM way/984780191 Port militaire - Arsenal de Cherbourg.
- Nominatim way/984780193 `49.6496403/-1.6345390` (~0.02 km of Overpass center).
- Soft→new ≈ **1.48 km**. Naval Group corporate Q1227511 HQ P159 is Paris — not used.
- Sibling DISTINCT: no other ARC-SHIP within 50 km of new pin.
- Tag `gis-densify-1047` (~10:47 MSK).

## Atlas
- Rebuilt via `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset --out atlas-proj`.
- `generated` **2026-09-28T08:00:14Z**, **1321** features / **70** shipyards / **156** ports / **103** cities. CRS primary EPSG:3996.
- Live: https://arctictradelanes.com/atlas/atlas.manifest.json

## Remaining soft preferred
- Ports: 127 Nuupiluk; 128 Indiga; 148 Ura Guba; 166 EMO (skip)
- Softish shipyards: 021–023, 027, 029, 033–034, 039, 052, 076, Zvezda-002
