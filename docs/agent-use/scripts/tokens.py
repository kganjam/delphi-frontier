import json,glob,os,sys,collections,datetime as dt
cut=dt.datetime(2026,10,30,tzinfo=dt.timezone.utc)
files=glob.glob('/home/ubuntu/.claude/projects/**/*.jsonl',recursive=True)+glob.glob('/home/ubuntu/Orchestra/data/claude_creds/*/projects/**/*.jsonl',recursive=True)
tot=collections.Counter();win=collections.Counter();models=collections.Counter();wmodels=collections.Counter()
active=0;seen=set();sess_first={};hourly_sess=collections.Counter();sub=0;subwin=0
for f in files:
    try: m=os.path.getmtime(f)
    except: continue
    isact=m>=cut.timestamp(); active+=isact
    is_sub='/subagents/' in f
    first=None
    try:
        for line in open(f,errors='ignore'):
            if '"assistant"' not in line and first is not None: continue
            try: d=json.loads(line)
            except: continue
            ts=d.get('timestamp')
            if ts and first is None: first=ts
            if d.get('type')!='assistant': continue
            msg=d.get('message') or {}
            u=msg.get('usage');
            if not u: continue
            key=(msg.get('id'),d.get('requestId'))
            if key[0] and key in seen: continue
            seen.add(key)
            t=dt.datetime.fromisoformat(ts.replace('Z','+00:00')) if ts else None
            vals={'input':u.get('input_tokens',0) or 0,'output':u.get('output_tokens',0) or 0,'cache_read':u.get('cache_read_input_tokens',0) or 0,'cache_creation':u.get('cache_creation_input_tokens',0) or 0,'messages':1}
            tot.update(vals); models[msg.get('model','?')]+=1
            if t and t>=cut: win.update(vals); wmodels[msg.get('model','?')]+=1
    except Exception as e: pass
    if first:
        t=dt.datetime.fromisoformat(first.replace('Z','+00:00'))
        if t>=cut:
            hourly_sess[t.strftime('%Y-%m-%dT%H')]+=1
            if is_sub: subwin+=1
json.dump(dict(files=len(files),active_since_cut=active,total=tot,window=win,models=models.most_common(),window_models=wmodels.most_common(),sessions_started_hourly=hourly_sess,subagent_transcripts_started_in_window=subwin,dedupe='message.id+requestId'),open(sys.argv[1],'w'),indent=1)
