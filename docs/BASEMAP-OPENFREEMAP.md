# Basemap: OpenFreeMap (no Carto)

ArcticTradeLanes.com uses **[OpenFreeMap](https://openfreemap.org)** (Cloudflare-sponsored) for free, no-API-key basemaps.

## Why

- Cashflow first: no Carto / Mapbox / Google basemap API keys.
- Polar primary CRS (`EPSG:3996`) still uses Natural Earth `land110.geojson` underlay (Mercator tiles smear when reprojected).
- Leaflet Mercator view (`ArcticMap`) uses OpenFreeMap **dark** MapLibre style: `https://tiles.openfreemap.org/styles/dark`.
- OpenLayers WGS84 toggle uses OpenFreeMap Natural Earth shaded relief raster: `https://tiles.openfreemap.org/natural_earth/ne2sr/{z}/{x}/{y}.png`.

## Client visual QA (2026-09-07)

Polar map looked like floating pins on a void because `land110` / sea-ice features ship GeoJSON `properties.kind` (`land` / `extent` / `median`) while the style function only read `layer`. Fix: bridge `kind` → `layer` in `PolarStereographicMap` feature styles. Also default-hide the 700+ `programs` pins and drop non-port text labels at overview zoom.

Attribution: © OpenFreeMap © OpenStreetMap contributors.
