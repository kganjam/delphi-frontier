import sys, glob, os, numpy as np
import importlib.util
spec = importlib.util.spec_from_file_location("r", os.path.join(sys.argv[2], "replicate-29_shuffle_null.py")); r = importlib.util.module_from_spec(spec); spec.loader.exec_module(r)
def run(seed, label):
    rng = np.random.default_rng(seed)
    for p in sorted(glob.glob(os.path.join(sys.argv[1], "*.fasta"))):
        h, s = r.read_fasta(p); x = r.enc(s)
        _, _, T5, _, _ = r.tandem_scores(x); Ta = r.tandem_scores(x)[0]; G = r.gapped_internal(x)
        nT=[];n5=[];nG=[]
        for _ in range(200):
            y = rng.permutation(x); a,_,b,_,_ = r.tandem_scores(y); nT.append(a); n5.append(b); nG.append(r.gapped_internal(y))
        pe=lambda o,n:(1+sum(v>=o for v in n))/201
        print(label, seed, h.split('|')[1], "T_all p=%.4f T_ge5 p=%.4f G_ge5 p=%.4f"%(pe(Ta,nT),pe(T5,n5),pe(G,nG)))
for sd in (1,2,3): run(sd, "B62")
I = np.full_like(r.B62, -1); np.fill_diagonal(I, 1); r.B62 = I; r.GAP = 2
for sd in (29,1): run(sd, "IDENT(+1/-1,gap2)")
