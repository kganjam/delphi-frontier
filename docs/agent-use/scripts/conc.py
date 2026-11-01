import json,glob,os,sys,datetime as dt,collections,re
cut=dt.datetime(2026,10,30,tzinfo=dt.timezone.utc).timestamp()
files=[f for f in glob.glob('/home/ubuntu/.claude/projects/**/*.jsonl',recursive=True)+glob.glob('/home/ubuntu/Orchestra/data/claude_creds/*/projects/**/*.jsonl',recursive=True) if os.path.getmtime(f)>=cut]
ev=[];top=sub=0;started=collections.Counter();started_sub=collections.Counter()
rx=re.compile(r'"timestamp":"([0-9T:\-\.]+)Z"')
for f in files:
    is_sub='/subagents/' in f; top+=not is_sub; sub+=is_sub
    sec=set();first=None
    for line in open(f,errors='ignore'):
        if '"type":"assistant"' not in line: 
            if first is None:
                m=rx.search(line)
                if m: first=m[1]
            continue
        m=rx.search(line)
        if m:
            first=first or m[1]
            sec.add(int(dt.datetime.fromisoformat(m[1]+'+00:00').timestamp()))
    if first and first>='2026-10-30':
        (started_sub if is_sub else started)[first[:13]]+=1
    if not is_sub:
        for s in sec: ev.append((s,f))
ev.sort();best=(0,None);cnt=collections.Counter();j=0
for i,(t,f) in enumerate(ev):
    cnt[f]+=1
    while ev[j][0]<t-180:
        g=ev[j][1];cnt[g]-=1
        if cnt[g]==0: del cnt[g]
        j+=1
    if len(cnt)>best[0]: best=(len(cnt),t)
json.dump(dict(active_files=len(files),top_level=top,subagent_files=sub,max_top_sessions_in_180s=best[0],window_end_utc=dt.datetime.fromtimestamp(best[1],dt.timezone.utc).isoformat() if best[1] else None,started_top_hourly=started,started_sub_hourly=started_sub,definition='distinct top-level transcript files (not under subagents/) with >=1 assistant message timestamp in a trailing 180 s window; files with mtime >= 2026-10-30T00:00Z'),open(sys.argv[1],'w'),indent=1)
