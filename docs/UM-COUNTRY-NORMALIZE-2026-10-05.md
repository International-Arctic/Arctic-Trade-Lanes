# UnicornsMap country field normalisation — 2026-10-05 (gis-umcountry-1724)

## Finding (live `https://unicornsmap.com/api/radar/geojson.json`, fetched 2026-10-05 14:26 UTC)

- 828 features (600 primary, 227 site, 1 corridor LineString).
- `radarGeojson()` sets `country` = last comma part of `city`, `locality` = first part. Result:
  - 198 of 600 primaries have `country === locality` (Seoul 67, Singapore 39 + 32, Hong Kong 18 + 11, Dubai 7, ...).
  - US state codes as countries: `NY` 5, `CA` 3 (California, collides with ISO `CA` = Canada), `FL`, `NC / San Francisco`, `TX / Hawthorne CA`.
  - Free-text notes as countries: `USA — Hugging Face HQ (individual location not publicly verified)` 27, `UAE / Frankfurt EU corridor` 4, `Curaçao (reported license domicile)`, ...
  - Mixed spellings: `USA` / `United States` / `US`, `UK` / `United Kingdom`, `UAE` / `United Arab Emirates` / `AE`, `South Korea` / `Seoul`.
  - 92 distinct raw strings for 49 real countries.

## Shipped (client-side, additive)

`packages/geo-filter` 0.1.7 adds `normalizePinCountries()` / `resolveCountry()` (`./country` export):
every pin gains `countryIso2` + `country_quality`; raw `country` untouched. Live: 827/827 Point
features resolve (707 name/ISO, 94 city tail, 16 US state, 10 multi-seat first seat).

Fixtures + live audit: `bun scripts/check-um-geo-quality.mjs --live`.

## Source-side data fixes found by a coordinate-vs-country scan (not applied here)

- `ethereum-foundation` site `Zug` is labelled country `USA`, but the point (8.5155, 47.1662) is Zug, Switzerland, so it should read `CH` / Switzerland.
- `regolith` primary city `Wyoming, USA (public HQ) · Dubai, UAE` got worker country `UAE` while the point (-107.32, 42.56) is Wyoming; the normaliser resolves it to `US` from the first seat, but the worker should do the same.

## Suggested worker follow-up (additive, one field)

In `radarGeojson()` emit `countryIso2` using the same rules (or call the shared table), keep `country`
for backward compatibility. That removes the client-side pass and makes country filters/legends work in
every consumer (Leaflet / MapLibre / GIS agents) without new server GIS.
