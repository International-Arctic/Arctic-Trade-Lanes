# Offshore land-pin audit and longitude sign-flip check (2026-10-05)

Cities, programs, industry sites, airports, rail and rescue centres should sit on land.
A land-layer pin that floats tens of kilometres out at sea is almost always a data-entry
error, and near the antimeridian the most common one is a negated longitude
(-177.5 instead of +177.5).

## What was fixed (gis-lonflip-1352)

| id | was | now | why |
|---|---|---|---|
| ARC-PORT-166 Unified Northern-Supply Sea Route (Anadyr gateway) | 64.732, -177.508 | 64.7333, 177.5042 | sign flip; Anadyr is Wikidata Q7978 |
| ARC-FAC-392 Nutekin Placer Gold (pin at Anadyr admin centre) | 64.7320, -177.5050 | 64.7333, 177.5042 | sign flip; row says "pin at Anadyr" |
| ARC-PROG-699 TOR "Chukotka" resident-pool row (pin Anadyr) | 64.7320, -177.6500 | 64.7333, 177.5042 | sign flip; row says "pin Anadyr" |
| ARC-PROG-716 GK "V komforte", Bilibino | 64.0019, -162.0090 | 68.0500, 166.4500 | was in Norton Sound, Alaska; Bilibino is Wikidata Q105116 |
| ARC-PROG-603 CanNor Canadian Innovation Week award | 64.5000, -13.5000 | 63.7494, -68.5217 | was east of Iceland; row city is Iqaluit, Wikidata Q2030 |

All five are admin-seat precision (town level), not site plans. The atlas build then
applies its usual display-only co-site nudge, so the three Anadyr rows do not stack.

Live atlas generation `2026-10-05T10:55:51Z`, 1321 features, only these 5 geometries changed.

## Running the check

```bash
python3 scripts/check_offshore_land_pins.py atlas.wgs84.geojson --km 10
```

It lists every land-layer pin more than 10 km offshore (ports and shipyards get 3 km of
extra slack), marks rows within 10 degrees of 0 or 180 whose mirrored longitude lands on the coast as sign-flip
suspects, and exits 1 if a fixed pin regresses. Rows that are offshore on purpose
(drift-ice base, offshore wind, schematic route layers) are listed in `EXPECTED_OFFSHORE`.

## Client-side rule (for viewers that load third-party rows)

Cheap to run in the browser with any land mask already used for the basemap:
if a land-layer point is more than ~10 km at sea and `(-lon, lat)` is on land, do not
silently flip it. Draw it with a "position suspect" style and keep the raw value in the
popup, so the data owner can confirm. Flipping automatically would hide genuine
far-east/far-west rows.

## Still open for review

The remaining >10 km offshore rows are mostly programs fanned around coastal admin seats
(Svalbard, Reykjavik, Helsinki) and a few schematic port rows (Franz Josef Land, Nordvik,
Qikiqtarjuaq, Maniitsoq). See the community issue for the list.

Proof on the two atlas generations: the pre-fix atlas (`2026-10-05T09:49:53Z`) gives 5 FAIL
lines and exactly 3 sign-flip suspects (the three Anadyr rows); the live atlas
(`2026-10-05T10:55:51Z`) gives 0 FAIL and 0 suspects.
