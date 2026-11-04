import sys, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
P=np.load(sys.argv[1])["P"]; out=sys.argv[2]
fig,ax=plt.subplots(3,1,figsize=(18,15))
for a,(i,j) in zip(ax,[(2,0),(2,1),(0,1)]):
    a.scatter(P[::2,i],P[::2,j],s=0.02,c='k'); a.set_aspect('equal'); a.set_xlabel("xyz"[i]); a.set_ylabel("xyz"[j]); a.grid(True,alpha=.4); a.minorticks_on()
plt.tight_layout(); plt.savefig(out,dpi=60)
