# GIS Quality Loop — gis-1244 (2026-10-12 ~12:44 MSK)

## Win: ARC-FAC-330 Sarfartoq densify (GEUS half-degree → Mindat)

**ARC-FAC-330** Greenland Mines — Sarfartoq Nd-Pr Rare Earth Project sat on GEUS Bulletin 17 (2009) map-centre half-degree pin `66.5000 / -51.2500` (66°30′N 51°15′W). Soft/half-degree audit flagged it as the remaining coarse industry candidate after soft-integer cleared.

Densified onto **Mindat loc-123391** Sarfartoq carbonatite complex `66°29′N 51°19′W` = `66.4833333 / -51.3166667` (**~3.49 km**). GEUS Bulletin 17 fig.1B inner/outer core `66°30′N / 51°15′–51°18′W` corroborates the same complex. OSM node/14164746277 Sarfartoq river `66.4292538 / -51.5082793` (~10.4 km) is same Isortoq/Sarfartoq valley — corroborates location family, **not** used as pin (river, not deposit). No dedicated Wikidata P625 (Q29050345 disambiguation only).

## Sources
- https://www.mindat.org/loc-123391.html
- https://www.geus.dk/media/13687/nr17_p69-72.pdf
- https://www.openstreetmap.org/node/14164746277
- https://greenlandmines.com/projects/sarfartoq-site/
- S-K 1300 Initial Assessment (Tetra Tech/GeoSim, effective 31-Jul-2026) — ST1 in northern part of complex; ~60 km SW of Kangerlussuaq

## Live
- Atlas gen `2026-10-12T09:51:06Z`, **1318** features; industry **109**.
- Geometry change: FAC-330 only (among industry).
- Soft-integer audit still **0**; FAC-330 cleared from half-degree/soft list.
- FAC-354 / FAC-370 remain tagged schematic (do not densify).
- Lock: `scripts/check_fac330_sarfartoq.py`
- CSV backups: `*.bak-gis-fac330-*`
- Builder: `atlas-proj/build_atlas.py --dataset ArcticTradeLanes-Dataset`
