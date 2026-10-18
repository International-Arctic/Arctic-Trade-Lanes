import json,collections
g=json.load(open('atlas.geojson')); slugs=json.load(open('slugs.json'))
brands=json.load(open('data/arctic-brands/brands.json'))
PREFIX={'ports':'port','cities':'city','programs':'program','lanes':'lane','industry':'industry','shipyards':'shipyard','icebreakers':'icebreaker','airports':'airport','rail':'rail','rescue':'rescue','tankers':'tanker'}
COUNCIL=['ru','no','fi','se','dk','gl','is','ca','us']
OBS=['cn','in','jp','kr','sg','de','fr','gb','it','nl','pl','es','ch']
OTHER=['ae']
ALIAS={'FO':'dk','SJ':'no'}
CUR={'ru':'RUB','no':'NOK','fi':'EUR','se':'SEK','is':'ISK','dk':'DKK','gl':'DKK','ca':'CAD','us':'USD','cn':'CNY','in':'INR','jp':'JPY','kr':'KRW','sg':'SGD','de':'EUR','fr':'EUR','gb':'GBP','it':'EUR','nl':'EUR','pl':'PLN','es':'EUR','ch':'CHF','ae':'AED'}
hubs={}
for iso in COUNCIL+OBS+OTHER:
    hubs[iso]={'iso':iso,'group':'council' if iso in COUNCIL else ('observer' if iso in OBS else 'partner'),'currency':CUR[iso],'layers':{},'programs':[],'brands':[],'brand_count':0}
for f in g['features']:
    p=f['properties']; i=(p.get('iso2') or '').upper()
    iso=ALIAS.get(i,i.lower())
    if iso not in hubs or p['id'] not in slugs or p['layer'] not in PREFIX: continue
    item={'n':p['name'],'h':f"/{PREFIX[p['layer']]}/{slugs[p['id']]}"}
    if p['layer']=='programs': hubs[iso]['programs'].append(item)
    else: hubs[iso]['layers'].setdefault(p['layer'],[]).append(item)
for b in brands:
    iso=ALIAS.get(b['country'],b['country'].lower())
    if iso in hubs:
        hubs[iso]['brand_count']+=1
        if len(hubs[iso]['brands'])<30: hubs[iso]['brands'].append(b['slug'])
for h in hubs.values():
    for k in h['layers']: h['layers'][k].sort(key=lambda x:x['n'])
    h['programs'].sort(key=lambda x:x['n'])
json.dump({'order':COUNCIL+OBS+OTHER,'hubs':hubs},open('src/home/v2/hubs.json','w'),ensure_ascii=False,separators=(',',':'))
for iso,h in hubs.items(): print(iso,h['group'],{k:len(v) for k,v in h['layers'].items()},'prog',len(h['programs']),'brands',h['brand_count'])
