#!/usr/bin/env python3
"""Generate neutral /people index + /people/<slug> pages for ArcticTradeLanes.com (22 locales).

Templates only: strings from src/home/home-extras.i18n.json, facts from src/home/home-extras.data.json.
Policy: neutral profiles (name, public role, Arctic relevance, UM radar link, related atlas pages).
NO ads, NO payment, NO token, NO sanctions wording or links on these pages.

Usage (from app root): python3 site/people-pages/build_people_pages.py [--out pages] [--routes factpages/.routes.json]
Writes pages/[<lc>/]people.html, pages/[<lc>/]people/<slug>.html and pages/sitemap-people.xml.
"""
import argparse, html, json, os, re, sys

ORIGIN = "https://arctictradelanes.com"
LOCALES = ["en","ru","zh","ja","ko","el","de","nl","fr","es","it","pt","tr","ar","hi","vi","id","da","fi","sv","nb","is"]
UM_LANGS = {"ru","zh"}
BANNED = re.compile(r"sanction|ofac|sdn list|restricted[- ]list|embargo", re.I)

ap = argparse.ArgumentParser()
ap.add_argument("--root", default=".")
ap.add_argument("--out", default="pages")
ap.add_argument("--routes", default="factpages/.routes.json")
ap.add_argument("--date", default="2026-10-18")
a = ap.parse_args()
root = a.root
I18N = json.load(open(os.path.join(root, "src/home/home-extras.i18n.json"), encoding="utf-8"))
DATA = json.load(open(os.path.join(root, "src/home/home-extras.data.json"), encoding="utf-8"))
routes = set()
rp = os.path.join(root, a.routes)
if os.path.exists(rp):
    routes = set(json.load(open(rp, encoding="utf-8"))["routes"].keys())

e = lambda s: html.escape(s, quote=True)
pre = lambda l: "" if l == "en" else "/" + l
tri = lambda v, l: v.get(l) or v["en"]
um = lambda slug, l: f"https://unicornsmap.com/{l + '/' if l in UM_LANGS else ''}radar/{slug}"
def T(l): d = dict(I18N["en"]); d.update(I18N.get(l, {})); return d

def route_ok(path, l):
    if not routes: return True
    full = path if l == "en" else f"/{l}{path}"
    return full in routes

CSS = """*{box-sizing:border-box}body{margin:0;background:#0b1220;color:#e5edf7;font:16px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,"Noto Sans",sans-serif}
a{color:#22d3ee;text-decoration:none}a:hover{text-decoration:underline}header{border-bottom:1px solid #1f2d44;background:#0a1626}
.w{max-width:960px;margin:0 auto;padding:0 16px}header .w{display:flex;gap:14px;align-items:center;justify-content:space-between;padding:12px 16px;flex-wrap:wrap}
.brand{font-weight:700;color:#22d3ee}main{padding:28px 0 56px}h1{font-size:clamp(24px,4vw,36px);line-height:1.2;margin:0 0 8px;color:#fff}
.role{font-size:18px;margin:0 0 16px}.card{background:#111a2b;border:1px solid #1f2d44;border-radius:14px;padding:16px;margin:0 0 14px;overflow-wrap:anywhere}
.card h2{font-size:14px;text-transform:uppercase;letter-spacing:.05em;color:#9fb0c6;margin:0 0 8px}.card p{margin:0}
ul.l{margin:0;padding-inline-start:18px}.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr))}
.grid .card h2{font-size:17px;text-transform:none;letter-spacing:0;color:#fff}.mute{color:#9fb0c6;font-size:14px}
.langs{display:flex;flex-wrap:wrap;gap:6px;font-size:12px;margin-top:22px}.langs a{padding:3px 8px;border:1px solid #1f2d44;border-radius:6px;color:#9fb0c6}
footer{border-top:1px solid #1f2d44;padding:18px 0;color:#9fb0c6;font-size:13px}"""

NAMES = {"en":"English","ru":"Русский","zh":"中文","ja":"日本語","ko":"한국어","el":"Ελληνικά","de":"Deutsch","nl":"Nederlands","fr":"Français","es":"Español","it":"Italiano","pt":"Português","tr":"Türkçe","ar":"العربية","hi":"हिन्दी","vi":"Tiếng Việt","id":"Bahasa Indonesia","da":"Dansk","fi":"Suomi","sv":"Svenska","nb":"Norsk bokmål","is":"Íslenska"}

def alternates(path):
    out = [f'<link rel="alternate" hreflang="{l}" href="{ORIGIN}{pre(l)}{path}">' for l in LOCALES]
    out.append(f'<link rel="alternate" hreflang="x-default" href="{ORIGIN}{path}">')
    return "\n".join(out)

def langbar(path):
    return '<nav class="langs" aria-label="Languages">' + "".join(f'<a href="{pre(l)}{path}" hreflang="{l}" lang="{l}">{NAMES[l]}</a>' for l in LOCALES) + "</nav>"

def page(l, path, title, desc, body, ld):
    s = T(l)
    return f"""<!doctype html>
<html lang="{l}" dir="{'rtl' if l == 'ar' else 'ltr'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta name="robots" content="index,follow">
<link rel="canonical" href="{ORIGIN}{pre(l)}{path}">
{alternates(path)}
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{ORIGIN}{pre(l)}{path}"><meta property="og:type" content="profile">
<link rel="icon" href="/favicon.svg">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False).replace('<', '\\u003c')}</script>
</head><body>
<header><div class="w"><a class="brand" href="{pre(l) or '/'}">ArcticTradeLanes.com</a><a href="{pre(l) or '/'}">{e(s['pp_map'])}</a></div></header>
<main><div class="w">
{body}
{langbar(path)}
</div></main>
<footer><div class="w">{e(s['pp_note'])}</div></footer>
</body></html>
"""

def crumbs(l, items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}

written, urls = [], []
for l in LOCALES:
    s = T(l)
    base = os.path.join(root, a.out, "" if l == "en" else l)
    os.makedirs(os.path.join(base, "people"), exist_ok=True)
    home = f"{ORIGIN}{pre(l) or '/'}"
    # index
    cards = []
    for p in DATA["people"]:
        cards.append(f'<div class="card"><h2><a href="{pre(l)}/people/{p["slug"]}">{e(tri(p["name"], l))}</a></h2><p class="role">{e(tri(p["role"], l))}</p><p class="mute">{e(tri(p["rel"], l))}</p></div>')
    body = f'<h1>{e(s["ppl_h"])}</h1><p class="mute">{e(s["ppl_lede"])}</p><div class="grid">{"".join(cards)}</div>'
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": s["ppl_h"], "url": f"{ORIGIN}{pre(l)}/people", "inLanguage": l,
         "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{ORIGIN}{pre(l)}/people/{p['slug']}", "name": tri(p["name"], l)} for i, p in enumerate(DATA["people"])]}},
        crumbs(l, [("ArcticTradeLanes.com", home), (s["ppl_h"], f"{ORIGIN}{pre(l)}/people")])]}
    out = page(l, "/people", s["pp_index_title"], s["ppl_lede"], body, ld)
    f = os.path.join(base, "people.html"); open(f, "w", encoding="utf-8").write(out); written.append(f)
    # person pages
    for p in DATA["people"]:
        name, role, rel = tri(p["name"], l), tri(p["role"], l), tri(p["rel"], l)
        rel_links = []
        for path, label in p["related"]:
            if not route_ok(path, l): continue
            if label is None:
                label = s.get("fx_" + path.strip("/"), path.strip("/"))
            rel_links.append(f'<li><a href="{pre(l)}{path}">{e(label)}</a></li>')
        body = (f'<h1>{e(name)}</h1><p class="role">{e(role)}</p>'
                f'<div class="card"><h2>{e(s["pp_rel"])}</h2><p>{e(rel)}</p></div>'
                f'<div class="card"><h2>{e(s["pp_related"])}</h2><ul class="l">{"".join(rel_links)}<li><a href="{pre(l) or "/"}">{e(s["pp_map"])}</a></li></ul></div>'
                f'<div class="card"><h2>{e(s["ppl_radar"])}</h2><p><a href="{um(p["slug"], l)}" rel="noopener">{e(um(p["slug"], l).replace("https://", ""))}</a></p></div>'
                f'<p><a href="{pre(l)}/people">← {e(s["pp_back"])}</a></p>')
        ld = {"@context": "https://schema.org", "@graph": [
            {"@type": "Person", "name": name, "alternateName": [v for k, v in p["name"].items() if v != name], "jobTitle": role, "description": rel,
             "url": f"{ORIGIN}{pre(l)}/people/{p['slug']}", "sameAs": [um(p["slug"], "en")]},
            {"@type": "ProfilePage", "url": f"{ORIGIN}{pre(l)}/people/{p['slug']}", "inLanguage": l, "dateModified": a.date},
            crumbs(l, [("ArcticTradeLanes.com", home), (s["ppl_h"], f"{ORIGIN}{pre(l)}/people"), (name, f"{ORIGIN}{pre(l)}/people/{p['slug']}")])]}
        out = page(l, f"/people/{p['slug']}", f"{name} · {role} · ArcticTradeLanes.com", f"{name}: {role}. {rel}", body, ld)
        f = os.path.join(base, "people", p["slug"] + ".html"); open(f, "w", encoding="utf-8").write(out); written.append(f)

# sitemap with hreflang alternates
paths = ["/people"] + [f"/people/{p['slug']}" for p in DATA["people"]]
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for path in paths:
    alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{ORIGIN}{pre(l)}{path}"/>' for l in LOCALES) + f'<xhtml:link rel="alternate" hreflang="x-default" href="{ORIGIN}{path}"/>'
    for l in LOCALES:
        sm.append(f"<url><loc>{ORIGIN}{pre(l)}{path}</loc><lastmod>{a.date}</lastmod>{alts}</url>")
sm.append("</urlset>")
open(os.path.join(root, a.out, "sitemap-people.xml"), "w", encoding="utf-8").write("\n".join(sm) + "\n")

bad = [f for f in written if BANNED.search(open(f, encoding="utf-8").read())]
if bad:
    print("BANNED WORDING IN:", bad); sys.exit(2)
print(f"wrote {len(written)} pages + sitemap-people.xml ({len(paths) * len(LOCALES)} urls)")
