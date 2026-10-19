import json
for f in ['i18n_en.py','i18n_core.py','i18n_b1.py','i18n_b2.py','i18n_b3.py','i18n_pp.py']: exec(open(f).read())
M={'en':EN,'ru':RU,'zh':ZH,'nb':NB,'da':DA,'de':DE,'fr':FR,'es':ES,'it':IT,'pt':PT,'nl':NL,'sv':SV,'fi':FI,'is':IS,'el':EL,'tr':TR,'ar':AR,'ja':JA,'ko':KO,'hi':HI,'vi':VI,'id':ID}
BASE=set(EN)
keys=['pp_role','pp_rel','pp_related','pp_back','pp_note','pp_map','pp_index_title']
assert len(M)==22 and set(PP)==set(M)
for l,d in M.items():
  assert set(d)==BASE,(l,BASE^set(d))
  d.update(dict(zip(keys,PP[l])))
json.dump(M,open('../src/home/home-extras.i18n.json','w'),ensure_ascii=False,indent=0)
print('ok',len(M),len(M['en']))
