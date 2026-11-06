# NOTE — Homepage enhancement (2026-11-07)

Additive-only changes to `src/home/homeExtras.ts` + `src/home/home-extras.i18n.json` (22 locales, 71 new keys each) and `src/home/home-extras.data.json` (HNWI yacht-owner tiers on the existing 6 verified people).

- 5 new sections: Corridor 2026 (CHNL NSR stats), Who it serves (business/enterprise/government), Fleet & real polar paths (Arc7 LNG, Arktika-class, Arc4 carriers), Atlas in numbers, Funding readiness (honest, no pre-seed promises; $ATL labelled upcoming/concept).
- Hardened: `esc()` null-safety, manifest counts cached once (was read on every locale render, fragile path), `cor_cta1` reused as a number label (would have read "Opportunity desk"), all new strings localized across 22 locales, RTL (ar) verified.
- People pins: polar-themed initials badge + HNWI/Gov/Business tier chips; only already-verified people shown, still no faces, no net-worth, no deal claims. x402 pay band + Bankr affiliate + UnicornsMap cross-banner untouched.
- Source for corridor numbers: CHNL via gCaptain, 19 Oct 2026 — https://gcaptain.com/northern-sea-route-transits-surpass-2025-total-as-arctic-shipping-gains-momentum (104 transits by 30 Sep 2026 vs 103 in all of 2025; 3.7 Mt est.; 7.8M DWT +26%; ~150 projected year-end, marked as projection).
- Build/deploy (live site is not a Vite build): `cp` the three files into `site/home-extras/src/home/` (done), then `curl -X POST localhost:51927/trigger` or restart service `svc_UpoHDo9rDHs`, verify `/` and `/ru` return 200 with `#atlx-corridor` present. Note: `bun run build` is broken upstream (`scripts/build_seo.ts` missing) — use `vite build` only after adding a root `index.html`.
