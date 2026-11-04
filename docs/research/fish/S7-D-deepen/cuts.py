import sys, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
P=np.load(sys.argv[1])["P"]; out=sys.argv[2]; axis=int(sys.argv[3]); vals=[float(v) for v in sys.argv[4].split(",")]; w=float(sys.argv[5])
box=[float(v) for v in sys.argv[6].split(",")]  # xlo,xhi,ylo,yhi,zlo,zhi
m=(P[:,0]>box[0])&(P[:,0]<box[1])&(P[:,1]>box[2])&(P[:,1]<box[3])&(P[:,2]>box[4])&(P[:,2]<box[5]); P=P[m]
o=[i for i in range(3) if i!=axis]
fig,ax=plt.subplots(1,len(vals),figsize=(7*len(vals),8))
for a,v in zip(np.atleast_1d(ax),vals):
    Q=P[abs(P[:,axis]-v)<w/2]
    a.scatter(Q[:,o[1]],Q[:,o[0]],s=1.5,c='k'); a.set_aspect('equal'); a.set_title(f"{'xyz'[axis]}={v:.0f}±{w/2:.0f}")
    a.set_xlabel("xyz"[o[1]]); a.set_ylabel("xyz"[o[0]]); a.set_xlim(box[2*o[1]],box[2*o[1]+1]); a.set_ylim(box[2*o[0]],box[2*o[0]+1])
    a.minorticks_on(); a.grid(True,alpha=.5); a.grid(True,which='minor',alpha=.2)
plt.tight_layout(); plt.savefig(out,dpi=55)
