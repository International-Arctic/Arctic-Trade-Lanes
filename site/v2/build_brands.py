#!/usr/bin/env python3
"""Build data/arctic-brands/{brands.json,brands.csv,labels.json} from Wikidata snapshots + ATL atlas.
Inclusion: Wikidata business entity, not dissolved (no P576), headquarters coordinates at or north of 60N,
country in the ATL hub set, >=2 Wikipedia sitelinks or (>=1 sitelink and an official website).
Facts are only statements present on the Wikidata item (inception, HQ, industry, stock exchange), each
with its Wikidata URL as source and the retrieval date. No people are named (no CEO/founder/owner)."""
import json,glob,csv,re,unicodedata,collections
RET='2026-10-18'
ids=json.load(open('wd/ids.json')); S=json.load(open('wd/sel.json')); L=S['labels']; sel=S['sel']
LG=json.load(open('wd/logos.json')); MUL=json.load(open('wd/mul.json'))
E={}
for f in glob.glob('wd/ent/*.json'): E.update(json.load(open(f)).get('entities',{}))
LANGS='en ru zh ja ko el de nl fr es it pt tr ar hi vi id da fi sv nb is'.split()
CUR={'RU':'RUB','NO':'NOK','FI':'EUR','SE':'SEK','IS':'ISK','DK':'DKK','GL':'DKK','FO':'DKK','CA':'CAD','US':'USD','CN':'CNY','IN':'INR','GB':'GBP','DE':'EUR','IT':'EUR','FR':'EUR','NL':'EUR','ES':'EUR','SG':'SGD','JP':'JPY','KR':'KRW','PL':'PLN','CH':'CHF','AE':'AED'}
OKLIC=re.compile(r'^(Public domain|CC0|CC BY(-SA)? [\d.]+|Copyrighted free use|FAL)$')
SECT=[('shipping',r'\bship|maritime|water transport|\bports?\b|\bferr|freight|logistic|\bmarine|offshore|subsea'),
 ('energy',r'energy|petroleum|oil|gas|electric|power|hydro|wind|nuclear|fuel'),
 ('mining',r'mining|metal|steel|iron|mineral|aluminium|nickel|quarr'),
 ('seafood',r'fish|seafood|aquaculture|mariculture|crustacean'),
 ('transport',r'transport|\brail|aviation|airline|airport|\bbus\b|\broad\b|\btoll\b|automotive|vehicle|aerospace'),
 ('construction',r'construct|engineering|real prop|real estate|renting|building|architect'),
 ('tech',r'software|technolog|telecom|internet|computer|video game|mobile phone|electronic|network operator|data'),
 ('finance',r'bank|financ|insurance|investment|holding'),
 ('forestry',r'forest|pulp|paper|wood|sawmill|timber'),
 ('food',r'food|beverage|brew|beer|dairy|alcohol|restaurant|gastronom|bakery|meat'),
 ('retail',r'retail|wholesale|shop|store|clothing|textile|furniture|sporting'),
 ('tourism',r'touris|hotel|hospitality|travel'),
 ('media',r'media|publish|newspaper|broadcast|film|music|perform'),
 ('industry',r'manufactur|industr|chemical|machin|mechanical|pharma|packag|weapon')]
def cl(e,p): return [c['mainsnak'].get('datavalue',{}).get('value') for c in e.get('claims',{}).get(p,[]) if c['mainsnak'].get('snaktype')=='value' and c.get('rank')!='deprecated']
def slugify(s):
    s=unicodedata.normalize('NFKD',s).encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+','-',s).strip('-')[:70]
TR=str.maketrans({'ø':'o','Ø':'O','æ':'ae','Æ':'AE','å':'a','ð':'d','þ':'th','ß':'ss'})
CYR=dict(zip('абвгдеёжзийклмнопрстуфхцчшщъыьэюя',['a','b','v','g','d','e','e','zh','z','i','y','k','l','m','n','o','p','r','s','t','u','f','kh','ts','ch','sh','shch','','y','','e','yu','ya']))
def translit(s): return ''.join(CYR.get(ch.lower(),ch) for ch in s.translate(TR))
rows=[]; used=set()
HQ=json.load(open('wd/hq.json'))
BIGT={'Q6256','Q3624078','Q43263','Q835714','Q831740','Q41162','Q184122','Q193512','Q192299','Q200547','Q35657','Q11828004','Q9357527','Q66724388','Q1048835','Q34763','Q23442','Q10864048','Q107390','Q56061','Q3336843','Q46395','Q1620908','Q82794','Q15642541','Q2221906'}
def good_hq(e):
    for v in cl(e,'P159'):
        if not isinstance(v,dict): continue
        h=HQ.get(v['id'])
        if h and h['coord'] and h['coord'][0]>=60 and not (set(h['p31'])&BIGT): return v['id'],h['coord']
    return None,None
NONCO=re.compile(r'universit|school|college|hospital|municipal|kommune|church|hamlet|city of|association|^null$|^municipal$')
def lab(q,lang='en'):
    d=L.get(q,{}); return d.get(lang) or d.get('en') or next(iter(d.values()),None)
for q in sel:
    e=E[q]; labels={k:v['value'] for k,v in e['labels'].items()}
    if q in MUL: labels.setdefault('en',MUL[q])
    name=next((labels[k] for k in ('en','nb','sv','fi','da','is','de','fr','nl','es','it','pt','ru') if labels.get(k)),next(iter(labels.values())))
    if NONCO.search(name.lower()): continue
    ghq,gco=good_hq(e)
    if not ghq: continue
    iso=ids[q]['iso']
    base=slugify(translit(name)) or q.lower(); s=base
    if s in used: s=f'{base}-{iso.lower()}'
    if s in used: s=f'{base}-{q.lower()}'
    used.add(s)
    src=f'https://www.wikidata.org/wiki/{q}'
    facts=[]
    inc=cl(e,'P571')
    if inc and isinstance(inc[0],dict) and inc[0].get('time'):
        y=inc[0]['time'][1:5]
        if y.isdigit() and int(y)>1000: facts.append({'kind':'founded','value':y,'fact':f'Founded {y}','source_url':src,'date':RET})
    hq=[ghq]
    if hq and lab(hq[0]): facts.append({'kind':'hq','qid':hq[0],'value':lab(hq[0]),'fact':f'Headquarters: {lab(hq[0])}','source_url':src,'date':RET})
    ind=[v['id'] for v in cl(e,'P452') if isinstance(v,dict) and lab(v['id'])][:3]
    if ind: facts.append({'kind':'industry','qids':ind,'value':', '.join(lab(i) for i in ind),'fact':'Industry: '+', '.join(lab(i) for i in ind),'source_url':src,'date':RET})
    ex=[v['id'] for v in cl(e,'P414') if isinstance(v,dict) and lab(v['id'])][:2]
    if ex: facts.append({'kind':'exchange','qids':ex,'value':', '.join(lab(i) for i in ex),'fact':'Listed on: '+', '.join(lab(i) for i in ex),'source_url':src,'date':RET})
    t1=' '.join(lab(i) or '' for i in ind).lower(); t2=' '.join(lab(v['id']) or '' for v in cl(e,'P31') if isinstance(v,dict)).lower()
    sector=next((k for k,rx in SECT if re.search(rx,t1)),None) or next((k for k,rx in SECT if re.search(rx,t2)),'other')
    logo_url=logo_lic=logo_src=''
    fn=LG['files'].get(q); inf=LG['info'].get(fn) if fn else None
    if inf and inf.get('lic') and OKLIC.match(inf['lic']) and inf.get('thumb'):
        logo_url=inf['thumb']; logo_lic=inf['lic']; logo_src=inf['page']
    web=next((w for w in cl(e,'P856') if isinstance(w,str) and w.startswith('http')),'')
    sl=len([k for k in e.get('sitelinks',{}) if k.endswith('wiki') and k!='commonswiki'])
    lat=round(gco[0],4); lon=round(gco[1],4)
    rows.append({'id':q,'slug':s,'name':name,'names':{k:labels[k] for k in LANGS if k in labels and labels[k]!=name},
      'logo_url':logo_url,'logo_license':logo_lic,'logo_source':logo_src,'country':iso,'sector':sector,
      'hq_lat':lat,'hq_lon':lon,'arctic_geo_lat':lat,'arctic_geo_lon':lon,'website':web,'facts':facts,
      'currency':CUR[iso],'source':'wikidata','wikidata':src,'sitelinks':sl})
# ATL atlas operators (clean names only, not already present)
g=json.load(open('atlas.geojson')); slugs=json.load(open('slugs.json'))
PREFIX={'ports':'port','shipyards':'shipyard','icebreakers':'icebreaker','tankers':'tanker','industry':'industry','rail':'rail','airports':'airport'}
have={slugify(translit(r['name'])) for r in rows}
BAD=re.compile(r'navy|fleet|coast guard|government|ministry|research|institute|administration|military|federal|state-owned|\(|\)|/|;| with |&|,')
ops=collections.defaultdict(list)
for f in g['features']:
    p=f['properties']; op=(p.get('operator') or '').strip()
    if p['layer'] not in PREFIX or not op or BAD.search(op.lower()) or NONCO.search(op.lower()) or op in ('Neste Oil',) or not p.get('iso2') or p['iso2'] not in CUR: continue
    if p['id'] not in slugs: continue
    ops[op].append((p,f['geometry']['coordinates']))
for op,items in sorted(ops.items()):
    s=slugify(translit(op))
    if not s or s in have or s in used: continue
    used.add(s); p0,c0=items[0]
    facts=[{'kind':'operates','value':p['name'],'href':f"/{PREFIX[p['layer']]}/{slugs[p['id']]}",'fact':f"Listed as operator of {p['name']} in the ATL atlas",'source_url':f"https://arctictradelanes.com/{PREFIX[p['layer']]}/{slugs[p['id']]}",'date':'2026-10-14'} for p,_ in items[:6]]
    sector='shipping' if p0['layer'] in('ports','shipyards','icebreakers','tankers') else ('transport' if p0['layer'] in('rail','airports') else 'industry')
    rows.append({'id':'atl-op-'+s,'slug':s,'name':op,'names':{},'logo_url':'','logo_license':'','logo_source':'','country':p0['iso2'],'sector':sector,
      'hq_lat':None,'hq_lon':None,'arctic_geo_lat':round(c0[1],4),'arctic_geo_lon':round(c0[0],4),'website':'','facts':facts,'currency':CUR[p0['iso2']],'source':'atl-atlas','wikidata':'','sitelinks':0})
rows.sort(key=lambda r:(-r['sitelinks'],r['slug']))
json.dump(rows,open('data/arctic-brands/brands.json','w'),ensure_ascii=False,indent=0)
with open('data/arctic-brands/brands.csv','w',newline='') as fh:
    w=csv.writer(fh); cols=['id','name','logo_url','logo_license','logo_source','country','sector','hq_lat','hq_lon','arctic_geo_lat','arctic_geo_lon','website','facts','currency']
    w.writerow(cols+['slug','source'])
    for r in rows: w.writerow([r[c] if c!='facts' else json.dumps([{k:f[k] for k in ('fact','source_url','date')} for f in r['facts']],ensure_ascii=False) for c in cols]+[r['slug'],r['source']])
need=set()
for r in rows:
    for f in r['facts']:
        if 'qid' in f: need.add(f['qid'])
        for x in f.get('qids',[]): need.add(x)
json.dump({q:L[q] for q in need if q in L},open('data/arctic-brands/labels.json','w'),ensure_ascii=False,separators=(',',':'))
c=collections.Counter(r['country'] for r in rows)
print('rows',len(rows),'wikidata',sum(r['source']=='wikidata' for r in rows),'atlas',sum(r['source']=='atl-atlas' for r in rows),'logos',sum(1 for r in rows if r['logo_url']))
print(c); print(collections.Counter(r['sector'] for r in rows))
print('nofacts',sum(1 for r in rows if not r['facts']))
