# Port ↔ city centroid densify (2026-09-08)

## Bug

Many canonical Arctic ports were pinned on the **exact city centroid** (0 m offset). On EPSG:3996 the harbour and town markers stack, so users bounce when they cannot tell quay from downtown.

## Fix (Zo control plane → live atlas)

Densified nine high-traffic ports onto verifiable OSM harbour / pier / industrial-port nodes (Nominatim). Distances are haversine from linked `city_id`.

| ID | Name | OSM target | ~Δ city |
|---|---|---|---|
| `ARC-PORT-012` | Reykjavik Port | Skarfabakki ferry terminal, Sundahöfn | ~3.8 km |
| `ARC-PORT-014` | Tromsø Port | Tromsø indre havn | ~411 m |
| `ARC-PORT-015` | Kirkenes Port | Kirkenes kai (Kaiveien) | ~1.0 km |
| `ARC-PORT-016` | Hammerfest LNG | Melkøya island (Equinor) | ~4.0 km |
| `ARC-PORT-017` | Longyearbyen Port | Longyearbyen Main Pier (Bykaia) | ~889 m |
| `ARC-PORT-018` | Bodø Port | Nertorget havn | ~1.2 km |
| `ARC-PORT-019` | Narvik Port | Narvik Havn waterfront | ~1.0 km |
| `ARC-PORT-028` | Oulu Port | Oulun satama (Nuottasaari) | ~3.3 km |
| `ARC-PORT-029` | Luleå Port | Södra hamn | ~489 m |

Live apex+www+Zo atlas generated `2026-09-08T12:18:30Z`, features **1321**, ports **156**. Projection stamp EPSG:4326 unchanged; www CNAME to Zo left grey-cloud.

## CI

```bash
node scripts/check-port-city-centroid-densify.mjs path/to/atlas.4326.geojson
node scripts/check-port-city-centroid-densify.mjs --csv path/to/ports.csv
```

## UM

`filterPeoplePins` / `filterEventPins` smoke OK (null-island + OOB + duplicate quarantine); no SPA redeploy this cycle.

## Notes

Do **not** mass-offset entrepreneur program HQ stacks. Remaining ~57 port↔city exact clones are fair game for later cycles when Nominatim/OSM pier nodes are verifiable.
