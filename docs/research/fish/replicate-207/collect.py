import subprocess,re,json,sys
G=['git','-C','/workspace/delphi-frontier']
# all blobs of docs/research/fish/challenge-N.md anywhere in history, excluding 207
out=subprocess.run(G+['log','--remotes','--format=%H','--name-only','--','docs/research/fish'],capture_output=True,text=True).stdout
pairs=[];c=None
for l in out.splitlines():
    if re.fullmatch(r'[0-9a-f]{40}',l): c=l
    elif re.fullmatch(r'docs/research/fish/challenge-\d+\.md',l) and '207' not in l: pairs.append((c,l))
seen={}
for c,f in pairs:
    b=subprocess.run(G+['rev-parse',f'{c}:{f}'],capture_output=True,text=True).stdout.strip()
    if not b or b in seen or 'fatal' in b: continue
    t=subprocess.run(G+['cat-file','-p',b],capture_output=True,text=True).stdout
    ms=re.findall(r'```swarm-challenge\s*(\{.*?\})\s*```',t,re.S)
    d=None
    if ms:
        try: d=json.loads(ms[-1])
        except Exception as e: d={'parse_error':str(e)}
    seen[b]=dict(commit=c,file=f,block=d)
json.dump(list(seen.values()),open('all.json','w'),indent=1)
print(len(seen))
