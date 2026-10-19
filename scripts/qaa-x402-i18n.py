#!/usr/bin/env python3
"""Hard QAA for the localized x402 money surface.

Covers, for every shipped locale:
  * /<lc>/x402/pay      — copy, head, hreflang, money contract, no English leak
  * /<lc>/receipt       — head, no-hash guard
  * /<lc>/              — the CTA band that makes the pay sheet reachable
  * /api/x402/fulfill   — localized receipt via ?lang, body locale and Accept-Language
  * negative paths      — 402 without a well-formed x402-payment header

Usage:
  python3 scripts/qaa-x402-i18n.py                     # local listener
  ATL_BASE=https://arctictradelanes.com python3 ...    # production

Exit code is non-zero if any check fails. Nothing here is advisory.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request

BASE = os.environ.get("ATL_BASE", "http://127.0.0.1:51927")
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACKS = os.path.join(REPO, "public/x402/i18n")
WALLET = "0x211D91beD006f7bB3Eaf97496260a8F905298Cea"
HEADER = f"x402:{WALLET}:5"
UA = {
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0 Safari/537.36",
    "accept": "text/html,application/json;q=0.9,*/*;q=0.8",
    "accept-language": "en-US,en;q=0.9",
}

LEAKS = [
    "Amount paid", "Network:", "Paid to:", "Transaction hash", "What you pay",
    "Request header", "Copy receipt as JSON", "Unlock the payload", "Step ",
    "Back to the live map", "Payment Required", "not supplied", "Recorded ",
    "Receipt", "Unlocking",
]

SEP = {
    "en": (",", "."), "zh": (",", "."), "ja": (",", "."), "ko": (",", "."),
    "hi": (",", "."), "ar": (",", "."),
    "de": (".", ","), "nl": (".", ","), "es": (".", ","), "it": (".", ","),
    "pt": (".", ","), "da": (".", ","), "sv": (" ", ","), "nb": (" ", ","),
    "fi": (" ", ","), "is": (".", ","), "ru": (" ", ","), "tr": (".", ","),
    "el": (".", ","), "fr": ("\u202f", ","), "id": (".", ","), "vi": (".", ","),
}

failures = []
checks = 0


def check(cond, label):
    global checks
    checks += 1
    if not cond:
        failures.append(label)


def fetch(path, headers=None, data=None):
    req = urllib.request.Request(
        BASE + path, data=data, headers={**UA, **(headers or {})},
        method="POST" if data is not None else "GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, r.read().decode("utf-8", "replace"), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace"), dict(e.headers)


def post(path, headers, body):
    return fetch(path, headers, json.dumps(body).encode())


def money(lang, value):
    """Mirror the page builder: integers stay integers, fractional quotes keep 2 dp."""
    thou, dec = SEP.get(lang, (",", "."))
    if abs(value - round(value)) < 1e-9:
        whole, frac = str(int(round(value))), ""
    else:
        whole, frac = f"{value:.2f}".split(".")
    grouped = ""
    while len(whole) > 3:
        grouped = thou + whole[-3:] + grouped
        whole = whole[:-3]
    return f"{whole}{grouped}{dec}{frac}" if frac else f"{whole}{grouped}"


def body_text(html):
    body = html.split("</head>", 1)[1] if "</head>" in html else html
    body = re.sub(r"<script.*?</script>", " ", body, flags=re.S)
    body = re.sub(r"<style.*?</style>", " ", body, flags=re.S)
    return re.sub(r"<[^>]+>", " ", body)


langs = sorted(f[:-5] for f in os.listdir(PACKS) if f.endswith(".json") and not f.startswith("_"))
check(len(langs) == 22, f"expected 22 locale packs, found {len(langs)}")

for lang in langs:
    with open(os.path.join(PACKS, f"{lang}.json"), encoding="utf-8") as fh:
        p = json.load(fh)
    prefix = "" if lang == "en" else f"/{lang}"

    # --- pay sheet --------------------------------------------------------
    path = prefix + "/x402/pay"
    status, html, _ = fetch(path)
    check(status == 200, f"{path}: status {status}")
    check(f'<html lang="{lang}"' in html, f"{path}: html lang not {lang}")
    check(('dir="rtl"' in html) == (lang == "ar"), f"{path}: dir mismatch")
    check(f'href="https://arctictradelanes.com{path}"' in html, f"{path}: canonical wrong")
    check("noindex" not in html, f"{path}: noindex on a shipped translation")
    check(html.count("hreflang=") == 23, f"{path}: hreflang count {html.count('hreflang=')}")
    check('hreflang="x-default"' in html, f"{path}: no x-default")
    title = re.search(r"<title>(.*?)</title>", html, re.S)
    check(bool(title) and p["h1"] in title.group(1), f"{path}: title not localized")
    text = body_text(html)
    check(p["h1"] in text, f"{path}: h1 missing from body")
    if lang != "en":
        leaked = [w for w in LEAKS if w in text]
        check(not leaked, f"{path}: English leaked {leaked[:3]}")
    check("5.00 USDC" in text, f"{path}: amount not 5.00 USDC")
    check("chainId 8453" in text, f"{path}: chain id missing")
    check(f"x402-payment: {HEADER}" in html, f"{path}: request header missing")
    check(WALLET in text, f"{path}: payTo not shown in full")
    check("https://bankr.bot?ref=um-radar" in html, f"{path}: bankr affiliate link missing")
    rate = float(p.get("local_per_usd") or 0)
    expected = money(lang, 5 * rate) if rate else ""
    check(bool(expected) and expected in text, f"{path}: local reference {expected} not shown")
    check(p.get("local_currency", "") in text, f"{path}: local currency code missing")
    check("{" not in body_text(html).replace("{{", ""), f"{path}: unresolved placeholder")
    check(f'"header": "{HEADER}"' in html, f"{path}: boot header wrong")
    check(f'"locale": "{lang}"' in html, f"{path}: boot locale wrong")
    check(f'href="{prefix}/x402/pay"' in html, f"{path}: nav self-link wrong")

    # --- receipt page -----------------------------------------------------
    path = prefix + "/receipt"
    status, html, _ = fetch(path)
    check(status == 200, f"{path}: status {status}")
    check(f'<html lang="{lang}"' in html, f"{path}: html lang not {lang}")
    check(f'href="https://arctictradelanes.com{path}"' in html, f"{path}: canonical wrong")
    check(p["receipt_heading"] in body_text(html), f"{path}: heading missing")
    check("location.replace" in html, f"{path}: missing no-hash guard")
    check(f"{prefix}/x402/pay" in html, f"{path}: guard target wrong")

    # --- home CTA band ----------------------------------------------------
    status, html, _ = fetch(prefix + "/" if prefix else "/")
    check(status == 200, f"home {lang}: status {status}")
    check("data-atlx-pay" in html, f"home {lang}: no x402 CTA band")
    check(f'href="{prefix}/x402/pay"' in html, f"home {lang}: CTA href wrong")
    check(p["h1"] in html, f"home {lang}: CTA label not localized")

    # --- fulfill API ------------------------------------------------------
    tx = "0x" + "a" * 64
    st, raw, _ = post(
        f"/api/x402/fulfill?slug=qaa-{lang}&lang={lang}&tx={tx}",
        {"content-type": "application/json", "x402-payment": HEADER, "accept-language": lang},
        {"slug": f"qaa-{lang}", "locale": lang},
    )
    check(st == 200, f"{lang}: fulfill status {st}")
    try:
        d = json.loads(raw)
    except Exception:
        d = {}
        check(False, f"{lang}: fulfill returned non-JSON")
    check(d.get("locale") == lang, f"{lang}: receipt locale {d.get('locale')}")
    lines = d.get("receipt", {}).get("lines", [])
    check(len(lines) == 7, f"{lang}: receipt line count {len(lines)}")
    check(bool(lines) and lines[0] == p["receipt_heading"], f"{lang}: receipt heading not localized")
    check("5.00 USDC" in " ".join(lines), f"{lang}: receipt amount not 5.00 USDC")
    check(any(tx in line for line in lines), f"{lang}: tx hash dropped from receipt")
    check(d.get("receipt", {}).get("verifiedOnchain") is False, f"{lang}: receipt overclaims settlement")
    check(bool(d.get("waypoints") or d.get("corridor")), f"{lang}: payload missing from fulfill")

# --- header negotiation without ?lang (what the page actually sends) -------
for lang, tag in (("ja", "ja-JP,ja;q=0.9"), ("de", "de-AT,de;q=0.9"), ("ar", "ar-AE,ar;q=0.9"),
                  ("is", "is-IS"), ("pt", "pt-BR"), ("zh", "zh-TW")):
    with open(os.path.join(PACKS, f"{lang}.json"), encoding="utf-8") as fh:
        p = json.load(fh)
    st, raw, _ = post("/api/x402/fulfill",
                      {"content-type": "application/json", "x402-payment": HEADER,
                       "accept-language": tag}, {})
    try:
        d = json.loads(raw)
    except Exception:
        d = {}
    check(st == 200 and d.get("locale") == lang, f"negotiate {tag}: {st} {d.get('locale')}")
    check(d.get("receipt", {}).get("lines", [""])[0] == p["receipt_heading"],
          f"negotiate {tag}: heading not localized")

# --- negative paths -------------------------------------------------------
st, _, _ = post("/api/x402/fulfill", {"content-type": "application/json"}, {})
check(st == 402, f"no header should be 402, got {st}")
st, _, _ = post("/api/x402/fulfill",
                {"content-type": "application/json", "x402-payment": "x402:0xdeadbeef:7"}, {})
check(st == 402, f"wrong amount should be 402, got {st}")
st, _, _ = post("/api/x402/fulfill",
                {"content-type": "application/json", "x402-payment": "pay:5"}, {})
check(st == 402, f"non-x402 header should be 402, got {st}")

# --- untouched surfaces ---------------------------------------------------
for path in ("/", "/ja", "/pricing", "/ja/pricing", "/collaborate", "/arctic-economic-atlas",
             "/.well-known/x402.json", "/api/x402/status", "/api/x402/schema"):
    st, _, _ = fetch(path)
    check(st == 200, f"{path}: regression {st}")

# --- the money surface stays out of the sitemap ---------------------------
st, sitemap, _ = fetch("/sitemap.xml")
if st == 200:
    check("/x402/pay" not in sitemap, "sitemap advertises the private pay sheet")

print(f"{checks - len(failures)}/{checks} checks passed")
for f in failures:
    print("FAIL", f)
sys.exit(1 if failures else 0)
