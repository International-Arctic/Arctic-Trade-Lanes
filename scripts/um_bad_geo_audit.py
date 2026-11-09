# Read-only bad-geo audit of the UnicornsMap.com main SPA bundle (+ /data/profiles-rail.json).
# Usage: curl the bundle to um.js and /data/profiles-rail.json to um_profiles-rail.json, then: python3 um_bad_geo_audit.py um.js
# Flags: non-numeric/null coords, null island, out-of-range, lat/lng swapped vs city table, exact-duplicate stacks, country-centroid placeholders, integer-degree coords.
import re, json, collections
js=open(__import__('sys').argv[1] if len(__import__('sys').argv)>1 else 'um.js',encoding='utf-8').read()
num=r'(-?\d+(?:\.\d+)?)'
recs=[]
for m in re.finditer(r'lat:'+num+r',lng:'+num, js):
    pre=js[max(0,m.start()-400):m.start()]
    slug=re.findall(r'slug:"([^"]+)"',pre); name=re.findall(r'name:"([^"]+)"',pre)
    bt=re.findall(r'beneficiary_type:"([^"]+)"',pre[-120:])
    city=re.findall(r'(?:hqCity|city|org):"([^"]+)"',pre[-250:])
    recs.append(dict(src='bundle',slug=slug[-1] if slug else '?',name=name[-1] if name else '?',type=bt[-1] if bt else '',city=city[-1] if city else '',lat=float(m.group(1)),lng=float(m.group(2))))
# city lookup dicts  key:[lat,lng]
citydict={}
for m in re.finditer(r'([A-Za-z_$][\w$]*|"[^"]+"):\['+num+','+num+r'\]', js):
    citydict[m.group(1).strip('"')]=(float(m.group(2)),float(m.group(3)))
rail=json.load(open('um_profiles-rail.json'))
def walk(o,path=''):
    if isinstance(o,dict):
        if 'lat' in o and ('lng' in o or 'lon' in o):
            recs.append(dict(src='rail',slug=o.get('slug',path),name=o.get('name',''),type=o.get('beneficiary_type',''),city=o.get('city',o.get('hqCity','')),lat=o['lat'],lng=o.get('lng',o.get('lon'))))
        for k,v in o.items(): walk(v,path+'/'+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): walk(v,path)
walk(rail)
print('records',len(recs),collections.Counter(r['src'] for r in recs),'citydict',len(citydict))
bad=lambda r: not isinstance(r['lat'],(int,float)) or not isinstance(r['lng'],(int,float))
nonnum=[r for r in recs if bad(r)]; print('non-numeric',len(nonnum),nonnum[:5])
R=[r for r in recs if not bad(r)]
null=[r for r in R if abs(r['lat'])<0.01 and abs(r['lng'])<0.01]; print('null-island',len(null),[ (r['slug'],r['lat'],r['lng']) for r in null[:10]])
oor=[r for r in R if abs(r['lat'])>90 or abs(r['lng'])>180]; print('out-of-range',len(oor),[(r['slug'],r['lat'],r['lng']) for r in oor[:10]])
cvals=set(citydict.values())
sw=[r for r in R if (r['lng'],r['lat']) in cvals and (r['lat'],r['lng']) not in cvals]; print('swapped-vs-citydict',len(sw),[(r['slug'],r['lat'],r['lng']) for r in sw[:10]])
cnt=collections.Counter((r['lat'],r['lng']) for r in R)
dups=[(k,v) for k,v in cnt.most_common() if v>1]
print('distinct coords',len(cnt),'coords shared by >1 record',len(dups),'records on shared coords',sum(v for k,v in dups))
inv={v:k for k,v in citydict.items()}
for k,v in dups[:25]:
    ex=[r['slug'] for r in R if (r['lat'],r['lng'])==k][:4]
    print(f'  {v:4d} {k} city={inv.get(k,"")} e.g. {ex}')
cent={'USA':(39.8283,-98.5795),'USA2':(37.0902,-95.7129),'China':(35.8617,104.1954),'India':(20.5937,78.9629),'Russia':(61.524,105.3188),'UK':(55.3781,-3.436),'Germany':(51.1657,10.4515),'France':(46.2276,2.2137),'Canada':(56.1304,-106.3468),'Brazil':(-14.235,-51.9253),'Australia':(-25.2744,133.7751),'Japan':(36.2048,138.2529),'UAE':(23.4241,53.8478),'Switzerland':(46.8182,8.2275),'Italy':(41.8719,12.5674),'Spain':(40.4637,-3.7492),'Netherlands':(52.1326,5.2913),'Israel':(31.0461,34.8516),'SKorea':(35.9078,127.7669),'Vietnam':(14.0583,108.2772),'Indonesia':(-0.7893,113.9213),'Nigeria':(9.082,8.6753),'Kenya':(-0.0236,37.9062),'Turkey':(38.9637,35.2433),'Sweden':(60.1282,18.6435),'Norway':(60.472,8.4689),'Saudi':(23.8859,45.0792),'Thailand':(15.87,100.9925),'Mexico':(23.6345,-102.5528),'Argentina':(-38.4161,-63.6167),'Estonia':(58.5953,25.0136),'Portugal':(39.3999,-8.2245),'Poland':(51.9194,19.1451),'Ukraine':(48.3794,31.1656),'Philippines':(12.8797,121.774),'Malaysia':(4.2105,101.9758),'SAfrica':(-30.5595,22.9375),'Egypt':(26.8206,30.8025),'Finland':(61.9241,25.7482),'Denmark':(56.2639,9.5018),'Ireland':(53.1424,-7.6921),'Austria':(47.5162,14.5501),'Belgium':(50.5039,4.4699),'Taiwan':(23.6978,120.9605),'Qatar':(25.3548,51.1839),'Kazakhstan':(48.0196,66.9237),'Georgia':(42.3154,43.3569),'Cyprus':(35.1264,33.4299),'NZ':(-40.9006,174.886),'Chile':(-35.6751,-71.543),'Colombia':(4.5709,-74.2973),'Pakistan':(30.3753,69.3451),'Bangladesh':(23.685,90.3563)}
cc=[]
for r in R:
    for c,(a,b) in cent.items():
        if abs(r['lat']-a)<0.05 and abs(r['lng']-b)<0.05: cc.append((c,r['slug'],r['lat'],r['lng']))
print('country-centroid matches',len(cc),collections.Counter(c[0] for c in cc).most_common(), cc[:12])
# integer/low-precision coords
lowp=[r for r in R if r['lat']==int(r['lat']) and r['lng']==int(r['lng'])]; print('integer-degree coords',len(lowp),[(r['slug'],r['lat'],r['lng']) for r in lowp[:10]])
types=collections.Counter(r['type'] for r in R); print('types',types)
json.dump(R,open('um_coords.json','w'),ensure_ascii=False,indent=0)
