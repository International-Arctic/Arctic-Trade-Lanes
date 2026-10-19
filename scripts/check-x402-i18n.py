#!/usr/bin/env python3
"""Gate for the x402 pay-sheet locale packs.

    python3 scripts/check-x402-i18n.py ja ru zh        # explicit locales
    python3 scripts/check-x402-i18n.py --all           # every pack on disk

Checks, per locale:
  * parses as a JSON object
  * identical key set AND identical key order to en.json
  * locale / local_currency / local_symbol / local_per_usd match the fixed FX snapshot
  * every {placeholder} that en.json uses is still present in that key
  * settlement tokens (USDC / Base / x402 / chainId 8453 / Bankr / payTo / $ATL …) survive
  * the money-truth keys are genuinely translated (not byte-identical to English)
Exit code 0 only when every requested locale is green.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

I18N = Path(__file__).resolve().parent.parent / "public" / "x402" / "i18n"

FX = {
    "en": ("USD", "$", 1), "ja": ("JPY", "¥", 152), "ru": ("RUB", "₽", 92.5),
    "zh": ("CNY", "¥", 7.24), "ko": ("KRW", "₩", 1390), "el": ("EUR", "€", 0.92),
    "de": ("EUR", "€", 0.92), "nl": ("EUR", "€", 0.92), "fr": ("EUR", "€", 0.92),
    "es": ("EUR", "€", 0.92), "it": ("EUR", "€", 0.92), "pt": ("EUR", "€", 0.92),
    "fi": ("EUR", "€", 0.92), "tr": ("TRY", "₺", 34.2), "ar": ("AED", "د.إ", 3.67),
    "hi": ("INR", "₹", 83.4), "vi": ("VND", "₫", 25400), "id": ("IDR", "Rp", 16200),
    "da": ("DKK", "kr", 6.85), "sv": ("SEK", "kr", 10.45), "nb": ("NOK", "kr", 10.75),
    "is": ("ISK", "kr", 138),
}

VERBATIM = {
    "settle_amount_value": "5.00 USDC",
    "settle_network_value": "Base · chainId 8453",
    "payto_label": "payTo",
    "nav_github": "GitHub",
    "bankr_label": "Bankr",
    "contact_line": "collaborate@arctictradelanes.com · partners@arctictradelanes.com",
}

# Tokens that must survive somewhere in the translated prose when EN uses them.
TOKEN_KEYS = {
    "h1": ["USDC", "x402"],
    "lede": ["Bankr", "Base"],
    "settle_amount_value": ["5.00 USDC"],
    "settle_network_value": ["Base", "8453"],
    "bankr_cta": ["Bankr", "USDC"],
    "step2_b": ["@bankrbot", "USDC", "Base"],
    "step3_b": ["USDC", "Base", "8453"],
    "step4_b": ["USDC", "Base"],
    "header_note": ["x402:<payTo>:<amount>", "/api/x402/fulfill"],
    "err_need_header": ["x402:<payTo>:5"],
    "token_warn": ["$ATL", "USDC", "Base"],
}

# English byte-identical values here are a defect: these are prose, not tokens.
MUST_TRANSLATE = [
    "h1", "lede", "settle_heading", "settle_local_label", "settle_local_note",
    "currency_warn", "bankr_cta", "steps_heading", "steps_intro", "step1_t", "step1_b",
    "step2_t", "step2_b", "step3_t", "step3_b", "step4_t", "step4_b", "step5_t",
    "step5_b", "header_label", "unlock_cta", "unlock_busy", "unlock_hint",
    "receipt_heading", "receipt_status_alpha", "err_need_header", "err_network",
    "token_warn", "contact_heading", "back_map", "footer_tag", "nav_collaborate",
    "nav_pricing", "nav_atlas", "settle_amount_label", "settle_network_label",
    "settle_local_format", "receipt_amount", "receipt_network", "receipt_payto",
    "receipt_txhash", "receipt_txhash_none", "receipt_status", "receipt_time",
    "receipt_copy", "receipt_copied", "discovery_label", "refcode_label",
]

PLACEHOLDER = re.compile(r"\{([a-z]+)\}")

# Values that legitimately read the same in every locale.
ALLOW_SAME = set(VERBATIM) | {
    "locale", "local_currency", "local_symbol", "local_per_usd", "dir",
}


def placeholders(value: str) -> list[str]:
    return sorted(PLACEHOLDER.findall(value))


def check(code: str, en: dict) -> list[str]:
    path = I18N / f"{code}.json"
    if not path.exists():
        return [f"{code}.json does not exist"]
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return [f"{code}.json is not valid JSON: {exc}"]
    if not isinstance(data, dict):
        return [f"{code}.json is not a JSON object"]

    fail: list[str] = []

    if list(data.keys()) != list(en.keys()):
        missing = [k for k in en if k not in data]
        extra = [k for k in data if k not in en]
        if missing:
            fail.append(f"missing keys: {', '.join(missing)}")
        if extra:
            fail.append(f"extra keys: {', '.join(extra)}")
        if not missing and not extra:
            fail.append("key order differs from en.json")

    ccy, sym, rate = FX.get(code, ("?", "?", 0))
    for key, want in (("locale", code), ("local_currency", ccy),
                      ("local_symbol", sym), ("local_per_usd", rate)):
        if data.get(key) != want:
            fail.append(f"{key}={data.get(key)!r} expected {want!r}")

    for key, want in VERBATIM.items():
        if key in en and data.get(key) != want:
            fail.append(f"{key} must stay {want!r}, got {data.get(key)!r}")

    for key, value in en.items():
        if not isinstance(value, str):
            continue
        got = data.get(key)
        if not isinstance(got, str):
            continue
        for ph in placeholders(value):
            if f"{{{ph}}}" not in got:
                fail.append(f"{key} lost placeholder {{{ph}}}")

    for key, tokens in TOKEN_KEYS.items():
        got = data.get(key, "")
        if not isinstance(got, str):
            continue
        for token in tokens:
            if token not in got:
                fail.append(f"{key} lost token {token!r}")

    for key in MUST_TRANSLATE:
        if key in en and key not in ALLOW_SAME and data.get(key) == en.get(key):
            fail.append(f"{key} is identical to English (untranslated)")

    if len(set(map(str, data.values()))) < 20:
        fail.append("too few distinct values — looks like a stub")

    return fail


def main(argv: list[str]) -> int:
    en_path = I18N / "en.json"
    if not en_path.exists():
        print(f"FAIL en.json missing at {en_path}")
        return 2
    en = json.loads(en_path.read_text(encoding="utf-8"))

    if not argv or argv == ["--all"]:
        codes = sorted(p.stem for p in I18N.glob("*.json") if p.stem != "en")
    else:
        codes = [a for a in argv if a != "en"]

    rc = 0
    for code in codes:
        problems = check(code, en)
        if problems:
            rc = 1
            print(f"FAIL {code}")
            for problem in problems[:12]:
                print(f"     - {problem}")
        else:
            print(f"OK   {code} — {len(en)} keys, placeholders + tokens intact")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
