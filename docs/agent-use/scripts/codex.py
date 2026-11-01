import json,glob,os,collections,sys
cut='2026-10-30T00:00:00'
K=['input_tokens','cached_input_tokens','output_tokens','reasoning_output_tokens','total_tokens']
tot=collections.Counter();win=collections.Counter();models=collections.Counter();n=0;nw=0;sess_started_hourly=collections.Counter();first_ts={}
for f in glob.glob(os.path.expanduser('~/.codex/sessions/**/*.jsonl'),recursive=True):
    last=None;before=None;model=None;first=None
    for line in open(f,errors='ignore'):
        if first is None and '"timestamp"' in line:
            try: first=json.loads(line).get('timestamp')
            except: pass
        if '"model"' in line and model is None:
            try:
                d=json.loads(line);p=d.get('payload',{})
                model=p.get('model') or model
            except: pass
        if 'total_token_usage' not in line: continue
        try: d=json.loads(line)
        except: continue
        info=(d.get('payload') or {}).get('info') or {}
        u=info.get('total_token_usage')
        if not u: continue
        if last is None or u.get('total_tokens',0)>=last.get('total_tokens',0): last=u
        if d.get('timestamp','')<cut: before=u
    n+=1
    if last:
        for k in K: tot[k]+=last.get(k,0)
        if last is not before:
            nw+=1
            for k in K: win[k]+=last.get(k,0)-((before or {}).get(k,0))
            models[model or '?']+=1
    if first and first>=cut: sess_started_hourly[first[:13]]+=1
json.dump(dict(files=n,files_with_usage_in_window=nw,total=tot,window=win,window_session_models=models.most_common(),sessions_started_hourly=sess_started_hourly,method='max cumulative total_token_usage per file; window = max minus last value timestamped before 2026-10-30T00:00Z'),open(sys.argv[1],'w'),indent=1)
