#!/usr/bin/env python3
"""ArcticTradeLanes.com static /funding and /advertise pages (restored 2026-10-18).

Restores the two Oct 2026 SPA routes as standalone, server-rendered HTML so they do not depend on the
lost React source. Content is ported from the Oct 6 SPA bundle (assets/index-atlr3-oct6.js: Fk funding
page, jk advertise page). Funding rows come from data/arctic-funding-programs-2026.csv (42 rows).

Usage: python3 build_pages.py [csv] [outdir] [build-date YYYY-MM-DD]
Writes outdir/funding.html, outdir/advertise.html and outdir/<lc>/{funding,advertise}.html for 21 locales.
"""
import csv, html, json, os, sys, datetime as dt

CSV = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "arctic-funding-programs-2026.csv")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(__file__), "pages")
TODAY = dt.date.fromisoformat(sys.argv[3]) if len(sys.argv) > 3 else dt.date.today()
SITE = "https://arctictradelanes.com"
LANGS = ["en","ru","zh","ja","ko","el","de","nl","fr","es","it","pt","tr","ar","hi","vi","id","da","fi","sv","nb","is"]
HREF = {"en":"en-US","ru":"ru-RU","zh":"zh-CN","ja":"ja-JP","ko":"ko-KR","el":"el-GR","de":"de-DE","nl":"nl-NL","fr":"fr-FR",
        "es":"es-ES","it":"it-IT","pt":"pt-PT","tr":"tr-TR","ar":"ar","hi":"hi-IN","vi":"vi-VN","id":"id-ID","da":"da-DK",
        "fi":"fi-FI","sv":"sv-SE","nb":"nb-NO","is":"is-IS"}
CSV_URL = "/arctic-funding-programs-2026.csv"
FUND_CONTACT = "cto@arctictradelanes.com"
ADS_CONTACT = "partners@arctictradelanes.com"   # contact address used on the Oct 2026 /advertise page
NEAR_DAYS = 21
e = html.escape

NAV = {"en":("Live map","Funding","Advertise","Pricing","Collaborate"),
       "ru":("Карта","Финансирование","Реклама на сайте","Цены","Сотрудничество"),
       "zh":("实时地图","融资计划","广告合作","价格","合作")}

CSS = """
:root{color-scheme:dark;--ink:#e8eef4;--mut:#90a4ae;--line:rgba(100,181,246,.22)}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Oxygen,Ubuntu,sans-serif;background:linear-gradient(160deg,#071018 0%,#0f2740 45%,#071018 100%);color:var(--ink);min-height:100vh;display:flex;flex-direction:column;line-height:1.55}
a{color:#90caf9}
header.site{padding:1.1rem 1.5rem;border-bottom:1px solid var(--line);display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap}
header.site .brand{font-size:1.15rem;font-weight:650;background:linear-gradient(90deg,#64b5f6,#81c784);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;text-decoration:none}
nav a{margin-left:1rem;font-size:.92rem;text-decoration:none}nav a:hover{text-decoration:underline}nav a[aria-current]{color:#81c784}
main{flex:1;width:100%;max-width:1180px;margin:0 auto;padding:2.25rem 1.5rem 3rem}
h1{font-size:2rem;line-height:1.2;margin-bottom:.85rem}h2{font-size:1.25rem;margin:2.25rem 0 .85rem}
p{color:#c3ced8;margin-bottom:1rem;max-width:75ch}.lede{font-size:1.06rem}
.kicker{font-size:.75rem;letter-spacing:.12em;text-transform:uppercase;color:#4dd0e1;margin-bottom:.5rem}
.actions{display:flex;flex-wrap:wrap;gap:.7rem;margin:1.1rem 0 .4rem}
.btn{display:inline-block;padding:.55rem .95rem;border-radius:9px;background:#1976d2;color:#fff;text-decoration:none;font-weight:600;font-size:.92rem}
.btn.sec{background:transparent;border:1px solid rgba(144,202,249,.5);color:#90caf9}
.pill{display:inline-block;padding:.5rem .85rem;border-radius:9px;border:1px solid rgba(129,199,132,.4);color:#a5d6a7;font-size:.9rem}
.near{border:1px solid rgba(255,183,77,.55);background:rgba(255,152,0,.10);border-radius:12px;padding:1rem 1.2rem;margin:1.2rem 0}
.near h2{margin:0 0 .5rem;font-size:1.05rem;color:#ffcc80}.near ul{margin-left:1.1rem;color:#ffe0b2}
.tw{overflow-x:auto;border:1px solid var(--line);border-radius:12px}
table{width:100%;border-collapse:collapse;font-size:.88rem}
th,td{text-align:left;padding:.55rem .6rem;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--mut);font-weight:600;background:rgba(7,16,24,.6);position:sticky;top:0}
tr.is-near td{background:rgba(255,152,0,.09)}tr.is-closed td{opacity:.62}
.rel{font-size:.7rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em;padding:.1rem .45rem;border-radius:5px;border:1px solid}
.rel-High{color:#a5d6a7;border-color:rgba(129,199,132,.5)}.rel-Medium{color:#ffe082;border-color:rgba(255,213,79,.5)}.rel-Low{color:#b0bec5;border-color:rgba(176,190,197,.4)}
.badge{display:inline-block;margin-top:.25rem;font-size:.68rem;font-weight:700;text-transform:uppercase;padding:.08rem .4rem;border-radius:5px}
.b-near{background:rgba(255,152,0,.25);color:#ffcc80}.b-closed{background:rgba(120,144,156,.25);color:#b0bec5}
.small{font-size:.8rem;color:var(--mut)}
code{background:rgba(0,0,0,.4);padding:.12rem .35rem;border-radius:5px;font-size:.87em}
.note{border-left:3px solid #81c784;padding:.5rem 0 .5rem .9rem;color:var(--mut);font-size:.92rem}
footer{padding:1rem 1.5rem;font-size:.8rem;color:#78909c;border-top:1px solid rgba(100,181,246,.15);display:flex;justify-content:space-between;gap:1rem;flex-wrap:wrap}
.atl-ad{position:relative;margin:1.5rem auto;max-width:728px;border:1px dashed rgba(144,164,174,.25);border-radius:8px}
.atl-ad-top{min-height:90px}.atl-ad-inc{min-height:250px}
@media (max-width:1023px){.atl-ad-top{min-height:100px;max-width:320px}}
.atl-ad-label{position:absolute;top:2px;left:6px;font-size:10px;color:#607d8b;letter-spacing:.06em;text-transform:uppercase}
.atl-ad-side{display:none;position:fixed;right:12px;top:96px;width:300px;height:600px;margin:0;z-index:30}
.atl-ad-mstick{display:none;position:fixed;left:0;right:0;bottom:0;height:calc(64px + env(safe-area-inset-bottom));margin:0;max-width:none;border-radius:0;background:#071018;z-index:30}
.atl-ad-close{position:absolute;right:6px;top:4px;background:none;border:0;color:#90a4ae;font-size:14px;cursor:pointer}
"""

RAILS_JS = """<script>(function(){var m=window.ATL_AD_SLOTS||{},r=window.ATL_AD_RESERVE||{},w=window.matchMedia&&matchMedia('(min-width:1024px)').matches;
function on(id){return !!(m[id]||m[id+':mobile'])||r.rails===true}
var s=document.getElementById('atl-ad-side'),b=document.getElementById('atl-ad-mstick'),closed=false;try{closed=sessionStorage.getItem('atl_mstick_closed')==='1'}catch(e){}
if(s&&w&&on('atl-ad-side')){s.style.display='block';document.body.style.paddingRight='324px'}
if(b&&!w&&!closed&&on('atl-ad-mstick')){b.style.display='block';document.body.style.paddingBottom='72px'}
var c=b&&b.querySelector('.atl-ad-close');if(c)c.onclick=function(){b.style.display='none';document.body.style.paddingBottom='';try{sessionStorage.setItem('atl_mstick_closed','1')}catch(e){}};
if(window.atlAds)window.atlAds.scan();})();</script>"""

def slot(id_, kind, close=False):
    btn = '<button type="button" class="atl-ad-close" aria-label="Close advertisement">✕</button>' if close else ""
    return (f'<aside id="{id_}" data-yandex-rtb-slot="{id_}" data-atl-ad="{kind}" aria-label="Advertisement" class="atl-ad atl-ad-{kind}">'
            f'<span class="atl-ad-label" aria-hidden="true">Advertisement</span><div id="yandex_rtb_{id_}" class="atl-ad-body"></div>{btn}</aside>')

def lp(lang, path):
    return path if lang == "en" else f"/{lang}{path}"

def head(lang, path, title, desc, ld):
    alts = "\n".join(f'  <link rel="alternate" hreflang="{HREF[l]}" href="{SITE}{lp(l, path)}" />' for l in LANGS)
    return f"""<!DOCTYPE html>
<html lang="{lang}"{' dir="rtl"' if lang == 'ar' else ''}>
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}" />
  <link rel="canonical" href="{SITE}{lp(lang, path)}" />
{alts}
  <link rel="alternate" hreflang="x-default" href="{SITE}{path}" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="ArcticTradeLanes.com" />
  <meta property="og:title" content="{e(title)}" />
  <meta property="og:description" content="{e(desc)}" />
  <meta property="og:url" content="{SITE}{lp(lang, path)}" />
  <meta name="twitter:card" content="summary_large_image" />
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
  <script src="/ads-config.js?v=20261005b"></script>
  <script src="/atl-ads.js?v=20261005b"></script>
  <script src="https://yandex.ru/ads/system/context.js" async></script>
  <script data-page-id="20141282" src="https://yandex.ru/ads/system/ap-loader.js" async></script>
  <style>{CSS}</style>
</head>
<body data-atl-page="{path.strip('/')}">
"""

def header(lang, cur):
    n = NAV.get(lang, NAV["en"])
    links = [("/", n[0]), ("/funding", n[1]), ("/advertise", n[2]), ("/pricing", n[3]), ("/collaborate", n[4])]
    a = "".join(f'<a href="{lp(lang, h) if h != "/" else lp(lang, "") or "/"}"{" aria-current=\"page\"" if h == cur else ""}>{e(t)}</a>' for h, t in links)
    return f'  <header class="site"><a class="brand" href="{lp(lang, "") or "/"}">Arctic Trade Lanes</a><nav>{a}</nav></header>\n'

def tail(lang, left):
    n = NAV.get(lang, NAV["en"])
    return f"""  {slot("atl-ad-side", "side")}
  {slot("atl-ad-mstick", "mstick", close=True)}
  <footer><span>{left}</span><span><a href="{lp(lang, '/funding')}">{e(n[1])}</a> · <a href="{lp(lang, '/advertise')}">{e(n[2])}</a> · <a href="https://github.com/International-Arctic/Arctic-Trade-Lanes" rel="noopener">GitHub</a></span></footer>
{RAILS_JS}
</body>
</html>
"""

# ---------------- funding ----------------
def parse_deadline(s):
    try:
        return dt.date.fromisoformat(s.strip()[:10])
    except ValueError:
        return None

def funding(rows, lang):
    order = {"High": 0, "Medium": 1, "Low": 2}
    for r in rows:
        d = parse_deadline(r["deadline"])
        r["_d"] = d
        r["_closed"] = bool(d and d < TODAY) or "closed" in r["deadline"].lower()
        r["_near"] = bool(d and not r["_closed"] and (d - TODAY).days <= NEAR_DAYS)
    rows = sorted(rows, key=lambda r: (order.get(r["arctic_relevance"], 9), 0 if r["_near"] else 1, 1 if r["_closed"] else 0, r["program"].lower()))
    high = sum(r["arctic_relevance"] == "High" for r in rows)
    near = sorted([r for r in rows if r["_near"]], key=lambda r: r["_d"])
    title = "Arctic funding programs 2026 — incubators, grants, cloud & AI credits | ArcticTradeLanes"
    desc = f"{len(rows)} funding programs for Arctic businesses: incubators, seed grants, Interreg calls and cloud or AI credits, with deadlines and eligibility. Free CSV download."
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": f"{SITE}{lp(lang, '/funding')}#page", "name": title, "description": desc, "url": f"{SITE}{lp(lang, '/funding')}", "inLanguage": lang,
         "isPartOf": {"@id": f"{SITE}/#organization"}},
        {"@type": "Dataset", "name": "Arctic funding programs 2026", "description": desc, "url": f"{SITE}/funding", "license": "https://creativecommons.org/licenses/by/4.0/",
         "creator": {"@type": "Person", "name": "Aleksei Dolgikh", "sameAs": "https://x.com/alexdolbun"},
         "distribution": {"@type": "DataDownload", "encodingFormat": "text/csv", "contentUrl": f"{SITE}{CSV_URL}"}, "dateModified": TODAY.isoformat()}]}
    out = [head(lang, "/funding", title, desc, ld), header(lang, "/funding"), "  <main>\n"]
    out.append('    <p class="kicker">ArcticTradeLanes.com</p>\n    <h1>Arctic funding programs 2026</h1>\n')
    out.append(f'    <p class="lede">{len(rows)} programs for Arctic businesses and the Arctic economy: incubators, seed grants, Interreg calls, and cloud or AI credits. High-relevance programs are listed first. Compiled by <a href="https://x.com/alexdolbun" rel="noopener">Aleksei Dolgikh @alexdolbun</a>. Contact <a href="mailto:{FUND_CONTACT}">{FUND_CONTACT}</a>.</p>\n')
    out.append(f'    <div class="actions"><a class="btn" href="{CSV_URL}" download>Download CSV ({len(rows)} rows)</a><span class="pill">{high} High relevance</span></div>\n')
    if near:
        li = "".join(f'<li><strong>{e(r["program"])}</strong> closes {e(r["deadline"])} ({(r["_d"] - TODAY).days} days left) · <a href="{e(r["apply_url"])}" rel="noopener" target="_blank">apply</a></li>' for r in near)
        out.append(f'    <section class="near" id="near-deadlines"><h2>Closing soon (as of {TODAY.isoformat()})</h2><ul>{li}</ul></section>\n')
    out.append("    " + slot("atl-ad-top", "top") + "\n")
    out.append('    <div class="tw"><table id="funding-table"><thead><tr><th>Program</th><th>Region</th><th>Type</th><th>Published amount</th><th>Deadline</th><th>Eligibility</th><th>Relevance</th><th>Apply</th></tr></thead><tbody>\n')
    for r in rows:
        cls = "is-near" if r["_near"] else ("is-closed" if r["_closed"] else "")
        badge = '<br><span class="badge b-near">Closing soon</span>' if r["_near"] else ('<br><span class="badge b-closed">Closed</span>' if r["_closed"] else "")
        amt = e(r["published_amount"] or "—") + (f' <span class="small">{e(r["currency"])}</span>' if r["currency"] else "")
        notes = f'<br><span class="small">{e(r["notes"])}</span>' if r["notes"] else ""
        out.append(f'      <tr class="{cls}" data-relevance="{e(r["arctic_relevance"])}"><td><strong>{e(r["program"])}</strong>{notes}</td><td>{e(r["region"])}</td><td>{e(r["type"])}</td>'
                   f'<td>{amt}</td><td>{e(r["deadline"] or "—")}{badge}</td><td>{e(r["eligibility"] or "—")}</td>'
                   f'<td><span class="rel rel-{e(r["arctic_relevance"])}">{e(r["arctic_relevance"])}</span></td>'
                   f'<td><a href="{e(r["apply_url"])}" rel="noopener" target="_blank">Program page →</a></td></tr>\n')
    out.append("    </tbody></table></div>\n")
    lc = max((r["last_checked"] for r in rows if r.get("last_checked")), default="")
    out.append(f'    <p class="small" style="margin-top:.8rem">Amounts and deadlines are as published by each program and were last checked {e(lc)}. Always confirm on the program page before applying.</p>\n')
    out.append("    " + slot("atl-ad-inc-1", "inc") + "\n  </main>\n")
    out.append(tail(lang, f'ArcticTradeLanes.com · Funding · <a href="{CSV_URL}">CSV</a> · last checked {e(lc)}'))
    return "".join(out), len(rows), near

# ---------------- advertise ----------------
ADV = {"en": dict(
    title="Advertise on ArcticTradeLanes.com — Arctic GIS OSINT ad inventory", h1="Advertise on ArcticTradeLanes.com",
    intro="ArcticTradeLanes.com is an open Arctic GIS OSINT platform: a live EPSG:3996 polar map of the Northern Sea Route, the Polar Silk Road and Arctic ports, shipyards, lanes and programmes, published in 22 languages.",
    audH="Audience", aud="Readers who follow Arctic shipping and logistics, the Northern Sea Route (NSR), the Polar Silk Road, Arctic energy and infrastructure, and open-source GIS / OSINT research — in 22 languages, including English, Russian, Chinese, Japanese, Korean, Arabic and Hindi. We do not publish traffic figures on this page; current statistics are shared on request.",
    slotsH="Placements", cols=["Placement", "Slot id", "Size", "Where"],
    rows=[["Top banner", "atl-ad-top", "728×90 desktop / 320×100 mobile", "Under the page header"],
          ["In-content", "atl-ad-inc-1 … n", "300×250 / responsive", "Between content sections, 2+ on long pages"],
          ["Sidebar", "atl-ad-side", "300×600, sticky", "Desktop only (1024 px and wider)"],
          ["Mobile sticky", "atl-ad-mstick", "320×50", "Bottom bar on mobile, closable"],
          ["Home top", "atl-ad-home-top", "728×90 desktop / 320×100 mobile", "Home: under H1 / above the map (not over the map)"],
          ["Home in-content", "atl-ad-home-inc-1 … 2", "Banner / adaptive in below-map strip", "Home: below-map strip only"],
          ["Home logo strip", "atl-ad-home-providers", "Slim logo strip", "Home: below-map logo row"]],
    progH="Programmatic", prog="Programmatic demand runs through the Yandex Advertising Network; authorised sellers are listed in", 
    contactH="Direct buys & sponsorships", contact="Write to",
    cryptoH="Pay in crypto (x402)", crypto="Direct buys can be paid in crypto through the site's existing x402 payment rail: USDC on Base, settled on-chain. The same rail sells per-run route intelligence at 5 USDC; see Pricing for current API prices.",
    doc="x402 discovery document", pricing="Pricing"),
  "ru": dict(
    title="Реклама на ArcticTradeLanes.com — рекламные места Arctic GIS OSINT", h1="Реклама на ArcticTradeLanes.com",
    intro="ArcticTradeLanes.com — открытая арктическая GIS OSINT-платформа: живая полярная карта EPSG:3996 Северного морского пути, Полярного шёлкового пути, арктических портов, верфей и программ на 22 языках.",
    audH="Аудитория", aud="Читатели, следящие за арктическим судоходством и логистикой, СМП, Полярным шёлковым путём, энергетикой и инфраструктурой Арктики и открытыми GIS/OSINT-исследованиями, на 22 языках. Мы не публикуем цифры трафика на этой странице; актуальная статистика — по запросу.",
    slotsH="Рекламные места", cols=["Место", "ID слота", "Размер", "Где"],
    rows=[["Верхний баннер", "atl-ad-top", "728×90 десктоп / 320×100 мобайл", "Под заголовком страницы"],
          ["В контенте", "atl-ad-inc-1 … n", "300×250 / адаптивный", "Между разделами, 2+ на длинных страницах"],
          ["Боковая панель", "atl-ad-side", "300×600, закреплённая", "Только десктоп (от 1024 px)"],
          ["Мобильная плашка", "atl-ad-mstick", "320×50", "Нижняя плашка на мобильных, закрывается"]],
    progH="Программатик", prog="Программатический спрос — через Рекламную сеть Яндекса; авторизованные продавцы перечислены в",
    contactH="Прямые закупки и спонсорство", contact="Пишите на",
    cryptoH="Оплата криптовалютой (x402)", crypto="Прямые закупки можно оплатить криптовалютой через существующий платёжный канал x402 сайта: USDC в сети Base. Тот же канал продаёт расчёт маршрута за 5 USDC; актуальные цены API — на странице «Цены».",
    doc="документ x402 discovery", pricing="Цены"),
  "zh": dict(
    title="在 ArcticTradeLanes.com 投放广告 — 北极 GIS OSINT 广告位", h1="在 ArcticTradeLanes.com 投放广告",
    intro="ArcticTradeLanes.com 是开放的北极 GIS OSINT 平台：以 EPSG:3996 极地投影实时展示北方海航道、冰上丝绸之路以及北极港口、船厂和项目，提供 22 种语言。",
    audH="受众", aud="关注北极航运与物流、北方海航道（NSR）、冰上丝绸之路、北极能源与基础设施以及开源 GIS/OSINT 研究的读者，覆盖 22 种语言。本页不公布流量数字；最新统计可按需提供。",
    slotsH="广告位", cols=["广告位", "广告位 ID", "尺寸", "位置"],
    progH="程序化购买", prog="程序化需求通过 Yandex 广告网络投放；授权卖家见",
    contactH="直接购买与赞助", contact="联系",
    cryptoH="加密货币支付 (x402)", crypto="直接购买可通过本站现有的 x402 支付通道以加密货币支付：Base 网络上的 USDC。同一通道以 5 USDC 出售单次航线分析；当前 API 价格见“价格”页面。",
    doc="x402 发现文档", pricing="价格")}

def advertise(lang):
    t = dict(ADV["en"]); t.update(ADV.get(lang, {}))
    ld = {"@context": "https://schema.org", "@type": "WebPage", "@id": f"{SITE}{lp(lang, '/advertise')}#page", "name": t["title"], "description": t["intro"],
          "url": f"{SITE}{lp(lang, '/advertise')}", "inLanguage": lang, "isPartOf": {"@id": f"{SITE}/#organization"}}
    rows = "".join(f'<tr><td>{e(a)}</td><td><code>{e(b)}</code></td><td>{e(c)}</td><td>{e(d)}</td></tr>' for a, b, c, d in t["rows"])
    cols = "".join(f"<th>{e(c)}</th>" for c in t["cols"])
    body = f"""  <main>
    <p class="kicker">ArcticTradeLanes.com · GIS OSINT</p>
    <h1>{e(t["h1"])}</h1>
    <p class="lede">{e(t["intro"])}</p>
    {slot("atl-ad-top", "top")}
    <h2>{e(t["audH"])}</h2>
    <p>{e(t["aud"])}</p>
    <h2>{e(t["slotsH"])}</h2>
    <div class="tw"><table id="ad-placements"><thead><tr>{cols}</tr></thead><tbody>{rows}</tbody></table></div>
    {slot("atl-ad-inc-1", "inc")}
    <h2>{e(t["progH"])}</h2>
    <p>{e(t["prog"])} <a href="/ads.txt">ads.txt</a>.</p>
    <h2>{e(t["contactH"])}</h2>
    <p>{e(t["contact"])} <a href="mailto:{ADS_CONTACT}">{ADS_CONTACT}</a>.</p>
    <h2 id="x402">{e(t["cryptoH"])}</h2>
    <p>{e(t["crypto"])}</p>
    <div class="tw"><table id="x402-rail"><tbody>
      <tr><td>Protocol</td><td>x402 v1</td></tr>
      <tr><td>Asset / network</td><td>USDC on Base</td></tr>
      <tr><td>Per-run route intelligence</td><td>5 USDC · <code>/api/x402/fulfill</code>, <code>/api/alpha/route-optimize</code></td></tr>
      <tr><td>Discovery</td><td><a href="/.well-known/x402.json">{e(t["doc"])}: /.well-known/x402.json</a></td></tr>
      <tr><td>Status</td><td><a href="/api/x402/status">/api/x402/status</a></td></tr>
    </tbody></table></div>
    <div class="actions"><a class="btn" href="mailto:{ADS_CONTACT}">{e(t["contactH"])}</a><a class="btn sec" href="{lp(lang, '/pricing')}">{e(t["pricing"])}</a><a class="btn sec" href="/.well-known/x402.json">x402.json</a></div>
    {slot("atl-ad-inc-2", "inc")}
  </main>
"""
    return head(lang, "/advertise", t["title"], t["intro"], ld) + header(lang, "/advertise") + body + tail(lang, f'ArcticTradeLanes.com · GIS OSINT · <a href="mailto:{ADS_CONTACT}">{ADS_CONTACT}</a>')

def main():
    with open(CSV, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for lang in LANGS:
        d = OUT if lang == "en" else os.path.join(OUT, lang)
        os.makedirs(d, exist_ok=True)
        page, n, near = funding([dict(r) for r in rows], lang)
        open(os.path.join(d, "funding.html"), "w", encoding="utf-8").write(page)
        open(os.path.join(d, "advertise.html"), "w", encoding="utf-8").write(advertise(lang))
    print(f"rows={n} near={[(r['program'], r['deadline']) for r in near]} out={OUT}")

if __name__ == "__main__":
    main()
