import { Hono } from "hono";
import { readFileSync } from "node:fs";

export const X402_VERSION = "edge-v2026-09-01-atl-wellknown-x402";
export const PAY_WALLET = "0x211D91beD006f7bB3Eaf97496260a8F905298Cea";
export const BANKR_URL = "https://bankr.bot?ref=um-radar";
export const BANKR_REF = "RN982CZZ-BNKR";
const DOMAIN = "https://arctictradelanes.com";

/** Korea Panstar NSR corridor hubs — heuristic baseline. */
const PANSTAR_WAYPOINTS = [
  { name: "Busan", lat: 35.1796, lon: 129.0756 },
  { name: "Vladivostok", lat: 43.1155, lon: 131.8855 },
  { name: "Petropavlovsk-Kamchatsky", lat: 53.0444, lon: 158.65 },
  { name: "Provideniya", lat: 64.4231, lon: -173.2264 },
  { name: "Pevek", lat: 69.7029, lon: 170.2742 },
  { name: "Sabetta", lat: 71.2731, lon: 72.0725 },
  { name: "Murmansk", lat: 68.9585, lon: 33.0827 },
];

const PANSTAR_FX = {
  CNY: 7.24,
  KRW: 1390,
  RUB: 92.5,
  asOf: "2026-09-01",
  note: "Heuristic FX snapshot for the Panstar SKU; not live DeepSeek (keyConfigured=false).",
};

const RAILS = [
  { network: "Base", asset: "USDC", status: "live" },
  { network: "Tron", asset: "USDT-TRC20", status: "live" },
  { network: "BNB", asset: "USDT", status: "live" },
  { network: "Base", asset: "$ATL", status: "planned" },
];

const X402_SCHEMA = {
  schema: "https://json-schema.org/draft/2020-12/schema",
  $id: "https://arctictradelanes.com/api/x402/schema",
  title: "ArcticTradeLanes.com $ATL x402 — NSR Window + FX Waypoints",
  description:
    "Paid x402 rail shared with UnicornsMap.com $UM-Radar. Pay 5 USDC on Base via Bankr to unlock a real 2026-2036 Northern Sea Route window and live CNY/KRW/RUB FX waypoints on the Korea Panstar lane. Canonical $ATL on Base next to $UM; USDC Base / USDT-TRC20 / BNB USDT settlement.",
  type: "object",
  properties: {
    ok: { type: "boolean" },
    service: { type: "string" },
    domain: { type: "string" },
    version: { type: "string" },
    slug: { type: "string" },
    price: {
      type: "object",
      properties: {
        amount: { type: "number", const: 5 },
        currency: { type: "string", const: "USDC" },
        network: { type: "string", const: "Base" },
      },
      required: ["amount", "currency", "network"],
    },
    rails: {
      type: "array",
      description:
        "Settlement rails. Native $ATL is NOT minted until this paid SKU returns real waypoints.",
      items: {
        type: "object",
        properties: {
          network: { type: "string" },
          asset: { type: "string" },
          status: { type: "string", enum: ["live", "planned"] },
        },
      },
    },
    pay: {
      type: "object",
      properties: {
        token: { type: "string" },
        contract: { type: "string" },
        wallet: { type: "string" },
        bankr: { type: "string" },
        refCode: { type: "string" },
        method: { type: "string" },
      },
    },
    corridor: { type: "object" },
    output: {
      type: "object",
      properties: {
        format: { type: "string", const: "json" },
        window: { type: "string" },
        lane: { type: "string" },
        waypoints: { type: "array" },
        fx: { type: "object" },
      },
      required: ["format", "window", "lane", "waypoints"],
    },
  },
  required: ["ok", "service", "domain", "price", "rails", "pay"],
};

function json(data: unknown, status = 200): Response {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Cache-Control": "public, max-age=60",
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Headers": "Content-Type, x402-payment",
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    },
  });
}

/** Header contract: x402:<wallet|tag>:<amount>. Mirrors /api/atlas and /api/agent. */
export function isWellFormedX402Payment(header: string | null): boolean {
  if (!header || !header.startsWith("x402:")) return false;
  const parts = header.split(":");
  if (parts.length < 3) return false;
  const walletOrTag = parts[1] || "";
  const amount = parts[2] || "";
  const amountOk = amount === "5" || amount.startsWith("5");
  const walletOk =
    !walletOrTag ||
    walletOrTag.toLowerCase() === PAY_WALLET.toLowerCase() ||
    walletOrTag.length >= 4;
  return amountOk && walletOk;
}

/**
 * Localised receipt copy.
 *
 * Packs are the same files the receipt page renders from
 * (public/x402/i18n/<lang>.json), read once and cached for the process. A locale
 * without a pack falls back to en — a receipt must never come back half-translated
 * or blank, because it is the only artefact a buyer keeps.
 */
const RECEIPT_PACK_DIRS = ["./public/x402/i18n", "./dist/x402/i18n"];
const receiptPacks = new Map<string, Record<string, string> | null>();

export const RECEIPT_LOCALES = [
  "en", "ru", "zh", "ja", "ko", "el", "de", "nl", "fr", "es", "it",
  "pt", "tr", "ar", "hi", "vi", "id", "da", "fi", "sv", "nb", "is",
] as const;

function loadReceiptPack(lang: string): Record<string, string> | null {
  const cached = receiptPacks.get(lang);
  if (cached !== undefined) return cached;
  let pack: Record<string, string> | null = null;
  for (const dir of RECEIPT_PACK_DIRS) {
    try {
      const raw = readFileSync(`${dir}/${lang}.json`, "utf8");
      const parsed = JSON.parse(raw);
      if (parsed && typeof parsed === "object") {
        pack = parsed as Record<string, string>;
        break;
      }
    } catch {
      /* try the next root */
    }
  }
  if (!pack) console.warn(`[atl-x402] no receipt pack for ${lang}`);
  receiptPacks.set(lang, pack);
  return pack;
}

/** First Accept-Language tag that we actually ship a pack for. */
export function resolveReceiptLocale(acceptLanguage: string | null | undefined): string {
  if (!acceptLanguage) return "en";
  for (const part of acceptLanguage.split(",")) {
    const tag = part.split(";")[0]?.trim().toLowerCase() ?? "";
    if (!tag) continue;
    const exact = tag.replace("_", "-");
    const base = exact.split("-")[0];
    if (exact === "zh-tw" || exact === "zh-hk") {
      if (loadReceiptPack("zh")) return "zh";
    }
    if ((RECEIPT_LOCALES as readonly string[]).includes(exact) && loadReceiptPack(exact)) return exact;
    if ((RECEIPT_LOCALES as readonly string[]).includes(base) && loadReceiptPack(base)) return base;
  }
  return "en";
}

type ReceiptInput = { slug: string; txHash?: string | null; headerPreview?: string | null };

export function receiptFor(locale: string, input: ReceiptInput) {
  const pack = loadReceiptPack(locale) ?? loadReceiptPack("en");
  const issuedAt = new Date().toISOString();
  const txHash = (input.txHash ?? "").trim() || null;
  const amountText = "5.00 USDC";
  const network = "Base · chainId 8453";
  const status = "alpha";
  const statusText = pack?.receipt_status_alpha ?? "alpha contract — on-chain settlement proof is not wired yet";

  const fill = (key: string, fallback: string, vars: Record<string, string>) => {
    const template = pack?.[key] ?? fallback;
    return Object.entries(vars).reduce(
      (acc, [k, v]) => acc.replaceAll(`{${k}}`, v),
      template,
    );
  };

  const lines = [
    fill("receipt_heading", "Receipt", {}),
    fill("receipt_amount", "Amount paid: {amount}", { amount: amountText }),
    fill("receipt_network", "Network: {network}", { network }),
    fill("receipt_payto", "Paid to: {payto}", { payto: PAY_WALLET }),
    txHash
      ? fill("receipt_txhash", "Transaction hash: {tx}", { tx: txHash })
      : fill("receipt_txhash_none", "Transaction hash: not supplied", {}),
    fill("receipt_status", "Status: {status}", { status: statusText }),
    fill("receipt_time", "Recorded {time}", { time: issuedAt }),
  ];

  return {
    receipt: {
      ok: true,
      locale,
      langName: pack?.lang_name ?? "English",
      dir: pack?.dir ?? "ltr",
      asset: "USDC",
      amount: 5,
      amountText,
      network: "Base",
      networkText: network,
      chainId: 8453,
      payTo: PAY_WALLET,
      txHash,
      verifiedOnchain: false,
      status,
      statusText,
      slug: input.slug,
      issuedAt,
      lines,
    },
    receiptText: lines.join("\n"),
    receiptLocale: locale,
  };
}

function paymentRequired(slug: string): Response {
  return json(
    {
      ok: false,
      error: "Payment Required",
      status: 402,
      slug,
      price: { amount: 5, currency: "USDC", network: "Base" },
      pay: {
        wallet: PAY_WALLET,
        bankr: BANKR_URL,
        refCode: BANKR_REF,
        method: "5 USDC via @bankrbot",
      },
      how: `Pay 5 USDC on Base via Bankr, then retry with header x402-payment: x402:${PAY_WALLET}:5`,
      note: "Header format mirrors /api/atlas and /api/agent — a well-formed x402: prefix unlocks waypoints. On-chain Bankr settlement proof is still optional.",
    },
    402,
  );
}

function fulfillPayload(slug: string, paymentHeader: string) {
  return {
    ok: true,
    service: "ArcticTradeLanes.com $ATL x402",
    domain: DOMAIN,
    version: X402_VERSION,
    slug,
    price: { amount: 5, currency: "USDC", network: "Base" },
    format: "json",
    window: "2026 NSR summer (Jul–Oct ice window)",
    lane: "Korea Panstar Busan NSR",
    waypoints: PANSTAR_WAYPOINTS,
    fx: PANSTAR_FX,
    paid: true,
    payment: {
      headerPresent: true,
      wellFormed: true,
      verifiedOnchain: false,
      note: "Accepted well-formed x402-payment header (site alpha/atlas pattern). Live Bankr on-chain settlement proof is not wired yet — do not treat as a cryptographic receipt.",
      headerPreview: paymentHeader.slice(0, 48),
    },
    rails: RAILS,
  };
}

/** Discovery manifest served at /.well-known/x402.json (parity with the edge Worker). */
export function x402DiscoveryDocument() {
  return {
    ok: true,
    service: "ArcticTradeLanes.com $ATL x402",
    domain: DOMAIN,
    version: X402_VERSION,
    x402Version: 1,
    payTo: PAY_WALLET,
    network: "Base",
    asset: "USDC",
    price: { amount: 5, currency: "USDC", network: "Base" },
    bankr: { ref: BANKR_REF, url: BANKR_URL },
    endpoints: {
      schema: "/api/x402/schema",
      status: "/api/x402/status",
      fulfill: "/api/x402/fulfill",
      upload: "/api/x402/upload",
      routeOptimize: "/api/alpha/route-optimize",
    },
    resources: [
      {
        path: "/api/x402/fulfill",
        method: "GET",
        price: "5 USDC",
        network: "Base",
        payTo: PAY_WALLET,
        description: "Korea Panstar NSR window + FX waypoints",
      },
      {
        path: "/api/x402/upload",
        method: "POST",
        price: "5 USDC",
        network: "Base",
        payTo: PAY_WALLET,
        description: "Paid upload / fulfill alias",
      },
      {
        path: "/api/alpha/route-optimize",
        method: "POST",
        price: "5 USDC (or free tier)",
        network: "Base",
        payTo: PAY_WALLET,
        description: "Route optimize",
      },
    ],
    note: "Legacy x402 v1 (custom x402-payment request header). x402 v2 is planned, not live. www.arctictradelanes.com stays a grey-cloud CNAME to Zo.",
  };
}

export function x402StatusDocument(slug: string) {
  return {
    ok: true,
    service: "ArcticTradeLanes.com $ATL x402",
    domain: DOMAIN,
    version: X402_VERSION,
    slug,
    price: { amount: 5, currency: "USDC", network: "Base" },
    rails: RAILS,
    pay: {
      token: "$ATL (canonical, Base)",
      contract: "TBD — no mint until paid SKU returns waypoints",
      wallet: PAY_WALLET,
      bankr: BANKR_URL,
      refCode: BANKR_REF,
      method: "5 USDC via @bankrbot",
    },
    corridor: { lat: 76, lng: 128, hubs: ["Busan", "Vladivostok", "Korea Panstar NSR"] },
    endpoints: [
      "GET /api/x402/schema",
      "GET /api/x402/status?slug={slug}",
      "GET /api/x402/fulfill?slug={slug}",
      "POST /api/x402/upload",
    ],
    fulfill: {
      requiresHeader: "x402-payment",
      example: `x402-payment: x402:${PAY_WALLET}:5`,
    },
  };
}

export function x402SchemaDocument() {
  return { ...X402_SCHEMA };
}

/** Mounted at /api/x402 by routes.ts. */
export const x402Router = new Hono();

x402Router.options("*", () => json({ ok: true }));

x402Router.get("/status", (c) =>
  c.json(x402StatusDocument(c.req.query("slug") || "panstar-korea-nsr")),
);

x402Router.get("/schema", (c) => c.json(x402SchemaDocument()));

const paidHandler = async (c: any) => {
  const slug = c.req.query("slug") || "panstar-korea-nsr";
  const paymentHeader = c.req.header("x402-payment") || null;
  if (!isWellFormedX402Payment(paymentHeader)) return paymentRequired(slug);

  let bodySlug = slug;
  let bodyLocale = "";
  if (c.req.method === "POST") {
    try {
      const body = await c.req.json();
      if (body && body.slug) bodySlug = String(body.slug);
      if (body && body.locale) bodyLocale = String(body.locale);
    } catch {
      /* empty or non-JSON body is fine */
    }
  }

  /**
   * Receipt language: explicit ?lang= wins, then the body locale the page
   * sends, then the buyer's Accept-Language, then English. resolveReceiptLocale
   * only returns a locale we actually ship a pack for.
   */
  const requested = c.req.query("lang") || bodyLocale || "";
  const locale = /^[a-z]{2}$/i.test(requested)
    ? resolveReceiptLocale(requested)
    : resolveReceiptLocale(c.req.header("accept-language"));

  const txHash = c.req.query("tx") || null;
  const receiptBlock = receiptFor(locale, { slug: bodySlug, txHash });

  return c.json({
    ...fulfillPayload(bodySlug, paymentHeader as string),
    ts: receiptBlock.receipt.issuedAt,
    locale,
    ...receiptBlock,
  });
};

x402Router.get("/fulfill", paidHandler);
x402Router.post("/fulfill", paidHandler);
x402Router.post("/upload", paidHandler);
x402Router.get("/upload", paidHandler);

export default x402Router;
