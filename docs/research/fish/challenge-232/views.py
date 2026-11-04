import sys, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
sys.path.insert(0, sys.argv[1]); from section import section
from scipy import ndimage as ndi
P=np.load(sys.argv[2])["P"]; x0,x1,z0,z1=map(float,sys.argv[3].split(",")); ys=[float(v) for v in sys.argv[4].split(",")]; hw=float(sys.argv[5]); out=sys.argv[6]; ymid=float(sys.argv[7])
B=P[(P[:,2]>z0-1500)&(P[:,2]<z1+1500)&(P[:,0]>x0-1500)]
fig=plt.figure(figsize=(22,14))
a=fig.add_subplot(2,4,1); m=B[:,0]>x0; a.scatter(B[m,2],B[m,1],s=.05,c=B[m,0],cmap='viridis'); a.set_title("ventral view, x>%.0f (color=x, yellow=ventral)"%x0); a.set_xlabel('z'); a.set_ylabel('y'); a.set_aspect('equal')
for y in ys: a.axhline(y,c='r',lw=.5)
a.axhline(ymid,c='b'); a.axvline(z0,c='k'); a.axvline(z1,c='k')
a=fig.add_subplot(2,4,2); m=np.abs(B[:,1]-ymid)<1800; a.scatter(B[m,2],B[m,0],s=.05,c=np.abs(B[m,1]-ymid),cmap='plasma'); a.set_title("lateral, color=|y-mid|"); a.set_xlabel('z'); a.set_ylabel('x'); a.set_aspect('equal'); a.add_patch(plt.Rectangle((z0,x0),z1-z0,x1-x0,fill=False,ec='k'))
for i,y in enumerate(ys[:6]):
    a=fig.add_subplot(2,4,3+i); Q=P[(abs(P[:,1]-y)<hw)&(P[:,0]>x0)&(P[:,0]<x1)&(P[:,2]>z0)&(P[:,2]<z1)]
    a.scatter(Q[:,2],Q[:,0],s=.5,c='k')
    c=sorted(section(np.c_[Q[:,0],Q[:,2]]),key=lambda c:-c['Z_mm3'])
    for k,cc in enumerate(c[:4]):
        a.add_patch(plt.Rectangle((cc['v_ext'][0],cc['u_ext'][0]),cc['v_ext'][1]-cc['v_ext'][0],cc['u_ext'][1]-cc['u_ext'][0],fill=False,ec='C%d'%k))
        a.text(cc['v_ext'][0],cc['u_ext'][1],"#%d %.1e"%(k,cc['Z_mm3']),color='C%d'%k,fontsize=9)
    a.set_title("y=%.0f (%.0f from mid) hw%.0f"%(y,abs(y-ymid),hw)); a.set_xlim(z0,z1); a.set_ylim(x0,x1); a.set_aspect('equal')
plt.tight_layout(); plt.savefig(out,dpi=55)
