# UnicornsMap country normalisation: 4 new unresolved tails (2026-10-20, gis-loop-1020-1817)

## Finding (read-only, about 18:25 MSK)
`bun scripts/check-um-geo-quality.mjs --live` against `https://unicornsmap.com/api/radar/geojson.json`
(860 features, 859 Points) resolved **855/859**. The 2026-10-12 baseline was 833/833. The live worker's own
`countryIso2` is also `null` (`country_quality: unresolved`) on the same 4 primary Points:

| slug | raw city / country | coords (lng, lat) | resolved (0.1.9) |
|---|---|---|---|
| `lic-2026-gstaad` | Gstaad / Gstaad | 7.2831, 46.4774 | CH (city_gazetteer) |
| `cii-fbn-nxg-jaipur-2026` | Jaipur / Jaipur | 75.7912768, 26.9196877 | IN (city_gazetteer) |
| `family-office-retreat-bermuda-2026` | Smith's Parish, Bermuda / Bermuda | -64.7098, 32.3219 | BM (iso_or_name) |
| `lugano-future-of-capital-markets-2026` | Lugano / Lugano | 8.948078, 45.9994838 | CH (city_gazetteer) |

All four coordinates fall inside the country assigned. There are no null-island, NaN or out-of-range coordinates.
`/api/radar/geo.json` still has 632 pins, with 0 bad coordinates and 0 duplicates.

## Change (`@international-arctic/geo-filter` 0.1.8 → 0.1.9)
Additive table keys only, in `packages/geo-filter/src/normalizeCountry.ts`. Raw `country` is never rewritten.
After the change: live audit **859/859** (`iso_or_name` 728, `city_gazetteer` 105, `us_state_tail` 16, `multi_city_first` 10).

## Not done here
The UnicornsMap worker (`radarGeojson()`, see `UM-COUNTRY-NORMALIZE-2026-10-12.md`) still emits
`countryIso2: null` for these 4 pins until its table gets the same four keys. That needs a code-only worker deploy (no SPA assets), so it is
left to the owner.

Related: #53, #58, `docs/UM-COUNTRY-NORMALIZE-2026-10-12.md`.
