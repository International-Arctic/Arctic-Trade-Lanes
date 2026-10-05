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

Proposed fixes need a public, checkable source (OSM object, Wikidata P625, an operator or government map). If a row is really several harbours, say so and suggest splitting it rather than picking one.

## Fixed since
- **ARC-PORT-147 Naiba (Nayba) planned deep-water port** (gis-naiba-1524, 2026-10-05): the pin at `71.9, 128.5` was near Tiksi, about 142 km from Naiba. The terminal is planned in Kharaulakh Bay near Naiba village, about 112 km from Tiksi ([morvesti.ru](https://morvesti.ru/news/1679/118608/)). It now sits on the village at `70.8496, 130.7551` from [Wikidata Q4312374](https://www.wikidata.org/wiki/Q4312374) (P625), cross-checked against OSM [way/1308280327](https://www.openstreetmap.org/way/1308280327). Settlement-level precision until a site plan is published. Guard: `scripts/check_port147_naiba.py` (3 km from the Wikidata anchor). Natural Earth 10m generalises the Kharaulakh Bay shore, so `check_port_inland.py` reads the village as ~5 km inland; it is locked at 8 km there.
- **ARC-PORT-050 Novaya Zemlya Ports** (gis-nzport-1555, 2026-10-05): the pin at `73.5, 55.0` was on the Severny Island ice cap, about 235 km from any harbour. It now sits on Belushya Guba, the archipelago's main port settlement, at `71.54075, 52.336411` from [Wikidata Q26324](https://www.wikidata.org/wiki/Q26324) (P625), cross-checked against OSM [way/583357819](https://www.openstreetmap.org/way/583357819). Settlement-level precision; if the row really covers several harbours, splitting it is welcome. Guard: `scripts/check_port050_nzport.py`.
- **ARC-PORT-164 Murmansk coal terminal "Lavna"** (gis-nzport-1555, 2026-10-05): this row is the same terminal as the densified ARC-PORT-031 (OSM [way/1300372902](https://www.openstreetmap.org/way/1300372902)). Its coordinates and UN/LOCODE `RULAV` now match ARC-PORT-031, so the build's soft dedupe drops it as an alias pin (manifest `port_alias_drops`, reason `duplicate_unlocode_coord`). The CSV row and its sources stay for provenance.

Still open: ARC-PORT-035 Kola Bay Fuel Terminal (`69.0, 33.25`, ~8.7 km inland east of Murmansk). We have not found a checkable fuel-terminal object yet; Kola Bay itself (Wikidata Q161591) is bay-level only. A source-backed proposal is welcome on issue #55.
