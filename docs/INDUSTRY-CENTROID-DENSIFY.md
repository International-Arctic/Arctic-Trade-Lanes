# Industry centroid densify (2026-09-08)

Map UX: stacked `industry` pins on shared town centroids looked like duplicate facilities and bounced GIS users. This cycle densifies verifiable sites off the worst stacks.

## Changes (live atlas generated `2026-09-08T06:13:21Z`)

| id | was | now | rationale / sources |
|----|-----|-----|---------------------|
| `ARC-FAC-366` Narvik Green Ammonia | Narvik port `68.4386, 17.4279` | Bjerkvik `68.5492, 17.5571` | Statkraft + High North News: plant locality Bjerkvik / Lailasletta–Kvandal, not Narvik Havn; OSM Bjerkvik |
| `ARC-FAC-309` Arctic World Archive | Longyearbyen `78.2232, 15.6267` | Gruve 3 `78.2384, 15.4446` | Wikipedia/Wikidata + OSM `Gruve 3` |
| `ARC-FAC-367` Hotellneset diesel plant | near-town `78.2172, 15.6397` | Hotellneset `78.2486, 15.4880` | OSM Hotellneset; Sysselmesteren KU for Hotellneset plant |
| `ARC-FAC-305` Svalbard Energi utility | Longyearbyen centroid | `78.2465, 15.4920` | ops near Hotellneset plant (distinct from 367) |
| `ARC-FAC-311` Global Music Vault | Longyearbyen centroid | `78.2370, 15.4500` | Gruve 3 / Platåberget vault cluster (near AWA) |
| `ARC-FAC-310` Where2O / Tilsig office | Longyearbyen centroid | `78.2238, 15.6350` | town innovation-office offset |
| `ARC-FAC-318` Svalbard fibre landing | Longyearbyen centroid | `78.2275, 15.6080` | harbour / coastal terminal approach |
| `ARC-FAC-312` Kystutviklingssenteret | Kirkenes centroid | `69.7275, 30.0520` | Thon Senter / Storgata area |
| `ARC-FAC-313` beredskapshub | Kirkenes centroid | `69.7300, 30.0410` | civic/admin north offset |
| `ARC-FAC-360` Energy Cluster | Kirkenes centroid | `69.7270, 30.0505` | co-located with Kystutviklingssenteret, slight offset |
| `ARC-FAC-361` Maritime Industrial Cluster | Kirkenes centroid | `69.7225, 30.0565` | toward KILA logistics area |
| `ARC-FAC-306` Sitnasuak | Nome shared pin | `64.4998, -165.4035` | Front St pier / fuel terminal offset |
| `ARC-FAC-400` Emerald Nuclear Nome study | Nome shared pin | `64.5040, -165.4120` | harbour-approach study pin |

Dataset: `International-Arctic/ArcticTradeLanes-Dataset` `arctic_industrial_facilities.csv`. Builder: Zo `ArcticTradeLanes.com/atlas-proj/build_atlas.py`. Live aliases: `/atlas.4326.geojson` + `/data/atlas.4326.geojson` (apex + www).

## CI

```bash
node scripts/check-industry-centroid-densify.mjs atlas.4326.geojson
```

Neutral sourcing only — institutional OSM / Wikipedia / Statkraft / municipal pages. No editorial slant in labels.
