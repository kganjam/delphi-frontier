import json,subprocess,collections,sys
R="/workspace/delphi-frontier"
def g(*a): return subprocess.run(["git","-C",R,*a],capture_output=True,text=True).stdout.strip()
rows=json.load(open("rows.json"))
seen={}
for r in rows:
    blob=g("rev-parse",f'{r["ref"]}:{r["path"]}')
    add=g("log","--diff-filter=A","--format=%cI","-1",r["ref"],"--",r["path"])
    k=(blob,str(r["claim_id"]),r["outcome"])
    if k not in seen or add<seen[k]["added"]: seen[k]=dict(r,blob=blob,added=add)
U=list(seen.values()); json.dump(U,open("unique.json","w"),indent=1)
def tally(L,label):
    c=collections.Counter(x["outcome"] for x in L); n=sum(c.values())
    print(label,"n=",n,dict(c),"survival=%.4f"%(c["survived"]/n if n else 0))
tally(U,"all unique-blob")
cut="2026-11-04T09:06:46+00:00"
tally([x for x in U if x["added"]<cut and str(x["claim_id"])!="207"],"before challenge-207 commit")
# one per claim_id: earliest
first={}
for x in sorted(U,key=lambda x:x["added"]): first.setdefault(str(x["claim_id"]),x)
tally(list(first.values()),"earliest per claim")
print(min(x["added"] for x in U), max(x["added"] for x in U))
