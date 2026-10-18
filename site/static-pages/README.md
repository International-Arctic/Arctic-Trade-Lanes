# Static /funding and /advertise pages (restored 2026-10-18)

Owner-approved restore (Aleksei Dolgikh @alexdolbun, 2026-10-18 19:22 MSK). Additive only: the homepage,
x402 routes, API routes, ads-config R-A placeholders, Yandex Autoplacement 20141282 and DNS are untouched.

Both pages were SPA routes until the 2026-10-13 folder wipe destroyed the React source. These files rebuild
them as standalone server-rendered HTML (no JS framework), ported from the Oct 6 bundle
(`assets/index-atlr3-oct6.js`, components `Fk` = funding, `jk` = advertise).

| file | purpose |
|---|---|
| `build_pages.py` | generator (stdlib Python 3). `python3 build_pages.py arctic-funding-programs-2026.csv pages 2026-10-18` |
| `arctic-funding-programs-2026.csv` | copy of `data/arctic-funding-programs-2026.csv` (42 rows, 13207 B, md5 7502781dcd72d3829977aeb934ea9ac3 = live CSV) |
| `pages/funding.html`, `pages/advertise.html` | EN pages; `pages/<lc>/…` for the other 21 locales (22-language hreflang + x-default) |
| `serve-pages.snippet.ts` | Hono middleware to paste into the Zo `server.ts` before the 404 handler |

## /funding
42-row table (High relevance first, near deadlines next), "Closing soon" box for deadlines within 21 days of the
build date (2026-10-18: UArctic Entrepreneurship Fund 2026-10-31, Arctic Business Incubator 2026-11-02 24:00 CET),
past deadlines greyed as Closed, download link `/arctic-funding-programs-2026.csv`, ad slots `atl-ad-top`, `atl-ad-inc-1`, rails.
Rebuild daily (or after a CSV edit) so the "days left" and Closed badges stay current.

## /advertise
Oct 4–6 content (EN/RU/ZH texts; other locales use EN): audience, placements table, Yandex programmatic + /ads.txt,
direct-buy contact, crypto payment via the existing x402 rail (USDC on Base, `/.well-known/x402.json`).
Ad slots `atl-ad-top`, `atl-ad-inc-1`, `atl-ad-inc-2`, `atl-ad-side`, `atl-ad-mstick`; loads `/ads-config.js?v=20261005b`,
`/atl-ads.js?v=20261005b`, Yandex `context.js` and Autoplacement `ap-loader.js` (data-page-id 20141282).
Wording changes vs Oct: the "Home providers / partner strip" row is now "Home logo strip"; contact is collaborate@arctictradelanes.com (was partners@).

## Deploy on Zo (ArcticTradeLanes.com/arctic-trade-lanes)
1. Copy `pages/` to `<app>/pages/` (new directory; nothing replaced).
2. Paste `serve-pages.snippet.ts` into `server.ts` before the catch-all/404 handler; back up server.ts first.
3. Restart the service only after confirming the backend source files exist (see the Oct 18 handoff note).
4. Verify: `curl -sI https://arctictradelanes.com/funding` → 200, `X-ATL-Page: funding`; homepage md5 unchanged.
