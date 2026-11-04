import json,subprocess,random,re
G=['git','-C','/workspace/delphi-frontier']
a=json.load(open('all.json'))
# latest version per claim_id by commit date
def cdate(c): return int(subprocess.run(G+['show','-s','--format=%ct',c],capture_output=True,text=True).stdout)
best={}
for x in a:
    x['t']=cdate(x['commit']); k=x['block']['claim_id']
    if k not in best or x['t']>best[k]['t']: best[k]=x
pop=[]
for k,x in sorted(best.items()):
    t=subprocess.run(G+['show',f"{x['commit']}:{x['file']}"],capture_output=True,text=True).stdout
    if '207' in t: continue
    pop.append(x)
print('population',len(pop))
random.seed(20261104)
s=random.sample(pop,10)
for x in s: print(x['block']['claim_id'],x['block']['outcome'],x['commit'][:10],x['file'])
json.dump(s,open('sample.json','w'),indent=1)
