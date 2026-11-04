import subprocess, re, json, sys
R="/workspace/delphi-frontier"
def g(*a): return subprocess.run(["git","-C",R,*a],capture_output=True,text=True).stdout
EXCL="claude/replicate-207-challenger-audit-1mwyh0"  # the derivation under test: not read
rows=[]
for ref in g("for-each-ref","--format=%(refname:short)","refs/remotes/origin").split():
    if ref.endswith(EXCL) or ref=="origin/HEAD": continue
    files=g("grep","-l","swarm-challenge",ref,"--","*.md").split("\n")
    for f in filter(None,files):
        path=f.split(":",1)[1]
        txt=g("show",f)
        for m in re.finditer(r"```swarm-challenge\s*\n(.*?)```",txt,re.S):
            body=m.group(1)
            try: d=json.loads(body)
            except Exception:
                cid=re.search(r'"claim_id"\s*:\s*"?(\w+)',body); oc=re.search(r'"outcome"\s*:\s*"(\w+)"',body)
                d={"claim_id":cid and cid.group(1),"outcome":oc and oc.group(1),"_parse":"regex"}
            date=g("log","-1","--format=%cI",ref,"--",path).strip()
            rows.append({"ref":ref,"path":path,"claim_id":d.get("claim_id"),"outcome":d.get("outcome"),"date":date,"parse":d.get("_parse","json")})
json.dump(rows,open(sys.argv[1],"w"),indent=1)
print(len(rows))
