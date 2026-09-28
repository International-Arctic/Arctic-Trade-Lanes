# ARC-SHIP-024 Ulstein Verft densify (`gis-densify-1020`)

## Change
| Field | Before (soft) | After |
|-------|---------------|-------|
| lat/lon | `62.3400 / 6.1400` | `62.3408333 / 5.8219444` |
| location | Ulsteinvik | Ulsteinvik (Osnesvegen 110), Møre og Romsdal |
| confidence | _(empty)_ | 92 |

Soft→new ≈ **16.4 km** (soft longitude was far east of Ulsteinvik harbour).

## Sources (verifiable)
- Wikidata [Q2477530](https://www.wikidata.org/wiki/Q2477530) Ulstein Verft **P625** `62.340833333/5.821944444` (P31 shipyard)
- Official [ulstein.com/contact](https://ulstein.com/contact): Osnesvegen 110, 6065 Ulsteinvik
- OSM [node/3125244133](https://www.openstreetmap.org/node/3125244133) place=house Osnesvegen 110 `62.3408460/5.8224144` (~0.03 km from WD)
- OSM [node/14014259145](https://www.openstreetmap.org/node/14014259145) defibrillator at Ulstein Verft reception `62.3408039/5.8225373`
- OSM [way/391644151](https://www.openstreetmap.org/way/391644151) Ulstein Verft Parkering operator=Ulstein Verft `62.3413284/5.8243482`

## DISTINCT siblings
- ARC-SHIP-072 Green Yard Kleven `62.3442/5.8471` ~**1.35 km**
- ARC-SHIP-026 Kleven Verft `62.32329874/5.84101439` ~**2.18 km**

## Commits / live
- Dataset: International-Arctic/ArcticTradeLanes-Dataset `2a934a7` (`gis-densify-1020`)
- Zo atlas gen `2026-09-28T07:24:14Z` — 1321 features / 70 shipyards / 156 ports / 103 cities EPSG:3996
- Live: https://arctictradelanes.com/atlas.manifest.json (static atlas sync; no SPA redeploy)

## Community ask
Softish shipyards still needing OSM/WD facility geometry: Vigor-021, VT Halter-022, Eastern-023, Greenland-027, Northern Marine-029, Sembcorp-033, Hyundai-034, Wuchang-039, Kolskaya-052, Zhatay-076, Zvezda-002. Soft ports: Nuupiluk-127, Indiga-128, Ura Guba-148 (see Issue #48).
