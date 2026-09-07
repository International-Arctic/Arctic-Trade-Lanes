# Program / industry ISO2 stamping (multi-country HQ)

## Problem

Arctic entrepreneur-program and industry pins often carry multi-country `country` strings
(`Nordic (NO/SE/FI)`, `EU cross-border (Aurora…)`, `Cross-Arctic (UArctic…)`) or swapped
CSV cells (`country` = locality, `city` = `Norway`). A naive name map leaves `iso2` empty,
so client joins to `arctic_reference` and country filters fail.

## Resolution order (neutral)

1. UN/LOCODE prefix when present (5+ chars, reject `NULL` placeholders).
2. Exact country-name map (ISO 3166-1 alpha-2).
3. **HQ / secretariat city** (`Helsinki`→`FI`, `Oslo`→`NO`, `Brussels`→`BE`, `Vienna`→`AT`, …).
4. First embedded Arctic/Nordic/Baltic ISO2 token inside the country string (`NO/SE/FI` → `NO` only if no city HQ).
5. Substring / slash fallbacks; swapped city-as-country repair.

No editorial ranking of states beyond HQ locality of the pin.

## Live check (2026-09-07)

After stamping + Helgeland Aqua CSV repair:

- `programs` 714 / missing iso2 **0** (was 20)
- `industry` 110 / missing iso2 **0** (was 1)
- lanes / reference overlays remain without point iso2 (multi-jurisdiction geometries)

## Contributor ask

- Extend `CITY_TO_ISO2` for new secretariat cities.
- Prefer fixing CSV `country`/`city` when cells are swapped.
- Keep labels politically neutral; stamp codes, do not rewrite program names.
