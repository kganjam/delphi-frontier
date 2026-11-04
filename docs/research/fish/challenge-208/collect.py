import subprocess,re,json,sys
G=['git','-C','/workspace/delphi-frontier']
refs=subprocess.run(G+['for-each-ref','--format=%(refname)','refs/remotes'],capture_output=True,text=True).stdout.split()
seen={}
for r in refs:
    files=subprocess.run(G+['ls-tree','-r','--name-only',r,'docs/research'],capture_output=True,text=True).stdout.split()
    for f in files:
        if not re.search(r'challenge-\d+',f): continue
        blob=subprocess.run(G+['rev-parse',f'{r}:{f}'],capture_output=True,text=True).stdout.strip()
        if blob in seen: continue
        t=subprocess.run(G+['cat-file','-p',blob],capture_output=True,text=True).stdout
        m=re.search(r'```swarm-challenge\s*(\{.*?\})\s*```',t,re.S)
        d=None
        if m:
            try: d=json.loads(m.group(1))
            except Exception as e: d={'parse_error':str(e),'raw':m.group(1)[:300]}
        seen[blob]=dict(ref=r,file=f,block=d,len=len(t))
json.dump(list(seen.values()),open(sys.argv[1] if len(sys.argv)>1 else 'all.json','w'),indent=1)
print(len(seen))
