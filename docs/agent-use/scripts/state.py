import subprocess,json,re,datetime as dt,sys,collections
J=json.load(open(sys.argv[1]+'/procs.json'))
obs=dt.datetime.now(dt.timezone.utc).isoformat()
out=[];C=collections.Counter()
for r in J['panes']:
    s=r['session']
    cap=subprocess.run(['tmux','capture-pane','-p','-t',s,'-S','-15'],capture_output=True,text=True).stdout
    lines=[l for l in cap.split('\n') if l.strip()]
    tail='\n'.join(lines[-10:]).lower()
    if r['state']=='dead-pane': st='no live process (pane dead)'
    elif 'esc to interrupt' in tail or re.search(r'\(\d+[hms][^)]*·[^)]*tokens',tail): st='working'
    elif 'oauth token revoked' in tail or 'please run /login' in tail: st='auth-blocked'
    elif re.search(r'usage limit|spend cap|hit your',tail): st='error (provider quota/spend limit)'
    elif re.search(r'^\s*[❯›]\s*$',cap.split('───')[-2] if cap.count('───')>=2 else '',re.M) or re.search(r'[❯›]',tail): st='idle'
    else: st='unknown'
    k=st.split(' (')[0] if st.startswith('error') else st
    C[k]+=1; out.append(dict(session=s,state=st,agent_processes=r['n_agent_procs'],start_local=[a[2] for a in r['agent_top']]))
json.dump(dict(observed_utc=obs,counts=C,panes=out),open(sys.argv[1]+'/states.json','w'),indent=1)
print(obs,dict(C))
for o in out: print(o['session'],'|',o['state'])
