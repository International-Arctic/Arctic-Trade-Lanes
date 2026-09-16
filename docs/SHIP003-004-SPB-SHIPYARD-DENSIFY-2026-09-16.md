# GIS densify — ARC-SHIP-003 Severnaya Verf + ARC-SHIP-004 Admiralty (2026-09-16 ~10:11 MSK)

Politically neutral OSINT only. Verifiable OSM industrial geometries; no invented offsets.

| ID | Name | Old soft-pin (WGS84) | New (WGS84) | OSM | Wikidata |
|----|------|---------------------|-------------|-----|----------|
| ARC-SHIP-003 | Severnaya Verf | 59.9420, 30.2600 | 59.8751941, 30.2331947 | [relation/1411836](https://www.openstreetmap.org/relation/1411836) Northern Shipyard `landuse=industrial` | [Q839974](https://www.wikidata.org/wiki/Q839974) |
| ARC-SHIP-004 | Admiralty Shipyards | 59.9360, 30.2750 | 59.9290278, 30.2796371 | [relation/1201710](https://www.openstreetmap.org/relation/1201710) Admiralty Shipyards `landuse=industrial` (Nominatim relation centroid) | [Q2292711](https://www.wikidata.org/wiki/Q2292711) |

## Skipped this cycle
- ARC-SHIP-069 Sevgiprorybflot — still Murmansk city centroid; no named OSM facility (help wanted #34).
- ARC-PORT-034 / 069 / 153 — still no pier/LNG OSM (help wanted #32).
- ARC-SHIP-006 Sredne-Nevsky — soft pin near Severnaya; densify separately when OSM shipyard geometry is confirmed (do not conflate with relation/1411836).

## Atlas
- Rebuild: `python3 atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`
- Live static sync only (no App.tsx / SPA redeploy).
- CI: `scripts/check-ship003-severnaya-verft-densify.mjs`, `scripts/check-ship004-admiralty-shipyards-densify.mjs`
