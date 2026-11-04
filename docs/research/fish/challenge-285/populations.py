import json,collections,sys
rows=json.load(open(sys.argv[1]))
def tab(rs,label):
    c=collections.Counter(r['out'] for r in rs);n=len(rs)
    print(f"{label}: n={n} {dict(c)} surv={c['survived']}/{n}={100*c['survived']/n:.1f}%")
for cut in [int(sys.argv[2]) if len(sys.argv)>2 else None, None]:
    rs=[r for r in rows if cut is None or r['t']<=cut]
    print('--- cutoff',cut)
    by=collections.defaultdict(list)
    for r in rs: by[r['cid']].append(r)
    for v in by.values(): v.sort(key=lambda r:r['t'])
    tab(rs,'all blobs')
    tab([v[-1] for v in by.values()],'latest per cid')
    tab([v[0] for v in by.values()],'first per cid')
    firsts=sorted([v[0] for v in by.values()],key=lambda r:r['t'])
    tab(firsts[:156],'first 156 by time')
    tab([v[-1] for v in by.values() if not any('207' and r['mentions207'] for r in v[-1:])],'latest, excl mentions 207')
    # claims with any refuted version
    print('cids ever refuted',sorted(k for k,v in by.items() if any(r['out']=='refuted' for r in v)))
