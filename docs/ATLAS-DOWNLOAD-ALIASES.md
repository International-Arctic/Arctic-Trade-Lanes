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
- https://arctictradelanes.com/data/atlas.geojson (= 4326/wgs84 bytes; restored 2026-09-08 GIS loop — was SPA HTML)
- https://arctictradelanes.com/atlas.geojson (= same)

`atlas.4326.geojson` is a **byte alias** of `atlas.wgs84.geojson` so EPSG:4326 crawlers and `llms.txt` links resolve without SPA HTML fallback.

## Maintainer note

When regenerating the atlas on Zo (`ArcticTradeLanes.com/arctic-trade-lanes`), copy into both `public/` and `dist/` **and** the `data/` subfolders, or crawlers will get `index.html` again.

## CRS metadata (2026-09-07 QA)

`atlas.4326.geojson` / `atlas.wgs84.geojson` carry **lon/lat degrees** and must declare:

```json
"crs": {"type": "name", "properties": {"name": "EPSG:4326"}},
"projection": {"epsg": 4326, "name": "WGS 84", "note": "RFC 7946 lon/lat degrees; companion to EPSG:3996 polar stereographic atlas"}
```

`atlas.3996.geojson` keeps EPSG:3996 (metres E/N) with the IBCAO polar stereographic stamp.

**Regression caught in GIS Quality Loop:** the WGS84/4326 files previously kept the EPSG:3996 `projection` object after inverse-projecting coordinates. Clients that trust `projection.epsg` would mis-read lon/lat as polar metres. Fixed in Zo `atlas-proj/build_atlas.py` (stamp 4326 after inverse) and live public/dist aliases.

### Maintainer checklist after rebuild

1. Run `python3 build_atlas.py` in `ArcticTradeLanes.com/atlas-proj`.
2. Copy `atlas.3996.geojson`, `atlas.wgs84.geojson`, `atlas.4326.geojson`, `atlas.geojson` (4326 alias), `atlas.manifest.json` into both `arctic-trade-lanes/public/` and `dist/` (and `data/` subfolders).
3. Spot-check: `jq '.projection.epsg' public/atlas.4326.geojson` → `4326`; same for `3996` → `3996`.
