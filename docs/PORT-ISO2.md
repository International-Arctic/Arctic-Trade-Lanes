# Port / layer `iso2` stamps (ATL atlas)

**Shipped 2026-09-07** on live ArcticTradeLanes atlas (`atlas.{3996,4326,wgs84}` + `/data/` aliases).

## Why

Atlas features carried free-text `country` but no ISO 3166-1 alpha-2, so clients could not cheaply join `arctic_reference` or filter by country code. Ports also had placeholder `unlocode` values (`NULL`, short codes like `CHV`) that must not be trusted as country letters.

## Builder rule (`build_atlas.py` → `_iso2`)

1. If `unlocode` looks like a real UN/LOCODE (≥5 chars, alpha country prefix) → use first two letters.
2. Else map normalized `country` via `COUNTRY_TO_ISO2` (incl. `USA`→`US`, `Danish`→`DK`, `Svalbard`/`Norway (Svalbard)`→`SJ`, dual `Finland / Sweden`→ first token).
3. Reject placeholders: `NULL`, `NONE`, `N/A`, `-`, `TODO`.

Stamped on: **ports, cities, shipyards, programs, airports, industry, rail, rescue, tankers, icebreakers**.

## Verify

```bash
# against a downloaded atlas.4326.geojson
node scripts/check-port-iso2.mjs path/to/atlas.4326.geojson
```

Expect: every port has non-empty `iso2`; no `NU` from `NULL` unlocodes; counts roughly match country mix (RU/US/NO/…).

## Help wanted

See Issue #3 — still open for UN/LOCODE completeness on planned/greenfield ports and registry cross-checks (IMO/MMSI on vessels).
Pan-Nordic / EU multi-country program rows may intentionally omit `iso2` (no single code). Core layers (ports, cities, tankers, icebreakers) must always stamp.
