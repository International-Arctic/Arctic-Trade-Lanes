# Maritime pins far inland (gis-portbay-1245, 2026-10-05)

## What was wrong
ARC-PORT-169, the planned VLT KORF transshipment hub in Korf Bay (Olyutorsky District, Kamchatka), was pinned at `60.2500, 163.0500`. That point is about 47 km inland (great-circle to the Natural Earth 10m coastline) and roughly 150 km west of Korf Bay. Users clicking around the NSR's Pacific end saw a "port" in the middle of the Koryak uplands.

## Fix
The terminal site plan is not public yet, so the pin now sits at the bay itself: `60.0333, 165.7333` from [Wikidata Q1108019](https://www.wikidata.org/wiki/Q1108019) (P625), cross-checked against the OSM `natural=bay` [node/1947664519](https://www.openstreetmap.org/node/1947664519) and the Korf / Tilichiki settlements ([way/690136906](https://www.openstreetmap.org/way/690136906), [way/690137323](https://www.openstreetmap.org/way/690137323)). The precision is bay-level on purpose and the dataset row says so. Exactly one atlas feature changed; the live atlas on arctictradelanes.com was re-synced without an SPA redeploy.

## Guard
`scripts/check_port_inland.py [atlas.wgs84.geojson] [ne_10m_land.geojson] [--km 5]`

- Fails only for pins in its `LOCKED` table (currently ARC-PORT-169 must stay on the water side).
- Reports every port or shipyard more than `--km` from the NE10m coastline. Natural Earth has no rivers or lakes in its land mask, so river ports (Dudinka, Salekhard, Khatanga), lake yards (Onega) and company HQ rows (Novatek Severny Inzhiniring in Moscow) are expected in the report. It is a review list, not a bulk-move list.

## Still worth a look (soft coordinates, 6–9 km inland)
| id | name | pin | why it looks soft |
|---|---|---|---|
| ARC-PORT-035 | Kola Bay Fuel Terminal | 69.0, 33.25 | round numbers, east of Murmansk on land |
| ARC-PORT-164 | Murmansk coal terminal "Lavna" | 69.0, 32.79 | round numbers; compare with densified ARC-PORT-031 Lavna |
| ARC-PORT-147 | Naiba (Nayba) deep-water port | 71.9, 128.5 | planned project, settlement-level guess |
| ARC-PORT-050 | Novaya Zemlya Ports | 73.5, 55.0 | archipelago centroid for several harbours |

Proposed fixes need a public, checkable source (OSM object, Wikidata P625, an operator or government map). If a row is really several harbours, say so and suggest splitting it rather than picking one.
