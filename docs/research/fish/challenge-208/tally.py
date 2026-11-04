"""Tally swarm-challenge verdicts. Usage: python3 -I tally.py all.json codes.json"""
import json,sys,re,collections
a=json.load(open(sys.argv[1])); codes=json.load(open(sys.argv[2]))
by=collections.defaultdict(list)
for x in a:
    b=x['block']
    if b and 'claim_id' in b: by[int(b['claim_id'])].append(b['outcome'].lower())
dispatch=set(list(range(32,36))+list(range(41,52))+list(range(53,69)))
def out(v): s=set(v); return 'split' if len(s)>1 else s.pop()
st=collections.Counter(('dispatch' if k in dispatch else 'science',out(v)) for k,v in by.items())
print('verdict files',sum(map(len,by.values())),'claims',len(by)); print(dict(st))
multi=[k for k,v in by.items() if len(v)>1]; split=[k for k in multi if out(by[k])=='split']
print('multiply-challenged',len(multi),'split',sorted(split))
sci_ns=sorted(k for k,v in by.items() if k not in dispatch and out(v) in('weakened','refuted'))
coded={k:c for c in 'ABCN' for k in codes[c]}
missing=[k for k in sci_ns if k not in coded]; extra=[k for k in coded if k not in sci_ns]
print('science non-survived',len(sci_ns),'uncoded',missing,'coded-but-not-in-set',extra)
cnt=collections.Counter(coded[k] for k in sci_ns if k in coded); n=sum(cnt.values())
print({c:(cnt[c],round(100*cnt[c]/n,1)) for c in 'ABCN'})
for k,o in codes['adversarial_or_replication_output_claims'].items(): print('adv',k,o,by[int(k)])
