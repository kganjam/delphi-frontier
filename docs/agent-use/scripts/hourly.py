import subprocess,collections,datetime as dt,sys,json
def commits(repo,refs):
    out=subprocess.run(['git','-C',repo,'log',*refs,'--date=iso-strict','--format=%H|%aI'],capture_output=True,text=True).stdout.split('\n')
    d={}
    for l in out:
        if '|' in l:
            h,a=l.split('|'); d[h]=dt.datetime.fromisoformat(a).astimezone(dt.timezone.utc)
    return d
f=commits('.',['--remotes=origin']); e=commits(sys.argv[1],['--all'])
print('frontier',len(f),min(f.values()),max(f.values())); print('evolve',len(e),min(e.values()),max(e.values()))
cf=collections.Counter(t.strftime('%Y-%m-%dT%H') for t in f.values()); ce=collections.Counter(t.strftime('%Y-%m-%dT%H') for t in e.values())
start=min(min(f.values()),min(e.values())).replace(minute=0,second=0); end=max(max(f.values()),max(e.values()))
h=start; rows=[]
while h<=end:
    k=h.strftime('%Y-%m-%dT%H'); rows.append((k,cf.get(k,0),ce.get(k,0))); h+=dt.timedelta(hours=1)
json.dump(rows,open(sys.argv[2],'w'))
# quiet stretches: gaps > 1h between consecutive commits (combined, and frontier-only)
for name,ts in (('frontier',sorted(f.values())),('evolve',sorted(e.values())),('combined',sorted(list(f.values())+list(e.values())))):
    for a,b in zip(ts,ts[1:]):
        if (b-a).total_seconds()>3600: print('gap',name,a.isoformat(),b.isoformat(),round((b-a).total_seconds()/3600,2),'h')
