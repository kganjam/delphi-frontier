import sys,re,numpy as np
three={'ALA':'A','ARG':'R','ASN':'N','ASP':'D','CYS':'C','GLN':'Q','GLU':'E','GLY':'G','HIS':'H','ILE':'I','LEU':'L','LYS':'K','MET':'M','PHE':'F','PRO':'P','SER':'S','THR':'T','TRP':'W','TYR':'Y','VAL':'V'}
def cifca(path,chain=None):
    cols=[];out={}
    for l in open(path):
        if l.startswith('_atom_site.'): cols.append(l.strip().split('.')[1]); continue
        if cols and l.startswith('ATOM'):
            r=l.split(); c={k:i for i,k in enumerate(cols)}
            if r[c['label_atom_id']]!='CA': continue
            if chain and r[c['auth_asym_id']]!=chain: continue
            if 'pdbx_PDB_model_num' in c and r[c['pdbx_PDB_model_num']]!='1': continue
            n=int(r[c['auth_seq_id']]); 
            if n in out: continue
            out[n]=(three.get(r[c['label_comp_id']],'X'),np.array([float(r[c['Cartn_x']]),float(r[c['Cartn_y']]),float(r[c['Cartn_z']])]))
    return out
def pdbca(path):
    out={}
    for l in open(path):
        if l.startswith('ATOM') and l[12:16].strip()=='CA':
            out[int(l[22:26])]=(three[l[17:20]],np.array([float(l[30:38]),float(l[38:46]),float(l[46:54])]))
    return out
def kabsch(P,Q):
    P=P-P.mean(0);Q=Q-Q.mean(0);H=P.T@Q;U,S,Vt=np.linalg.svd(H);d=np.sign(np.linalg.det(Vt.T@U.T))
    D=np.diag([1,1,d]);R=Vt.T@D@U.T;return np.sqrt(((P@R.T-Q)**2).sum(1).mean())
ref=cifca(sys.argv[1],'A'); ks=sorted(ref); rs=''.join(ref[k][0] for k in ks)
print('ref chainA nres',len(ks),ks[0],ks[-1])
def find(seq,mot): return [m.start() for m in re.finditer(mot,seq)]
models={p.split('/')[-1]:(pdbca(p) if p.endswith('.pdb') else cifca(p)) for p in sys.argv[2:]}
q=models[list(models)[0]]; qs=''.join(q[k][0] for k in sorted(q))
pairs=[]
for mot,qstart in [('T.G[YF]G',98),('T.G[YF]G',203)]:
    pass
# map filters: find motif positions in ref
hits=[(i,rs[i:i+5]) for i in range(len(rs)-4) if re.match(r'[TS].[GAS][YFL]G',rs[i:i+5])]
print('ref motifs',[(ks[i],s) for i,s in hits])
W=8
for (qi,(ri,_)) in zip([98,203],hits):
    qw=''.join(q[k][0] for k in range(qi-W,qi+5+W)); rw=''.join(ref[ks[j]][0] for j in range(ri-W,ri+5+W))
    ident=sum(a==b for a,b in zip(qw,rw))/len(qw)
    print('window q%d %s | ref %s ident %.2f'%(qi,qw,rw,ident))
    pairs+= [(k,ks[ri-qi+k]) for k in range(qi-W,qi+5+W)]
for name,m in models.items():
    P=np.array([m[a][1] for a,b in pairs]);Q=np.array([ref[b][1] for a,b in pairs])
    # also filters only
    fp=[(a,b) for a,b in pairs if (98<=a<=102) or (203<=a<=207)]
    P2=np.array([m[a][1] for a,b in fp]);Q2=np.array([ref[b][1] for a,b in fp])
    print('%-22s pore-region(%d CA) RMSD %.2f A ; filters-only(%d CA) RMSD %.2f A'%(name,len(P),kabsch(P,Q),len(P2),kabsch(P2,Q2)))
print('--- per pore domain separately (21 CA window each; 5 CA filter)')
for lo in (98,203):
    for name,m in models.items():
        sel=[(a,b) for a,b in pairs if lo-W<=a<lo+5+W]; f=[(a,b) for a,b in sel if lo<=a<lo+5]
        r1=kabsch(np.array([m[a][1] for a,b in sel]),np.array([ref[b][1] for a,b in sel]))
        r2=kabsch(np.array([m[a][1] for a,b in f]),np.array([ref[b][1] for a,b in f]))
        print(' %d %-22s window RMSD %.2f  filter RMSD %.2f'%(lo,name,r1,r2))
