# Atlas download aliases (live)

ArcticTradeLanes.com serves the GIS OSINT atlas as static GeoJSON (edge-cheap). Schema.org / crawler discovery previously pointed at broken `/data/*` paths and a missing `atlas.4326.geojson` name.

## Canonical live URLs (2026-09-07)

| CRS | URL |
|-----|-----|
| EPSG:3996 | https://arctictradelanes.com/atlas.3996.geojson |
| EPSG:4326 / WGS84 | https://arctictradelanes.com/atlas.4326.geojson |
| WGS84 (legacy name) | https://arctictradelanes.com/atlas.wgs84.geojson |
| Manifest | https://arctictradelanes.com/atlas.manifest.json |

## Discovery aliases (same bytes)

- https://arctictradelanes.com/data/atlas.3996.geojson
- https://arctictradelanes.com/data/atlas.4326.geojson
- https://arctictradelanes.com/data/atlas.wgs84.geojson
- https://arctictradelanes.com/data/atlas.manifest.json

`atlas.4326.geojson` is a **byte alias** of `atlas.wgs84.geojson` so EPSG:4326 crawlers and `llms.txt` links resolve without SPA HTML fallback.

## Maintainer note

When regenerating the atlas on Zo (`ArcticTradeLanes.com/arctic-trade-lanes`), copy into both `public/` and `dist/` **and** the `data/` subfolders, or crawlers will get `index.html` again.
