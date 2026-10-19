# ATL v2 additive layer (2026-10-18)

Deployed on Zo (commit ff1592f31). Mirrors the app paths:

* `src/home/v2/atlV2.ts`: renderer for the hero band, flag strip, logo wall and sprint story (injected into the home-extras block
  **below** the SPA map), `/[lc/]country/<iso2>`, `/[lc/]companies`, `/[lc/]company/<slug>`, `/sitemaps/atl-v2-<lc>.xml`,
  `/sitemap-index.xml`, `/atl-hero/*` and the `/advertise` campaigns section. Verification meta comes from `config/atl-site-verification.json`.
* `src/home/v2/v2Routes.ts`: `GET /api/atl-fx`, ECB daily reference rates plus Bank of Russia (RUB, AED), dated and cached for 6 h.
* `src/home/v2/v2.i18n.json`: 106 keys × 22 locales (sources in `i18n-src/`). `hubs.json` is built by `build_hubs.py` from the atlas.
* `public/atl-hero/`: 4 WebP images under 60 KB each, plus `credits.json` (Wikimedia Commons: PD, PD, CC BY-SA 3.0, CC0).
* `patch_server_v2.py`: idempotent additive patch for `server.ts` (marker `ATL-V2-HOOK`).
* Registry data: `data/arctic-brands/` (see its README). `build_brands.py` rebuilds it from Wikidata snapshots.

Kill switch: `ATL_V2=0`. Rollback: restore `server.ts.bak-20261018-v2` and restart.
