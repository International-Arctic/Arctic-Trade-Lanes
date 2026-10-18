import { existsSync, readFileSync } from "node:fs";

/**
 * ATL SEO shell middleware (restored 2026-10-14).
 *
 * server.ts calls `seoHtml(path, shellHtml)` for every production request that
 * did not match a real file in ./dist. Responsibilities:
 *   1. resolve the locale prefix (22 locales) and the canonical base path
 *   2. inject title / description / canonical / hreflang cluster / OG / JSON-LD
 *   3. serve a real per-route document when one exists on disk
 *      (./dist{c}.html, ./dist{c}/index.html, ./pages{c}.html)
 *   4. otherwise fall back to the static shell with SEO injected
 *
 * Unknown paths keep the long-standing soft-200 behaviour of this origin.
 */

export const SITE_ORIGIN = "https://arctictradelanes.com";

export const LOCALES = [
  "en", "ru", "zh", "ja", "ko", "el", "de", "nl", "fr", "es", "it",
  "pt", "tr", "ar", "hi", "vi", "id", "da", "fi", "sv", "nb", "is",
] as const;

const RTL = new Set(["ar", "he", "fa", "ur"]);

type RouteSeo = {
  title: string;
  description: string;
  ogType?: string;
  jsonLdType?: string;
};

const DEFAULT_SEO: RouteSeo = {
  title: "ArcticTradeLanes.com — Arctic GIS OSINT · NSR · Polar Silk Road",
  description:
    "Arctic GIS OSINT atlas of ports, lanes, cities, programmes, shipyards and industry sites for the Northern Sea Route and the Polar Silk Road. Live GeoJSON, EPSG:3996 polar map, 22 languages.",
  ogType: "website",
  jsonLdType: "WebPage",
};

const ROUTE_SEO: Record<string, RouteSeo> = {
  "/": {
    title: "ArcticTradeLanes.com — Arctic GIS OSINT Atlas · NSR · Polar Silk Road",
    description:
      "Open polar-stereographic (EPSG:3996) Arctic atlas: ports, trade lanes, shipyards, programmes and industry sites on the Northern Sea Route and Polar Silk Road. Free GeoJSON, machine-payable route intelligence.",
    ogType: "website",
    jsonLdType: "WebSite",
  },
  "/collaborate": {
    title: "Collaborate — Arctic trade corridor partnerships · ArcticTradeLanes.com",
    description:
      "Partner with ArcticTradeLanes.com on RU, CA-AK and KR-JP-CN trade corridors: open GIS OSINT, machine-payable APIs, corridor intelligence and settlement today via x402 USDC on Base.",
    ogType: "website",
    jsonLdType: "WebPage",
  },
  "/pricing": {
    title: "Pricing — x402 USDC settlement · ArcticTradeLanes.com",
    description:
      "ArcticTradeLanes.com pricing: free atlas lookups, x402 v1 route intelligence at 5 USDC on Base via Bankr, and enterprise corridor feeds for the Northern Sea Route and Polar Silk Road.",
    ogType: "website",
    jsonLdType: "Product",
  },
  "/opportunity": {
    title: "Corridor opportunity — Arctic trade economics · ArcticTradeLanes.com",
    description:
      "Arctic corridor opportunity tracking: NSR transit volumes, ice windows, chokepoint repricing and Polar Silk Road capacity, sourced from public records.",
    jsonLdType: "WebPage",
  },
  "/arctic-economic-atlas": {
    title: "Arctic economic atlas — ports, lanes, programmes · ArcticTradeLanes.com",
    description:
      "The Arctic economic atlas: 155 ports, 27 lanes, 109 industry sites, 69 shipyards, 713 programmes, 103 cities and 51 tankers mapped on an EPSG:3996 polar projection with live GeoJSON export.",
    jsonLdType: "Dataset",
  },
  "/china-polar-silk-road": {
    title: "China Polar Silk Road — route and capacity intelligence · ArcticTradeLanes.com",
    description:
      "Polar Silk Road intelligence: Chinese Arctic shipping capacity, ice-container tonnage and NSR transit windows, mapped against public records.",
    jsonLdType: "WebPage",
  },
  "/x402/pay": {
    title: "Pay 5 USDC via x402 — Arctic route intelligence · ArcticTradeLanes.com",
    description:
      "Settle ArcticTradeLanes.com route intelligence with x402: 5 USDC on Base per report, machine-payable by agents, with the free atlas lookup tier unchanged.",
    jsonLdType: "WebPage",
  },
  "/receipt": {
    title: "Receipt — 5.00 USDC on Base via x402 · ArcticTradeLanes.com",
    description:
      "Unlock the ArcticTradeLanes.com corridor payload and keep the receipt: 5.00 USDC on Base, payTo address, transaction hash and status, in your own language.",
    jsonLdType: "WebPage",
  },
};

/**
 * Routes whose head copy is localised at request time.
 *
 * The receipt surface is part of the money path, so its <title>/description come
 * from the same locale pack the page body is rendered from
 * (public/x402/i18n/<lang>.json) instead of from the English ROUTE_SEO entry.
 * A missing or unreadable pack falls back to English rather than an empty title.
 */
const LOCALISED_HEAD_ROUTES: Record<string, { title: string; description: string }> = {
  "/receipt": { title: "receipt_heading", description: "step5_b" },
  "/x402/pay": { title: "h1", description: "lede" },
};

const packCache = new Map<string, Record<string, unknown> | null>();

function readPack(lang: string): Record<string, unknown> | null {
  const cached = packCache.get(lang);
  if (cached !== undefined) return cached;
  let data: Record<string, unknown> | null = null;
  for (const dir of PAGE_DIRS) {
    try {
      const parsed = JSON.parse(readFileSync(`${dir}/x402/i18n/${lang}.json`, "utf8"));
      if (parsed && typeof parsed === "object") {
        data = parsed as Record<string, unknown>;
        break;
      }
    } catch {
      /* try the next root */
    }
  }
  packCache.set(lang, data);
  return data;
}

function resolveSeo(lang: string, basePath: string): RouteSeo {
  const base = ROUTE_SEO[basePath] ?? DEFAULT_SEO;
  const keys = LOCALISED_HEAD_ROUTES[basePath];
  if (!keys || lang === "en") return base;
  const pack = readPack(lang);
  if (!pack) return base;
  const heading = typeof pack[keys.title] === "string" ? String(pack[keys.title]) : "";
  const body = typeof pack[keys.description] === "string" ? String(pack[keys.description]) : "";
  if (!heading && !body) return base;
  return {
    ...base,
    title: heading ? `${heading} · ArcticTradeLanes.com` : base.title,
    description: body || base.description,
  };
}

function normalise(path: string): string {
  let p = (path || "/").split("?")[0].split("#")[0];
  if (!p.startsWith("/")) p = `/${p}`;
  if (p.length > 1) p = p.replace(/\/+$/, "");
  return p === "" ? "/" : p;
}

function splitLocale(path: string): { lang: string; basePath: string } {
  const segments = path.split("/").filter(Boolean);
  if (segments.length > 0 && (LOCALES as readonly string[]).includes(segments[0])) {
    return { lang: segments[0], basePath: `/${segments.slice(1).join("/")}` };
  }
  return { lang: "en", basePath: path };
}

function hrefFor(lang: string, basePath: string): string {
  const clean = basePath === "/" ? "" : basePath;
  return lang === "en" ? `${SITE_ORIGIN}${clean || "/"}` : `${SITE_ORIGIN}/${lang}${clean}`;
}

function escapeHtml(value: string): string {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

const PAGE_DIRS = ["./dist", "./pages", "./public"];

/** Locale-aware candidates. English is the source locale and lives at the bare path. */
function pageCandidates(basePath: string, lang: string): string[] {
  if (basePath === "/") return [];
  const out: string[] = [];
  if (lang !== "en") {
    for (const dir of PAGE_DIRS) out.push(`${dir}/${lang}${basePath}.html`);
  }
  for (const dir of PAGE_DIRS) {
    out.push(`${dir}${basePath}.html`, `${dir}${basePath}/index.html`);
  }
  return out;
}

function readPage(basePath: string, lang: string): string | null {
  for (const candidate of pageCandidates(basePath, lang)) {
    try {
      if (existsSync(candidate)) {
        const raw = readFileSync(candidate, "utf8");
        if (raw.trim().length > 0) return raw;
      }
    } catch {
      /* ignore and keep looking */
    }
  }
  return null;
}

/**
 * Candidates that hold a locale's OWN copy of a page.
 *
 * `pageCandidates()` deliberately falls back to the English file so a visitor on
 * /de/collaborate still gets content. That fallback must not be used to decide
 * whether a translation EXISTS, or every locale looks translated the moment the
 * English page ships.
 */
function ownCandidates(basePath: string, lang: string): string[] {
  if (basePath === "/") return [];
  const out: string[] = [];
  if (lang !== "en") {
    for (const dir of PAGE_DIRS) {
      out.push(`${dir}/${lang}${basePath}.html`, `${dir}/${lang}${basePath}/index.html`);
    }
  } else {
    for (const dir of PAGE_DIRS) {
      out.push(`${dir}${basePath}.html`, `${dir}${basePath}/index.html`);
    }
  }
  return out;
}

function readOwnPage(basePath: string, lang: string): string | null {
  for (const candidate of ownCandidates(basePath, lang)) {
    try {
      if (existsSync(candidate)) {
        const raw = readFileSync(candidate, "utf8");
        if (raw.trim().length > 0) return raw;
      }
    } catch {
      /* ignore and keep looking */
    }
  }
  return null;
}

/**
 * Locales whose translated page genuinely exists on disk. hreflang is derived
 * from this, never from the full locale list, so we never advertise a
 * translated URL that would silently fall back to English copy.
 *
 * 2026-10-14 FIX: this used `readPage()`, whose English fallback reported every
 * one of the 22 locales as translated the moment the English page existed. The
 * live pages advertised 23 hreflang alternates while only en/ru/zh/ja/ko had
 * real copy, and each phantom locale self-canonicalised - the exact
 * duplicate-content signal the sentence above promises to avoid.
 */
export function availableLocales(basePath: string): string[] {
  if (basePath === "/" || readOwnPage(basePath, "en") === null) return ["en"];
  return ["en", ...LOCALES.filter((l) => l !== "en" && readOwnPage(basePath, l) !== null)];
}

type HeadContext = {
  basePath: string;
  lang: string;
  seo: RouteSeo;
  /** Locales with a real translated page on disk. */
  available: string[];
  /** True when this URL is an English-copy fallback for a locale we do not ship. */
  noindex: boolean;
};

function headBlock(ctx: HeadContext): string {
  const { basePath, lang, seo, available, noindex } = ctx;
  const hasOwnCopy = lang === "en" || available.includes(lang);
  const canonical = hasOwnCopy ? hrefFor(lang, basePath) : hrefFor("en", basePath);
  const contentLang = hasOwnCopy ? lang : "en";
  const alternates = [
    ...available.map(
      (l) => `    <link rel="alternate" hreflang="${l}" href="${escapeHtml(hrefFor(l, basePath))}" />`
    ),
    `    <link rel="alternate" hreflang="x-default" href="${escapeHtml(hrefFor("en", basePath))}" />`,
  ].join("\n");

  const jsonLd = {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "Organization",
        "@id": `${SITE_ORIGIN}/#organization`,
        name: "ArcticTradeLanes.com",
        url: SITE_ORIGIN,
        founder: { "@type": "Person", name: "Aleksei Dolgikh", sameAs: "https://x.com/alexdolbun" },
        sameAs: [
          "https://github.com/International-Arctic/Arctic-Trade-Lanes",
          "https://github.com/International-Arctic/ArcticTradeLanes-Dataset",
        ],
      },
      {
        "@type": seo.jsonLdType ?? "WebPage",
        "@id": `${canonical}#page`,
        name: escapeHtml(seo.title),
        description: escapeHtml(seo.description),
        url: canonical,
        inLanguage: contentLang,
        isPartOf: { "@id": `${SITE_ORIGIN}/#organization` },
      },
    ],
  };

  return [
    `    <title>${escapeHtml(seo.title)}</title>`,
    `    <meta name="description" content="${escapeHtml(seo.description)}" />`,
    `    <link rel="canonical" href="${escapeHtml(canonical)}" />`,
    alternates,
    ...(noindex ? [`    <meta name="robots" content="noindex, follow" />`] : []),
    `    <meta property="og:type" content="${seo.ogType ?? "website"}" />`,
    `    <meta property="og:site_name" content="ArcticTradeLanes.com" />`,
    `    <meta property="og:title" content="${escapeHtml(seo.title)}" />`,
    `    <meta property="og:description" content="${escapeHtml(seo.description)}" />`,
    `    <meta property="og:url" content="${escapeHtml(canonical)}" />`,
    `    <meta name="twitter:card" content="summary_large_image" />`,
    `    <script type="application/ld+json">${JSON.stringify(jsonLd)}</script>`,
  ].join("\n");
}

/**
 * The shipped shell carries its own hard-coded head declarations. They must be
 * removed before injection, or the locale machinery fights itself:
 *   * /ja served two hreflang clusters at once — the shell's 25 hard-coded
 *     alternates plus the real, copy-backed cluster — and Google reads
 *     contradictory alternates as noise;
 *   * the shell's `index, follow` robots tag overrode the per-locale noindex
 *     that keeps an English-fallback URL out of the index.
 */
const VENDORED_HEAD_TAGS = [
  /<link\s+rel=["']alternate["'][^>]*>\s*/gi,
  /<meta\s+property=["']og:locale(?::alternate)?["'][^>]*>\s*/gi,
  /<meta\s+name=["']robots["'][^>]*>\s*/gi,
];

function inject(html: string, ctx: HeadContext): string {
  const head = headBlock(ctx);
  const contentLang = ctx.lang === "en" || ctx.available.includes(ctx.lang) ? ctx.lang : "en";
  let out = html;

  for (const pattern of VENDORED_HEAD_TAGS) out = out.replace(pattern, "");

  if (out.includes("<!--ATL-SEO-->")) {
    out = out.replace("<!--ATL-SEO-->", head);
  } else {
    out = out
      .replace(/<title>[\s\S]*?<\/title>\s*/i, "")
      .replace(/<meta\s+name=["']description["'][^>]*>\s*/i, "");
    out = out.includes("</head>")
      ? out.replace("</head>", `${head}\n  </head>`)
      : `${head}\n${out}`;
  }

  /** `lang` describes the copy actually served, not the URL prefix that asked for it. */
  out = out.replace(
    /<html([^>]*)\blang=["'][^"']*["']/i,
    `<html$1lang="${contentLang}"`
  );
  if (!/<html[^>]*\blang=/i.test(out) && out.includes("<html")) {
    out = out.replace(/<html/i, `<html lang="${contentLang}"`);
  }
  if (RTL.has(contentLang)) {
    out = out.replace(/<html([^>]*)>/i, `<html$1 dir="rtl">`);
  }
  return out;
}

export function seoHtml(path: string, shellHtml: string): string {
  const normalised = normalise(path);
  const { lang, basePath } = splitLocale(normalised);
  const seo = resolveSeo(lang, basePath);
  const available = availableLocales(basePath);
  const hasOwnCopy = lang === "en" || available.includes(lang);
  const page = readPage(basePath, lang);
  return inject(page ?? shellHtml, {
    basePath,
    lang,
    seo,
    available,
    noindex: !hasOwnCopy,
  });
}

export function knownRoutePaths(): string[] {
  return Object.keys(ROUTE_SEO);
}

/**
 * Content routes only — the set sitemap.xml and llms.txt advertise.
 *
 * `/x402/pay` is deliberately excluded: it is a settlement entry point reached
 * from CTAs, not a page anyone should find by searching.
 */
export const SITEMAP_ROUTES = [
  "/",
  "/collaborate",
  "/pricing",
  "/opportunity",
  "/arctic-economic-atlas",
  "/china-polar-silk-road",
] as const;

/**
 * True when a request path maps to a route this origin actually ships.
 *
 * Used to separate "serve the page" from "this URL does not exist". Before
 * 2026-10-14 the two were indistinguishable: every unmatched dotless path got
 * the shell with HTTP 200.
 */
export function isKnownRoutePath(path: string): boolean {
  const { basePath } = splitLocale(normalise(path));
  return basePath === "/" || basePath in ROUTE_SEO;
}
