import subprocess,re,json,collections,sys
def g(*a): return subprocess.run(['git',*a],capture_output=True,text=True).stdout
# every commit touching challenge-N.md across all remote refs, with time
out=g('log','--remotes','--format=@@%H %ct','--name-only','--diff-filter=AM','--','docs/research/fish/')
recs=[];cur=None
for line in out.splitlines():
    if line.startswith('@@'):
        h,t=line[2:].split();cur=(h,int(t))
    else:
        m=re.fullmatch(r'docs/research/fish/challenge-(\d+)\.md',line.strip())
        if m and cur: recs.append((cur[1],cur[0],int(m.group(1)),line.strip()))
blobs={}
for t,h,n,p in recs:
    b=g('rev-parse',f'{h}:{p}').strip()
    if b in blobs and blobs[b][0]<=t: continue
    blobs[b]=(t,h,n)
rows=[];bad=0
for b,(t,h,n) in blobs.items():
    txt=g('cat-file','-p',b)
    ms=re.findall(r'```swarm-challenge\s*(\{.*?\})\s*```',txt,re.S)
    if not ms: bad+=1;continue
    try: d=json.loads(ms[-1])
    except Exception: bad+=1;continue
    rows.append(dict(t=t,blob=b,file=n,cid=d.get('claim_id'),out=str(d.get('outcome')).lower().strip(),mentions207=('207' in txt)))
json.dump(rows,open(sys.argv[1],'w'))
print('blobs',len(blobs),'parsed',len(rows),'unparsed',bad)
print('file!=cid',sum(r['file']!=r['cid'] for r in rows))
print(collections.Counter(r['out'] for r in rows))
