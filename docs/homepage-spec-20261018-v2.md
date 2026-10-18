# Homepage spec v2 — 2026-10-18 23:10 MSK (owner order, relayed by Chief of Staff)

Builds on v1 (`homepage-spec-20261018.md`, GitHub 0e25535, Zo e7d5cfe9a, kill switch `ATL_HOME_EXTRAS`).

## Hard rules (unchanged + new)

- Additive only; keep the kill switch. Keep the H1, original JSON-LD, og image, the 6 home slot IDs,
  Yandex Autoplacement 20141282 and the ads-config R-A placeholders untouched. x402 semantics untouched.
- Neutral wording only (standing content policy); neutral profiles. No buy / deal / payment / token
  elements on pages about Russian officials or businesspeople, including Russian company pages that
  name individuals.
- Templates / programmatic generation only; no per-page AI prose. No PII in the repo.
- **NEW:** the GIS polar map stays the first-screen hero on every viewport and is never covered or hidden.

## Process

Ship block by block; test on spare port 51999; back up server.ts before each change; verify live
(status, size, map first screen at 1440 and 430, no overflow, RTL for ar, no console errors);
batch restarts where safe.

## Blocks

1. **Hero background** around/behind the map: crossfade every 8–12 s, CSS or tiny post-paint script,
   prefers-reduced-motion respected, reserved size (no CLS), lazy, WebP/AVIF < 60 KB each. Themes:
   atlas, ports/NSR shipping, aurora, international business. Own or clearly licensed images with
   credits file + footer; alt text in 22 languages via templates; never overlays the map.
2. **Flag strip**: Arctic Council 8 (RU, NO, FI, SE, DK+GL, IS, CA, US), observers (CN, IN, JP, KR, SG,
   DE, FR, GB, IT, NL, PL, ES, CH) and AE, each linking to a templated hub `/country/{iso2}` (+ locale
   prefixes): currency code/name, ports and atlas entities from existing data, registry brands,
   /funding programs by country where data allows, hreflang. No prices, no invented figures.
3. **OSS brand registry** `data/arctic-brands/` (brands.csv, brands.json, README.md, CONTRIBUTING.md):
   id, name, logo_url, logo_license, logo_source, country, sector, hq_lat, hq_lon, arctic_geo_lat,
   arctic_geo_lon, website, facts[{fact, source_url, date}], currency. Seeded from public sources
   (Wikidata); every fact sourced and dated; logos only where reuse is allowed, else text wordmark.
   Pages `/company/{slug}` + `/companies` in 22 languages, Organization JSON-LD, sitemap, links to hubs.
4. **Logo wall** on the homepage from the registry (CSS scroll, paused under reduced motion, lazy,
   wordmark fallback), neutral heading "Arctic companies in the registry"; banned brand-strip wording
   avoided.
5. **2026–2036 sprint scroll story** with a client-side currency switcher (RUB, NOK, SEK, DKK, ISK, CAD,
   USD, EUR, CNY, JPY, KRW, INR, …) using dated public FX (ECB reference rates, server-side cached, date
   shown). Every figure sourced and dated, else omitted. Sections: FX/stablecoins; yield/borrowing
   (categories only); government/institutional support (/funding); index funds / collective investment
   (concept); $ATL token concept (link docs/atl-token-concept.md, "concept, not an offer"); GIS OSINT
   alpha / OSS "Agentic Swarm Orchestra Conductor".
6. **Ads + search**: keep Yandex slots; `docs/ad-network-plan.md` (AdSense, Baidu Union, Yahoo Japan,
   Microsoft/Bing, VK/Mail.ru, Naver, Seznam, …) with hidden placeholder containers and no fake IDs;
   /advertise section on cross-platform brand campaigns; hreflang on all new pages; per-language
   sitemaps + sitemap index; Yandex/Baidu/Bing/Naver verification meta as config-driven empty values
   (no tag until set); Schema.org Organization, Place, Dataset; localized titles/descriptions.
7. **Performance**: no heavy JS on first paint; Cache-Control with s-maxage for static pages without
   affecting dynamic APIs; TTFB measured (cold/warm) for / and a hub page; long content on hub/company
   pages, homepage increase kept modest.

## Report

Live URLs with status/bytes (/, /ru, /ar, a hub, /companies, a company, sitemap index); brand count and
licensed-logo count; image credits; TTFB; GitHub + Zo SHAs; rollback steps; items needing the owner
(ad account IDs, verification codes, image licences); deferred items. Screenshots: /workspace/atl-home-1018-v2/.
