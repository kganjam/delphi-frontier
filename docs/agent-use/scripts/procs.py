import subprocess,re,json,datetime as dt
obs=dt.datetime.now(dt.timezone.utc)
ps=subprocess.run(['ps','-eo','pid=,ppid=,lstart=,comm=,args='],capture_output=True,text=True).stdout.split('\n')
P={}
for l in ps:
    m=re.match(r'\s*(\d+)\s+(\d+)\s+(\w+ \w+ +\d+ [\d:]+ \d+)\s+(\S+)\s+(.*)',l)
    if m: P[int(m[1])]=dict(ppid=int(m[2]),start=m[3],comm=m[4],args=m[5])
kids={}
for p,v in P.items(): kids.setdefault(v['ppid'],[]).append(p)
def desc(p):
    out=[p]
    for c in kids.get(p,[]): out+=desc(c)
    return out
def is_agent(v):
    a=v['args']; c=v['comm']
    return (c in('claude','codex') or re.search(r'(^|/)(claude|codex)( |$)',a.split(' --')[0]) or re.search(r'@openai/codex|claude-code/cli',a)) and 'tmux' not in c
panes=[l.split('|') for l in open(f'{__import__("sys").argv[1]}/panes.txt').read().split('\n') if l]
res=[];allagent=set()
for s,pid,cmd,dead in panes:
    ag=[]
    for d in desc(int(pid)):
        v=P.get(d)
        if v and is_agent(v): ag.append(d)
    # keep only top agent processes (whose parent is not agent)
    top=[a for a in ag if P[a]['ppid'] not in ag]
    allagent|=set(ag)
    cap=subprocess.run(['tmux','capture-pane','-p','-t',s,'-S','-25'],capture_output=True,text=True).stdout
    low=cap.lower()
    if dead=='1': st='dead-pane'
    elif not top: st='no-agent'
    elif re.search(r'oauth|log ?in|/login|authenticat|token (has been )?revoked|401',low) and not re.search(r'esc to interrupt',low): st='auth-blocked?'
    elif re.search(r'esc to interrupt|working|thinking|running…|esc to cancel',low): st='working'
    elif re.search(r'usage limit|spend cap|rate limit|error|exceeded',low): st='error?'
    else: st='idle?'
    res.append(dict(session=s,pane_pid=int(pid),agent_top=[(a,P[a]['comm'],P[a]['start']) for a in top],n_agent_procs=len(ag),state=st,tail=[x for x in cap.strip().split('\n') if x.strip()][-4:]))
json.dump(dict(observed_utc=obs.isoformat(),panes=res,agent_procs_total=len(allagent)),open(f'{__import__("sys").argv[1]}/procs.json','w'),indent=1)
for r in res: print(r['session'],r['state'],r['n_agent_procs'],[(c,s) for _,c,s in r['agent_top']], '||', ' / '.join(t.strip()[:70] for t in r['tail'][-2:]))
print('observed',obs, 'agent procs under tmux', len(allagent))
# agent procs anywhere
allp=[p for p,v in P.items() if is_agent(v)]
print('agent procs system-wide',len(allp), 'outside tmux', len(set(allp)-allagent))
for p in set(allp)-allagent: print('  outside',p,P[p]['comm'],P[p]['start'],P[p]['args'][:80])
