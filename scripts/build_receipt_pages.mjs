/**
 * Render the transactional receipt surface for every locale.
 *
 *   bun scripts/build_receipt_pages.mjs
 *
 * Writes public/<lang>/receipt.html for en + the 21 locale packs in
 * public/x402/i18n/*.json. The SEO middleware serves the same file at
 * /<lang>/receipt and injects title/canonical/hreflang from the locale pack, so
 * this script only owns the body.
 *
 * Why a standalone document instead of a route inside the SPA: the receipt is
 * the one step of the x402 journey the shipped bundle does not implement (it
 * hands off to Bankr on X and never shows a receipt). Mounting this on a NEW
 * path keeps the SPA's own routes untouched — nothing here can shadow /pricing
 * or the map shell.
 *
 * Deterministic: same packs in, same bytes out. Safe to re-run.
 */
import { mkdirSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const PACK_DIR = join(ROOT, "public", "x402", "i18n");
const OUT_ROOT = join(ROOT, "public");

const PAY_TO = "0x211D91beD006f7bB3Eaf97496260a8F905298Cea";
const AMOUNT = 5;
const BANKR_URL = "https://bankr.bankr.bot";
const BANKR_REF = "RN982CZZ-BNKR";

const pack = (code) => JSON.parse(readFileSync(join(PACK_DIR, `${code}.json`), "utf8"));

function styles() {
  return `    :root { color-scheme:dark; --ink:#e8eef4; --mut:#90a4ae; --line:rgba(100,181,246,.22); }
    * { box-sizing:border-box; margin:0; padding:0; }
    body { font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,sans-serif;
           background:linear-gradient(160deg,#071018 0%,#0f2740 45%,#071018 100%);
           color:var(--ink); min-height:100vh; display:flex; flex-direction:column; line-height:1.55; }
    a { color:#90caf9; }
    header { padding:1.1rem 1.5rem; border-bottom:1px solid var(--line); display:flex;
             align-items:center; justify-content:space-between; gap:1rem; flex-wrap:wrap; }
    header .brand { font-size:1.15rem; font-weight:650;
             background:linear-gradient(90deg,#64b5f6,#81c784); -webkit-background-clip:text;
             background-clip:text; -webkit-text-fill-color:transparent; text-decoration:none; }
    nav a { margin-inline-start:1rem; font-size:.92rem; text-decoration:none; }
    nav a:hover { text-decoration:underline; }
    main { flex:1; width:100%; max-width:960px; margin:0 auto; padding:2.25rem 1.5rem 3rem; }
    h1 { font-size:1.9rem; line-height:1.2; margin-bottom:.85rem; }
    h2 { font-size:1.2rem; margin:2rem 0 .75rem; }
    p { color:#c3ced8; margin-bottom:1rem; max-width:70ch; }
    .lede { font-size:1.05rem; }
    table { width:100%; border-collapse:collapse; margin:.5rem 0 1rem; font-size:.93rem; }
    th, td { text-align:start; padding:.55rem .6rem; border-bottom:1px solid var(--line); vertical-align:top; }
    th { color:var(--mut); font-weight:600; }
    code { background:rgba(0,0,0,.4); padding:.12rem .35rem; border-radius:5px; font-size:.87em;
           word-break:break-all; }
    .note { border-inline-start:3px solid #81c784; padding:.5rem 0 .5rem .9rem; color:var(--mut);
            font-size:.92rem; }
    .warn { border-inline-start:3px solid #ffb74d; padding:.5rem 0 .5rem .9rem; color:#ffcc80;
            font-size:.92rem; }
    .actions { display:flex; flex-wrap:wrap; gap:.7rem; margin:1.25rem 0 .4rem; align-items:center; }
    .btn { display:inline-block; padding:.62rem 1rem; border-radius:9px; background:#1976d2; color:#fff;
           text-decoration:none; font-weight:600; font-size:.94rem; border:0; cursor:pointer; }
    .btn.sec { background:transparent; border:1px solid rgba(144,202,249,.5); color:#90caf9; }
    .btn[disabled] { opacity:.6; cursor:progress; }
    input[type=text] { width:100%; max-width:34rem; padding:.55rem .7rem; border-radius:8px;
           border:1px solid var(--line); background:rgba(0,0,0,.35); color:var(--ink); font-size:.92rem; }
    label { display:block; font-size:.86rem; color:var(--mut); margin:.6rem 0 .3rem; }
    #receipt { margin-top:1.25rem; background:rgba(15,39,64,.62); border:1px solid var(--line);
           border-radius:14px; padding:1.15rem 1.25rem; }
    #receipt[hidden] { display:none; }
    #receipt dl { display:grid; grid-template-columns:auto 1fr; gap:.35rem .9rem; font-size:.93rem; }
    #receipt dt { color:var(--mut); }
    #receipt dd { word-break:break-all; }
    footer { padding:1rem 1.5rem; font-size:.8rem; color:#78909c; border-top:1px solid rgba(100,181,246,.15);
             display:flex; justify-content:space-between; gap:1rem; flex-wrap:wrap; }`;
}

function page(code, p) {
  const nav = `<a href="/${code === "en" ? "" : code + "/"}">${p.back_map}</a>`;
  return `<!DOCTYPE html>
<html lang="${code}"${p.dir === "rtl" ? ' dir="rtl"' : ""}>
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <!--ATL-SEO-->
  <style>
${styles()}
  </style>
</head>
<body>
  <header>
    <a class="brand" href="/${code === "en" ? "" : code}">Arctic Trade Lanes</a>
    <nav>${nav}</nav>
  </header>
  <main>
    <h1>${p.receipt_heading}</h1>
    <p class="lede">${p.step5_b}</p>

    <h2>${p.settle_heading}</h2>
    <table><tbody>
      <tr><td>${p.settle_amount_label}</td><td><strong>${p.settle_amount_value}</strong></td></tr>
      <tr><td>${p.settle_network_label}</td><td>${p.settle_network_value}</td></tr>
      <tr><td>${p.payto_label}</td><td><code>${PAY_TO}</code></td></tr>
      <tr><td>${p.bankr_label}</td><td><a href="${BANKR_URL}" rel="noopener">${BANKR_URL}</a> · ${p.refcode_label} <code>${BANKR_REF}</code></td></tr>
    </tbody></table>
    <p class="note"><span data-local-ref></span></p>
    <p class="warn">${p.currency_warn}</p>

    <h2>${p.header_label}</h2>
    <p>${p.header_note}</p>
    <table><tbody><tr><td><code data-header>${p.header_label}: x402:${PAY_TO}:${AMOUNT}</code></td></tr></tbody></table>

    <h2>${p.step4_t}</h2>
    <p>${p.step4_b}</p>
    <label for="tx">${p.receipt_txhash.replace("{tx}", "")}</label>
    <input id="tx" type="text" autocomplete="off" placeholder="0x…" />
    <div class="actions">
      <button class="btn" id="unlock" type="button">${p.unlock_cta}</button>
      <span class="note" data-hint>${p.unlock_hint}</span>
    </div>

    <section id="receipt" hidden aria-live="polite">
      <h2 style="margin-top:0">${p.receipt_heading}</h2>
      <dl data-receipt></dl>
      <div class="actions">
        <button class="btn sec" id="copy" type="button">${p.receipt_copy}</button>
        <span class="note" id="copied" hidden>${p.receipt_copied}</span>
      </div>
    </section>

    <p class="warn">${p.token_warn}</p>
    <h2>${p.contact_heading}</h2>
    <p>${p.contact_line}</p>
  </main>
  <footer>
    <span>${p.footer_tag}</span>
    <span>EPSG:3996 · ${p.settle_network_value}</span>
  </footer>
  <script type="application/json" id="pack">${JSON.stringify(p).replace(/</g, "\\u003c")}</script>
  <script>
  (function () {
    var pack = JSON.parse(document.getElementById("pack").textContent);
    var PAY_TO = ${JSON.stringify(PAY_TO)};
    var AMOUNT = ${AMOUNT};
    var header = "x402:" + PAY_TO + ":" + AMOUNT;
    document.querySelector("[data-header]").textContent = pack.header_label + ": " + header;

    var local = pack.settle_local_format
      .replace("{amount}", String(Math.round(AMOUNT * pack.local_per_usd * 100) / 100))
      .replace("{currency}", pack.local_currency);
    document.querySelector("[data-local-ref]").textContent =
      pack.settle_local_label + ": " + local + " — " + pack.settle_local_note;

    var render = function (r) {
      var rows = [
        [pack.receipt_amount.replace("{amount}", r.amount), ""],
        [pack.receipt_network.replace("{network}", r.network), ""],
        [pack.receipt_payto.replace("{payto}", r.payTo), ""],
        [r.txHash ? pack.receipt_txhash.replace("{tx}", r.txHash) : pack.receipt_txhash_none, ""],
        [pack.receipt_status.replace("{status}", pack.receipt_status_alpha), ""],
        [pack.receipt_time.replace("{time}", r.issuedAt), ""]
      ];
      var dl = document.querySelector("[data-receipt]");
      dl.textContent = "";
      rows.forEach(function (row) {
        var dt = document.createElement("dt");
        var dd = document.createElement("dd");
        dt.textContent = row[0];
        dd.textContent = row[1];
        dl.appendChild(dt);
        dl.appendChild(dd);
      });
      return {
        ok: true, amount: r.amount, currency: "USDC", network: r.network,
        chainId: 8453, payTo: r.payTo, txHash: r.txHash || null,
        status: "alpha", issuedAt: r.issuedAt, locale: pack.locale
      };
    };

    var btn = document.getElementById("unlock");
    var out = document.getElementById("receipt");
    var hint = document.querySelector("[data-hint]");
    var last = null;

    btn.addEventListener("click", function () {
      btn.disabled = true;
      hint.textContent = pack.unlock_busy;
      var body = { slug: "receipt", txHash: document.getElementById("tx").value.trim() || null };
      fetch("/api/x402/fulfill", {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json", "x402-payment": header, "Accept-Language": pack.locale },
        body: JSON.stringify(body)
      }).then(function (res) {
        return res.json().then(function (data) { return { ok: res.ok, data: data }; });
      }).then(function (r) {
        if (!r.ok) { hint.textContent = pack.err_need_header; return; }
        var receipt = r.data.receipt || {};
        last = render({
          amount: receipt.amountText || "5.00 USDC",
          network: receipt.network || pack.settle_network_value,
          payTo: receipt.payTo || PAY_TO,
          txHash: receipt.txHash || body.txHash,
          issuedAt: receipt.issuedAt || new Date().toISOString()
        });
        out.hidden = false;
        hint.textContent = r.data.receiptText || pack.unlock_hint;
      }).catch(function () {
        hint.textContent = pack.err_network;
      }).finally(function () {
        btn.disabled = false;
      });
    });

    document.getElementById("copy").addEventListener("click", function () {
      if (!last) return;
      navigator.clipboard.writeText(JSON.stringify(last, null, 2)).then(function () {
        var c = document.getElementById("copied");
        c.hidden = false;
        setTimeout(function () { c.hidden = true; }, 1800);
      });
    });
  })();
  </script>
</body>
</html>
`;
}

const codes = readdirSync(PACK_DIR)
  .filter((f) => f.endsWith(".json") && f !== "index.json")
  .map((f) => f.replace(/\.json$/, ""))
  .sort();

let written = 0;
for (const code of codes) {
  const p = pack(code);
  const dir = code === "en" ? OUT_ROOT : join(OUT_ROOT, code);
  mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, "receipt.html"), page(code, p));
  written += 1;
}
console.log(`[receipt] wrote ${written} locale receipt page(s) to public/<lang>/receipt.html`);
