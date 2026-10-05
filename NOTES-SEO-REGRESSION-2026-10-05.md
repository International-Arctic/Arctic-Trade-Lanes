# Homepage SEO regression fix — 2026-10-05

**Zo tip:** `c96d85f` (`seo-home-regression: fix ld+json ItemList orphan, nav once, SSR h1`)
**Live:** https://arctictradelanes.com (svc_UpoHDo9rDHs)
**Parent tip:** a5a1e23 (Arctic agenda strip)

## Bugs fixed (additive only)

1. **JSON-LD** — `seoMiddleware` ItemList regex stopped at the first `ListItem` `},` and left pretty-printed ListItems 2–10 as orphans → `JSON.parse` Extra data. Now replaces via `JSON.parse` of the ld+json block and `@graph` ItemList swap. Verified `/`, `/ru`, `/zh`: Organization, WebSite, Product, Dataset, NewsArticle, ItemList (numberOfItems=10). Organization.logo + NewsArticle.image intact.
2. **Nav** — Home header keeps `/funding` + `/advertise` once each (i18n `agenda.navFunding` / `navAdvertise`, all 22 locales). Removed duplicate pair from bottom control bar. SSR injects the same two links once inside `#root` (`data-atl-funding-link` / `data-atl-advertise-link`). Agenda noscript still has 2 caption links to `/funding` (not nav chrome).
3. **H1** — SSR injects real `<h1 data-atl-ssr-h1>` with brand + keyword for every home locale. Client H1 keeps brand look; keyword span stays in DOM (`max-sm:sr-only` instead of `hidden`).

## Untouched
map · 6 home ad slots · agenda assets · ads-config · server.ts x402 · Arctic-panel SSR carve-out · no sanctions wording

## Verify (2026-10-05 ~23:20 MSK)
- JSON.parse OK on /, /ru, /zh
- EN H1: `ArcticTradeLanes — Northern Sea Route GIS OSINT`
- RU H1: `ArcticTradeLanes — СМП · GIS OSINT`
- ZH H1: `ArcticTradeLanes — 北方海航道 GIS OSINT`
