# UnicornsMap countryIso2 on live geojson — 2026-10-12 (gis-umcountry-0922)

## Before
Live `https://unicornsmap.com/api/radar/geojson.json` still emitted raw `country` only (92 distinct strings; 0 `countryIso2`). Client package `@international-arctic/geo-filter` 0.1.7 already had `normalizePinCountries`, but the worker did not.

## After (worker deploy, code-only, no SPA assets)
`radarGeojson()` now adds additive `countryIso2` + `country_quality` on every Point (primary + site). Raw `country` unchanged.

Live check 2026-10-12 ~09:32 MSK: **833/833** Points resolved — quality mix `iso_or_name` 713, `city_gazetteer` 94, `us_state_tail` 16, `multi_city_first` 10. Worker version `edfcedc9-86e4-44da-9cce-1d5cb82b0bf7`.

Related: Issue #58, `docs/UM-COUNTRY-NORMALIZE-2026-10-05.md`, `packages/geo-filter` 0.1.7.
