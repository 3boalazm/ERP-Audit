import json,glob,collections,re
B=json.load(open('c2/buckets.json'))
order=['C1','C2','C3','C4','C5','C6','C7','C8','C9','C10']
R=json.load(open('c2/RECON.json'))
reqs=[];rules=[];decs=[];mapping={}
for b in order:
    rs=json.load(open(f'c2/{b}.reqs.json'))
    for r in rs: r['bucket']=b
    rs+= [dict(x,bucket=b) for x in R.get('new_reqs',{}).get(b,[])]
    reqs+=rs
    rules+=[dict(x,bucket=b) for x in json.load(open(f'c2/{b}.rules.json'))+R.get('new_rules',{}).get(b,[])]
    decs+=[dict(x,bucket=b) for x in json.load(open(f'c2/{b}.decisions.json'))+R.get('new_decisions',{}).get(b,[])]
    for sid,d in json.load(open(f'c2/{b}.mapping.json')).items():
        mapping[sid]={'bucket':b,'disp':d}
for sid,v in R['mapping'].items():
    mapping[sid]={'bucket':v['target'],'disp':v['disposition'],'recon_from':mapping.get(sid,{}).get('bucket')}
byid={r['req_id']:r for r in reqs}
for rid,adds in R.get('source_additions',{}).items():
    if rid in byid: byid[rid].setdefault('sources',[]).extend(adds)
    else: print('missing source_add target',rid)
ids=[r['req_id'] for r in reqs]; dup=[i for i,c in collections.Counter(ids).items() if c>1]; print('dup req ids',dup)
dids=[d['dec_id'] for d in decs]; print('dup dec',[i for i,c in collections.Counter(dids).items() if c>1])
bids=[x['br_id'] for x in rules]; print('dup br',[i for i,c in collections.Counter(bids).items() if c>1])
raw={json.loads(l)['sid']:json.loads(l) for f in glob.glob('raw/B*.jsonl') for l in open(f)}
print('raw',len(raw),'mapped',len(mapping),'missing',len(set(raw)-set(mapping)),'extra',len(set(mapping)-set(raw)))
# check dispositions targets
bad=0
for sid,v in mapping.items():
    m=re.match(r'(REQ|DUP_OF|CLAIM_OF|NFR_OF|NEW):\s*(\S+)',v['disp'])
    if m and m.group(2) not in byid: bad+=1; print('bad target',sid,v)
    m=re.match(r'(OPEN_Q|CONFLICT):\s*(\S+)',v['disp'])
    if m and m.group(2) not in set(dids): bad+=1; print('bad dec',sid,v)
print('bad',bad)
json.dump({'reqs':reqs,'rules':rules,'decs':decs,'mapping':mapping},open('final/master.json','w'),ensure_ascii=False)
cls=collections.Counter(r['class'] for r in reqs); print(len(reqs),cls)
print('prio',collections.Counter(r['priority'] for r in reqs))
norm=lambda s:(s or '').split()[0].strip(' (').upper() if s else ''
print('B',collections.Counter(norm(r['status_baseline']) for r in reqs)); print('C',collections.Counter(norm(r['status_current']) for r in reqs))
print('disp',collections.Counter(re.split(r'[:\s]',v['disp'])[0] for v in mapping.values()))
print('rules',len(rules),'decs',len(decs),collections.Counter(d['kind'] for d in decs), sum(1 for d in decs if d.get('blocking')))
