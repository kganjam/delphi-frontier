import sys, numpy as np, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import ndimage as ndi
P=np.load(sys.argv[1])["P"]; x0,x1,z0,z1=[float(v) for v in sys.argv[2].split(",")]; ys=[float(v) for v in sys.argv[3].split(",")]; out=sys.argv[4]
P=P[(P[:,0]>x0)&(P[:,0]<x1)&(P[:,2]>z0)&(P[:,2]<z1)]
fig,ax=plt.subplots(2,len(ys),figsize=(6*len(ys),10))
for r,hw in enumerate((15,30)):
  for a,y in zip(ax[r],ys):
    Q=P[abs(P[:,1]-y)<hw]; px=10
    idx=np.floor((np.c_[Q[:,0],Q[:,2]]-[x0,z0])/px).astype(int); g=np.zeros((int((x1-x0)/px)+1,int((z1-z0)/px)+1),bool); g[idx[:,0],idx[:,1]]=True
    st=ndi.iterate_structure(ndi.generate_binary_structure(2,1),3)
    f=ndi.binary_erosion(ndi.binary_fill_holes(ndi.binary_dilation(g,structure=st)),structure=st)|g
    a.imshow(f,origin='lower',extent=[z0,z1,x0,x1],cmap='Greys'); a.scatter(Q[:,2],Q[:,0],s=0.6,c='r')
    a.set_title(f"y={y:.0f} hw={hw}"); a.set_xlabel("z"); a.set_ylabel("x")
plt.tight_layout(); plt.savefig(out,dpi=50)
