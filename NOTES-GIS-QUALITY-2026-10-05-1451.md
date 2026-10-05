# GIS Quality Loop — gis-latfix-1451 (2026-10-05 ~14:51 MSK)

## Win
Moved 3 pins that were sitting on open water (Natural Earth 10m land mask):

| ID | Name | Before | After | Source | Shift |
|---|---|---|---|---|---|
| ARC-PORT-102 | Qikiqtarjuaq Deep Sea Port | 67.8569 / -64.0306 (~33 km N of hamlet, Davis Strait) | 67.5581 / -64.0247 | Wikidata Q1370641 | 33 km |
| ARC-PORT-047 | Nordvik Port (historic) | 74.5000 / 111.5000 (~56 km N of settlement, Khatanga Gulf) | 73.9980 / 111.4693 | OSM node/3290343023 + Wikidata Q2364258 | 56 km |
| ARC-CITY-049 | Yamburg | 67.9240 / 74.4980 (~15 km W in Ob Bay) | 67.9250 / 74.9241 | OSM way/136398746 (settlement) | 15 km |

## Audit notes (not fixed this cycle)
- Franz Josef / Novaya Zemlya coarse ports (ARC-PORT-049/050) remain archipelago-level placeholders.
- Chukotka ports with W longitude (Provideniya, Egvekinot, Wrangel) are correct (past 180°E).
- Mys Shmidta -179.4 vs 179.4 E is ~50 km across the antimeridian — deferred (needs Wikidata confirm).
- Prior routine ~14:16 MSK: no crash log found on Zo; likely parent timeout / aborted mid-audit. Working-tree cities.csv already had additive source columns (kept).

## Live
- atlas gen **2026-10-05T11:56:41Z**, aliases synced (10 dirs), no SPA redeploy.
