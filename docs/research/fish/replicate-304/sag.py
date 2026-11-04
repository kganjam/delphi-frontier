# sagittal planes (normal y), box x 4500-6900, z 4000-7500; bending about z => depth along x
import sys, numpy as np, json
sys.path.insert(0,sys.argv[0].rsplit('/',1)[0]); from slice import slice_mesh; from secprops import raster, props
from scipy import ndimage
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
fn=sys.argv[1]; ys=[float(v) for v in sys.argv[2].split(',')]; out=sys.argv[3]
V=np.load(fn+'.V.npy'); F=np.load(fn+'.F.npy'); h=2.0
box=(4000,7500,4500,6900)  # u=z, v=x
res=[]; nc=5; nr=(len(ys)+nc-1)//nc
fig,ax=plt.subplots(nr,nc,figsize=(5*nc,4*nr)); ax=np.ravel(ax)
for n,y in enumerate(ys):
    S=slice_mesh(V,F,np.array([0,1.,0]),y)
    M,uc,vc=raster(S,2,0,box,h)
    L,nl=ndimage.label(M); secs=[]
    for k in range(1,nl+1):
        Mk=L==k
        if Mk.sum()<100: continue
        p=props(Mk,uc,vc,h)   # u=z, v=x: Iu = sum (x-xbar)^2 => bending about z-parallel axis, c along x
        secs.append(dict(A=p['A'],Z=p['Zu'],zc=p['ub'],xc=p['vb'],ext_x=p['ext_v']))
    secs.sort(key=lambda s:-s['Z'])
    tot=sum(s['Z'] for s in secs)
    res.append(dict(y=y,largest=secs[0] if secs else None,sum=tot,n=len(secs)))
    a=ax[n]; a.imshow(L>0,origin='lower',extent=[box[0],box[1],box[2],box[3]],cmap='Greys'); 
    if secs: a.plot(secs[0]['zc'],secs[0]['xc'],'r+',ms=15)
    a.set_title(f"y={y:.0f} Zmax={secs[0]['Z']:.3g} sum={tot:.3g}" if secs else f"y={y}")
plt.tight_layout(); plt.savefig(out+'.png',dpi=45); json.dump(res,open(out+'.json','w'))
for r in res:
    l=r['largest']; print(f"y={r['y']:.0f} n={r['n']} largestZ={l['Z']:.3g} at z={l['zc']:.0f},x={l['xc']:.0f} A={l['A']:.0f} extx={l['ext_x']:.0f}  planesum={r['sum']:.3g}")
