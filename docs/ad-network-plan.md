# Ad network plan (2026-10-18)

Status: **Yandex Advertising Network is live** (6 original R-A slots + 3 home-extras slots + 2 net units, rendered by
`public/atl-ads.js` only when `window.ATL_AD_SLOTS` maps a real R-A id). Every other network below is **planned**.
The homepage carries hidden, empty placeholder containers for them
(`<div class="atl-net-placeholders" hidden>` → `div[data-atl-network][data-atl-slot=""]`).
**No publisher IDs, slot IDs or verification codes are invented.** Nothing loads for a network until a real ID is
configured.

| network | markets / languages | what's needed from the account owner | placeholder key |
|---|---|---|---|
| Google AdSense | global; en, de, fr, es, it, pt, nl, nordic, hi, id, vi, tr | `ca-pub-…` publisher ID, ad unit IDs, `ads.txt` line, site approval | `adsense` |
| Baidu Union (百度联盟) | zh (mainland) | Union account, site verification, ad slot IDs; ICP filing may be required for mainland serving | `baidu-union` |
| Yahoo! JAPAN Ads (YDN / YDA) | ja | publisher contract via an authorised partner, ad unit codes | `yahoo-japan` |
| Microsoft Advertising (publisher / Bing) | en, global | publisher account, ad unit IDs; Bing Webmaster verification | `microsoft` |
| VK Ads / Mail.ru (VK Реклама) | ru, CIS | VK Ads site account, block IDs | `vk` |
| Naver (네이버 애드포스트 / GFA) | ko | Naver publisher account, unit IDs; Naver Search Advisor verification | `naver` |
| Seznam (Sklik) | cs | Sklik partner account, zone IDs (Czech audience; reached through the en/de editions until a cs edition exists) | `seznam` |

## Activation (per network)

1. The owner (Aleksei) opens the account and sends the IDs.
2. Add the IDs to a config map (same pattern as `ATL_AD_SLOTS` for Yandex), plus the `ads.txt` lines.
3. Add the loader script for that network only on locales where it serves (lazy, after first paint).
4. Fill `data-atl-slot` in the placeholder and remove `hidden` for that one container.
5. Check that the map stays first screen on 1440 and 430 viewports, no CLS (reserve the slot height), no console errors.

## Search engine verification

`config/atl-site-verification.json` holds `google`, `yandex`, `bing`, `baidu` and `naver`, all empty.
`src/home/v2/atlV2.ts` emits `<meta name="google-site-verification|yandex-verification|msvalidate.01|baidu-site-verification|naver-site-verification">`
**only for non-empty values** (homepage + v2 pages). Restart the service after editing.

## Cross-platform brand campaigns (/advertise)

The `/advertise` page (22 locales) carries a "Cross-platform brand campaigns" section. One brief can cover
homepage and fact-page display slots per language edition, country hubs, sponsored registry spotlights and newsletter mentions.
Campaigns are booked per language and region. The CTA goes to `/collaborate`.

Rules that stay in force: no ads, payment or token elements on people pages or on company pages; nothing is
placed over or inside the first-screen GIS map.
