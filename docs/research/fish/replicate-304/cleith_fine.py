# dorsal cleithral limb: x-normal slices, moment about z (AP) => I about z-parallel axis (depth along y)
import sys, numpy as np, json
sys.path.insert(0,sys.argv[0].rsplit('/',1)[0]); from slice import slice_mesh; from secprops import raster, props
from scipy import ndimage
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fn=sys.argv[1]; side=sys.argv[2]; out=sys.argv[3]
V=np.load(fn+'.V.npy'); F=np.load(fn+'.F.npy')
h=float(sys.argv[5])
if side=='R': box=(3900,4900,5100,6400); win=(4050,4700,5350,6300)
else: box=(900,1900,5100,6400); win=(1100,1750,5350,6300)
xs=np.arange(float(sys.argv[6]),float(sys.argv[7])-1,-float(sys.argv[4]))
seed=tuple(map(float,sys.argv[8].split(',')))
res=[]; fig,ax=plt.subplots(4,6,figsize=(24,22)); ax=ax.ravel()
for n,x in enumerate(xs):
    S=slice_mesh(V,F,np.array([1.,0,0]),x)
    M,uc,vc=raster(S,1,2,box,h)
    L,nl=ndimage.label(M)
    best=None
    for k in range(1,nl+1):
        jj,ii=np.nonzero(L==k)
        if len(ii)<200: continue
        cu,cv=uc[ii].mean(),vc[jj].mean()
        dd=np.hypot(cu-seed[0],cv-seed[1])
        if dd<250 and (best is None or dd<best[1]): best=(k,dd,cu,cv)
    if n<len(ax):
        ax[n].imshow(L>0,origin='lower',extent=[box[0],box[1],box[2],box[3]],cmap='Greys',alpha=0.4)
    if best is None: continue
    seed=(best[2],best[3]); Mk=L==best[0]; p=props(Mk,uc,vc,h); p['x']=x; res.append(p)
    if n<len(ax):
        ax[n].contour(uc,vc,Mk,[0.5],colors='r'); ax[n].set_title(f"x={x:.0f} A={p['A']:.0f} Zz={p['Zv']:.3g}")
plt.tight_layout(); plt.savefig(out+'.png',dpi=45)
json.dump(res,open(out+'.json','w'))
for p in res: print(f"x={p['x']:.0f} A={p['A']:.0f} ext_y={p['ext_u']:.0f} ext_z={p['ext_v']:.0f} Iz={p['Iv']:.3g} c={p['cu']:.0f} Zz={p['Zv']:.4g} Zy={p['Zu']:.4g} Imin={p['Imin']:.3g}")
