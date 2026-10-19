/* ArcticTradeLanes.com — localized x402 receipt client.
 *
 * Server-rendered copy only: every string comes from the page's locale pack, so
 * this file stays language-neutral and can never leak English onto the money
 * surface. The unlock posts the same x402-payment header the page shows and
 * renders the receipt lines the server localises for this locale.
 */
(function () {
  "use strict";

  var boot = window.__ATL_X402__;
  if (!boot || !boot.t) return;

  var t = boot.t;
  var $ = function (id) { return document.getElementById(id); };

  var suppliedTx = "";
  try {
    suppliedTx = new URLSearchParams(window.location.search).get("tx") || "";
  } catch (e) { /* no location: stay empty */ }
  if (suppliedTx && !/^0x[0-9a-fA-F]{16,}$/.test(suppliedTx)) suppliedTx = "";

  var lastReceipt = null;

  function payloadBox() {
    var box = $("payload");
    if (box) box.hidden = false;
  }

  /* Money strings, addresses and ISO timestamps must not be re-ordered by the
   * bidi algorithm on an RTL page: "5.00 USDC" otherwise renders as "USDC 5.00"
   * and a hash or timestamp is split in the middle. Each such run is isolated
   * as an LTR <bdi>; the surrounding sentence keeps the page direction. */
  var LTR_RUN = /(0x[0-9a-fA-F]{16,}|\d{4}-\d{2}-\d{2}T[\d:.]+Z|\d+(?:[.,]\d+)?\s*USDC)/g;

  function lineNode(text) {
    var el = document.createElement("li");
    var parts = String(text).split(LTR_RUN);
    for (var i = 0; i < parts.length; i += 1) {
      if (!parts[i]) continue;
      if (i % 2 === 1) {
        var b = document.createElement("bdi");
        b.setAttribute("dir", "ltr");
        b.textContent = parts[i];
        el.appendChild(b);
      } else {
        el.appendChild(document.createTextNode(parts[i]));
      }
    }
    return el;
  }

  function renderLines(lines) {
    var box = $("r-lines");
    if (!box) return;
    box.textContent = "";
    /* Line 0 is the pack's receipt heading, which the page already shows above
     * the unlock button. Repeating it as a bullet reads like a duplicated row. */
    var start = lines.length > 1 && lines[0] === t.receiptHeading ? 1 : 0;
    for (var i = start; i < lines.length; i += 1) {
      box.appendChild(lineNode(lines[i]));
    }
  }

  function fallbackLines(receipt) {
    var payment = (receipt && receipt.payment) || {};
    var tx = receipt.txHash || payment.txHash || payment.transactionHash || suppliedTx || "";
    var status = receipt.statusText || t.receiptStatusAlpha;
    var out = [
      t.receiptAmount.replace("{amount}", receipt.amountText || t.amount),
      t.receiptNetwork.replace("{network}", receipt.networkText || t.network),
      t.receiptPayto.replace("{payto}", receipt.payTo || boot.payTo),
      (tx ? t.receiptTxhash.replace("{tx}", tx) : t.receiptTxhashNone),
      t.receiptStatus.replace("{status}", status)
    ];
    var when = receipt.issuedAt || receipt.ts || "";
    if (when) out.push(t.receiptTime.replace("{time}", when));
    return out;
  }

  function render(receipt) {
    lastReceipt = receipt;
    var lines = receipt && receipt.lines && receipt.lines.length ? receipt.lines : fallbackLines(receipt || {});
    renderLines(lines);
    var section = $("receipt");
    if (section) section.hidden = false;
    var err = $("r-err");
    if (err) err.hidden = true;
  }

  function fail(message) {
    var err = $("r-err");
    if (!err) return;
    err.textContent = message;
    err.hidden = false;
  }

  var unlock = $("unlock");
  if (unlock) {
    unlock.addEventListener("click", function () {
      var original = unlock.textContent;
      unlock.disabled = true;
      unlock.textContent = t.busy;
      var slug = "corridor-route-intelligence";
      try {
        var q = new URLSearchParams(window.location.search).get("slug");
        if (q) slug = q;
      } catch (e) { /* ignore */ }

      fetch(boot.endpoint + "?slug=" + encodeURIComponent(slug) + "&lang=" + encodeURIComponent(boot.locale), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Accept": "application/json",
          "Accept-Language": boot.locale,
          "x402-payment": boot.header
        },
        body: JSON.stringify({ slug: slug, locale: boot.locale })
      })
        .then(function (r) {
          return r.text().then(function (body) {
            var data = null;
            try { data = JSON.parse(body); } catch (e) { data = null; }
            return { ok: r.ok, status: r.status, data: data };
          });
        })
        .then(function (res) {
          if (!res.data || res.data.ok !== true || !res.data.receipt) {
            fail(t.errHeader);
            return;
          }
          render(res.data.receipt);
          payloadBox();
        })
        .catch(function () { fail(t.errNetwork); })
        .then(function () {
          unlock.disabled = false;
          unlock.textContent = original;
        });
    });
  }

  var copy = $("copy");
  if (copy) {
    copy.addEventListener("click", function () {
      var text = JSON.stringify(
        lastReceipt || { locale: boot.locale, payTo: boot.payTo, amount: boot.amount, network: boot.network },
        null,
        2
      );
      var done = function () {
        copy.textContent = t.receiptCopied;
        setTimeout(function () { copy.textContent = t.receiptCopy; }, 1800);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, function () {});
      } else {
        var ta = document.createElement("textarea");
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand("copy"); done(); } catch (e) { /* ignore */ }
        document.body.removeChild(ta);
      }
    });
  }

  /* Deep link with a known hash (Bankr share links carry ?tx=) renders the
   * receipt immediately instead of making the buyer press unlock again. */
  if (suppliedTx) {
    render({
      amountText: t.amount,
      networkText: t.network,
      payTo: boot.payTo,
      issuedAt: "",
      txHash: suppliedTx,
      payment: { headerPresent: true, wellFormed: true, verifiedOnchain: false }
    });
    payloadBox();
  }
})();
