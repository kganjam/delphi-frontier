import sys,re,statistics as st
def cif(path):
    cols=[];rows=[];inloop=False
    for l in open(path):
        if l.startswith('_atom_site.'): cols.append(l.strip()); continue
        if cols and (l.startswith('ATOM') or l.startswith('HETATM')): rows.append(l.split())
    c={k.split('.')[1]:i for i,k in enumerate(cols)}
    ca={}
    allb={}
    for r in rows:
        resi=int(r[c['label_seq_id']]); b=float(r[c['B_iso_or_equiv']])
        allb.setdefault(resi,[]).append(b)
        if r[c['label_atom_id']]=='CA': ca[resi]=b
    return ca,allb
def pdb(path):
    ca={};allb={}
    for l in open(path):
        if l.startswith('ATOM'):
            resi=int(l[22:26]); b=float(l[60:66])
            allb.setdefault(resi,[]).append(b)
            if l[12:16].strip()=='CA': ca[resi]=b
    return ca,allb
seq=''.join(x.strip() for x in open(sys.argv[1]) if not x.startswith('>'))
ms=[(m.start()+1,m.group()) for m in re.finditer(r'(?=([TS].[GAS][YFL]G))',seq)]
ms=[(m.start()+1,seq[m.start():m.start()+5]) for m in re.finditer(r'(?=[TS].[GAS][YFL]G)',seq)]
print('len',len(seq),'motifs',ms)
for p in sys.argv[2:]:
    ca,allb=(pdb if p.endswith('.pdb') else cif)(p)
    sc=1
    if max(ca.values())<=1.0: sc=100
    v=[ca[i]*sc for i in sorted(ca)]
    print(p.split('/')[-1],'nres',len(ca),'meanCA %.2f'%st.mean(v),'>70 %.1f%%'%(100*sum(x>70 for x in v)/len(v)),'<50 %.1f%%'%(100*sum(x<50 for x in v)/len(v)))
    for s,mo in ms:
        r=range(s,s+5)
        a=st.mean(ca[i]*sc for i in r); b=st.mean(x*sc for i in r for x in allb[i])
        # window +-5
        w=[ca[i]*sc for i in range(s-5,s+10) if i in ca]
        print('  %s %d-%d CA %.2f allatom %.2f window15 %.2f per-res %s'%(mo,s,s+4,a,b,st.mean(w),[round(ca[i]*sc,1) for i in r]))
    for lo,hi in [(1,250),(261,448)]:
        print('  %d-%d mean %.2f'%(lo,hi,st.mean(ca[i]*sc for i in range(lo,hi+1))))
