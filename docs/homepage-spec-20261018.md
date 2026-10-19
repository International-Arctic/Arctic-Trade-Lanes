# Homepage growth spec — 2026-10-18 (what shipped)

Owner order (Aleksei Dolgikh, 2026-10-18 19:37 MSK, relayed by Chief of Staff): the homepage
performs well and should grow. **Additive only — do not break the current render.**

## Constraints honoured

- The SPA (Oct 6 bundle, OpenLayers EPSG:3996 polar map in the first screen, keyword H1, existing
  JSON-LD, og image, 6 home ad slot ids, Yandex Autoplacement 20141282) is untouched. Verified: the
  served HTML with the new block removed is **byte-identical** to the previous homepage (en, ru).
- No App.tsx change, no SPA rebuild/redeploy. `server.ts` x402 routes untouched; ads-config R-A
  placeholders untouched.
- Templates only: all strings come from `home-extras.i18n.json` (22 locales; core EN, RU, ZH, NB, DA),
  facts from `home-extras.data.json`. No per-page prose.
- Neutral wording only (standing content policy). Brands wording rules respected.
- People content is strictly neutral (name, public role, Arctic relevance, radar link) with no ads,
  token, payment or support CTA inside or adjacent to it.

## Architecture

- `site/home-extras/src/home/homeExtras.ts` renders one block per locale and injects it right after
  `<div id="root"></div>` (React owns only `#root`). Scoped CSS under `#atl-x`, RTL for Arabic,
  mobile-first, no horizontal overflow.
- `server.ts` hook (applied by `site/home-extras/patch_server.py`, idempotent): for `/` and `/<lc>` it
  serves the same `seoHtml()` shell plus the block, cached in the render cache (`X-ATL-Home: extras`).
  Any error falls through to the original chain. Kill switch: `ATL_HOME_EXTRAS=0`.
- `site/home-extras/src/home/intakeRoutes.ts`: `POST /api/atl-interest`, `POST /api/contributions`.
  JSON or form posts, honeypot `website`, 5 per IP per 10 min (per worker), 16 KB body cap, strict
  validation. Stored as NDJSON **outside the repo** on the server (`ATL_INTAKE_DIR`), mode 0600,
  IPs only as salted hash prefixes. Contributions are `status: pending`; nothing is auto-published.
- `site/people-pages/build_people_pages.py`: neutral `/people` index + `/people/<slug>` pages in 22
  locales (Person + ProfilePage + BreadcrumbList JSON-LD, hreflang ×22 + x-default, canonical) and
  `/sitemap-people.xml` (added to robots.txt). Related links only to fact pages that exist in
  `factpages/.routes.json`. The generator fails if banned wording appears.

## Homepage sections (below the map)

1. Sticky section nav (anchors).
2. **Project North Star** — entity graph, API-first (x402), alerts, core languages; roadmap 2026–2036;
   internal links to /ports, /lanes, /programs, /shipyards, /icebreakers (localized).
3. Ad slot `atl-ad-home-inc-3`.
4. **$ATL token (upcoming · concept)** — 4 intended-mechanics cards, early-interest form (email or
   wallet), risk disclaimer; FAQPage JSON-LD for the disclaimer. Then the UnicornsMap.com text
   cross-banner (`utm_source=arctictradelanes&utm_medium=crossbanner`).
5. **Arctic events and deadlines** — verified dates only (funding deadlines link to /funding;
   conferences link to organizers). Upcoming conferences emitted as Event JSON-LD.
6. **Arctic key people** — 5 AIM Congress 2026 NSR mega-panel speakers, neutral cards linking to
   `/people/<slug>` and the verified UnicornsMap radar page.
7. **Contribute data** — business / event / port / correction into the moderated queue.
8. Ad slot `atl-ad-home-inc-4` + network unit `atl-net-home-1`.
9. **Support Arctic Trade Lanes** — /funding, /advertise, $ATL interest list.
10. Ad slot `atl-ad-home-inc-5` + network unit `atl-net-home-2`.
11. Language links (22 locales, hreflang).

New ad slots reuse the SPA markup (`data-yandex-rtb-slot`, `yandex_rtb_<id>`) and the
`atl-ad-home-inc` family key (pageNumber 3–5); they stay collapsed until a block renders. Network
units stay collapsed while empty.

## Events (verified 2026-10-18)

UArctic Entrepreneurship Fund deadline 2026-10-31; Arctic Business Incubator intake 2026-11-02;
Arctic Accelerator (Northern Norway) 2026-12-01; Arctic Frontiers 2027, Tromsø, 1–4 Feb 2027;
Arctic Circle Polar Dialogue, Bolzano, 17–18 Feb 2027; Kirkenes Conference 26–27 May 2027; Arctic
Circle Assembly 2027, Reykjavík, 14–16 Oct 2027. Recent: Arctic Circle Assembly 2026 (8–10 Oct),
AIM Congress 2026 NSR mega panel (9 Sep, Dubai), Kirkenes Conference 2026 (20–21 May), Arctic
Encounter Summit 2026 (15–17 Apr). Arctic Economic Council: no verifiable upcoming date found, omitted.

## Deferred

- Ad-network scripts for `atl-net-home-*` (containers only; no network chosen yet).
- Moderation UI / export for the intake queues (files only for now).
- UnicornsMap image banner (text/CSS banner until the asset is confirmed).
