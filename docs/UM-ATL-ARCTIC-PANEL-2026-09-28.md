# UM × ATL Arctic-panel pages (2026-09-28)

These are server-rendered OSINT pages on ArcticTradeLanes.com for the **AIM Congress 2026 NSR Mega Panel**: *"Arctic Development: Unlocking the Potential of the Northern Sea Route"*. It ran at DWTC, Dubai, on Day 3, 9 Sep 2026, 12:00–13:00 GST. The congress ran 7–9 Sep 2026.

Source post: https://x.com/alexdolbun/status/2080674977775288575

## Pages (6 people + 1 event × 22 locales = 154 URLs)

| Page | EN | RU |
|---|---|---|
| Event | https://arctictradelanes.com/events/aim-congress-2026-arctic-panel | https://arctictradelanes.com/ru/events/aim-congress-2026-arctic-panel |
| Kirill Dmitriev (tagged in post; not a listed panelist) | https://arctictradelanes.com/people/kirill-dmitriev | https://arctictradelanes.com/ru/people/kirill-dmitriev |
| Alexey Chekunkov | https://arctictradelanes.com/people/alexey-chekunkov | https://arctictradelanes.com/ru/people/alexey-chekunkov |
| Andrey Chibis | https://arctictradelanes.com/people/andrey-chibis | https://arctictradelanes.com/ru/people/andrey-chibis |
| Aisen Nikolaev | https://arctictradelanes.com/people/aisen-nikolaev | https://arctictradelanes.com/ru/people/aisen-nikolaev |
| Artyom Dovlatov | https://arctictradelanes.com/people/artyom-dovlatov | https://arctictradelanes.com/ru/people/artyom-dovlatov |
| Vladimir Panov | https://arctictradelanes.com/people/vladimir-panov | https://arctictradelanes.com/ru/people/vladimir-panov |

Other locales use the prefix `/<lc>/…`. The 22 locales are: en ru zh ja ko el de nl fr es it pt tr ar hi vi id da fi sv nb is. EN, RU, ZH, AR and HI have fully localized facts. The other locales have localized UI and roles, with English facts marked `lang="en"`.

## What each page contains
- A self-canonical link, 22 hreflang alternates plus x-default, and JSON-LD `Person` (or `Event`).
- `sameAs` pointing to the UnicornsMap `$UM-Radar` counterpart (`https://unicornsmap.com/[<lc>/]radar/<slug>`), plus a visible do-follow link to it.
- An **EPSG:3996 pin** block: an SVG polar map and a coordinate table. Pins are taken only from existing ATL atlas features (`atlas.3996.geojson` / `atlas.4326.geojson`, by ID) or Wikidata coordinates. EPSG:3996 x/y is computed with the IBCAO polar-stereographic formula (lat_ts 75°N, lon_0 0°, WGS 84), which reproduces the atlas values.
- **Sanctions status, stated factually.** Entries were checked on 2026-09-28 against the OFAC SDN, EU consolidated and UK Sanctions List downloads. Each entry shows its ID and a link. Institutions (RDIF, VEB.RF, Rosatom Arctic, Atomflot) are listed separately.
- Publicly reported figures with **display-only** currency chips at Bank of Russia rates of 2026-09-26. These are not offers or payments.
- Numbered public sources for every biographical claim.
- Portraits only where a CC BY 4.0 kremlin.ru or government.ru image exists, with attribution. Panov and Dovlatov have none.
- No contact, deal, investment or partnership CTAs, and no payment rails.

## Implementation (additive)
- The generator is `scripts/ssr_arctic_panel/gen.py` (with `data.py` for facts and sources, and `i18n.py`). It writes to `ssr/`.
- `server.ts` serves `./ssr/<path>.html` for `/[lc/]people|events/<slug>` in front of the SPA fallback. All other routes are unchanged.
- Sitemap entries come from `scripts/build_seo.ts` ROUTES. IndexNow was pinged on 2026-09-28 (api.indexnow.org, Yandex, Bing, Naver, Seznam).

Found by Aleksei Dolgikh @alexdolbun
