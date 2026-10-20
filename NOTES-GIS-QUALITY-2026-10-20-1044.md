# GIS Quality Loop gis-loop-1020-1044 (~10:44 MSK, 2026-10-20)

## ARC-PORT-139 Tromsø Havn (NOTRO): pinned to the Breivika cargo port (owner decision 2026-10-20)
- Old pin 69.6546 / 18.9590 (4 decimals) sat on land in Tromsø city: it reverse-geocodes to St. Hanshaugen 5, Nordbyen.
- Tromsø Havn lists Breivika as its main cargo port area (tromso.havn.no/tjenester/kaiplass, /en/services/quays): Kai 20, Kai 21-24 (410 m, 10.4-11.0 m), Kai 24 nord, Kai 25 (11.5 m), Kai 28, Kai 38 nord, Ro-Ro ramp. The record names no single quay or terminal, so the pin goes to the port-level harbour point.
- New pin **69.6757237 / 18.989445** = OSM node/5355453054 `harbour=yes`, `seamark:type=harbour`, `seamark:name=Tromsø`, `source=Kystverket` (Norwegian Coastal Administration import). It lies in the harbour water off the straight ~450 m Breivika quay front (OSM coastline way/301393812, matching Kai 21-24). The move is about 2.63 km NNE (bearing ~27°).
- `position_quality=facility_site` (a harbour reference point, not a surveyed berth line). Confidence stays at 82, `last_verified` is now 2026-10-20, all other attributes unchanged (UN/LOCODE NOTRO).
- Prostneset: no distinct Prostneset record exists, so no feature was added. The inner harbour remains covered by ARC-PORT-014 (Tromso Port, unchanged).

## Atlas regression gate
- Built from the canonical Zo `atlas-proj` with `ref/ne_10m_land.geojson` against the Dataset (a pre-patch rebuild matched live exactly except `generated`).
- 1317 features; IDs, order and top level identical to the 07:31:40Z gen; the only differing feature is ARC-PORT-139 (geometry, position_quality, position_note, position_anchor).
- 25/25 lanes water-routed, land-mask fan 563, ship water fan 101 (display_offset 131 = live).
- Previously fixed ports did not move (including 014, 039, 066, 079, 083, 093, 132, 135, 157).

## Live
- Atlas gen `2026-10-20T07:55:12Z`, 1317 features, EPSG:3996 (md5 3996 e0287d06, 4326 7fc889bc).
